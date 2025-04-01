# scout_tracking
This project helps to generate reports and perform quality checks for scout advancement data, patrol membership, and requirements. It includes several scripts that can be run from the command line.

Collectively, these scripts process a Scoutbook data export to produce an advancement chart for each Patrol in a Troop.

This README describes:
[CLI Commands and Usage](#CLI-Commands-and-Usage)
[Example Input Files](#Example-Input-Files)
[Expected Output Files](#Expected-Output-Files)
[License](#License)
[Attribution](#Attribution)


## CLI Commands and Usage

### 1. **clean_advancement.py**
**Purpose**: Process the Scoutbook export/backup file to prepare it for subsequent report generation work. This script removes extra fields and records not related to Scout Advancement Work (for example, Cub Scout Awards).

**Usage**:
```
python clean_advancement.py <input_file> <output_file>
```

**Arguments**:
- `input_file`: Path to the advancement data backup file downloaded from Scoutbook (CSV format).
- `output_file`: Path and name for the output file (CSV format).

**Example**:
```
python clean_advancement.py troop_100__advancement.csv advancement.csv
```

**Output**:
A CSV file containing slected information from the Scoutbook backup, formatted for input to subsequent report and QC scripts included in this repository.



#### Expected Output:
**advancement.csv**
```
Scout Name,Requirement,Completion Date
Frank Jones,Scout Rank Requirement 2b,7/19/2024
```

---
### 2. `generate_report.py`

**Purpose**: Generate a patrol report summarizing the advancement progress of each scout in a specific patrol, a list of patrols, or all the patrols.

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
### 3. `check_scouts_in_patrols.py`

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

### 4. `check_requirements_in_advancement.py`

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

### 1.`troop100__advancement.csv`
(for clean_advancement.py)
```
"BSA Member ID","First Name","Middle Name","Last Name","Advancement Type","Advancement","Version","Date Completed","Approved","Awarded","MarkedCompletedBy","MarkedCompletedDate","CounselorApprovedBy","CounselorApprovedDate","LeaderApprovedBy","LeaderApprovedDate","AwardedBy","AwardedDate"
12600561,"Frank","A","Jones","Scout Rank Requirement","2b",2022,"7/19/2024",1,,ASM_Bill,8/6/2024,,,SM_Mary,8/27/2024,,
```

### 2. `advancement.csv`
```
Scout Name,Requirement,Completion Date
Frank Jones,Scout Rank Requirement 2b,7/19/2024
John Doe,Scout Rank Requirement 3a,7/19/2024
Jane Smith,First Class Rank Requirement 4,8/1/2024
John Doe,Tenderfoot Rank Requirement 1a,8/8/2024
Alice Brown,Scout Rank Requirement 1a,8/1/2024
Bob Green,Second Class Rank Requirement 2g,8/1/2024
Bob Green,Tenderfoot Rank Requirement 1a,8/1/2024
```

### 3. `patrols.tsv`
```
Scout Name    Patrol
Frank Jones   Ninjas
Jane Smith    Lions
Bob Green     Lions
John Doe      Tigers
Alice Brown   Tigers
```

### 4. `requirements.tsv`
```
Requirement Name        Alternative Text
Scout Rank Requirement 2b              2nd 2b
Tenderfoot Rank Requirement 1a                Tenderfoot 1a
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
Requirements in advancement.csv not found in requirements.tsv:
first class rank requirement 4
second class rank requirement 2g
scout rank requirement 3a
scout rank requirement 1a
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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Attribution

The original code was generated with the assistance of ChatGPT (OpenAI). Thanks to OpenAI for providing the language model that assisted in creating this code.

