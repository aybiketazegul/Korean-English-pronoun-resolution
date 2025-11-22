# Simple rule-based Korean→English pronoun resolution prototype

# A small mapping of known Korean names to gender
NAME_GENDER = {
    "민수": "male",
    "영희": "female",
    "지민": "unknown"
}

def detect_honorific(sentence):
    """Detect honorific features."""
    return ("시" in sentence) or ("님" in sentence)

def detect_subject(sentence):
    """Very simple subject detection using 이/가 or 은/는."""
    particles = ["이", "가", "은", "는"]
    for p in particles:
        if p in sentence:
            idx = sentence.index(p)
            subject = sentence[:idx].strip()
            return subject
    return None  # pro-drop case

def choose_pronoun(subject, honorific=False):
    """Choose English pronoun based on gender/honorific rules."""
    if honorific:
        return "they"

    # Known names
    if subject in NAME_GENDER:
        g = NAME_GENDER[subject]
        if g == "male":
            return "he"
        elif g == "female":
            return "she"
        else:
            return "they"

    # Neutral nouns → they
    neutral_nouns = ["사람", "분", "아이", "친구"]
    if any(n in subject for n in neutral_nouns):
        return "they"

    # Animals → it
    if ("강아지" in subject) or ("개" in subject):
        return "it"

    # Default
    return "they"

def resolve_pronoun(sentence):
    """Main function: detect subject + determine pronoun."""
    subject = detect_subject(sentence)
    honorific = detect_honorific(sentence)

    if subject is None:
        return "(he/she/they)"

    # remove particles
    for p in ["이", "가", "은", "는"]:
        subject = subject.replace(p, "")

    subject = subject.strip()
    return choose_pronoun(subject, honorific)

# Quick manual test
if __name__ == "__main__":
    tests = [
        "학교에 갔다.",
        "민수가 집에 갔다.",
        "영희는 숙제를 끝냈다.",
        "선생님이 오셨어요.",
        "저 사람은 의사예요."
    ]

    for t in tests:
        print(t, "→", resolve_pronoun(t))
