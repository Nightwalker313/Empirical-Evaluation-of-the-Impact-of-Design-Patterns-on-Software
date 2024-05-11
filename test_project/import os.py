import os
import csv
from radon.complexity import cc_visit
from radon.metrics import h_visit
from radon.raw import analyze
from math import log

def calculate_maintainability_index(cc_analysis, h_analysis, raw_analysis):
    """Calculate maintainability index based on cyclomatic complexity, Halstead metrics, and raw metrics."""
    cyclomatic_complexity = sum(func.complexity for func in cc_analysis)
    halstead_volume = h_analysis.total.volume
    lines_of_code = raw_analysis.loc
    maintainability_index = 171 - 5.2 * log(halstead_volume) - 0.23 * cyclomatic_complexity - 16.2 * log(lines_of_code)
    return max(0, min(maintainability_index, 100))  # Maintainability index is between 0 and 100

def calculate_metrics_for_file(file_path):
    """Calculate metrics for a single file."""
    try:
        with open(file_path, 'r') as file_obj:
            code = file_obj.read()
            cc_analysis = cc_visit(code)
            h_analysis = h_visit(code)
            raw_analysis = analyze(code)
            maintainability_index = calculate_maintainability_index(cc_analysis, h_analysis, raw_analysis)
            return maintainability_index
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def write_metrics_to_csv(directory, csv_file):
    """Write maintainability metrics for all Python files in a directory to a CSV file."""
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['File', 'Maintainability Index']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    maintainability_index = calculate_metrics_for_file(file_path)
                    if maintainability_index is not None:
                        writer.writerow({'File': file_path, 'Maintainability Index': maintainability_index})

def main():
    directory = os.getcwd()  # Current working directory
    csv_file = 'maintainability_metrics.csv'
    write_metrics_to_csv(directory, csv_file)
    print(f"Maintainability metrics written to {csv_file}")

if __name__ == '__main__':
    main()