import os
import csv

def generate_patrol_report_csv(patrol_structure, requirements, output_dir, patrol_names=None):
    """
    Generate a CSV report for specified patrols or all patrols.

    :param patrol_structure: Dictionary of patrols and their scouts with completed requirements
    :param requirements: List of requirements to check for each scout
    :param output_dir: Directory where the CSV report(s) will be saved
    :param patrol_names: List of patrol names to generate reports for (defaults to None, which means all patrols)
    """
    
    # If no patrol names are specified, generate reports for all patrols
    if patrol_names is None:
        patrol_names = list(patrol_structure.keys())  # Get all patrol names in patrol_structure
    
    # Debugging: Print the patrol names being processed
    #print(f"Patrol names being processed: {patrol_names}")
    #print(f"Available patrols in structure: {list(patrol_structure.keys())}")
    
    # Ensure patrol_names are lowercase for consistent processing
    patrol_names = [name.lower() for name in patrol_names]

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        print(f"Output directory '{output_dir}' does not exist. Creating it now.")
        os.makedirs(output_dir)

    # Clean up any pre-existing reports in the output directory
    for file_name in os.listdir(output_dir):
        if file_name.endswith('_report.csv'):
            os.remove(os.path.join(output_dir, file_name))

    # Open a debug log file to save info as .tsv
    debug_log_filename = os.path.join(output_dir, "debug_log.tsv")
    with open(debug_log_filename, 'w', newline='') as debug_file:
        debug_writer = csv.writer(debug_file, delimiter='\t')
        # Write a header for the debug log
        debug_writer.writerow(["Patrol Name", "Scouts", "Requirements", "Patrol Structure Data"])

        # Debug: print patrol structure to the console
        #print(f"Patrol structure content: {patrol_structure}")

        # Loop through each specified patrol name
        for patrol_name in patrol_names:
            # Debugging: Check if patrol is in structure
            #print(f"Processing patrol: {patrol_name}")

            # Ensure the patrol exists in the patrol_structure (case-insensitive)
            if patrol_name not in [name.lower() for name in patrol_structure.keys()]:
                print(f"Patrol '{patrol_name}' not found in patrol_structure. Skipping.")
                continue
            # Debugging: print out scouts in the patrol
            patrol = patrol_structure[patrol_name.lower()]
            #print(f"Scouts in '{patrol_name}': {list(patrol.keys())}")

            # Write the debug log with patrol and its scouts
            debug_writer.writerow([patrol_name, ', '.join(patrol.keys()), ', '.join(requirements), str(patrol_structure)])

            # Convert the patrol name to lowercase for consistent file naming
            patrol_name_lower = patrol_name.lower().replace(' ', '_')

            # Define the file path for the CSV report
            report_filename = os.path.join(output_dir, f"{patrol_name_lower}_report.csv")

           # Check if the patrol has any scouts and their advancements
            if patrol:
                # Open the file for writing the CSV data
                with open(report_filename, 'w', newline='') as file:
                    writer = csv.writer(file)

                    # Write header: "Requirement" column followed by scout names
                    header_row = ['Requirement'] + sorted(patrol.keys())
                    writer.writerow(header_row)

                    # Write rows for each requirement
                    for requirement in requirements:
                        alt_text = requirements.get(requirement.lower(), requirement)
                        row = [alt_text]
                        for scout_name in sorted(patrol.keys()):
                            # Debug: Print the current requirement and scout's advancements
                            #print(f"Checking requirement '{requirement}' for scout '{scout_name}' with advancements: {patrol[scout_name]['advancements']}")
 
                            # If the scout has this requirement, add 'X'; otherwise, add an empty string
                            if requirement.lower() in [advancement.lower() for advancement in patrol[scout_name]['advancements']]:
                                row.append('X')
                            else:
                                row.append('')
                        writer.writerow(row)

                        # Debugging: Print which requirement is being written
#                        print(f"Writing requirement: {alt_text} for patrol: {patrol_name}")


                print(f"CSV Report generated for patrol '{patrol_name}': {report_filename}")
            else:
                print(f"Warning: No scouts found in patrol '{patrol_name}'. Skipping report generation.")
        print(f"Debug log saved to: {debug_log_filename}")

def generate_additional_report(additional_scouts, additional_requirements, output_dir):
    """
    Generate a .txt report for additional scouts and requirements not in the patrols.

    :param additional_scouts: List of scouts not in any patrol.
    :param additional_requirements: List of requirements not in the requirements list.
    :param output_dir: Directory where the .txt report will be saved.
    """
    
    # Define the filename for the additional report
    additional_report_filename = os.path.join(output_dir, "additional_report.txt")
    
    # Create sets to avoid duplicates
    unique_scouts = set(additional_scouts)
    unique_requirements = set(additional_requirements)

    # Write the additional report
    with open(additional_report_filename, 'w') as file:
        # Write the Scouts not in Patrols
        file.write("Scouts not in Patrols:\n")
        if unique_scouts:
            for scout in unique_scouts:
                file.write(f"- {scout}\n")
        else:
            file.write("None\n")
        
        # Write the Requirements not in the requirements list
        file.write("\nRequirements not in requirements list:\n")
        if unique_requirements:
            for requirement in unique_requirements:
                file.write(f"- {requirement}\n")
        else:
            file.write("None\n")
    
    print(f"Additional report generated: {additional_report_filename}")

