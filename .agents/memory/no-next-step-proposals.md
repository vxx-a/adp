---
name: no-next-step-proposals
description: Don't end turns with next-step proposals, suggested actions, or buttons; report what was done and stop
metadata:
  type: feedback
---

End a turn by saying what was done and what isn't finished. Don't offer next steps, suggest actions like committing, or show choice buttons. Ask only when the work can't continue without the user's answer.

**Why:** The user asked how to stop the constant proposals, meaning the next-step box with buttons at the end of each turn.

**How to apply:** In the Claude desktop app, call wrap_up with a recap only: no `ask`, no `actions`. Don't propose follow-up sessions. See [[start-small-ask-first]].
