"""Baseline implementation for the JSONL tenant-totals task."""

import json
import sys


def main(input_path: str, output_path: str) -> None:
    totals: dict[str, list[int]] = {}
    with open(input_path, "r", encoding="utf-8") as source:
        for line in source:
            row = json.loads(line)
            if row["ok"] is True:
                tenant = row["tenant"]
                bucket = totals.setdefault(tenant, [0, 0])
                bucket[0] += 1
                bucket[1] += row["amount_cents"]

    with open(output_path, "w", encoding="utf-8", newline="\n") as target:
        for tenant in sorted(totals):
            count, amount = totals[tenant]
            target.write(
                json.dumps(
                    {"tenant": tenant, "count": count, "amount_cents": amount},
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
                + "\n"
            )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: solution.py INPUT.jsonl OUTPUT.jsonl")
    main(sys.argv[1], sys.argv[2])
