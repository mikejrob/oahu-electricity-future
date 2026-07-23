# Comment and response policy

This analysis is published as a **pre-release for public scrutiny**. We invite
comments, corrections, and challenges from anyone — Hawaiian Electric, the
Public Utilities Commission, state agencies, JERA, advocates, academics, and
members of the public. This page states what we commit to, so that both good
faith and bad faith are easy to recognize.

## What we commit to

1. **Every specific, sourced claim gets investigated and answered publicly.**
   If you assert that an input is wrong, a source is misread, a calculation
   fails, or a scenario is mis-specified — and you point to the file, number,
   or passage — we will check it and publish what we find, whether it
   confirms our work or corrects it.
2. **Corrections are published whichever direction they cut.** The record of
   this project shows corrections that strengthened the case for LNG and
   corrections that weakened it; that practice continues.
3. **Responses come in batches on a regular cadence** (approximately every
   two weeks during the comment period), as a tagged repository release with
   a changelog entry per comment addressed: what was claimed, what we found,
   what changed. Between tags the published version is frozen — numbers do
   not drift.
4. **Private comments are welcome and can be answered publicly in anonymized
   form.** Some knowledgeable readers cannot comment under their own names.
   Email the authors; if the comment is substantive we will address it in the
   public record as "a reviewer noted…" unless you ask otherwise.

## How to comment

- **GitHub issue** (preferred): one issue per distinct point. Label it
  `data`, `method`, `scenario`, or `question`.
- **Email**: mjrobert@hawaii.edu — same treatment, with anonymity on request.
- The most useful comments name **(a)** the specific input, number, or claim,
  **(b)** the file or section where it appears, and **(c)** the source you
  believe supports a different value. `REVIEWER_GUIDE.md` shows the fastest
  paths to check anything.

## What we do not commit to

- **Unsourced generalities** ("the model is wrong," "everyone knows solar
  can't work here") are acknowledged and indexed; investigation goes to comments that
  point at something checkable, which move to the front of the queue.
- **Duplicates** are consolidated into the first issue on the point.
- **Questions of motive** — ours or anyone else's — are outside scope. The
  numbers are checkable by anyone; that is the point of publishing them.
- We do not commit to real-time engagement. The cadence above is the
  commitment; it is chosen to be sustainable for the duration of the comment
  period.

## Revision discipline

The pre-release will be tagged (`v1.0-pre1`) when this repository opens for comment. Each response batch produces a new
tag (`-pre2`, `-pre3`, …) whose changelog lists every change and the comment
that prompted it. When the comment period closes, the final version is tagged
`v1.0` with a complete summary of what changed during public review, and the
pre-release banner is removed. Citations should name the tag.

## Scope of the comment period

Comments on inputs, sources, methods, scenarios, and interpretation are all
in scope. So are requests for additional scenarios — the roadmap
(`ROADMAP.md`) lists what is already planned, and public requests have
already shaped the analysis (the no-mandate and conversion cases in Section
4.6 originated as challenges we posed ourselves; better versions of such
challenges are exactly what we are asking for).
