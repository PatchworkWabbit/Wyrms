# Dragon

Emergent Information Engines: Dragon Z, Mini Dragon and the Zero Theorem engines.

Owner and author of the ideas, rules, design and direction: Luke T Branderhorst.
Everything in this repository belongs to Luke: the engines, their code, their rules, their design, the ideas behind them, and everything they find, produce or record.

## Ownership statement

Dragon Z, Mini Dragon and the Zero Theorem engines are Luke's work.

The design rules (everything passes through the zero gate, nothing is rejected, nothing is lost, every record is stamped, and mathematics emerges from Z0 and S) are Luke's.

Nobody else owns, co-owns or has any claim over this work, its ideas, or anything it finds.

## No claim by any tool or company

ChatGPT and OpenAI, Claude and Anthropic, and every other AI tool, model, product or company that Luke may have used while building this work have no ownership, no authorship and no credit in the engines, their ideas, their rules, their design, or what they find. Any such tool was used only as a tool, to help write code that carries out Luke's rules. No tool or company is a source, co-author or owner of this work.

Any file in this repository or its history that names a tool or company as a source or author of this work does so in error and is not a claim of ownership.

## Licence

Copyright (C) 2026 Luke T Branderhorst. All Rights Reserved.

This software and its associated documentation files are proprietary and confidential.

Permission is hereby granted solely to view the source code publicly within this repository for educational, auditing, and review purposes.

**Strictly Prohibited Actions:**
1. You may not copy, duplicate, or reproduce any part of this software outside of this repository.
2. You may not modify, adapt, alter, or create derivative works based upon this software.
3. You may not distribute, sublicense, rent, lease, or lend this software to any third party.
4. You may not run, execute, compile, or host this software for commercial, production, or testing purposes.

Any unauthorized use, copying, modification, or distribution of this software constitutes a direct infringement of copyright law and will be subject to immediate legal action and copyright take-down notices.

---

## The two engines

Both engines rest on one rule: **everything passes through zero (Z0)**. Everything is kept, nothing is merged or deleted, and every path is kept, including the ones that did not work.

