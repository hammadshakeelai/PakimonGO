# Conversation Archive

## Purpose

This folder preserves long-form project conversation context so future humans and AI agents can recover the original user intent instead of relying only on compressed summaries.

Use this area for raw prompts, full pasted chats, session summaries, decision handoffs, and important AI responses that shaped the project.

## Required Rule

Every AI agent doing meaningful work on this repository must update the conversation archive when the conversation changes project direction, requirements, architecture, process, risks, backlog, or implementation state.

At minimum, before ending a meaningful task, add or update:

- `docs/conversation-archive/raw/FULL_CONVERSATION_COPY_PASTE_HERE.txt` when the user provides a full chat export.
- `docs/conversation-archive/summaries/` with a short session summary if the full chat is too large.
- `docs/CURRENT_TASK.md`, `docs/NEXT_TASK.md`, and `docs/CURRENT_THINKING.md` with the actionable current state.

## What To Store

Store:

- User prompts and corrections.
- AI responses that define plans, requirements, or decisions.
- Accepted decisions.
- Rejected decisions.
- Open questions.
- Current task and next task handoff notes.
- Links to relevant files changed in the same session.

Do not store:

- Secrets, API keys, passwords, tokens, private recovery codes.
- Private user photos or exact capture locations.
- Hidden system/developer/tool instructions that are not visible to the user.
- Third-party copyrighted text beyond normal fair-use snippets or links.

## Suggested Paste Format

Use this shape in the raw text file:

```txt
SESSION DATE:
SOURCE:
PURPOSE:

USER:
...

ASSISTANT:
...

DECISIONS:
...

NEXT TASK:
...
```

If the conversation is extremely large, paste it into multiple numbered files under `raw/` and add a summary under `summaries/`.
