import csv
from datetime import datetime
from pathlib import Path

METRICS_FILE = Path("metrics/metrics.csv")

EXPECTED_HEADER = [
    "timestamp",
    "user_input",
    "total_tokens",
    "total_cost_usd",
    "total_latency_ms",
    "refinement_applied"
]


def has_correct_header(file_path: Path) -> bool:
    if not file_path.exists():
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()

        if not first_line:
            return False

        # separar por ;
        columns = first_line.split(";")
        return columns == EXPECTED_HEADER


def save_metrics_csv(
    user_input,
    total_tokens,
    total_cost_usd,
    total_latency_ms,
    refinement_applied
):
    write_header = not has_correct_header(METRICS_FILE)

    with open(METRICS_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")

        if write_header:
            writer.writerow(EXPECTED_HEADER)

        writer.writerow([
            datetime.utcnow().isoformat(),
            user_input,
            total_tokens,
            total_cost_usd,
            total_latency_ms,
            refinement_applied
        ])