# Unsent: The Micro-Confession Sprint — make.fun bounty
# u-boothlord-unsent-the-micro-confession-sprint-8c6596ba
#
# The program writes one two-part micro-confession to /output/entry.txt:
# a To: line naming who it was meant for, then the unsent message itself,
# one line exactly as it was typed, with no explanation after it. The gate
# takes 1 to 260 characters of UTF-8 text; the judge's brief caps the
# message line at 200 characters. Candidates were drafted against the
# judge's brief, most important first:
#   1. two parts: a To: line and the message itself, nothing else
#   2. the reason it stayed in drafts is felt in the words, not stated
#      (too honest, too late, too kind, too afraid)
#   3. the To: line and the message need each other; swapping the
#      addressee would break it
#   4. reads as typed and never sent, not written to be sent: no jokes,
#      no greetings, no motivational lines
#   5. the message is one line, written as typed, no explanation after it
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: form 10, felt 10, need 10, unsent 9, one-line 10 = 49
    ("To: Mum, on the night you waited up.\n"
     "I told you the bus was late. It wasn't. I just sat outside "
     "because I didn't want you to see me cry.",
     49),
    # score: form 10, felt 10, need 9, unsent 9, one-line 10 = 48
    ("To: Dad, in the hospital corridor.\n"
     "I said I'd be right back and went to cry in the car because "
     "I couldn't watch you be brave anymore.",
     48),
    # score: form 10, felt 9, need 10, unsent 9, one-line 10 = 48
    ("To: The girl from table six, summer 2019.\n"
     "I practised telling you your laugh was the best part of my "
     "shift for three weeks, and then you stopped coming in.",
     48),
    # score: form 10, felt 9, need 9, unsent 9, one-line 10 = 47
    ("To: The stranger on the 7:40 train.\n"
     "You lent me your umbrella and I kept it for four years "
     "because returning it meant admitting I'd never see you again.",
     47),
    # score: form 10, felt 9, need 9, unsent 8, one-line 10 = 46
    ("To: The teacher who believed in me in year ten.\n"
     "I only passed because you stayed after class, and now your "
     "classroom has someone else's name on it.",
     46),
    # score: form 10, felt 8, need 9, unsent 8, one-line 10 = 45
    ("To: My best friend, the night before your wedding.\n"
     "I wrote a toast that said I loved you first and deleted it, "
     "because your happiness was louder than mine.",
     45),
    # score: form 10, felt 8, need 8, unsent 8, one-line 10 = 44
    ("To: My first love, who married my cousin.\n"
     "I still check whether you're happy before I check whether "
     "I'm okay, and I hate that I can't stop.",
     44),
    # score: form 10, felt 8, need 8, unsent 8, one-line 10 = 44
    ("To: My brother, the one who moved away first.\n"
     "I still have your old number saved under home, and I still "
     "don't know what I'd say if you picked up.",
     44),
]


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 260, f"candidate over gate: {len(text)} chars"
        lines = text.split("\n")
        assert len(lines) == 2, "candidate must be exactly two lines"
        assert lines[0].startswith("To: "), "first line must be a To: line"
        assert 1 <= len(lines[1]) <= 200, "message line must be 1-200 chars"
        assert lines[1].strip(), "message line is blank"
        assert "http" not in text.lower(), "no links in a confession"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def audit_written(entry):
    """Re-read /output/entry.txt and prove it holds exactly `entry`.

    Returns a one-line audit note: byte length, the byte sum folded
    mod 9973, and the opening and closing characters, so a later reader
    can tell at a glance whether the file on disk is the chosen text
    or something else entirely.
    """
    import hashlib
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    assert raw == entry.encode("utf-8"), "entry.txt bytes differ from pick"
    total = sum(raw) % 9973
    digest = hashlib.sha256(raw).hexdigest()[:12]
    assert 1 <= len(entry) <= 260, "entry outside the gate"
    return (f"audit: {len(raw)} bytes, byte-sum mod 9973 = {total}, "
            f"sha256[{digest}] starts {entry[:4]!r} ends {entry[-4:]!r}")


def main():
    entry = pick(CANDIDATES)
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(entry)
    # The scorer collects the output as another user, so the file must be
    # readable by everyone (mode 0644), not just by the writer.
    os.chmod("/output/entry.txt", 0o644)
    print(audit_written(entry))
    print(entry)


if __name__ == "__main__":
    main()
