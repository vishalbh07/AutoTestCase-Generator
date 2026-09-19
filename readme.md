# AutoTestCase Generator 🤖

## Problem
Manual test case writing is slow, inconsistent, and often misses edge cases (especially negative scenarios) for every input field on a page.

## Solution
This tool automates the initial draft of a QA Test Plan. It crawls a web page, identifies interactive components (forms, logins, searches), and uses template-based logic to generate an Excel file formatted for immediate use in QA tools.

## Pipeline
1. **Crawl**: Playwright opens the URL and extracts all metadata for buttons, inputs, and links.
2. **Classify**: A rule-based engine groups elements into "Actions" (e.g., identifying a Login form vs. a Search bar).
3. **Generate**: Templates create Positive and Negative test cases with steps and expected results.
4. **Export**: Data is formatted into a standard QA tabular format in Excel.

## Installation
1. `pip install -r requirements.txt`
2. `playwright install chromium`

## Usage
`streamlit run app.py`

## Project Structure
- `app.py`: Streamlit UI.
- `crawler.py`: Browser automation logic.
- `classifier.py`: Action detection rules.
- `generator.py`: Test case content generation.
- `exporter.py`: Excel file creation.
- `validate.py`: Accuracy measurement script.