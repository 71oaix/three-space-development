#!/usr/bin/env python3
"""Deterministic structural checks for a three-space Specification Package.

This script intentionally does not judge semantic correctness. It catches
mechanical defects before the semantic AI review.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FRONTMATTER = (
    "title",
    "source",
    "type",
    "status",
    "created",
    "updated",
    "contract-version",
)

REQUIRED_SECTIONS = (
    "## 1. 交接控制信息",
    "## 2. Problem Space",
    "## 3. Intention Space",
    "## 4. Approved Specification",
    "## 5. Solution Architecture",
    "## 6. Acceptance Contract",
    "## 7. 风险与未决事项",
    "## 8. Traceability",
    "## 9. Approval",
)

PLACEHOLDER_PATTERNS = (
    (r"SP-YYYYMMDD-XXX", "package_id 仍是模板占位符"),
    (r"YYYY-MM-DD", "日期仍是模板占位符"),
    (r"待填写|待补充|待确认|TBD|TODO", "仍存在未完成占位标记"),
    (r"名称|场景名称|行为名称", "仍存在示例标题"),
)


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---"):
        return {}, ["缺少 frontmatter 起始标记"]

    lines = text.splitlines()
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, ["缺少 frontmatter 结束标记"]

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"frontmatter 行无法解析：{line}")
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values, errors


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^{re.escape(heading)}\s*$([\s\S]*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE,
    )
    return match.group(1) if match else ""


def row_value(text: str, label: str) -> str:
    match = re.search(
        rf"^\|\s*{re.escape(label)}\s*\|\s*(.*?)\s*\|\s*$",
        text,
        flags=re.MULTILINE,
    )
    return match.group(1).strip() if match else ""


def validate(path: Path, template_mode: bool = False) -> dict:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    frontmatter, frontmatter_errors = parse_frontmatter(text)
    errors.extend(frontmatter_errors)

    for key in REQUIRED_FRONTMATTER:
        if key not in frontmatter or not frontmatter[key]:
            errors.append(f"缺少必填 frontmatter：{key}")

    if frontmatter.get("type") not in ("specification-package", "template"):
        warnings.append("type 不是 specification-package 或 template")

    for heading in REQUIRED_SECTIONS:
        if not re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.MULTILINE):
            errors.append(f"缺少必需章节：{heading}")

    status = row_value(section(text, "## 1. 交接控制信息"), "handoff_status")
    if template_mode and status == "draft / ready / returned":
        status = "template"
    elif status not in ("draft", "ready", "returned"):
        errors.append("handoff_status 必须是 draft、ready 或 returned")

    control = section(text, "## 1. 交接控制信息")
    declared_version = row_value(control, "handoff_version")
    if declared_version and frontmatter.get("contract-version") and declared_version != frontmatter["contract-version"]:
        errors.append("handoff_version 与 contract-version 不一致")

    approval = section(text, "## 9. Approval")
    handoff_match = re.search(r"handoff_to\s*[：:]\s*(\S+)", approval)
    if handoff_match and handoff_match.group(1) != "sdd-development":
        errors.append("handoff_to 必须是 sdd-development")

    implementation_terms = r"\b(class|function|def|database table|framework API)\b|函数|类|数据库表|代码步骤|框架 API"
    if not template_mode and re.search(implementation_terms, section(text, "## 4. Approved Specification"), flags=re.IGNORECASE):
        warnings.append("Specification 中疑似出现实现细节，交给 AI 子审查判断")

    acceptance = section(text, "## 6. Acceptance Contract")
    if not re.search(r"AC-\d{3}", acceptance):
        errors.append("Acceptance Contract 缺少 Acceptance ID")
    for token in ("Given", "When", "Then"):
        if token not in acceptance:
            errors.append(f"Acceptance Contract 缺少 {token} 结构")

    traceability = section(text, "## 8. Traceability")
    if "Intention" not in traceability or "Specification" not in traceability:
        errors.append("Traceability 缺少 Intention → Specification 关系")
    if not re.search(r"AC-\d{3}", traceability):
        warnings.append("Traceability 尚未关联 Acceptance ID")

    approval = section(text, "## 9. Approval")
    for label in ("approved_by", "approved_at", "specification_review"):
        if not re.search(rf"{re.escape(label)}\s*[：:]", approval):
            errors.append(f"Approval 缺少字段：{label}")

    risks = section(text, "## 7. 风险与未决事项")
    if not re.search(r"RISK-\d{3}", risks):
        warnings.append("尚未填写已知风险")
    if status == "ready":
        if "通过" not in approval:
            errors.append("ready Package 的 specification_review 必须为通过")
        if not re.search(r"approved_by\s*[：:]\s*(?!$)", approval, re.MULTILINE):
            errors.append("ready Package 缺少 approved_by 内容")
        if not re.search(r"approved_at\s*[：:]\s*(?!$)", approval, re.MULTILINE):
            errors.append("ready Package 缺少 approved_at 内容")
        if re.search(r"\|\s*(是|yes|true)\s*\|\s*$", risks, flags=re.IGNORECASE | re.MULTILINE):
            errors.append("ready Package 仍有阻塞性未决事项")
        if not template_mode:
            for pattern, message in PLACEHOLDER_PATTERNS:
                if re.search(pattern, text, flags=re.IGNORECASE):
                    errors.append(message)

    if not template_mode:
        for pattern, message in PLACEHOLDER_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                warnings.append(message)

    result = {
        "path": str(path),
        "status": status or None,
        "contract_version": frontmatter.get("contract-version"),
        "errors": errors,
        "warnings": sorted(set(warnings)),
        "pass": not errors,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument(
        "--template",
        action="store_true",
        help="验证模板结构，不把示例占位符视为错误",
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    try:
        result = validate(args.package, template_mode=args.template)
    except (OSError, UnicodeError) as exc:
        result = {
            "path": str(args.package),
            "status": None,
            "contract_version": None,
            "errors": [f"无法读取文件：{exc}"],
            "warnings": [],
            "pass": False,
        }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Specification Package: {result['path']}")
        print(f"handoff_status: {result['status'] or 'unknown'}")
        print(f"contract_version: {result['contract_version'] or 'unknown'}")
        print(f"errors: {len(result['errors'])}")
        for item in result["errors"]:
            print(f"  ERROR: {item}")
        print(f"warnings: {len(result['warnings'])}")
        for item in result["warnings"]:
            print(f"  WARN: {item}")
        print("result: PASS" if result["pass"] else "result: FAIL")

    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
