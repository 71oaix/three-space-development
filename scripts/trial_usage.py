#!/usr/bin/env python3
"""Append, validate, and summarize Three-Space trial observations.

The source repository's .run-log.jsonl is a maintenance log. Real project
observations live in <project>/.three-space/trial-usage.jsonl.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime
import json
from pathlib import Path
import sys


RELATIVE_LOG = Path(".three-space/trial-usage.jsonl")
MECHANISMS = frozenset(
    {
        "intention.frontier",
        "intention.fact-decision",
        "intention.shared-understanding",
        "spec.no-repeat",
        "evidence.research",
        "evidence.code-conflict",
        "evidence.testing-seam",
        "evidence.prototype",
        "architecture.adr-heuristic",
    }
)
PHASES = frozenset({"intention", "specification", "architecture"})
STATUSES = frozenset({"used", "eligible_skipped"})
VERDICTS = frozenset({"helped", "neutral", "hurt", "unknown"})
OBSERVATION_FIELDS = (
    "trigger",
    "action",
    "expected_effect",
    "observed_effect",
    "evidence_ref",
    "cost",
)


def validate_record(record: object, label: str) -> list[str]:
    if not isinstance(record, dict):
        return [f"{label}: expected a JSON object"]

    errors: list[str] = []
    if record.get("schema_version") != "1.0":
        errors.append(f"{label}: schema_version must be 1.0")

    stamp = record.get("ts")
    if not isinstance(stamp, str):
        errors.append(f"{label}: ts must be an ISO timestamp with timezone")
    else:
        try:
            parsed = datetime.fromisoformat(stamp)
            if parsed.tzinfo is None or parsed.utcoffset() is None:
                raise ValueError("timezone missing")
        except ValueError:
            errors.append(f"{label}: ts must be an ISO timestamp with timezone")

    for field in ("case_ref", "artifact_ref"):
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}: {field} must be non-empty text")

    kind = record.get("record_type")
    if kind == "run":
        phases = record.get("phases")
        if not isinstance(phases, list) or not phases or any(
            not isinstance(phase, str) or phase not in PHASES for phase in phases
        ):
            errors.append(f"{label}: phases must be a non-empty list of stages")
        eligible = record.get("eligible_mechanisms")
        used = record.get("used_mechanisms")
        for field, values in (("eligible_mechanisms", eligible), ("used_mechanisms", used)):
            if not isinstance(values, list) or any(
                not isinstance(value, str) or value not in MECHANISMS for value in values
            ):
                errors.append(f"{label}: {field} must be a list of known mechanism IDs")
            elif len(values) != len(set(values)):
                errors.append(f"{label}: {field} contains duplicates")
        if isinstance(eligible, list) and isinstance(used, list) and all(
            isinstance(value, str) for value in eligible + used
        ) and not set(used).issubset(set(eligible)):
            errors.append(f"{label}: used_mechanisms must be a subset of eligible_mechanisms")
        return errors
    if kind != "observation":
        errors.append(f"{label}: record_type must be run or observation")
        return errors

    for field in OBSERVATION_FIELDS:
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}: {field} must be non-empty text")

    if not isinstance(record.get("mechanism"), str) or record["mechanism"] not in MECHANISMS:
        errors.append(f"{label}: unknown mechanism")
    if not isinstance(record.get("phase"), str) or record["phase"] not in PHASES:
        errors.append(f"{label}: invalid phase")
    if not isinstance(record.get("status"), str) or record["status"] not in STATUSES:
        errors.append(f"{label}: invalid status")
    if not isinstance(record.get("verdict"), str) or record["verdict"] not in VERDICTS:
        errors.append(f"{label}: invalid verdict")
    if record.get("status") == "eligible_skipped" and record.get("verdict") != "unknown":
        errors.append(f"{label}: eligible_skipped must have unknown verdict")
    if isinstance(record.get("verdict"), str) and record["verdict"] in {"helped", "neutral", "hurt"}:
        evidence = record.get("evidence_ref")
        if isinstance(evidence, str) and evidence.strip().lower() in {"none", "无", "无直接证据"}:
            errors.append(f"{label}: non-unknown verdict requires evidence_ref")
    return errors


def check_coverage(entries: list[tuple[Path, dict]]) -> list[str]:
    latest_runs: dict[tuple[Path, str], dict] = {}
    latest_observations: dict[tuple[Path, str, str], dict] = {}
    for path, record in entries:
        if record["record_type"] == "run":
            latest_runs[(path, record["case_ref"])] = record
        else:
            latest_observations[(path, record["case_ref"], record["mechanism"])] = record

    errors: list[str] = []
    for (path, case_ref), run in latest_runs.items():
        for mechanism in run["eligible_mechanisms"]:
            observation = latest_observations.get((path, case_ref, mechanism))
            if observation is None:
                errors.append(f"{path}: {case_ref}: missing observation for {mechanism}")
                continue
            expected_status = "used" if mechanism in run["used_mechanisms"] else "eligible_skipped"
            if observation["status"] != expected_status:
                errors.append(f"{path}: {case_ref}: {mechanism} status disagrees with run")
            if observation["phase"] not in run["phases"]:
                errors.append(f"{path}: {case_ref}: {mechanism} phase absent from run")
    for path, case_ref, mechanism in latest_observations:
        run = latest_runs.get((path, case_ref))
        if run is None:
            errors.append(f"{path}: {case_ref}: observation has no run record")
        elif mechanism not in run["eligible_mechanisms"]:
            errors.append(f"{path}: {case_ref}: {mechanism} absent from eligible_mechanisms")
    return errors


def read_log(path: Path) -> tuple[list[dict], list[str]]:
    if not path.is_file():
        return [], [f"{path}: file not found"]
    records: list[dict] = []
    errors: list[str] = []
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            errors.append(f"{path}:{number}: empty line")
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{number}: invalid JSON ({exc.msg})")
            continue
        errors.extend(validate_record(record, f"{path}:{number}"))
        if isinstance(record, dict):
            records.append(record)
    return records, errors


def append(args: argparse.Namespace) -> int:
    try:
        record = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"stdin: invalid JSON ({exc.msg})", file=sys.stderr)
        return 1
    errors = validate_record(record, "stdin")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    project_root = args.project_root.resolve()
    if not project_root.is_dir():
        print(f"Project root not found: {project_root}", file=sys.stderr)
        return 1
    path = project_root / RELATIVE_LOG
    if not path.resolve().is_relative_to(project_root):
        print(f"Trial log resolves outside project root: {path}", file=sys.stderr)
        return 1
    if path.exists():
        _, errors = read_log(path)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(path)
    return 0


def validate(args: argparse.Namespace) -> int:
    entries: list[tuple[Path, dict]] = []
    all_errors: list[str] = []
    for path in args.logs:
        records, errors = read_log(path)
        entries.extend((path.resolve(), record) for record in records)
        all_errors.extend(errors)
    if not all_errors:
        all_errors.extend(check_coverage(entries))
    if all_errors:
        print("\n".join(all_errors), file=sys.stderr)
        return 1
    print(f"valid trial log entries: {len(entries)}")
    return 0


def summary(args: argparse.Namespace) -> int:
    all_records: list[tuple[Path, dict]] = []
    all_errors: list[str] = []
    for path in args.logs:
        records, errors = read_log(path)
        all_records.extend((path.resolve(), record) for record in records)
        all_errors.extend(errors)
    if not all_errors:
        all_errors.extend(check_coverage(all_records))
    if all_errors:
        print("\n".join(all_errors), file=sys.stderr)
        return 1

    latest_runs: dict[tuple[Path, str], dict] = {}
    latest: dict[tuple[Path, str, str], dict] = {}
    for path, record in all_records:
        if record["record_type"] == "run":
            latest_runs[(path, record["case_ref"])] = record
        else:
            latest[(path, record["case_ref"], record["mechanism"])] = record

    grouped: dict[str, dict[str, object]] = defaultdict(
        lambda: {"cases": set(), "status": Counter(), "verdict": Counter()}
    )
    for (path, _, _), record in latest.items():
        item = grouped[record["mechanism"]]
        item["cases"].add((path, record["case_ref"]))
        item["status"][record["status"]] += 1
        item["verdict"][record["verdict"]] += 1
    print("mechanism | cases | used | skipped | helped | neutral | hurt | unknown")
    for mechanism in sorted(grouped):
        item = grouped[mechanism]
        print(
            f"{mechanism} | {len(item['cases'])} | "
            f"{item['status']['used']} | {item['status']['eligible_skipped']} | "
            f"{item['verdict']['helped']} | {item['verdict']['neutral']} | "
            f"{item['verdict']['hurt']} | {item['verdict']['unknown']}"
        )
    print(
        f"runs: {len(latest_runs)}; zero-cue runs: "
        f"{sum(not record['eligible_mechanisms'] for record in latest_runs.values())}; "
        f"observations: {len(latest)}; log entries: {len(all_records)}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    append_parser = subparsers.add_parser("append", help="Read one JSON object from stdin and append it")
    append_parser.add_argument("--project-root", type=Path, required=True)
    append_parser.set_defaults(handler=append)
    validate_parser = subparsers.add_parser("validate", help="Validate project trial logs")
    validate_parser.add_argument("logs", nargs="+", type=Path)
    validate_parser.set_defaults(handler=validate)
    summary_parser = subparsers.add_parser("summary", help="Summarize one or more project trial logs")
    summary_parser.add_argument("logs", nargs="+", type=Path)
    summary_parser.set_defaults(handler=summary)
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
