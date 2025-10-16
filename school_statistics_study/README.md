## About the Project 

The idea here is to make some statistical analysis for Students in my class

## Project Structure

```
school_statistics_study/
│
├── main_lib/                   # Core code
│   ├── __init__.py
│   └── school_study.py         # Placeholder for functions (students implement)
│
├── tests/                      # Unit tests
│   ├── __init__.py
│   └── school_study_t/
│       ├── __init__.py
│       └── test_school_study.py # unit tests for school_study
│
├── run_test.sh          # Script to run all tests
├── setup.py
└── README.md
```

## Setup Instructions

1. **Create a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. **Install in editable mode:**

```bash
pip install -e .
```

## Running the study

After installation, launch the study using:

```bash
run_study
```

## Running Tests

All unit tests are executed using the provided `run_test.sh` script:

```bash
./run_test.sh
```

This will run all tests in the `tests/` directory using the `unittest` framework.
