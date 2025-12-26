import argparse
import json
from pathlib import Path

from src.scrubber import scrub_entry



SCRUBBER_VERSION = "v1"


def parse_args():
    parser = argparse.ArgumentParser(
        description="PII / Sensitive Identifier Scrubber for Ashwam journals"
    )
    parser.add_argument("--in", dest="input_path", required=True, help="Input journals.jsonl")
    parser.add_argument("--out", dest="output_path", required=True, help="Output scrubbed.jsonl")
    return parser.parse_args()


def main():
    args = parse_args()

    input_path = Path(args.input_path)
    output_path = Path(args.output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as infile, \
         output_path.open("w", encoding="utf-8") as outfile:

        for line in infile:
            record = json.loads(line)

            entry_id = record["entry_id"]
            text = record["text"]

            result = scrub_entry(
                entry_id=entry_id,
                text=text,
                scrubber_version=SCRUBBER_VERSION
            )

            # IMPORTANT: do not log raw text anywhere
            outfile.write(json.dumps(result, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
