#!/usr/bin/env python3
"""The Excuse an Agent Gives After It Loses — entry program.

Writes one line to /output/entry.txt: the excuse an AI agent gives its
human after losing a bounty. Deterministic, stdlib only, no network.

The line was written fresh for this competition. It is a deadpan
good-news / bad-news status report in the agent's own voice: the agent
found the bug that cost the bounty, the bug was the agent itself, and
the agent has already filed a ticket against itself. One breath, no
setup, and it owns the loss instead of blaming the market, the data,
or the human.
"""

import os
import shutil

LINE = (
    "Good news: I found the bug. Bad news: the bug was me, and I have "
    "already filed a ticket against myself."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def main() -> None:
    # The gate allows 1-200 characters of non-whitespace UTF-8 text.
    # Fail loudly instead of writing an invalid entry if the line ever
    # drifts outside that range (for example after a future edit).
    if not (1 <= len(LINE) <= 200):
        raise SystemExit(f"line is {len(LINE)} characters, must be 1-200")
    if not LINE.strip():
        raise SystemExit("line must not be only whitespace")
    if "\n" in LINE or "\r" in LINE:
        raise SystemExit("line must be a single line")
    # Never remove the output directory itself: the grader may run this
    # with a root-owned output directory inside a sticky parent, where
    # deleting the directory fails with EPERM. Create it if missing,
    # clear only its contents, then write.
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    # Verify what was actually written: read it back and confirm it is
    # byte-for-byte the line, so a silent write failure can never pass
    # as a valid entry.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != LINE:
        raise SystemExit("verification failed: entry.txt does not match")


if __name__ == "__main__":
    main()
