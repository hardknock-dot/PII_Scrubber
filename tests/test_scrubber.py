from src.scrubber import scrub_entry


def test_email_scrub():
    text = "Email me at test@example.com"
    result = scrub_entry("x1", text, "v1")
    assert "[EMAIL]" in result["scrubbed_text"]


def test_phone_false_positive():
    text = "Steps today: 6234 not a phone"
    result = scrub_entry("x2", text, "v1")
    assert result["scrubbed_text"] == text


def test_idempotency():
    text = "Call me on +61 412 345 678"
    first = scrub_entry("x3", text, "v1")["scrubbed_text"]
    second = scrub_entry("x3", first, "v1")["scrubbed_text"]
    assert first == second
def test_provider_scrub():
    text = "Appointment at Sunrise IVF tomorrow."
    result = scrub_entry("x4", text, "v1")
    assert "[PROVIDER]" in result["scrubbed_text"]
def test_name_scrub():
    text = "Therapy session with Dr. Anna Lee today."
    result = scrub_entry("n1", text, "v1")
    assert "[NAME]" in result["scrubbed_text"]


def test_name_not_over_scrub():
    text = "Took ibuprofen for migraine."
    result = scrub_entry("n2", text, "v1")
    assert result["scrubbed_text"] == text
def test_address_scrub():
    text = "Met at 22 Bloomfield Rd, Carlton VIC 3053."
    result = scrub_entry("a1", text, "v1")
    assert "[ADDRESS]" in result["scrubbed_text"]


def test_address_not_false_positive():
    text = "School pickup at Riverdale Primary."
    result = scrub_entry("a2", text, "v1")
    assert result["scrubbed_text"] == text

