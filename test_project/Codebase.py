import os
import csv
import math
import cc_visit
from radon.visitors import FunctionVisitor

def calculate_metrics_for_file(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()
            cyclomatic_complexity = FunctionVisitor(code).get_cyclomatic_complexity()
            halstead_difficulty = halstead_difficulty(cc_visit(code).get_operators().total, cc_visit(code).get_operands().total)
            return [{'cyclomatic_complexity': cyclomatic_complexity, 'halstead_difficulty': halstead_difficulty}]
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return []

def halstead_difficulty(n1, n2):
    """Calculate Halstead difficulty."""
    return (n1 / 2) * (n2 / (cc_visit(code).get_vocabulary().total - 1))

def calculate_maintainability_index(cyclomatic_complexity, halstead_difficulty):
    """Calculate maintainability index."""
    maintainability = 171 - 5.2 * math.log2(cyclomatic_complexity) - 0.23 * math.log2(halstead_difficulty)
    return maintainability

def calculate_metrics_for_directory(directory):
    total_cyclomatic_complexity = 0
    total_halstead_difficulty = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                metrics = calculate_metrics_for_file(file_path)
                total_cyclomatic_complexity +=sum(metric['cyclomatic_complexity'] for metric in metrics)
                total_halstead_difficulty += sum(metric['halstead_difficulty'] for metric in metrics)
    
    maintainability = calculate_maintainability_index(total_cyclomatic_complexity, total_halstead_difficulty)
    
    return total_cyclomatic_complexity, total_halstead_difficulty, maintainability

def write_metrics_to_csv(metrics, csv_file):
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['File', 'Cyclomatic Complexity', 'Halstead Difficulty', 'Maintainability Index']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for file_name, file_metrics in metrics.items():
            print(f"File: {file_name}")
            print("Metrics:", file_metrics)  # Print out the metrics for debugging
            writer.writerow({'File': file_name,
                             'Cyclomatic Complexity': sum(metric['cyclomatic_complexity'] for metric in file_metrics),
                             'Halstead Difficulty': sum(metric['halstead_difficulty'] for metric in file_metrics),
                             'Maintainability Index': metrics['maintainability']})

def main():
    directory = os.getcwd()
    metrics = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                metrics[file] = calculate_metrics_for_file(file_path)
    
    metrics['maintainability'] = calculate_metrics_for_directory(directory)[2]
    write_metrics_to_csv(metrics, 'metrics.csv')
    print("Metrics written to metrics.csv")

if __name__ == '__main__':
    main()