import os
import sys
import argparse
import csv
from scout_tracking.initialize import initialize_patrol_structure
from scout_tracking.load_patrol_data import load_patrol_data
from scout_tracking.load_requirements import load_requirements
from scout_tracking.load_advancements import load_advancements
from scout_tracking.report import generate_patrol_report_csv, generate_additional_report

def main():
    # Step 1: Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate patrol reports.')
    
    parser.add_argument('patrol_tsv', type=str, help='Path to the patrol structure TSV file')
    parser.add_argument('requirements_tsv', type=str, help='Path to the requirements TSV file')
    parser.add_argument('advancement_csv', type=str, help='Path to the advancement CSV file')
    parser.add_argument('output_dir', type=str, help='Directory to save the generated reports')
    parser.add_argument('patrol_names', nargs='*', help='Specific patrol names to generate reports for (default: all patrols)')
    
    args = parser.parse_args()

    # Step 2: Load the patrol data from TSV
    patrol_data = load_patrol_data(args.patrol_tsv)
    print(f"patrol data loaded\n")

    # Step 3: Load requirements from TSV
    requirements = load_requirements(args.requirements_tsv)  # Load requirements from TSV
    print(f"requirements loaded\n")

    # Step 4: Initialize the multi-dimentional data structure
    patrol_structure = initialize_patrol_structure(patrol_data)
    print(f"structure initialized\n")

    # Step 5: load advancement data to data structure
    patrol_structure, additional_scouts, additional_requirements = load_advancements(args.advancement_csv, patrol_structure, requirements)
    print(f"advancement data loaded\n")

    # Step 6: Generate reports for the specified patrols or all patrols
    if not args.patrol_names:
        args.patrol_names = list(patrol_structure.keys())
    generate_patrol_report_csv(patrol_structure, requirements, args.output_dir, patrol_names=args.patrol_names)

    # Step 7: Generate the additional report for scouts and requirements that are not in the patrols
    generate_additional_report(additional_scouts, additional_requirements, args.output_dir)

if __name__ == '__main__':
    main()

