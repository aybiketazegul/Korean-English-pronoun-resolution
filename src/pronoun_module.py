"""
pronoun_module.py

A very small rule-based prototype for Korean → English pronoun resolution.
Given a simple Korean clause, it tries to:

1. Detect a likely subject using case/topic particles (이/가/은/는).
2. Check whether the sentence contains honorific morphology (시, 님).
3. Map the detected subject to an English pronoun (he, she, they, it).

This is intentionally simple and meant for controlled examples,
not for real-world text.
"""

# A small mapping of known Korean names to gender.
NAME_GENDER = {
    "민수": "male",
    "영희": "female",
    "지민": "unknown",  # ambiguous in Korean
}


def detect_honorific(sentence: str) -> bool:
    """
    Return True if the sentence contains basic honorific morphology.

    We treat the presence of '시' or '님' as a coarse indicator of
    an honorific subject (e.g., 선생님, 저 분, 부모님).
    """
    return ("시" in sentence) or ("님" in sentence)


def detect_subject(sentence: str) -> str | None:
    """
    Very simple subject detection using surface particles.

    Strategy:
    - Look for the first occurrence of one of the particles:
      이, 가, 은, 는
    - Take everything before that particle as the "subject" string.
    - If no particle is found, return None (treated as pro-drop).

    This ignores many real complexities (embedded clauses, etc.).
    """
    particles = ["이", "가", "은", "는"]

    for p in particles:
        if p in sentence:
            idx = sentence.index(p)
            subject = sentence[:idx].strip()
            # Empty string → treat like "no subject"
            return subject or None

    # No particle detected → pro-drop case
    return None


def choose_pronoun(subject: str, honorific: bool = False) -> str:
    """
    Choose an English pronoun for a given subject string.

    Parameters
    ----------
    subject : str
        A rough subject candidate (e.g., '민수', '저 사람', '강아지').
    honorific : bool
        Whether the sentence contained honorific morphology.

    Returns
    -------
    str
        One of: 'he', 'she', 'they', 'it'.
        (In ambiguous cases, defaults to 'they'.)
    """
    # If there is honorific morphology, default to 'they'
    # (gender-neutral, respectful)
    if honorific:
        return "they"

    # Known proper names → use small gender mapping
    if subject in NAME_GENDER:
        g = NAME_GENDER[subject]
        if g == "male":
            return "he"
        elif g == "female":
            return "she"
        else:
            return "they"

    # Neutral human nouns → 'they'
    neutral_nouns = ["사람", "분", "아이", "친구"]
    if any(n in subject for n in neutral_nouns):
        return "they"

    # Animals → 'it' (very simplified)
    if ("강아지" in subject) or ("개" in subject):
        return "it"

    # Default safe choice
    return "they"


def resolve_pronoun(sentence: str) -> str:
    """
    Main entry point: given a Korean sentence, return an English pronoun.

    - Attempts to detect the subject.
    - Checks for honorific morphology.
    - If no subject can be detected, returns a generic '(he/she/they)' placeholder.

    This function is what we evaluate on the controlled dataset in data/sentences.json.
    """
    subject = detect_subject(sentence)
    honorific = detect_honorific(sentence)

    # Pro-drop or failure to detect subject
    if subject is None:
        return "(he/she/they)"

    # Remove particles from the detected subject string
    for p in ["이", "가", "은", "는"]:
        subject = subject.replace(p, "")

    subject = subject.strip()

    if subject == "":
        return "(he/she/they)"

    return choose_pronoun(subject, honorific)


if __name__ == "__main__":
    # Quick manual test on a few examples
    tests = [
        "학교에 갔다.",
        "민수가 집에 갔다.",
        "영희는 숙제를 끝냈다.",
        "선생님이 오셨어요.",
        "저 사람은 의사예요.",
    ]
    for t in tests:
        print(t, "→", resolve_pronoun(t))
