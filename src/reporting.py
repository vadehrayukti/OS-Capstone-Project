
import csv
import json
import logging
import os
import matplotlib.pyplot as plt


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(PROJECT_ROOT, "outputs", "results")
LOGS_DIR = os.path.join(PROJECT_ROOT, "outputs", "logs")


def setup_logging():
    """Configure application logging."""

    os.makedirs(LOGS_DIR, exist_ok=True)

    log_file = os.path.join(LOGS_DIR, "application.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        force=True
    )


def save_result(filename, result):
    """Save algorithm results in JSON format."""

    os.makedirs(RESULTS_DIR, exist_ok=True)

    file_path = os.path.join(RESULTS_DIR, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    logging.info("Result saved: %s", filename)

    return file_path


def save_comparison_chart(title, labels, values, ylabel, filename):
    """Generate and save a bar chart."""

    os.makedirs(RESULTS_DIR, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)

    plt.title(title)
    plt.xlabel("Algorithms")
    plt.ylabel(ylabel)

    plt.tight_layout()

    file_path = os.path.join(RESULTS_DIR, filename)

    plt.savefig(file_path)
    plt.close()

    logging.info("Chart generated: %s", filename)

    return file_path


def save_comparison_csv(filename, headers, rows):
    """Save comparison data in CSV format."""

    os.makedirs(RESULTS_DIR, exist_ok=True)

    file_path = os.path.join(RESULTS_DIR, filename)

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(headers)
        writer.writerows(rows)

    logging.info("CSV report saved: %s", filename)

    return file_path


def display_comparison_table(headers, rows):
    """Display a formatted comparison table."""

    column_widths = []

    for index, header in enumerate(headers):
        width = len(str(header))

        for row in rows:
            width = max(width, len(str(row[index])))

        column_widths.append(width)

    separator = "-+-".join(
        "-" * width for width in column_widths
    )

    header_line = " | ".join(
        str(header).ljust(column_widths[index])
        for index, header in enumerate(headers)
    )

    print("\n" + header_line)
    print(separator)

    for row in rows:
        row_line = " | ".join(
            str(value).ljust(column_widths[index])
            for index, value in enumerate(row)
        )

        print(row_line)
