# Cooper Labs — Claude plugins

The marketplace Cooper Labs uses to distribute its Claude plugins. Add it
once, install what you need, and updates arrive when a new version is
pushed here.

## Install

**In Cowork**: Customize → Plugins → Add marketplace → from a repository,
then enter this repository's URL. The catalogue appears as **cooper-labs**;
click Install on **cooper-brand**. To pick up a new version later, remove
the marketplace and add it again.

**In Claude Code**:

```
/plugin marketplace add Nexarion434/cooper-labs
/plugin install cooper-brand@cooper-labs
```

**In ChatGPT / Codex**: the same repository is also a Codex marketplace
(`.agents/plugins/marketplace.json`, and `.codex-plugin/plugin.json` in the
plugin). In Codex CLI: `codex plugin marketplace add cooper-labs-tech/cooper-plugin`,
then enable **cooper-brand** in the Plugins tab (ChatGPT desktop or web,
Codex app; not the IDE extension). The skills are the same files; their
build commands use `${CLAUDE_PLUGIN_ROOT}`, which Codex does not set, so
set `S` to the plugin's `assets/scripts` folder by hand there.

## Plugins

| Plugin | What it does |
|---|---|
| **cooper-brand** | Cooper Labs' brand kit: the A4 internal-document template with sixteen page styles (proposal, case study, spec, post-mortem, memo, guide), the 16:9 deck, the A4 fact sheet, the social cards of the Figma file (post, partner, X cover, social preview) in eleven sizes, the banners, the thread cards, the animated MP4, the six renders. See [its README](plugins/cooper-brand/README.md) and [CHANGELOG](plugins/cooper-brand/CHANGELOG.md). |

## Layout

```
.claude-plugin/marketplace.json    the catalogue
plugins/<name>/                    one folder per plugin, with its own .claude-plugin/plugin.json
```

## Keep this repository private

`plugins/cooper-brand/assets/fonts/private/` carries the licensed PP Eiko
file so that documents and cards render exactly in a cloud session. It
must not be redistributed: keep the repository private (see the README in
that folder and the `.gitignore` at the root).

## Publishing an update

Bump `version` in the plugin's `plugin.json` and in `marketplace.json`,
commit, push. The design source is the Figma file *Brand Identity* for the
social cards and the plugin itself for the documents (see the CHANGELOG's
design decisions); when either changes, the CSS and the assets follow, and
the version is bumped.
