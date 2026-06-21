# Plausible analytics

Arjuna Badger Press uses Plausible as the public-site analytics layer. The static site sends no
cookies and does not require accounts for analytics.

## Current instrumentation

The generated site emits the Plausible script from `site/build.py` when `ABP_PLAUSIBLE_DOMAIN` is
set, defaulting to `arjunabadger.press`.

Tracked events:

| Event | Fired when | Props |
| --- | --- | --- |
| `Rating` | A reader clicks a book star rating | `book`, `score` |
| `Download` | A public download link is clicked | `file`, `type`, `label`, `location` |
| `CTA` | A primary button/support/feedback link is clicked | `label`, `href`, `location` |
| `Contact` | A `mailto:` link is clicked | `label`, `location` |
| `Lead` | An intake form is submitted | `form`, `action`, `location` |
| `Reader Import` | The local reader imports files | `kind`, `count`, `location` |
| `Reader Open` | The local reader opens an imported item | `kind`, `location` |
| `Reader Clear` | The local reader session is cleared | `location` |

Privacy rule: the local reader never sends imported filenames. It only sends file kind and count.
Public download links send the public download path because that file is already on the website.

## Launch dashboard

Watch these first:

1. Traffic by source for launch posts: `visit:source`.
2. Landing pages: `event:page`.
3. Ebook/PDF interest: `Download` grouped by `type` and `file`.
4. Marketplace demand: `Lead` grouped by `form`.
5. Reader-app demand: `Reader Import` and `Reader Open` grouped by `kind`.
6. Book quality signal: `Rating` grouped by `book` and `score`.
7. Consulting/profile interest: `CTA` and `Contact` on `/cv.html`.

## Plausible CLI workflow

The referenced `plausible-cli` project uses the binary name `plausible`.

Install it from its GitHub releases, or build from source if Go is available. Then set tokens:

```bash
export PLAUSIBLE_DOMAIN=arjunabadger.press
export PLAUSIBLE_TOKEN='plugins-api-token-from-site-settings'
export PLAUSIBLE_STATS_TOKEN='stats-api-key-from-account-settings'
```

Useful commands:

```bash
plausible goals list --all
plausible custom-props list
plausible tracker-config get
plausible stats query --metrics visitors,visits,pageviews --dimensions visit:source --date-range 7d
plausible stats query --metrics events --dimensions event:name --date-range 7d
plausible stats query --metrics events --dimensions event:name,event:props:form --date-range 30d
```

Create event goals in the Plausible UI or with the CLI:

```bash
plausible goals create --body '{"goals":[{"goal_type":"event","event_name":"Lead"}]}'
plausible goals create --body '{"goals":[{"goal_type":"event","event_name":"Download"}]}'
plausible goals create --body '{"goals":[{"goal_type":"event","event_name":"Reader Import"}]}'
plausible goals create --body '{"goals":[{"goal_type":"event","event_name":"Rating"}]}'
plausible goals create --body '{"goals":[{"goal_type":"event","event_name":"Contact"}]}'
```

Enable custom properties you actually query:

```bash
plausible custom-props enable --body '{"custom_props":["book","score","form","action","location","file","type","label","href","kind","count"]}'
```

Do not store Plausible tokens in the repo. Use shell exports, a local password manager, or
`~/.config/plausible/config.yaml`.
