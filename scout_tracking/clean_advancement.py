import pandas as pd
import argparse

def clean_csv(input_file, output_file):
    # Load the CSV file
    df = pd.read_csv(input_file)

    # Filter out unwanted advancement values
    advancement_remove_values = [
        'Bobcat', 'Tiger', 'Wolf', 'Bear', 'Webelos',
        'Arrow of Light', 'Venturing', 'Discovery',
        'Pathfinder', 'Summit', 'Lion'
    ]
    advancement_type_remove_prefixes = [
        'Venturing', 'Discovery', 'Pathfinder',
        'Summit', 'Merit', 'Award', 'Webelos',
        'Arrow of Light', 'Adventure', 'Tiger',
        'Lion', 'Bobcat', 'Wolf', 'Bear', 'Webelos',
        'Academics'
    ]
    df = df[~df['Advancement'].isin(advancement_remove_values)]
    df = df[~df['Advancement Type'].str.startswith(tuple(advancement_type_remove_prefixes))]

    # Create simplified columns
    df['Name'] = df['First Name'].str.strip() + ' ' + df['Last Name'].str.strip()
    df['Advancement Info'] = df['Advancement Type'].str.strip() + ' ' + df['Advancement'].str.strip()
    df['Date Completed'] = pd.to_datetime(df['Date Completed'], errors='coerce').dt.strftime('%-m/%-d/%Y')

    # Select only the desired columns
    result = df[['Name', 'Advancement Info', 'Date Completed']]

    # Drop rows with missing dates
    result = result.dropna(subset=['Date Completed'])

    # Sort by name and date
    result = result.sort_values(by=['Name', 'Date Completed'])

    # Save to CSV
    result.to_csv(output_file, index=False)

    print(f"Cleaning complete! The cleaned file is saved as '{output_file}'.")

def main():
    parser = argparse.ArgumentParser(description="Clean and simplify a BSA advancement CSV file.")
    parser.add_argument('input_file', help="Path to the input CSV file")
    parser.add_argument('output_file', help="Path to save the cleaned CSV file")
    args = parser.parse_args()
    clean_csv(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
