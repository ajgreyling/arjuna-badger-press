# Scripts

## `deploy_static_webdock.sh`

Dry-run-first static deploy helper for a future Webdock migration.

Default behavior is safe:

```bash
scripts/deploy_static_webdock.sh
```

It builds `site/public/`, probes common Webdock SSH users, and runs `rsync --dry-run`.

Run a real deploy only after the dry run looks correct:

```bash
ABP_DEPLOY_SERVER=your.webdock.host \
ABP_DEPLOY_DRY_RUN=0 \
ABP_REMOTE_RELOAD="sudo systemctl reload caddy" \
scripts/deploy_static_webdock.sh
```

Cost-saving default: keep `arjunabadger.press` on GitHub Pages and use Webdock only for
`api.arjunabadger.press` until the static site has a reason to move.
