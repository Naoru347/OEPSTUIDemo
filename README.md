
# OEPS (Oral of English Proficiency Screening) Examination & Reporting Platform

The OEPS program is a comprehensive system designed to manage English proficiency assessments, generate detailed reports, and handle various aspects of the examination and reporting process. This system is composed of multiple Python scripts, with the main script serving as the entry point and orchestrating the functionality of the other scripts.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Main Script](#main-script)
  - [Top-Level Menu Options](#top-level-menu-options)
- [Scripts Overview](#scripts-overview)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install and set up the OEPS program, follow these steps:

1. **Clone the repository:**

   ```sh
   git clone https://github.com/your-repo/OEPS.git
   ```

2. **Navigate to the project directory:**

   ```sh
   cd OEPS
   ```

3. **Install the required dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Main Script

The main script (`OEPS_main.py`) serves as the entry point for the OEPS system. It provides a command line menu to access various functionalities including administering exams, generating reports, and processing assessment data.

**To run the main script:**

```sh
python OEPS_main.py
```

### Top-Level Menu Options

Upon running the main script, you will be presented with the following top-level menu options:

1. **Begin new exam**: Starts a new examination session.
2. **Generate placement report**: Generates a placement report based on the assessment data.
3. **Generate annual report**: Generates an annual report summarizing the data for the year.
4. **Generate x-year report**: Generates a report for a custom range of years.
5. **Exit**: Exits the program.

**To make a selection, enter the number of your choice (e.g., 1, 5, etc.)**.

## Scripts Overview

### `OEPS_main.py`

Handles the primary functionalities of the OEPS system, including:

- Loading and saving data
- Validating examiner and student names
- Administering questions and scoring responses
- Calculating total scores
- Orchestrating other scripts through a command line menu

### `OEPS_EXT_Reporting.py`

Generates extended PDF reports with visualizations, including:

- Reading and filtering assessment data
- Generating visualizations using `matplotlib`
- Creating PDF reports with `reportlab`

### `OEPS_Examination.py`

Administers the examination process, including:

- Loading questions from a file
- Timing and scoring the exam
- Collecting responses from examinees

### `OEPS_AR.py`

Processes and analyzes assessment data to generate reports, including:

- Processing raw assessment data
- Analyzing data for trends and insights
- Generating detailed assessment reports

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests with improvements or bug fixes.

1. **Fork the repository**
2. **Create a new branch**
3. **Make your changes**
4. **Submit a pull request**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
