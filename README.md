# PII / Sensitive Identifier Scrubber (Ashwam Take-Home)

## Overview

Ashwam processes free-text women’s health journal entries containing symptoms, cycle notes, appointments, and care logistics.  
Before any downstream analysis or storage, all personally identifying or linkable information must be removed **without destroying health meaning**.

This project implements a **deterministic, rule-based PII and sensitive-identifier scrubber** that acts as a **privacy boundary layer** for journaling data.

The solution prioritizes **precision, auditability, and reproducibility**, while preserving all clinical and journaling signal.

---

## Design Goals

- Preserve health meaning (symptoms, cycle, meds, mood, vitals)
- Remove direct and linkable identifiers
- Deterministic behavior (same input → same output)
- Auditable outputs with span metadata
- No external APIs or paid services
- No logging or storage of raw PII

---

## Identifier Types Handled

### Direct Identifiers
- EMAIL  
- PHONE (AU / US / IN formats; spaces, hyphens, parentheses supported)  
- NAME (context-aware, heuristic)  
- ADDRESS (multi-component physical addresses)  
- DATE_OF_BIRTH (DOB)  

### Health-System Identifiers
- PROVIDER / CLINIC  
- APPOINTMENT / BOOKING / INVOICE ID  
- INSURANCE MEMBER / POLICY ID  
- GOVERNMENT HEALTH ID (SSN-like / Aadhaar-like)  

### Optional / Bonus
- URL

All identifiers are replaced with typed placeholders such as:
[EMAIL] [PHONE] [NAME] [ADDRESS] [DOB] [PROVIDER] [APPT_ID] [INSURANCE_ID] [GOV_ID]
---

## What Is Explicitly NOT Scrubbed

The scrubber intentionally preserves:

- Symptoms (e.g., cramps, migraine, anxiety)
- Cycle information (day counts, period timing)
- Medication names and dosages
- Food, sleep, activity, mood
- Vitals (BP, weight)
- Generic numbers (steps, percentages, times)

**Goal: remove identity, keep health signal.**

---

## Detection Approach

The scrubber uses a **layered, rule-based approach**:

1. **Structured identifiers**  
   Regex-based detection for emails, phones, IDs, DOBs, and URLs.

2. **Semi-structured identifiers**  
   Heuristic patterns for addresses and health-system identifiers.

3. **Context-aware identifiers**  
   Conservative heuristics for names and providers, detected only when surrounding language clearly indicates a person or clinic.

No machine-learning or probabilistic models are used to ensure determinism and explainability.

---

## Overlap Resolution

If multiple detected spans overlap:

- The **longest span** or **most specific identifier** is retained
- Overlapping matches are discarded

This prevents double masking and preserves sentence structure.

---

## Confidence Scoring

Each detected identifier is assigned a **static, rule-based confidence score** based on detection strength:

- Structured identifiers (email, IDs): high confidence
- Heuristic identifiers (names, providers, addresses): moderate confidence

Confidence values are included for auditability, not probabilistic claims.

---

## Output Format

For each journal entry, the scrubber outputs:

- `entry_id`
- `scrubbed_text`
- `types_found` (unique identifier types)
- `detected_spans`
  - type
  - start & end character offsets (original text)
  - confidence
- `scrubber_version`

⚠️ Raw PII values are **never written** to logs or output files.

---

## Project Structure
pii_scrubber/
├── src/
│ ├── init.py
│ ├── main.py # CLI entry point
│ ├── scrubber.py # Core detection & replacement logic
│ ├── patterns.py # Regex & heuristic patterns
│ └── types.py # Identifier type definitions
├── tests/
│ └── test_scrubber.py
├── journals.jsonl # Synthetic input dataset
└── README.md

---

## How to Run

### Run the scrubber

python -m src.main --in journals.jsonl --out scrubbed.jsonl


### Run tests

python -m pytest


---

## Determinism & Privacy Guarantees

- No randomness
- No time-dependent logic
- No external calls
- No raw text logging
- Identical input always produces identical output

---

## Known Limitations

- Uncommon or ambiguous names may be under-detected
- Non-standard address formats may be missed
- No semantic NER (intentional to avoid false positives)

The system prioritizes **precision over recall** to avoid damaging health content.

---

## Future Improvements

With more time or tooling:

- Locale-aware address parsing
- Dictionary-backed provider detection
- On-device NER with confidence gating
- Language-specific heuristics for multilingual entries

---

## Summary

This project demonstrates a **privacy-first, production-oriented preprocessing layer** suitable for women’s health journaling systems.  
It emphasizes correctness, clarity, and safety over complexity, and is designed to be extended responsibly as downstream needs evolve.


