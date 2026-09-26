# JSONL tenant totals

Improve `solution.py` for this fixed task. The evaluator invokes it as:

```text
python -B solution.py INPUT.jsonl OUTPUT.jsonl
```

Each input line is one UTF-8 JSON object. Every object has a string `tenant`, an integer `amount_cents`, and an `ok` value. Count a row only when `ok` is the JSON boolean `true` (not `1`, `"true"`, or another truthy value). For each tenant, sum the counted rows and their `amount_cents`; amounts may be negative. Ignore any other fields. Tenants may be empty strings or contain non-ASCII characters.

Write one UTF-8 JSON object per tenant with at least one counted row, sorted by tenant in Python's string order. Each line must have exactly this field order and compact form, followed by `\n`:

```text
{"tenant":"acme","count":2,"amount_cents":150}
```

Use unescaped UTF-8 for non-ASCII characters. Do not print data to stdout. Exit nonzero on invalid invocation or processing failure. Only `solution.py` is editable during the pilot; this README is the task contract.
