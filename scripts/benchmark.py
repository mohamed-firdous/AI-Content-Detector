from __future__ import annotations

import argparse
import time
from pathlib import Path

from detector.pipeline import run_full_analysis


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark analysis runtime for a sample file.")
    parser.add_argument("file", type=str, help="Path to .txt/.pdf/.docx file")
    parser.add_argument("--runs", type=int, default=3, help="Number of timed runs")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    blob = path.read_bytes()
    durations = []

    for i in range(args.runs):
        start = time.perf_counter()
        out = run_full_analysis(filename=path.name, file_bytes=blob)
        elapsed = time.perf_counter() - start
        durations.append(elapsed)
        print(f"Run {i + 1}: {elapsed:.3f}s (pipeline reported {out.elapsed_seconds:.3f}s)")

    avg = sum(durations) / len(durations)
    print(f"Average runtime: {avg:.3f}s")
    if avg <= 20:
        print("PASS: under 20 second target")
    else:
        print("WARN: over 20 second target")


if __name__ == "__main__":
    main()
