"""Compute diff coverage."""

import argparse
import json
import re
import sys
from collections import defaultdict
from collections.abc import Iterable
from typing import Any


def get_changed_lines(diff: str) -> dict[str, set[int]]:
    """Get the lines that were changed or added.

    Adpated from https://stackoverflow.com/a/12179492/13242055
    by John Mellor
    """
    changed = defaultdict(set)
    for line in diff.split("\n"):
        if match := re.match(r"\+\+\+\ (?:b/)?(\S+).*", line):
            path = match.group(1)
        elif match := re.match(
            r"@@\ -[0-9]+(?:,[0-9]+)?\ \+([0-9]+)(?:,[0-9]+)?\ @@.*", line
        ):
            line_num = int(match.group(1))
        elif match := re.match(r"^(?:\[[0-9;]*m)*([\\\ +-])(.*)", line):
            prefix = match.group(1)
            if prefix == "+":
                changed[path].add(line_num)
            if prefix in (" ", "+"):
                line_num += 1
    return dict(changed)


def remove_docstring_lines(path: str, lines: Iterable[int]) -> set[int]:
    """Remove docstring lines from list."""
    with open(path) as stream:
        file = stream.read().split("\n")
    return {
        line
        for line in lines
        if not re.match(r"^\s*(\"\"\"|''')", file[line - 1])
    }


def get_covered_lines(
    coverage: dict[str, Any],
) -> tuple[dict[str, set[int]], dict[str, set[int]]]:
    """Get covered lines."""
    executed = {
        path: remove_docstring_lines(path, value["executed_lines"])
        for path, value in coverage["files"].items()
    }
    missing = {
        path: remove_docstring_lines(path, value["missing_lines"])
        for path, value in coverage["files"].items()
    }
    return executed, missing


def intersect(
    lines1: dict[str, set[int]], lines2: dict[str, set[int]]
) -> dict[str, set[int]]:
    """Compute intersection of line sets."""
    intersection = dict()
    for path, lines in lines1.items():
        if path in lines2:
            intersection[path] = lines2[path] & lines
    return intersection


def num_stmts(cov: dict[str, set[int]]) -> int:
    """Compute total number of statements."""
    return len(cov["executed"]) + len(cov["missing"])


def num_miss(cov: dict[str, set[int]]) -> int:
    """Compute number of uncovered statements."""
    return len(cov["missing"])


def pct_cover(cov: dict[str, set[int]]) -> float:
    """Compute percent of statements covered."""
    return len(cov["executed"]) / num_stmts(cov) * 100


def format_missing(missing: set[int]) -> str:
    """Return formatted string list of missing lines."""
    output = ""
    start = 0
    end = 0
    for line in sorted(missing):
        if line == end + 1:
            end = line
            continue
        if start:
            if start == end:
                output += f"{end:d}, "
            else:
                output += f"{start:d}-{end:d}, "
        start = line
        end = line
    if start:
        if start == end:
            output += f"{end:d}"
        else:
            output += f"{start:d}-{end:d}"
    return output


def generate_report_line(
    cov: dict[str, set[int]], include_missing: bool = True
) -> str:
    """Generate the report line for a single file."""
    try:
        cover = f"{pct_cover(cov):6.0f}%"
    except ZeroDivisionError:
        cover = " " * 7
    output = f"{num_stmts(cov):8d}" + f"{num_miss(cov):7d}" + cover
    if include_missing:
        output += "   " + format_missing(cov["missing"])
    return output


def generate_report(coverage: dict[str, dict[str, set[int]]]) -> str:
    """Generate report.

    Example:
        Name             Stmts   Miss  Cover   Missing
        ----------------------------------------------
        src/example.py       8      4    50%   11-13, 17
        ----------------------------------------------
        TOTAL                8      4    50%
    """
    name_width = max(len(path) for path in coverage) if coverage else 5
    header = "Name".ljust(name_width, " ") + "   Stmts   Miss  Cover   Missing"
    separator = "-" * len(header)
    lines = [
        path.ljust(name_width, " ") + generate_report_line(cov)
        for path, cov in coverage.items()
    ]
    total_cov = {
        "executed": set().union(
            *[cov["executed"] for cov in coverage.values()]
        ),
        "missing": set().union(*[cov["missing"] for cov in coverage.values()]),
    }
    total = "TOTAL".ljust(name_width, " ") + generate_report_line(
        total_cov, include_missing=False
    )
    return "\n".join([header, separator, *lines, separator, total])


def main(diff_txt: str, coverage_json: str, threshold: int) -> None:
    """Compute diff coverage."""
    with open(diff_txt) as stream:
        diff = stream.read()
    changed = get_changed_lines(diff)
    with open(coverage_json) as stream:
        coverage = json.load(stream)
    executed, missing = get_covered_lines(coverage)

    diff_executed = intersect(changed, executed)
    diff_missing = intersect(changed, missing)

    diff_coverage = {
        path: {
            "executed": diff_executed.get(path, set()),
            "missing": diff_missing.get(path, set()),
        }
        for path in set(diff_executed) | set(diff_missing)
    }
    print(generate_report(diff_coverage), end="")

    total_diff_cov = {
        "executed": set().union(
            *[cov["executed"] for cov in diff_coverage.values()]
        ),
        "missing": set().union(
            *[cov["missing"] for cov in diff_coverage.values()]
        ),
    }
    try:
        if pct_cover(total_diff_cov) < threshold:
            sys.exit(1)
    except ZeroDivisionError:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--threshold",
        type=int,
        default=70,
        help="Set the threshold value (default: 70)",
    )
    parser.add_argument("diff_txt")
    parser.add_argument("coverage_json")
    args = parser.parse_args()
    main(args.diff_txt, args.coverage_json, args.threshold)
