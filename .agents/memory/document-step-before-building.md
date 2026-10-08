---
name: document-step-before-building
description: The pipeline is organized as features made of steps; fully document a step in plan/<feature>/<step>.md before building any skill or agent for it
metadata:
  type: project
---

ADP is organized into features (development, testing, security, and so on), and each feature has steps. Architecture is one step of the development feature. Before creating any skill, agent, or template file for a step, write everything about that step in `plan/<feature>/<step>.md`: what it decides, its inputs and outputs, and how each conclusion was reached.

**Why:** The user wants each step's design settled and recorded before it's implemented.

**How to apply:** For each new step, start with notes, not a skill. Treat "agent or skill" as an open question until the notes are complete. See [[start-small-ask-first]].