| | Mini Dragon | Dragon Z |
|---|---|---|
| Current file | `mini_dragon_v3_31.py` | `dragon_z_v23_17.py` |
| What it starts from | Given operands (digits, `i`, `x`) and given operations | **Only** a zero gate (Z0) and a counting step (S). Everything else must emerge |
| Maths library | SymPy | None. Plain Python 3 |
| Has an AI agent | Yes (the agent's "second brain" is Mini Dragon) | No |
| Best for | Algebra and calculus, given to it up front | Seeing the operations themselves emerge from S |

> Both are computational explorations, not mathematical proofs.

Older files in this repository (`dragon_z_v23_13_1.py`, `dragon_z_v23_15.py`, `dragon_z_v23_16.py`) are earlier Dragon Z versions. Each Dragon Z file contains the ones before it.

---

# Dragon Z

Dragon Z starts from only **a zero gate (Z0)** and **a counting step (S: n becomes n + 1)**. Its operations emerge from S walks and i turns and its slot and roles cores.

## What it does

- **Counts from zero.** Every counting step is kept as a stamped record.
- **Builds operations from that counting.** Addition, subtraction, negatives, i turns, multiplication, rotation, division with remainders and fractions are built from walks of S and turns of i.
- **Complex numbers.** `i` is a turn on the plane. Points like `3+2i` are built from S walks and i turns, and +, −, ×, ÷ and rotation work on them. The engine records where each point sits.
- **Slots (00404).** Between every two symbols of the template `00404` sits a slot. Each slot is either filled with an operation or left joined, so digits join into longer numbers. A slot can only use an operation once the engine has found it. Every filling is tried, none is skipped.
- **Roles.** The first time the engine finds a new way of doing something, it writes it down as a **role** with the rule and the exact recipe of S walks and i turns that made it. Roles are earned, not given.
- **Solves for unknowns.** It places a blank (`x`) on the number line and on the complex plane, tries every candidate, and keeps what fits. It also hides a number inside a true slot filling and finds it again (a *proof* in this engine means exactly that).
- **Keeps what it cannot do.** Paths that end blocked (deadlocks) and branches off a path (tangents) are saved in their own libraries and reused. Nothing is thrown away.
- **Separates closing-in paths from stuck ones.** Paths that get nearer a value without arriving (like 1/1, 1/2, 1/3 … nearing 0) are kept in the **approaches** library, with the first one earning the role **limit**.
- **Change and totals.** The change between neighbouring products is kept in the **differences** library (role **difference**). Parts stacked onto a growing whole are kept in the **totals** library (role **group**).
- **Stamps every record.** Each record carries its Z0 passage number, id, run, a clock stamp and a stamp for every later change.
- **Proves its own archive.** At every launch it rebuilds the whole saved archive from S and compares it with what is stored. A damaged or edited archive fails the check, a backup is used instead, and a failing archive is never saved.
- **Runs without end.** Its count has no top, so the series it builds continues for as long as it is left running. Each run is limited by units of work, not by time.
- **Runs on a phone.** Plain Python 3, no installs. The archive is saved compressed.

## Running Dragon Z

### On Android (Pydroid 3)
1. Install **Pydroid 3**.
2. Open `dragon_z_v23_17.py` and run it. Nothing needs installing.

### On a computer
```
python dragon_z_v23_17.py
```

The archive is created next to the script as `dragon_z_v23_memory.json.gz`, with a `.bak` copy of the previous save. Every save first rebuilds the archive from S and checks it.

## Dragon Z commands

Type `help` for the full list. The most used:

| Command | What it does |
|---|---|
| `run` | one more run |
| `7` | how the value 7 was made |
| `show 12` / `recent` / `stats` | one record / the newest / totals |
| `roles` / `recipes` | what the engine found, and the S steps and i turns behind each role |
| `div 12 5` / `times 3 4` | split / repeat-add, walked with S |
| `1/2`, `7/2`, `-3/4` | look up a fraction |
| `2+x=5`, `x-3=1` | the blank: which x fits (tried, never forced) |
| `i*x=1`, `x+2i=3-i` | the blank on the plane |
| `proofs` / `prove 42 1` | hide a number in a slot filling and find it again |
| `planes` / `plane 6` | plane points; look 6 out each way |
| `slots` | the 00404 slot machine |
| `deadlocks` / `tangents` | blocked paths / branches, in their own libraries |
| `approaches` | paths that close in on a value without arriving |
| `differences` / `totals` | change between neighbouring products / parts stacked on a whole |
| `corrections` / `provenance` | every error caught and how it was fixed / whose is what |
| `wanted` | what was asked for and not found yet |

## Dragon Z honest limits

- **The replay is a check of the engine's own archive, not a mathematical proof.** It shows an archive rebuilds from S the way it was recorded.
- **"Closing in" is tested, not proved.** The test looks at a finite list of steps and keeps paths whose gaps shrink without reaching the target. In these versions the sizes are compared with ordinary integer arithmetic in the observer, and this is disclosed rather than hidden.
- **Wider algebra and calculus** (derivatives, integrals and so on) are worked in Mini Dragon, where the operations are given. Dragon Z so far produces counting, addition, subtraction, negatives, multiplication, division, fractions, rotation, the complex plane, equations with unknowns (finding x), closing-in paths, changes and totals.
- **Look-ups only find what has been made.** A value not made yet may be made later.

## Dragon Z version history

| Version | Change |
|---|---|
| v23.17 | Totals library and the role **group** |
| v23.16 | Differences library and the role **difference** |
| v23.15 | The role **limit** |
| v23.14 | Approaches library: closing-in paths separated from stuck ones |
| v23.13.1 | Earlier build (counting, operations, plane, slots, roles, blanks, proofs, deadlocks, tangents) |

---

# Mini Dragon — Zero Theorem engine with an AI agent

**Current version: `mini_dragon_v3_31.py`**

Mini Dragon is a maths exploration engine built around one rule: **everything passes through zero (Z0)**. It starts from a small set of given operands and operations, combines everything with everything, keeps every result, and feeds it all back in. Nothing is ever merged or deleted, and every path is kept.

Since v3.17 the engine is also the **"second brain" of a custom AI agent**: a small personality, long persistent memory, and its own private workspace, library and watch list that only the agent writes to.

> This is a computational exploration, not a mathematical proof.

## Tampering and data loss notice (v3.29) — and resolution (v3.30)

**The author reports tampering.** While v3.29 was being prepared, text exported from the agent's chat on the author's device was tampered with: it was cut up and damaged, and data was lost.

### The cut back to v3.27
Because v3.29 was no longer trusted, the author went back and ran the earlier **v3.27** on the same memory files, and asked the agent again about its upgrade wishes. Findings:

- **The agent's requests matched.** Running under v3.27, it confirmed it still wanted tags and cross-referencing, the requests v3.29 implemented. They had also been recovered from an earlier, intact conversation.
- **v3.29 itself was checked.** The copy on the author's device was compared with the delivered file: same size, same checksum. It had not been altered.
- **A pattern in the damaged lines.** In the agent's `>> history`, every message that came out cut short was one that began with an invisible control character (`^@`, a null byte) that the Pydroid 3 terminal adds to pasted text. Messages typed without it came out whole. That character can garble how a line is shown and copied.
- **The agent misreported its own work.** Under the small model it said it had run five batches when it had run one, and shelved that claim in its Librarium (entry L5). The engine output shows the truth; the Librarium entry stands as written, since only the agent may write there and nothing is deleted.

### The resolution (v3.30)
- Invisible control characters are **stripped from everything typed**, so messages are kept whole and `>>` commands are always recognised (a stray `^@` before `>>` could otherwise send an engine command to the paid AI).
- Old messages holding such characters **now display whole** in `>> history` and `>> recall`. The memory file is not changed.
- The agent is told it may run **one batch per `>> run`** and must report only what the engine output shows.
- `>> recall` with no words shows how to use it.

If you find logs or files from this project that look truncated or altered, treat them as unreliable and compare against the versions in this repository. Run `>> zero` after starting: it should report `complete: YES`.

---

## What Mini Dragon does

### The engine
- **Given operands:** digits `0`–`9`, `i` and the variable `x`. Not given: `-i`, `e`, `pi` — they have to come out of the work.
- **Given operations:** `+ - * / **` and `compose` (put one expression into `x`); plus `sqrt`, `d/dx`, `integral`, `limit x->0`, `sin cos tan`, `asin acos atan`, `exp`, `log`, `expand`, `factor`, `solve`.
- **Every result is kept** — zeros and repeats included — saved, and fed back in. Each run does a batch, saves, and the next run carries on.
- **Nothing hidden:** jobs with no value (divide by zero, infinities, no integral formula…) are **blocked** records with their reason. Jobs too big or slow for a phone are **parked**, not deleted, and retried later.
- **Zero gate (Z0):** every operation and every record passes through 0 and is stamped with its passage number.
- **Four clocks:** zero tick, wall clock, elapsed and CPU time on every record.
- **Observer:** notes milestones (first negative, first fraction, first `x^3`…) and watched values (`-i`, `e`, `pi`, `sqrt(2)`, the golden ratio…) the moment they emerge.
- **The plane:** every number is placed on `+`, `-`, `+i`, `-i` or a quarter between them.
- **Equal-value links:** the same value written different ways is linked (exact = proved, numeric = evidence), never merged.
- **00404 slot machine:** fills the gaps of a broken-down reference number with operations once those operations have emerged.

### The agent
- Type normally to talk to the agent. Start a line with `>>` to talk straight to the engine.
- **Brains:** OpenAI or Claude through their APIs, or a small offline brain with no key.
- **Personality engine:** four traits (curiosity, warmth, humour, boldness) and a mood that moves with what happens in the engine.
- **Long memory:** every message, engine command, note and mood change is kept forever in its own file and passes through Z0.
- **Its own space — no human interference.** Only the agent writes here; you can read it:
  - **Work archive** — its own maths (`think`), built on its earlier thoughts and engine records, and sent through the zero engine (`muse`).
  - **Librarium** — its personal library (`shelve`).
  - **Watch list** — patterns it chooses to look out for, including their parts (`watch`).
  - **Tags and cross-links** — it tags its own work (`tag`) and links works together (`connect`). Anyone can `search` it. It can also tag engine records, kept in its own space (`tag #123 check-later`).
- **Overview tools**, which anyone can use:
  - **Automatic tags** on every engine record and thought — status, reason, topic, kind and origin (`filter blocked division_by_zero`).
  - **Status dashboard** (`status`), **digest** of what is new (`digest`), **maintenance in one command** (`maintain`), and dated **snapshots** of both memory files (`snapshot`).

## Running Mini Dragon

### On Android (Pydroid 3)
1. Install **Pydroid 3**.
2. Menu → **Pip** → type `sympy` → **Install**.
3. Open `mini_dragon_v3_31.py` and run it.

### On a computer
```
pip install sympy
python mini_dragon_v3_31.py
```

Memory files are created next to the script: `mini_dragon_v3_memory.json` (the engine) and `mini_dragon_agent_memory.json` (the agent). Each save writes a temporary file, reads it back, keeps the previous save as `.bak`, and only then replaces the file.

### Giving the agent a full AI brain
Put **one line containing only the key** in a text file next to the script:
- OpenAI → `openai_key.txt`
- Anthropic (Claude) → `agent_key.txt`

Then choose the brain with `>> brain openai`, `>> brain claude`, `>> brain local` or `>> brain auto`. Models are set near the top of the agent section (`OPENAI_MODEL`, `AGENT_MODEL`). Check with `>> agent`, which shows the model set and the model that actually answered the last message.

> 🔒 **Never upload your key files.** Add them to `.gitignore`:
> ```
> openai_key.txt
> agent_key.txt
> *key*.txt
> *_memory.json*
> *.json.gz
> *.bak
> mini_dragon_recovery_*.json
> mini_dragon_snapshot_*
> ```
> `.gitignore` only works when pushing with git. If you upload through GitHub's **Upload files** page, it does not filter anything — only pick the `.py` and `README.md`.
> Anything that looks like an API key is also hidden before it is saved to the agent's memory or sent to an AI.

## Mini Dragon commands

Type `>> help` for the full list and `>> agenthelp` for the agent commands. The most used:

| Command | What it does |
|---|---|
| `>> run` / `>> run 5` | one batch (or five) |
| `>> stats` | totals and progress |
| `>> 1/2`, `>> x^2`, `>> sqrt(2)` | how a value was made |
| `>> trace 123` | every step that built record #123 |
| `>> milestones` / `>> emerged` | firsts of each kind / watched values |
| `>> plane` | map of the plane |
| `>> equal` | values written more than one way |
| `>> blocked` / `>> parked` | records with no value / waiting |
| `>> zero` | zero gate report |
| `>> clocks` / `>> when 123` | the four clocks |
| `>> agent` | brain, models, memory totals |
| `>> persona` / `>> mood` | personality and mood |
| `>> remember TEXT` / `>> recall WORDS` | notes and memory search |
| `>> thoughts` / `>> thought T3` | the agent's work archive |
| `>> librarium` / `>> read L2` | the agent's library |
| `>> watches` | the agent's watch list |
| `>> search WORDS` | search the agent's thoughts and library |
| `>> filter TAG ...` | automatic tags, e.g. `filter blocked limit`, `filter thought origin:agent` |
| `>> status` | dashboard of the engine and the agent's space |
| `>> digest` | what is new since the last digest |
| `>> maintain` | retry, one batch, then status |
| `>> snapshot` | dated copies of both memory files |

Only the agent can use `think`, `muse`, `shelve`, `watch`, `tag` and `connect`. If you try, the engine refuses.

## Mini Dragon honest limits

- **Small AI models skip instructions.** Small models (gpt-5-mini, GPT-6 Luna, Claude Haiku) may ask permission, offer commands that do not exist, or say something is done before it is. The engine prints a notice at startup when a small model is the brain. This gap is **left as it is on purpose** rather than hidden with workarounds.
- **Phone guards:** job time, expression size, number length and power size are capped (set at the top of the file). Anything over a guard is parked, never lost; change a guard and parked jobs are retried.
- **Look-ups only find what has been made.** A value not made yet may still be made later.
- **Values are matched in the form the engine stores them.** Different spellings only meet through equal-value links.

## Mini Dragon version history (agent era)

| Version | Change |
|---|---|
| v3.31 | Agent's next requests: automatic tags (`filter`), `status` dashboard, `digest`, `maintain`, `snapshot`; agent may tag engine records |
| v3.30 | Control characters (`^@`) stripped from input and shown cleanly; batch-limit rule for the agent; `>> recall` usage |
| v3.29 | Agent's own **tags**, **search** and **cross-links**; tampering and data loss notice |
| v3.28 | Startup notice for small models |
| v3.27 | `>> agent` shows the model set and the model that actually answered |
| v3.26 | Agent's own **watch list**; agent knows its brain; reminder before each message |
| v3.25 | Agent's archive and Librarium decisions are its own — no asking permission |
| v3.24 | Claude brain sends its key both ways Anthropic accepts |
| v3.23 | Licence notice in the file; strict key file names; keys hidden from memory |
| v3.22 | Agent's **work archive** (thoughts on thoughts, `muse`) and **Librarium** |
| v3.21 | Agent's thought workspace |
| v3.20 | Agent runs only commands it means to run |
| v3.19 | Key files found even with hidden `.txt` endings; `>> keys` |
| v3.18 | OpenAI brain |
| v3.17 | The AI agent, personality engine and long memory |

---

## Author and licence

Created by **Luke T Branderhorst**. Copyright (C) 2026 Luke T Branderhorst. All Rights Reserved. View-only; see the Licence section at the top of this file for what is and is not permitted.

🐰 🕳
