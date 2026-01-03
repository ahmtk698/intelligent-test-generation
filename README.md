# README.MD

## PROJECT OVERVIEW
This project is an automated system designed to analyze Python source code and generate unit tests without manual intervention. It utilizes the Llama-3 model via the Groq API for logical reasoning and the Hypothesis library for property-based testing. The primary goal is to achieve 100% code coverage on standard logic modules while identifying edge cases that traditional manual testing might overlook

## KEY FEATURES
* **RAPID GENERATION:** Uses Groq's inference engine for near-instant creation of test suites.
* **FULL COVERAGE:** Specifically targets 100% line coverage, verified through pytest-cov integration
* **EDGE CASE DETECTION:** Implements property-based testing to find boundary-value failures.
* **VALIDATION LOOP:** The system does not just write code; it executes it and provides a real-time coverage report.
* **FALLBACK SYSTEM:** Includes a local knowledge base to handle API rate limits or connectivity issues.

## SYSTEM ARCHITECTURE
The application consists of three main components:
1. **FRONTEND:** A Streamlit-based dashboard for file management and result visualization.
2. **ANALYSIS ENGINE:** An AST (Abstract Syntax Tree) parser that breaks down source code into functional metadata.
3. **EXECUTION ENGINE:** A validation layer that runs the generated tests in a controlled environment using Pytest.



## TECHNICAL STACK
* **LANGUAGE:** Python 3.10+
* **INFERENCE:** Groq API (Llama-3.3-70b-versatile)
* **WEB:** Streamlit 
* **TESTING:** Pytest, Pytest-cov, Hypothesis
* **ENVIRONMENT:** python-dotenv 

## INSTALLATION AND SETUP

### 1. CLONE REPOSITORY
```bash
git clone <repository-url>
cd intelligent-test-generation
```

### 2. ENVIRONMENT AND DEPENDENCIES
   Create a virtual environment and install the required packages:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

```

### 3. CONFIGURATION
   Create a file named .env in the root folder and add your API key:
   GROQ_API_KEY='gsk_*********************************************'

### USAGE
Start the dashboard with the following command:
```bash
streamlit run app.py
```

After the dashboard starts, upload your Python files through the sidebar, click the generation button, and then run the validation to see the coverage results.

### PROJECT STRUCTURE
APP.PY: The main entry point for the Streamlit UI.

SRC/ANALYZER.PY: Logic for parsing Python source files into AST nodes.

SRC/TEST_GENERATOR.PY: Handles API communication and prompt construction.

SAMPLES/: Directory containing the source code to be tested.

TESTS/: Directory where the generated test scripts are stored.

### ACADEMIC CONTEXT
This system was developed as a final project for the SEN0414 Advanced Programming course at Istanbul Kultur University. It follows the AI4SE (AI for Software Engineering) framework for automated quality assurance.

### AUTHOR: Ahmet Kaya (2100005631) 
INSTRUCTOR: Yusuf Altunel, PhD





