"""Check source files for license headers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java",
    ".c", ".cpp", ".h", ".hpp", ".rb", ".php", ".sh",
}
DEFAULT_IGNORED = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "dist", "build", ".tox", ".mypy_cache",
}


def _normalize_extensions(values: str) -> set[str]:
    extensions: set[str] = set()
    for value in values.split(","):
        value = value.strip().lower()
        if not value:
            continue
        extensions.add(value if value.startswith(".") else f".{value}")
    return extensions


def _normalize_names(values: str) -> set[str]:
    return {value.strip() for value in values.split(",") if value.strip()}


def has_header(path: Path, markers: list[str], max_lines: int = 15) -> bool:
    """Return whether one of the markers appears in the first lines."""
    lowered_markers = [marker.lower() for marker in markers]
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for _ in range(max_lines):
                line = handle.readline()
                if not line:
                    break
                lowered = line.lower()
                if any(marker in lowered for marker in lowered_markers):
                    return True
    except OSError:
        return False
    return False


def scan(
    root: Path,
    extensions: set[str],
    markers: list[str],
    ignored: set[str],
    max_lines: int,
) -> list[Path]:
    """Return source files under root that lack a matching header."""
    missing: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        relative = path.relative_to(root)
        if any(part in ignored for part in relative.parts[:-1]):
            continue
        if not has_header(path, markers, max_lines):
            missing.append(path)
    return sorted(missing, key=lambda item: str(item))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check source files for a license header."
    )
    parser.add_argument("path", nargs="?", default=".", help="directory to scan")
    parser.add_argument(
        "--marker", action="append", default=None,
        help="text to look for; may be repeated",
    )
    parser.add_argument(
        "--spdx", action="store_true",
        help="shorthand for --marker SPDX-License-Identifier",
    )
    parser.add_argument(
        "--extensions", default=",".join(sorted(DEFAULT_EXTENSIONS)),
        help="comma-separated file extensions to scan",
    )
    parser.add_argument(
        "--ignore", default=",".join(sorted(DEFAULT_IGNORED)),
        help="comma-separated directory names to skip",
    )
    parser.add_argument(
        "--max-lines", type=int, default=15,
        help="number of leading lines to inspect",
    )
    parser.add_argument(
        "--format", choices=("text", "json"), default="text",
        help="output format",
    )
    args = parser.parse_args(argv)

    markers = list(args.marker or [])
    if args.spdx:
        markers.append("SPDX-License-Identifier")
    if not markers:
        markers = ["SPDX-License-Identifier", "Copyright"]

    extensions = _normalize_extensions(args.extensions)
    ignored = _normalize_names(args.ignore)
    missing = scan(Path(args.path), extensions, markers, ignored, args.max_lines)

    if args.format == "json":
        print(json.dumps({"missing": [str(path) for path in missing]}, indent=2))
    elif missing:
        print(f"{len(missing)} file(s) missing a license header:")
        for path in missing:
            print(f"  {path}")
    else:
        print("All scanned files have a license header.")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
