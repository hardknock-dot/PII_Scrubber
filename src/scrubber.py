from dataclasses import dataclass
from typing import List, Dict

from src.patterns import PATTERNS
from src.types import IdentifierType



@dataclass
class DetectedSpan:
    type: IdentifierType
    start: int
    end: int
    confidence: float


CONFIDENCE_MAP = {
    IdentifierType.EMAIL: 0.95,
    IdentifierType.PHONE: 0.9,
    IdentifierType.DATE_OF_BIRTH: 0.85,
    IdentifierType.APPOINTMENT_ID: 0.95,
    IdentifierType.INSURANCE_ID: 0.9,
    IdentifierType.GOVERNMENT_ID: 0.9,
    IdentifierType.URL: 0.95,
    IdentifierType.PROVIDER: 0.7,
    IdentifierType.NAME: 0.65,
    IdentifierType.ADDRESS: 0.75,
}


def detect_spans(text: str) -> List[DetectedSpan]:
    spans: List[DetectedSpan] = []

    for id_type, pattern in [
        (IdentifierType.EMAIL, PATTERNS.EMAIL),
        (IdentifierType.PHONE, PATTERNS.PHONE),
        (IdentifierType.DATE_OF_BIRTH, PATTERNS.DOB),
        (IdentifierType.ADDRESS, PATTERNS.ADDRESS),
        (IdentifierType.APPOINTMENT_ID, PATTERNS.APPOINTMENT_ID),
        (IdentifierType.INSURANCE_ID, PATTERNS.INSURANCE_ID),
        (IdentifierType.GOVERNMENT_ID, PATTERNS.GOVERNMENT_ID),
        (IdentifierType.URL, PATTERNS.URL),
        (IdentifierType.PROVIDER, PATTERNS.PROVIDER),
        (IdentifierType.NAME, PATTERNS.NAME),

    ]:
        for match in pattern.finditer(text):
            spans.append(
                DetectedSpan(
                    type=id_type,
                    start=match.start(),
                    end=match.end(),
                    confidence=CONFIDENCE_MAP[id_type],
                )
            )

    return resolve_overlaps(spans)


def resolve_overlaps(spans: List[DetectedSpan]) -> List[DetectedSpan]:
    # Sort by longest span first, then earlier start
    spans = sorted(spans, key=lambda s: (-(s.end - s.start), s.start))

    resolved = []
    occupied = set()

    for span in spans:
        if any(i in occupied for i in range(span.start, span.end)):
            continue
        for i in range(span.start, span.end):
            occupied.add(i)
        resolved.append(span)

    return sorted(resolved, key=lambda s: s.start)


def apply_replacements(text: str, spans: List[DetectedSpan]) -> str:
    result = []
    last_idx = 0

    for span in spans:
        result.append(text[last_idx:span.start])
        result.append(f"[{span.type.value}]")
        last_idx = span.end

    result.append(text[last_idx:])
    return "".join(result)


def scrub_entry(entry_id: str, text: str, scrubber_version: str) -> Dict:
    spans = detect_spans(text)
    scrubbed_text = apply_replacements(text, spans)

    return {
        "entry_id": entry_id,
        "scrubbed_text": scrubbed_text,
        "types_found": sorted({span.type.value for span in spans}),
        "detected_spans": [
            {
                "type": span.type.value,
                "start": span.start,
                "end": span.end,
                "confidence": span.confidence,
            }
            for span in spans
        ],
        "scrubber_version": scrubber_version,
    }
