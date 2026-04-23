from pathlib import Path

# Resolve paths from the actual package location so the same code works
# both in the repo (`source/code/...`) and inside Docker (`/app/...`).
CODE_DIR = Path(__file__).resolve().parents[2]

if CODE_DIR.name == "code" and CODE_DIR.parent.name == "source":
    BASE_DIR = CODE_DIR.parents[1]
else:
    BASE_DIR = CODE_DIR

RUNTIME_DIR = CODE_DIR / 'runtime_definitions'

# Path to files folder
FILES_DIR = BASE_DIR / 'resource'

# Path to JSON files
JSON_DIR = FILES_DIR / 'json'
DATAFORDELER_JSON_DIR = JSON_DIR / 'datafordeler'
CIRCLEK_JSON_DIR = JSON_DIR / 'circlek'
