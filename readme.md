# NLP and Parallel Computing Final Project
A profanity recognizer for English and Filipino languages via Named Entity Recognition using Levenshtein distance
## Setup
1. Install Python 3.11 or higher.
```bash 
git clone https://github.com/jcmsj/nlparallel.git
cd <project folder>
# Create a python virtual environment
python -m venv .venv 

pip install -r requirements.txt 
```

## Example usage
1. Check the notebook [here](./profanity-filter.ipynb.ipynb)
### Adding dependencies
1. When adding dependencies, update the requirements.txt
```bash
cd <project folder>
pip freeze > requirements.txt
```

### Testing
1. Use doctests
2. See [tests.py](./tests.py) for more examples
