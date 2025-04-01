# scout_tracking
This project helps to generate reports and perform quality checks for scout advancement data, patrol membership, and requirements. It includes several scripts that can be run from the command line.

Collectively, these scripts process a Scoutbook data export to produce an advancement chart for each Patrol in a Troop.

## CLI Commands and Usage

### 1. **clean_advancement.py**
This script processes the Scoutbook export/backup file to remove extra fields and records not related to Scout Advancement Work (for example, Cub Scout Awards).

#### Command:
```
python clean_advancement.py <input_file> <output_file>
```

#### Example Input:
**troop100__advancement.csv**
```
"BSA Member ID","First Name","Middle Name","Last Name","Advancement Type","Advancement","Version","Date Completed","Approved","Awarded","MarkedCompletedBy","MarkedCompletedDate","CounselorApprovedBy","CounselorApprovedDate","LeaderApprovedBy","LeaderApprovedDate","AwardedBy","AwardedDate"
12600561,"Frank","A","Jones",,"Scout Rank Requirement","2b",2022,"7/19/2024",1,,ASM_Bill,8/6/2024,,,SM_Mary,8/27/2024,,
```

#### Expected Output:
**advancement.csv**
'''
Scout Name,Requirement,Completion Date
Frank Jones,Scout Rank Requirement 2b,7/19/2024
'''

---

### 2. `check_scouts_in_patrols.py`

**Purpose**: Check whether there are any Scouts in the advancement.csv file who are not in the patrols.tsv file.

**Usage**:
```
python check_scouts_in_patrols.py <advancement_file> <patrols_file> [--output_file <output_file>]
```

**Arguments**:
- `advancement_file`: Path to the advancement data file (CSV format).
- `patrols_file`: Path to the patrol membership file (TSV format).
- `--output_file`: Optional path to save the results (default is `scouts_in_patrols.tsv`).

**Example**:
```
python check_scouts_in_patrols.py scout_tracking/advancement.csv scout_tracking/patrols.tsv --output_file ./reports/scouts_in_patrols.tsv
```

**Output**:
A TSV file listing scouts in the advancement file but not assigned to any patrol.

---

### 3. `check_requirements_in_advancement.py`

**Purpose**: Check if there are any requirements in the advancement.csv file that are not in the requirements.tsv file.

**Usage**:
```
python check_requirements_in_advancement.py <advancement_file> <requirements_file> [--output_file <output_file>]
```

**Arguments**:
- `advancement_file`: Path to the advancement data file (CSV format).
- `requirements_file`: Path to the requirements list file (TSV format).
- `--output_file`: Optional path to save the results (default is `requirements_in_advancement.tsv`).

**Example**:
```
python check_requirements_in_advancement.py scout_tracking/advancement.csv scout_tracking/requirements.tsv --output_file ./reports/requirements_in_advancement.tsv
```

**Output**:
A TSV file listing requirements in the advancement file that are not listed in the requirements file.

---

### 4. `generate_report.py`

**Purpose**: Generate a patrol report summarizing the advancement progress of each scout in a specific patrol.

**Usage**:
```
python generate_report.py <advancement_file> <patrols_file> <requirements_file> <output_dir> [--patrol_name <patrol_name>]
```

**Arguments**:
- `advancement_file`: Path to the advancement data file (CSV format).
- `patrols_file`: Path to the patrol membership file (TSV format).
- `requirements_file`: Path to the requirements list file (TSV format).
- `output_dir`: Directory where the reports will be saved.
- `--patrol_name`: Optional patrol name to generate report for a specific patrol (default is all patrols).

**Example**:
```
python generate_report.py scout_tracking/advancement.csv scout_tracking/patrols.tsv scout_tracking/requirements.tsv ./reports --patrol_name Lions
```

**Output**:
A TSV report for the specified patrol, showing each scout and their completion status for each requirement.

---

### 5. `qc_checks.py`

**Purpose**: Run all quality checks (scouts not assigned to patrols and requirements not found in the requirements file) and save the results to separate reports.

**Usage**:
```
python qc_checks.py <advancement_file> <patrols_file> <requirements_file> <output_dir>
```

**Arguments**:
- `advancement_file`: Path to the advancement data file (CSV format).
- `patrols_file`: Path to the patrol membership file (TSV format).
- `requirements_file`: Path to the requirements list file (TSV format).
- `output_dir`: Directory where the QC reports will be saved.

**Example**:
```
python qc_checks.py scout_tracking/advancement.csv scout_tracking/patrols.tsv scout_tracking/requirements.tsv ./reports
```

**Output**:
- A report of scouts not assigned to any patrol: `scouts_in_patrols.tsv`.
- A report of requirements in the advancement file that are not listed in the requirements file: `requirements_in_advancement.tsv`.

---

## Example Input Files

### 1. `advancement.csv`
```
Scout Name,Requirement,Completion Date
John Doe,First Aid,2025-01-01
Jane Smith,Camping,2025-02-15
John Doe,Camping,2025-02-20
Alice Brown,First Aid,2025-01-10
Bob Green,First Aid,2025-03-01
Bob Green,Emergency Preparedness,2025-03-01
```

### 2. `patrols.tsv`
```
Scout Name    Patrol
Jane Smith    Lions
Bob Green     Lions
John Doe      Tigers
Alice Brown   Tigers
```

### 3. `requirements.tsv`
```
Requirement Name        Alternative Text
First Aid              Basic First Aid
Camping                Camping Skills
```

---

## Expected Output Files

### 1. From `check_scouts_in_patrols.py`
```
Scout Name    Patrol
john doe      Tigers
```

### 2. From `check_requirements_in_advancement.py`
```
Requirement
Emergency Preparedness
```

### 3. From `generate_report.py`
For the `Lions` patrol, the report will look like:
```
Requirement        Jane Smith   Bob Green
Basic First Aid     ✔           ✔
Camping Skills                  ✔
```

For the `Tigers` patrol, the report will look like:
```
Requirement        John Doe    Alice Brown
Basic First Aid     ✔           ✔
Camping Skills      ✔
```

### 4. From `qc_checks.py`
- `scouts_in_patrols.tsv` will show:
```
Scout Name
bob green
```
- `requirements_in_advancement.tsv` will show:
```
Requirement
Emergency Preparedness
```

You can run it from the command line like: 
`python clean_advancement.py input_file output_file'

# Scout Advancement Report Generator
`generate_report.py` - load the advancement info, list of patrols, and list of requirements, process them to produce an advancement report for each patrol, along with a report for any scouts not connected to patrols, or any requirements from the report that aren't included in the list of requirements.

You can run it from the command line like:
'python generate_report.py advancement.tsv patrols.tsv requirements.tsv ./reports'

#advancement.tsv
an example cleaned advancement report (what would be produced by `clean_advancement.py`

# requirements.tsv
a list of advancement requirements through first class rank (as of 2025)

# patrols_example.tsv
an example roster of a pretend Troop

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The original code was generated with the assistance of ChatGPT (OpenAI). Thanks to OpenAI for providing the language model that assisted in creating this code.

