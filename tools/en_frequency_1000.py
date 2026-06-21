#!/usr/bin/env python3
"""Generate en→lang translation cache for frequency ladder (up to 10k English lemmas).

Source list: docs/corpus/frequency/en_frequency.txt (Google 10k ordering).
See docs/corpus/FREQUENCY_LADDER.md. Ingest uses tools/ingest_frequency_lists.py.

Usage:
    python3 tools/en_frequency_1000.py --write-cache     # fill frequency_translations.json
    python3 tools/en_frequency_1000.py --dry-run         # counts only
    python3 tools/build_sa_urban_corpus.py               # rebuild corpus with freq rows
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CORPUS_DIR = REPO / "docs" / "corpus"
WORD_LIST = CORPUS_DIR / "frequency" / "en_frequency.txt"
CACHE_PATH = CORPUS_DIR / "frequency_translations.json"
PLATFORM_ENV = REPO.parent / "arjuna-badger-platform" / ".env"

FREQ_LANGS = ("af", "zu", "xh", "tn", "st", "sw")
FREQ_WEIGHT = 20
FREQ_CONTRIBUTOR = "auto-frequency-seed"
FREQ_SOURCE = (
    "https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt"
)
WIKI_SOURCE = "https://en.wiktionary.org/wiki/{word}"

LANG_NAMES = {
    "af": "Afrikaans (everyday South African speech, not formal/Bible register)",
    "zu": "isiZulu (KZN/Gauteng urban everyday speech)",
    "xh": "isiXhosa (everyday speech)",
    "tn": "Setswana (everyday Botswana/South Africa speech)",
    "st": "Sesotho (everyday Lesotho/South Africa speech)",
    "sw": "Swahili (East African colloquial, not classical)",
}

# Human-curated glosses for the highest-frequency lemmas (override auto output).
CURATED: dict[str, dict[str, str]] = {
    "af": {
        "the": "die", "and": "en", "or": "of", "to": "na", "of": "van", "in": "in",
        "for": "vir", "is": "is", "on": "op", "that": "dat", "with": "met", "you": "jy",
        "it": "dit", "not": "nie", "be": "wees", "are": "is", "from": "van", "at": "by",
        "as": "as", "your": "jou", "all": "al", "have": "het", "new": "nuwe", "more": "meer",
        "an": "'n", "was": "was", "we": "ons", "will": "sal", "home": "huis", "can": "kan",
        "us": "ons", "about": "oor", "if": "as", "my": "my", "has": "het", "but": "maar",
        "our": "ons", "one": "een", "other": "ander", "do": "doen", "no": "nee", "time": "tyd",
        "they": "hulle", "he": "hy", "up": "op", "what": "wat", "which": "watter",
        "their": "hulle", "out": "uit", "there": "daar", "see": "sien", "so": "so",
        "his": "sy", "when": "wanneer", "here": "hier", "who": "wie", "now": "nou",
        "get": "kry", "how": "hoe", "were": "was", "me": "my", "some": "sommige",
        "like": "soos", "than": "as", "find": "vind", "back": "terug", "people": "mense",
        "had": "het", "name": "naam", "just": "net", "over": "oor", "year": "jaar",
        "day": "dag", "into": "in", "two": "twee", "go": "gaan", "work": "werk",
        "last": "laaste", "good": "goed", "well": "wel", "where": "waar", "book": "boek",
        "books": "boeke", "life": "lewe", "know": "weet", "way": "pad", "days": "dae",
        "car": "kar", "take": "neem", "want": "wil", "family": "familie", "long": "lank",
        "house": "huis", "water": "water", "sun": "son", "language": "taal", "food": "kos",
        "money": "geld", "man": "man", "woman": "vrou", "women": "vroue", "men": "mans",
        "child": "kind", "children": "kinders", "friend": "vriend", "love": "liefde",
        "yes": "ja", "hello": "hallo", "thank": "dankie", "thanks": "dankie", "please": "asseblief",
        "sorry": "jammer", "help": "help", "world": "wêreld", "country": "land", "city": "stad",
        "road": "pad", "school": "skool", "hand": "hand", "eye": "oog", "head": "kop",
        "heart": "hart", "night": "nag", "morning": "oggend", "big": "groot", "small": "klein",
        "old": "oud", "young": "jonk", "hot": "warm", "cold": "koud", "run": "hardloop",
        "walk": "stap", "eat": "eet", "drink": "drink", "sleep": "slaap", "read": "lees",
        "write": "skryf", "speak": "praat", "listen": "luister", "think": "dink", "give": "gee",
        "come": "kom", "make": "maak", "say": "sê", "tell": "vertel", "ask": "vra",
        "look": "kyk", "open": "open", "close": "toe", "start": "begin", "stop": "stop",
        "live": "leef", "die": "sterf", "buy": "koop", "sell": "verkoop", "pay": "betaal",
        "dog": "hond", "cat": "kat", "bird": "voël", "fish": "vis", "tree": "boom",
        "fire": "vuur", "rain": "reën", "wind": "wind", "sky": "lug", "moon": "maan",
        "star": "ster", "light": "lig", "dark": "donker", "black": "swart", "white": "wit",
        "red": "rooi", "blue": "blou", "green": "groen", "happy": "gelukkig", "sad": "hartseer",
        "afraid": "bang", "strong": "sterk", "weak": "swak", "fast": "vinnig", "slow": "stadig",
    },
    "zu": {
        "the": "i-", "and": "na", "or": "noma", "to": "ku", "of": "ka", "in": "ku",
        "for": "ngoba", "is": "yi", "on": "ku", "that": "ukuthi", "with": "no",
        "you": "wena", "it": "kona", "not": "hhayi", "be": "ba", "are": "ba",
        "from": "kusuka", "at": "ku", "as": "njengoba", "your": "wakho", "all": "konke",
        "have": "ba", "new": "okusha", "more": "okuningi", "an": "i-", "was": "kwakuyi",
        "we": "thina", "will": "kuzoba", "home": "ekhaya", "can": "ngingakwazi",
        "us": "thina", "about": "mayelana", "if": "uma", "my": "wami", "has": "une",
        "but": "kodwa", "our": "wethu", "one": "munye", "other": "okunye", "do": "yenza",
        "no": "cha", "time": "isikhathi", "they": "bona", "he": "yena", "up": "phezulu",
        "what": "yini", "which": "yiphi", "their": "babo", "out": "ngaphandle",
        "there": "lapho", "see": "bona", "so": "njalo", "his": "yakhe", "when": "nini",
        "here": "lapha", "who": "ubani", "now": "manje", "get": "thola", "how": "kanjani",
        "were": "babeyi", "me": "mina", "some": "abanye", "like": "njengoba",
        "than": "kune", "find": "thola", "back": "emuva", "people": "abantu",
        "had": "babenayo", "name": "igama", "just": "nje", "over": "phezulu",
        "year": "unyaka", "day": "usuku", "into": "ngaphakathi", "two": "abantu ababili",
        "go": "hamba", "work": "sebenza", "last": "okokugcina", "good": "kuhle",
        "well": "kahle", "where": "kuphi", "book": "incwadi", "books": "izincwadi",
        "life": "impilo", "know": "azi", "way": "indlela", "days": "izinsuku",
        "car": "imoto", "take": "thatha", "want": "funa", "family": "umndeni",
        "long": "inde", "house": "indlu", "water": "amanzi", "sun": "ilanga",
        "language": "ulimi", "food": "ukudla", "money": "imali", "man": "indoda",
        "woman": "owesifazane", "women": "abesifazane", "men": "amadoda",
        "child": "ingane", "children": "izingane", "friend": "umngane", "love": "uthando",
        "yes": "yebo", "hello": "sawubona", "thank": "ngiyabonga", "thanks": "ngiyabonga",
        "please": "ngicela", "sorry": "uxolo", "help": "usizo", "world": "umhlaba",
        "country": "izwe", "city": "idolobha", "road": "umgwaqo", "school": "isikole",
        "hand": "isandla", "eye": "iso", "head": "ikhanda", "heart": "inhliziyo",
        "night": "ubusuku", "morning": "ekuseni", "big": "mkhulu", "small": "ncane",
        "old": "mdala", "young": "semncane", "hot": "shisa", "cold": "kubanda",
        "run": "gijima", "walk": "hamba", "eat": "dla", "drink": "phuza", "sleep": "lala",
        "read": "funda", "write": "bhala", "speak": "khuluma", "listen": "lalela",
        "think": "cabanga", "give": "nika", "come": "za", "make": "enza", "say": "thi",
        "tell": "tshela", "ask": "buza", "look": "bheka", "open": "vula", "close": "vala",
        "start": "qala", "stop": "misa", "live": "phila", "die": "fa", "buy": "thenga",
        "sell": "dayisa", "pay": "khokha", "dog": "inja", "cat": "ikati", "bird": "inyoni",
        "fish": "inhlanzi", "tree": "isihlahla", "fire": "umlilo", "rain": "imvula",
        "wind": "umoya", "sky": "isibhakabhaka", "moon": "inyanga", "star": "inkanyezi",
        "light": "ukukhanya", "dark": "mnyama", "black": "mnyama", "white": "mhlophe",
        "red": "bomvu", "blue": "luhlaza okwesibhakabhaka", "green": "luhlaza",
        "happy": "ujabule", "sad": "dumele", "afraid": "esaba", "strong": "qinile",
        "weak": "butha", "fast": "shesha", "slow": "kancane",
    },
    "xh": {
        "the": "i-", "and": "na", "or": "okanye", "to": "ku", "of": "ka", "in": "ku",
        "for": "ngoba", "is": "yi", "on": "ku", "that": "ukuba", "with": "no",
        "you": "wena", "it": "koko", "not": "hayi", "be": "ba", "are": "ba",
        "from": "usuka", "at": "ku", "your": "wakho", "all": "yonke", "have": "ba",
        "new": "entsha", "more": "ngakumbi", "we": "thina", "will": "kuya", "home": "ekhaya",
        "can": "ngakwazi", "us": "thina", "about": "malunga", "if": "ukuba", "my": "wam",
        "but": "kodwa", "our": "wethu", "one": "nye", "other": "enye", "do": "yenza",
        "no": "hayi", "time": "ixesha", "they": "bona", "he": "yena", "what": "yintoni",
        "which": "yeyiphi", "their": "babo", "there": "apho", "see": "bona", "here": "apha",
        "who": "ngubani", "now": "ngoku", "get": "fumana", "how": "njani", "me": "mna",
        "people": "abantu", "name": "igama", "year": "unyaka", "day": "usuku", "two": "mbini",
        "go": "hamba", "work": "sebenza", "good": "kulungile", "where": "phi", "book": "incwadi",
        "life": "ubomi", "know": "azi", "way": "indlela", "car": "imoto", "want": "funa",
        "family": "usapho", "house": "indlu", "water": "amanzi", "sun": "ilanga",
        "language": "ulwimi", "food": "ukutya", "money": "imali", "man": "indoda",
        "woman": "umfazi", "child": "umntwana", "children": "abantwana", "friend": "umhlobo",
        "love": "uthando", "yes": "ewe", "hello": "molo", "thanks": "enkosi", "please": "nceda",
        "sorry": "uxolo", "help": "uncedo", "world": "ihlabathi", "country": "ilizwe",
        "city": "isixeko", "road": "umgama", "school": "isikolo", "hand": "isandla",
        "eye": "iliso", "head": "intloko", "heart": "intliziyo", "night": "ubusuku",
        "morning": "ekuseni", "big": "mkhulu", "small": "ncinci", "old": "mdala",
        "run": "baleka", "walk": "hamba", "eat": "tya", "drink": "sela", "sleep": "lala",
        "read": "funda", "write": "bhala", "speak": "thetha", "come": "za", "make": "yenza",
        "dog": "inja", "cat": "ikati", "bird": "intaka", "fish": "intlazi", "tree": "umthi",
        "fire": "umlilo", "rain": "imvula", "wind": "umoya", "sky": "izulu", "moon": "inyanga",
        "star": "inkwenkwezi", "light": "ukukhanya", "black": "mnyama", "white": "mhlophe",
        "happy": "vuyile", "hot": "shushu", "cold": "kubanda",
    },
    "tn": {
        "the": "e", "and": "le", "or": "kgotsa", "to": "go", "of": "ya", "in": "mo",
        "for": "bakeng", "is": "ke", "on": "mo", "that": "gore", "with": "le",
        "you": "wena", "it": "e", "not": "e se", "be": "be", "are": "ba",
        "from": "go tswa", "at": "mo", "your": "gago", "all": "tsotlhe", "have": "na",
        "new": "sešwa", "more": "go feta", "we": "re", "will": "tla", "home": "gae",
        "can": "ka kgona", "us": "re", "about": "ka", "if": "fa", "my": "gaka",
        "but": "mme", "our": "rônê", "one": "one", "other": "se sengwe", "do": "dira",
        "no": "nnyaa", "time": "nako", "they": "bone", "he": "ene", "what": "eng",
        "which": "e efe", "their": "babo", "there": "fo", "see": "bona", "here": "fano",
        "who": "mang", "now": "gompieno", "get": "bona", "how": "jang", "me": "nna",
        "people": "batho", "name": "leina", "year": "ngwaga", "day": "letsatsi", "two": "pedi",
        "go": "tsamaya", "work": "bereka", "good": "sentle", "where": "kae", "book": "buka",
        "life": "botshelo", "know": "itsi", "way": "tsela", "car": "koloi", "want": "batla",
        "family": "losika", "house": "ntlo", "water": "metsi", "sun": "letsatsi",
        "language": "puo", "food": "dijo", "money": "madi", "man": "monna",
        "woman": "mosadi", "child": "ngwana", "children": "bana", "friend": "tsala",
        "love": "lorato", "yes": "ee", "hello": "dumela", "thanks": "ke a leboga",
        "please": "tsweetswee", "sorry": "maswi a me", "help": "thuso", "world": "lefatshe",
        "country": "naga", "city": "toropo", "road": "tsela", "school": "sekolo",
        "hand": "tshogo", "eye": "leitlho", "head": "hloho", "heart": "pelo",
        "night": "bosigo", "morning": "mosong", "big": "kgolo", "small": "nyenyane",
        "old": "kgologolo", "run": "kitima", "walk": "tsamaya", "eat": "ja", "drink": "nwa",
        "sleep": "robala", "read": "bala", "write": "kwala", "speak": "bua", "come": "tla",
        "make": "dira", "dog": "ntja", "cat": "katse", "bird": "nonyane", "fish": "tlhapi",
        "tree": "sefatlha", "fire": "molelo", "rain": "pula", "wind": "phefo", "sky": "loapi",
        "moon": "ngwedi", "star": "naledi", "light": "lesedi", "black": "ntsho", "white": "tshweu",
        "happy": "itumetse", "hot": "molemo", "cold": "tshologa",
    },
    "st": {
        "the": "e", "and": "le", "or": "kapa", "to": "ho", "of": "ya", "in": "ho",
        "for": "bakeng", "is": "ke", "on": "ho", "that": "hore", "with": "le",
        "you": "wena", "it": "e", "not": "ha", "be": "be", "are": "ba",
        "from": "ho tswa", "at": "ho", "your": "hau", "all": "tsohle", "have": "na",
        "new": "e ncha", "more": "haholo", "we": "re", "will": "tla", "home": "hae",
        "can": "ka khona", "us": "re", "about": "ka", "if": "haeba", "my": "ka",
        "but": "empa", "our": "rōna", "one": "e 'ngoe", "other": "e 'ngoe", "do": "etsa",
        "no": "che", "time": "nako", "they": "bona", "he": "eena", "what": "eng",
        "which": "e fe", "their": "bō bona", "there": "moo", "see": "bona", "here": "mona",
        "who": "mang", "now": "honajwale", "get": "fumana", "how": "jwang", "me": "nna",
        "people": "batho", "name": "lebitso", "year": "selemo", "day": "letsatsi", "two": "peli",
        "go": "tsamaea", "work": "sebetsa", "good": "hantle", "where": "kae", "book": "buka",
        "life": "bophelo", "know": "tseba", "way": "tsela", "car": "koloi", "want": "batla",
        "family": "lelapa", "house": "ntlo", "water": "metsi", "sun": "letsatsi",
        "language": "puo", "food": "lijo", "money": "chelete", "man": "monna",
        "woman": "mosadi", "child": "ngwana", "children": "bana", "friend": "metswalle",
        "love": "lerato", "yes": "e", "hello": "lumela", "thanks": "ke a leboha",
        "please": "ka kopo", "sorry": "tshwarelo", "help": "thuso", "world": "lefatše",
        "country": "naha", "city": "motse", "road": "tsela", "school": "sekolo",
        "hand": "letsoho", "eye": "leihlo", "head": "hlooho", "heart": "pelo",
        "night": "bosiu", "morning": "hoseng", "big": "holo", "small": "nyane",
        "old": "khale", "run": "matha", "walk": "tsamaea", "eat": "ja", "drink": "noa",
        "sleep": "robala", "read": "bala", "write": "ngola", "speak": "bua", "come": "tla",
        "make": "etsa", "dog": "ntja", "cat": "katse", "bird": "nonyana", "fish": "litlhapi",
        "tree": "sefate", "fire": "mollo", "rain": "pula", "wind": "moea", "sky": "leholimo",
        "moon": "khoeli", "star": "naledi", "light": "khanya", "black": "ntsho", "white": "tshoeu",
        "happy": "thabetse", "hot": "chente", "cold": "batang",
    },
    "sw": {
        "the": "ya", "and": "na", "or": "au", "to": "ku", "of": "ya", "in": "katika",
        "for": "kwa", "is": "ni", "on": "juu", "that": "kwamba", "with": "na",
        "you": "wewe", "it": "hicho", "not": "si", "be": "kuwa", "are": "ni",
        "from": "kutoka", "at": "kwenye", "your": "wako", "all": "wote", "have": "na",
        "new": "mpya", "more": "zaidi", "we": "sisi", "will": "itakuwa", "home": "nyumbani",
        "can": "naweza", "us": "sisi", "about": "kuhusu", "if": "kama", "my": "wangu",
        "but": "lakini", "our": "yetu", "one": "moja", "other": "nyingine", "do": "fanya",
        "no": "hapana", "time": "wakati", "they": "wao", "he": "yeye", "what": "nini",
        "which": "ipi", "their": "wao", "there": "hapo", "see": "ona", "here": "hapa",
        "who": "nani", "now": "sasa", "get": "pata", "how": "jinsi", "me": "mimi",
        "people": "watu", "name": "jina", "year": "mwaka", "day": "siku", "two": "mbili",
        "go": "enda", "work": "fanya kazi", "good": "nzuri", "where": "wapi", "book": "kitabu",
        "life": "maisha", "know": "jua", "way": "njia", "car": "gari", "want": "taka",
        "family": "familia", "house": "nyumba", "water": "maji", "sun": "jua",
        "language": "lugha", "food": "chakula", "money": "pesa", "man": "mwanaume",
        "woman": "mwanamke", "child": "mtoto", "children": "watoto", "friend": "rafiki",
        "love": "upendo", "yes": "ndiyo", "hello": "habari", "thanks": "asante",
        "please": "tafadhali", "sorry": "pole", "help": "msaada", "world": "dunia",
        "country": "nchi", "city": "mji", "road": "barabara", "school": "shule",
        "hand": "mkono", "eye": "jicho", "head": "kichwa", "heart": "moyo",
        "night": "usiku", "morning": "asubuhi", "big": "kubwa", "small": "ndogo",
        "old": "zee", "run": "kimbia", "walk": "tembea", "eat": "kula", "drink": "kunywa",
        "sleep": "lala", "read": "soma", "write": "andika", "speak": "sema", "come": "kuja",
        "make": "tengeneza", "dog": "mbwa", "cat": "paka", "bird": "ndege", "fish": "samaki",
        "tree": "mti", "fire": "moto", "rain": "mvua", "wind": "upepo", "sky": "anga",
        "moon": "mwezi", "star": "nyota", "light": "mwanga", "black": "nyeusi", "white": "nyeupe",
        "happy": "furaha", "hot": "joto", "cold": "baridi",
    },
}


def _load_env() -> None:
    if not PLATFORM_ENV.is_file():
        return
    for line in PLATFORM_ENV.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def load_word_list(*, tier: int = 1000) -> list[str]:
    if not WORD_LIST.is_file():
        raise SystemExit(f"Missing word list: {WORD_LIST}")
    words: list[str] = []
    for line in WORD_LIST.read_text(encoding="utf-8").splitlines():
        w = line.strip().lower()
        if w and w.isalpha():
            words.append(w)
        if len(words) >= tier:
            break
    return words[:tier]


def load_cache() -> dict:
    if CACHE_PATH.is_file():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {"source": FREQ_SOURCE, "languages": {}}


def save_cache(data: dict) -> None:
    CACHE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def corpus_path(lang: str) -> Path:
    return CORPUS_DIR / f"sa_urban_{lang}.json"


def existing_translate_originals(lang: str) -> set[str]:
    path = corpus_path(lang)
    if not path.is_file():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("corrections") or data.get("accepted") or []
    return {
        (e.get("original") or "").strip().lower()
        for e in items
        if e.get("kind") == "translate" and (e.get("original") or "").strip()
    }


def wiktionary_lookup(word: str, lang: str) -> str | None:
    """Best-effort single-word gloss from Wiktionary API."""
    wiki_lang = {
        "af": "Afrikaans", "zu": "Zulu", "xh": "Xhosa",
        "tn": "Tswana", "st": "Sotho", "sw": "Swahili",
    }.get(lang)
    if not wiki_lang:
        return None
    title = urllib.parse.quote(word.capitalize())
    url = (
        "https://en.wiktionary.org/w/api.php?"
        + urllib.parse.urlencode(
            {
                "action": "parse",
                "page": word,
                "prop": "wikitext",
                "format": "json",
            }
        )
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ArjunaBadgerPress/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError):
        return None
    wikitext = payload.get("parse", {}).get("wikitext", {}).get("*", "")
    if not wikitext:
        return None
    # Look for === Language === followed by # gloss
    pattern = rf"===\s*{re.escape(wiki_lang)}\s*===.*?(?:\n#+\s*[^\n]+\n)?(?:\n|\r\n)((?:# .+\n)+)"
    m = re.search(pattern, wikitext, re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    for line in m.group(1).splitlines():
        if not line.startswith("# "):
            continue
        gloss = line[2:].strip()
        gloss = re.sub(r"\[\[([^|\]]+\|)?([^\]]+)\]\]", r"\2", gloss)
        gloss = re.sub(r"\{\{[^}]+\}\}", "", gloss).strip()
        gloss = re.sub(r"\s*\([^)]*\)", "", gloss).strip()
        if gloss and len(gloss) < 80:
            return gloss.split(",")[0].split(";")[0].strip()
    return None


def anthropic_translate_batch(words: list[str], lang: str) -> dict[str, str]:
    word_block = ", ".join(words)
    prompt = f"""Translate each English word below to {LANG_NAMES[lang]}.

