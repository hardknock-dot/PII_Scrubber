import re
from types import SimpleNamespace


PATTERNS = SimpleNamespace(

    EMAIL=re.compile(
        r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
    ),

    PHONE=re.compile(
        r"""
        (?:
            (\+?\d{1,3}[\s-]?)?
            (\(?\d{2,4}\)?[\s-]?)
            \d{3,4}[\s-]?\d{3,4}
        )
        """,
        re.VERBOSE
    ),

PROVIDER=re.compile(
    r"""
    \b
    (?:[A-Z][a-z]+(?:\s[A-Z][a-z]+)*)   # capitalized name
    \s
    (Clinic|Hospital|IVF|Fertility|Pathology|Labs|Laboratory|Health Centre|Medical Centre)
    \b
    """,
    re.VERBOSE
    ),
    NAME = re.compile(
        r"""
        \b
        (Dr\.|Patient:|Partner|Met|with)
        \s+
        ([A-Z][a-z]+(?:\s[A-Z][a-z]+)?|[A-Z]\.\s?[A-Z][a-z]+)
        \b
        """,
        re.VERBOSE
    ),
    ADDRESS = re.compile(
    r"""
    \b
    (?:Flat\s+\w+,\s*)?          # optional flat/unit
    \d{1,4}\s                   # street number
    [A-Z][a-z]+(?:\s[A-Z][a-z]+)*\s
    (Street|St|Road|Rd|Lane|Ln|Avenue|Ave)
    (?:,\s*[A-Z][a-z]+(?:\s[A-Z][a-z]+)*)?
    (?:\s*(VIC|NSW|QLD|Pune))?
    (?:\s*\d{4,6})?
    \b
    """,
    re.VERBOSE
)


,
    DOB=re.compile(
        r"\b(DOB|Date of Birth)[:\s]*\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b",
        re.IGNORECASE
    ),

    APPOINTMENT_ID=re.compile(
        r"\b(APPT|INV|BKG)-\d+\b",
        re.IGNORECASE
    ),

    INSURANCE_ID=re.compile(
        r"\b[A-Z]{2,}-[A-Z]{2,}-\d+\b"
    ),

    GOVERNMENT_ID=re.compile(
        r"\b\d{3}-\d{2}-\d{4}\b|\b\d{4}\s\d{4}\s\d{4}\b"
    ),

    URL=re.compile(
        r"https?://\S+"
    )
)
