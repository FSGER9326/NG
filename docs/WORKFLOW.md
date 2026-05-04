# NG Workflow

## Source of truth

GitHub is the permanent source of truth.

ChatGPT project memory, chat history, and local editor state are useful but secondary. Anything important should be written into the repo.

## Durable handoff files

Future chats should start by reading:

1. `docs/PROJECT_STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/GAME_DESIGN.md`
4. `docs/ART_BIBLE.md`
5. `docs/BUGFIXING.md`
6. `docs/ASSET_POLICY.md`

## How to request work in a new chat

Use this prompt:

```text
Open GitHub repo FSGER9326/NG. Read docs/PROJECT_STATUS.md, docs/ROADMAP.md, docs/WORKFLOW.md, and docs/BUGFIXING.md first. Continue from the current roadmap. Keep changes small, update PROJECT_STATUS if priorities change, and validate JSON with tools/validate_project.py.
```

## Development rules

- Prefer small commits.
- Prefer one feature per branch/PR once the project gets larger.
- Keep content data in JSON.
- Keep design decisions in Markdown.
- Keep code in small GDScript files.
- Do not rely on hidden Godot editor state.
- Add or update validation when a new data format is introduced.
- Do not add large raw asset dumps directly to the repo.

## Recommended branch pattern

- `main`: stable project state
- `feature/area-prototype`
- `feature/dialogue-system`
- `feature/combat-prototype`
- `content/wolfpine-village`
- `assets/ui-foundation`

## Best collaboration model

For each task, aim for:

1. Inspect relevant files.
2. Patch a small set of files.
3. Update docs if behavior/design changes.
4. Run or reason through validation.
5. Report exact files changed and next task.

## What belongs in ChatGPT Project instructions

The web ChatGPT project instructions should be short and procedural, not a full design document.

Suggested project instruction:

```text
For the NG RPG project, GitHub repo FSGER9326/NG is the source of truth. Before work, read docs/PROJECT_STATUS.md, docs/ROADMAP.md, docs/WORKFLOW.md, and docs/BUGFIXING.md. Prefer small text-first changes. Keep game content data-driven in JSON/Markdown/GDScript. Update PROJECT_STATUS.md and ROADMAP.md when priorities or scope change. Always preserve low-spec Godot 4 Compatibility renderer target.
```

## What project sources should contain

If using ChatGPT Project Sources, upload or sync only high-level stable docs:

- `docs/PROJECT_STATUS.md`
- `docs/ROADMAP.md`
- `docs/GAME_DESIGN.md`
- `docs/ART_BIBLE.md`
- `docs/WORKFLOW.md`
- `docs/BUGFIXING.md`

Do not rely on project sources for code truth. Code truth stays in GitHub.
