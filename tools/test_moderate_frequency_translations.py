#!/usr/bin/env python3
"""Offline unit tests for frequency translation moderation (mocked judges, no live API)."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))

import moderate_frequency_translations as mod  # noqa: E402


def mock_judge_factory(scores_by_provider: dict[str, dict[str, int]]):
    def fn(provider: str, en_word: str, translation: str, lang: str) -> dict:
        dims = scores_by_provider.get(provider, {"accuracy": 8, "everyday_register": 8, "not_bible_formal": 8})
        parsed = {
            dim: {"score": score, "rationale": f"mock {dim}"}
            for dim, score in dims.items()
        }
        parsed["brief_summary"] = f"mock verdict for {en_word}"
        parsed["suggested_fix"] = None
        return {"provider": provider, "parsed": parsed, "raw_response": "{}", "citations": []}

    return fn


class ModerationLogicTests(unittest.TestCase):
    def test_classify_approved(self):
        self.assertEqual(mod.classify_status(7.5, 1.0, threshold=6.0, max_disagreement=2.0), "approved")

    def test_classify_flagged_low_score(self):
        self.assertEqual(mod.classify_status(5.5, 0.5, threshold=6.0, max_disagreement=2.0), "flagged")

    def test_classify_flagged_disagreement(self):
        self.assertEqual(mod.classify_status(7.0, 3.0, threshold=6.0, max_disagreement=2.0), "flagged")

    def test_classify_rejected(self):
        self.assertEqual(mod.classify_status(4.5, 1.0, threshold=6.0, max_disagreement=2.0), "rejected")

    def test_aggregate_entry(self):
        judge_fn = mock_judge_factory({
            "anthropic": {"accuracy": 9, "everyday_register": 8, "not_bible_formal": 9},
            "openai": {"accuracy": 8, "everyday_register": 8, "not_bible_formal": 8},
            "perplexity": {"accuracy": 7, "everyday_register": 7, "not_bible_formal": 7},
        })
        result = mod.judge_pair("water", "amanzi", lang="zu", judge_fn=judge_fn)
        self.assertIn("dimensions", result)
        self.assertGreaterEqual(result["aggregate_score"], 7.0)
        self.assertGreater(result["disagreement"], 0.0)

    def test_parse_judge_json_with_fences(self):
        raw = '```json\n{"accuracy": {"score": 8}}\n```'
        parsed = mod.parse_judge_json(raw)
        self.assertEqual(parsed["accuracy"]["score"], 8)

    def test_should_skip_single_char(self):
        self.assertTrue(mod.should_skip_word("c"))
        self.assertTrue(mod.should_skip_word("e"))
        self.assertFalse(mod.should_skip_word("the"))

    def test_compute_summary(self):
        entries = {
            "zu:a": {"status": "approved"},
            "zu:b": {"status": "flagged"},
            "zu:c": {"status": "judge_error"},
            "zu:d": {"status": "skipped"},
        }
        summary = mod.compute_summary(entries)
        self.assertEqual(summary["scored"], 4)
        self.assertEqual(summary["approved"], 1)
        self.assertEqual(summary["flagged"], 1)
        self.assertEqual(summary["judge_error"], 1)
        self.assertEqual(summary["skipped"], 1)


class RateLimitRetryTests(unittest.TestCase):
    def test_429_retry_then_success(self):
        attempts = {"n": 0}
        good_json = (
            '{"accuracy": {"score": 8, "rationale": "x"}, '
            '"everyday_register": {"score": 8, "rationale": "x"}, '
            '"not_bible_formal": {"score": 8, "rationale": "x"}, '
            '"suggested_fix": null, "brief_summary": "ok"}'
        )

        def side_effect(provider, en_word, translation, lang):
            attempts["n"] += 1
            if attempts["n"] == 1:
                raise RuntimeError("HTTP 429 from https://openrouter.ai/api/v1/chat/completions: rate limited")
            return (good_json, [])

        with patch.object(mod, "fetch_judge_raw", side_effect=side_effect):
            with patch.object(mod.time, "sleep"):
                result = mod.call_judge_with_retries(
                    "anthropic", "water", "amanzi", lang="zu", delay=0.0, max_retries=3,
                )
        self.assertEqual(attempts["n"], 2)
        self.assertEqual(result["parsed"]["accuracy"]["score"], 8)

    def test_empty_response_marks_judge_error(self):
        def judge_fn(provider: str, en_word: str, translation: str, lang: str) -> dict:
            raise ValueError("empty judge response")

        result = mod.judge_pair("water", "amanzi", lang="zu", judge_fn=judge_fn, delay=0.0)
        self.assertTrue(result["judge_errors"])
        self.assertEqual(result["aggregate_score"], 0.0)

    def test_invalid_json_retry_once_then_error(self):
        attempts = {"n": 0}

        def side_effect(provider, en_word, translation, lang):
            attempts["n"] += 1
            if attempts["n"] == 1:
                return ("not json", [])
            return ('{"accuracy": {"score": 7, "rationale": "x"}, '
                    '"everyday_register": {"score": 7, "rationale": "x"}, '
                    '"not_bible_formal": {"score": 7, "rationale": "x"}, '
                    '"suggested_fix": null, "brief_summary": "ok"}', [])

        with patch.object(mod, "fetch_judge_raw", side_effect=side_effect):
            with patch.object(mod.time, "sleep"):
                result = mod.call_judge_with_retries(
                    "openai", "water", "amanzi", lang="zu", delay=0.0, max_retries=0,
                )
        self.assertEqual(attempts["n"], 2)
        self.assertEqual(result["parsed"]["accuracy"]["score"], 7)


class ModerationPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        mod.CORPUS_DIR = self.root
        mod.FREQ_DIR = self.root / "frequency"
        mod.FREQ_DIR.mkdir()
        mod.CACHE_PATH = self.root / "frequency_translations.json"
        mod.SCORES_PATH = mod.FREQ_DIR / "moderation_scores.json"
        mod.QUEUE_PATH = mod.FREQ_DIR / "moderation_queue.json"
        mod.REJECTED_PATH = mod.FREQ_DIR / "moderation_rejected.json"
        mod.WORD_LIST = mod.FREQ_DIR / "en_frequency.txt"
        mod.WORD_LIST.write_text("the\nwater\nbook\n", encoding="utf-8")
        mod.CACHE_PATH.write_text(json.dumps({
            "languages": {
                "zu": {"the": "i-", "water": "amanzi", "book": "incwadi"},
            }
        }), encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_run_moderation_dry_run(self):
        doc = mod.run_moderation(
            langs=["zu"],
            words=["the", "water", "book"],
            limit=None,
            threshold=6.0,
            max_disagreement=2.0,
            resume=False,
            dry_run=True,
        )
        self.assertEqual(doc["summary"]["pending"], 3)

    def test_run_and_apply_moderation(self):
        def judge_fn(provider: str, en_word: str, translation: str, lang: str) -> dict:
            if en_word == "book":
                scores = {"accuracy": 4, "everyday_register": 4, "not_bible_formal": 4}
            elif en_word == "the":
                scores = {"accuracy": 5, "everyday_register": 6, "not_bible_formal": 6}
            else:
                scores = {"accuracy": 9, "everyday_register": 9, "not_bible_formal": 9}
            parsed = {d: {"score": s, "rationale": "x"} for d, s in scores.items()}
            parsed["brief_summary"] = "mock"
            parsed["suggested_fix"] = "incwadi encane" if en_word == "book" else None
            return {"provider": provider, "parsed": parsed, "raw_response": "{}", "citations": []}

        doc = mod.run_moderation(
            langs=["zu"],
            words=["the", "water", "book"],
            limit=None,
            threshold=6.0,
            max_disagreement=2.0,
            resume=False,
            dry_run=False,
            judge_fn=judge_fn,
        )
        self.assertEqual(doc["summary"]["scored"], 3)
        self.assertTrue(mod.SCORES_PATH.is_file())

        apply_result = mod.apply_moderation(doc)
        cache = json.loads(mod.CACHE_PATH.read_text(encoding="utf-8"))
        self.assertIn("water", cache["languages"]["zu"])
        self.assertNotIn("book", cache["languages"]["zu"])
        self.assertGreater(int(apply_result["rejected_removed"]), 0)
        queue = json.loads(mod.QUEUE_PATH.read_text(encoding="utf-8"))
        self.assertTrue(any(k.startswith("zu:the") for k in queue.get("entries", {})))

    def test_summary_updated_on_each_save(self):
        judge_fn = mock_judge_factory({})
        doc = mod.run_moderation(
            langs=["zu"],
            words=["the", "water"],
            limit=None,
            threshold=6.0,
            max_disagreement=2.0,
            resume=False,
            dry_run=False,
            delay=0.0,
            judge_fn=judge_fn,
        )
        saved = json.loads(mod.SCORES_PATH.read_text(encoding="utf-8"))
        self.assertEqual(saved["summary"]["scored"], 2)
        self.assertEqual(doc["summary"]["scored"], 2)

    def test_skip_noise_tokens(self):
        mod.WORD_LIST.write_text("c\nthe\n", encoding="utf-8")
        mod.CACHE_PATH.write_text(json.dumps({
            "languages": {"zu": {"c": "x", "the": "i-"}},
        }), encoding="utf-8")
        judge_fn = mock_judge_factory({})
        doc = mod.run_moderation(
            langs=["zu"],
            words=["c", "the"],
            limit=None,
            threshold=6.0,
            max_disagreement=2.0,
            resume=False,
            dry_run=False,
            delay=0.0,
            judge_fn=judge_fn,
        )
        self.assertEqual(doc["entries"]["zu:c"]["status"], "skipped")
        self.assertEqual(doc["summary"]["skipped"], 1)
        self.assertEqual(doc["summary"]["approved"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