Rules:
- Everyday spoken register (people's language), NOT formal scripture or textbook tone.
- Return ONLY valid JSON: an object mapping each English word (lowercase key) to its translation.
- One concise translation per word (noun/verb/adj lemma form).
- For English function words with no direct equivalent (e.g. "the" in Bantu langs), give the most natural spoken equivalent or short gloss used when teaching the word.
- Do not skip words. Do not add commentary.

Words: {word_block}"""

    platform = REPO.parent / "arjuna-badger-platform"
    if platform.is_dir():
        sys.path.insert(0, str(platform))
        try:
            from engine.llm_client import call_anthropic, openrouter_enabled

            if openrouter_enabled() or os.environ.get("ANTHROPIC_API_KEY"):
                text = call_anthropic(prompt, max_tokens=4096).strip()
                if text.startswith("```"):
                    text = re.sub(r"^```(?:json)?\n?", "", text)
                    text = re.sub(r"\n?```$", "", text)
                result = json.loads(text)
                out: dict[str, str] = {}
                for w in words:
                    val = result.get(w) or result.get(w.capitalize())
                    if isinstance(val, str) and val.strip():
                        out[w] = val.strip()
                return out
        except Exception:
            pass

    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit(
            "ANTHROPIC_API_KEY or OPENROUTER_API_KEY required for gap fill "
            "(set in arjuna-badger-platform/.env)"
        )

    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    client = anthropic.Anthropic(api_key=api_key)
    msg = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    text = msg.content[0].text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    result = json.loads(text)
    out = {}
    for w in words:
        val = result.get(w) or result.get(w.capitalize())
        if isinstance(val, str) and val.strip():
            out[w] = val.strip()
    return out


def fill_translations(
    words: list[str],
    lang: str,
    cache: dict,
    *,
    use_api: bool = True,
    use_wiktionary: bool = False,
) -> int:
    langs = cache.setdefault("languages", {})
    table: dict[str, str] = dict(langs.get(lang, {}))
    curated = CURATED.get(lang, {})
    added = 0

    missing = [w for w in words if w not in table]
    for w in missing:
        if w in curated:
            table[w] = curated[w]
            added += 1

    missing = [w for w in words if w not in table]
    if use_wiktionary:
        for w in missing:
            gloss = wiktionary_lookup(w, lang)
            if gloss:
                table[w] = gloss
                added += 1
                time.sleep(0.05)

    missing = [w for w in words if w not in table]
    if missing and use_api:
        batch_size = 40
        total_batches = (len(missing) + batch_size - 1) // batch_size
        for i in range(0, len(missing), batch_size):
            batch = missing[i : i + batch_size]
            batch_no = i // batch_size + 1
            print(f"    {lang} API batch {batch_no}/{total_batches} ({len(batch)} words)...", flush=True)
            try:
                batch_result = anthropic_translate_batch(batch, lang)
            except Exception as exc:  # noqa: BLE001
                print(f"  WARN {lang} batch {batch_no}: {exc}", file=sys.stderr, flush=True)
                continue
            for w, fix in batch_result.items():
                if w not in table and fix:
                    table[w] = fix
                    added += 1
            langs[lang] = table
            save_cache(cache)
            time.sleep(0.2)

    langs[lang] = table
    return added


def existing_translate_originals_from(entries: list[dict]) -> set[str]:
    return {
        (e.get("original") or "").strip().lower()
        for e in entries
        if e.get("kind") == "translate" and (e.get("original") or "").strip()
    }


def frequency_entries_for_lang(
    lang: str,
    words: list[str],
    translations: dict[str, str],
    *,
    existing: set[str] | None = None,
) -> list[dict]:
    if existing is None:
        existing = existing_translate_originals(lang)
    entries: list[dict] = []
    n = 0
    for word in words:
        if word in existing:
            continue
        fix = translations.get(word) or CURATED.get(lang, {}).get(word)
        if not fix:
            continue
        n += 1
        entries.append(
            {
                "id": f"freq-{lang}-{n:03d}",
                "source_lang": "en",
                "lang": lang,
                "kind": "translate",
                "original": word,
                "fix": fix,
                "temp_min": 0.0,
                "temp_max": 1.0,
                "weight": FREQ_WEIGHT,
                "source_url": FREQ_SOURCE,
                "contributor": FREQ_CONTRIBUTOR,
            }
        )
    return entries


def merge_frequency_into(entries: list[dict], lang: str, words: list[str], translations: dict[str, str]) -> tuple[list[dict], int]:
    """Append frequency rows not already present (by kind+original)."""
    seen = {(e.get("kind"), (e.get("original") or "").strip().lower()) for e in entries}
    existing = existing_translate_originals_from(entries)
    freq = frequency_entries_for_lang(lang, words, translations, existing=existing)
    added = 0
    for row in freq:
        key = (row["kind"], row["original"].strip().lower())
        if key in seen:
            continue
        entries.append(row)
        seen.add(key)
        added += 1
    return entries, added


def report_sample(translations: dict[str, dict[str, str]], words: list[str]) -> None:
    sample = ["the", "and", "water", "sun", "car", "people", "language", "book", "home", "good"]
    print("\nSample translations:")
    for w in sample:
        if w not in words:
            continue
        parts = []
        for lang in FREQ_LANGS:
            fix = translations.get(lang, {}).get(w) or CURATED.get(lang, {}).get(w, "?")
            parts.append(f"{lang}={fix}")
        print(f"  {w}: {', '.join(parts)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build frequency-1000 translation cache")
    parser.add_argument("--write-cache", action="store_true", help="Fill gaps via Wiktionary + Anthropic")
    parser.add_argument("--wiktionary", action="store_true", help="Try Wiktionary before API (slow)")
    parser.add_argument("--dry-run", action="store_true", help="Show counts only")
    parser.add_argument("--tier", type=int, default=1000, help="Max en lemmas to process (default 1000)")
    parser.add_argument("--lang", choices=FREQ_LANGS, help="Single language only")
    args = parser.parse_args()

    words = load_word_list(tier=args.tier)
    print(f"Word list: {len(words)} lemmas from {WORD_LIST.name}")

    cache = load_cache()
    _load_env()

    langs = [args.lang] if args.lang else list(FREQ_LANGS)
    if args.write_cache:
        for lang in langs:
            before = len(cache.get("languages", {}).get(lang, {}))
            added = fill_translations(
                words, lang, cache, use_api=True, use_wiktionary=args.wiktionary,
            )
            after = len(cache.get("languages", {}).get(lang, {}))
            print(f"  {lang}: {before} -> {after} translations (+{added} new)")
        cache["source"] = FREQ_SOURCE
        save_cache(cache)
        print(f"Wrote {CACHE_PATH}")

    cache = load_cache()
    translations = cache.get("languages", {})

    if args.dry_run or not args.write_cache:
        for lang in langs:
            table = translations.get(lang, {})
            existing = existing_translate_originals(lang)
            would_add = sum(
                1 for w in words
                if w not in existing and (table.get(w) or CURATED.get(lang, {}).get(w))
            )
            print(f"  {lang}: {len(table)} cached, {would_add} would merge (skip {len(existing & set(words))} dupes)")

    report_sample(translations, words)
    return 0


if __name__ == "__main__":
    sys.exit(main())
