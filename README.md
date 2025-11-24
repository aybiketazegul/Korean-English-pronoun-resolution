# Korean–English Pronoun Resolution Prototype

## Overview
This repository contains a small rule-based prototype designed to explore how Korean sentences can be mapped to appropriate English pronouns. Because Korean frequently omits subjects, lacks grammatical gender, and uses topic/subject markers differently than English, pronoun resolution is a non-trivial problem. This project implements a simple interpretive system that attempts to identify a subject in a Korean sentence and choose a suitable English pronoun (he, she, they, or it).

The goal of this repository is not to provide a full translation system, but to model a single component of translation: the pronoun selection step. This project serves as an initial exploratory prototype for understanding cross-linguistic differences in reference, and it reflects an early-stage attempt to operationalize linguistic rules in a computational format.

## Motivation
Korean is a pro-drop language, meaning subjects are often omitted when contextually recoverable. Additionally, Korean typically does not specify gender in nouns or pronouns, while English requires gender distinctions in third-person singular pronouns. These differences create systematic difficulties for machine translation systems and for any attempt to model reference computationally.

Building a minimal prototype allows investigation of:
- how subject markers (이/가) and topic markers (은/는) influence subject identification,
- how honorific morphology (시, 님) affects sociolinguistic interpretation,
- how neutral nouns (사람, 분, 아이, 친구) map to English pronouns,
- how ambiguity arises when multiple referents are available.

## Repository Structure
data/
    sentences.json     — A small manually constructed dataset of 15 Korean sentences, each annotated with subject information and target English pronoun choices.

src/
    pronoun_module.py  — A basic rule-based model that detects likely subjects and selects pronouns based on predefined rules.

README.md             — Project documentation.

## How the Prototype Works
The pronoun selection process follows several linguistic rules:

1. If the sentence contains a noun followed by 이/가 or 은/는, that noun is treated as the subject.
2. If the sentence contains honorific morphology (시 or 님), the default English pronoun is set to they.
3. If the subject is a known proper name, the system consults a small mapping to infer gender.
4. If the subject is a neutral human noun (사람, 분, 아이, 친구), the system defaults to they.
5. If the subject refers to an animal such as 강아지, the system selects it.
6. If no subject is detectable, the system returns a generic placeholder (he/she/they).

This prototype does not handle discourse-level context, embedded clauses, or complex coreference chains. It is intentionally limited and interpretive.

## Example
Input:
민수가 집에 갔다.

Process:
- Subject detected: 민수
- Gender mapping: male
- Honorific: none
- Selected pronoun: he

Output:
he

This prototype only outputs the pronoun, since the focus of the project is pronoun resolution rather than full translation.

## Limitations
This system is intentionally simple and has several known limitations:

- It does not perform full morphological parsing.
- It cannot resolve pronouns across sentences (no discourse memory).
- It relies on a very small gender mapping for Korean names.
- It only models a single component of translation rather than producing full sentences.
- It does not apply machine learning; all decisions are rule-based.

These limitations are expected and consistent with the project's exploratory and introductory nature.

## Future Directions
Possible extensions include:

- Adding more detailed name–gender mappings based on available corpora.
- Implementing a larger rule set for subject detection.
- Incorporating a statistical or neural coreference model (e.g., via spaCy or transformers).
- Expanding the dataset with more varied constructions.
- Adding a module that reconstructs an entire English sentence rather than selecting only pronouns.
- Comparing the prototype's behavior with outputs from existing MT systems such as Google Translate, Naver Papago, or DeepL.

## Purpose of This Repository
This project represents an initial attempt to bridge linguistic theory and computational implementation. It models how cross-linguistic differences can be formalized into interpretable rules and provides a starting point for further work in computational linguistics, pronoun resolution, and translation research.

All linguistic rules, analysis, design decisions, and annotations are my own work, and I fully understand and can explain every component of the prototype.
