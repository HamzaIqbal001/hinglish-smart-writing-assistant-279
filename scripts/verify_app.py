import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import process_hinglish, EXAMPLES

def test_samples():
    print(f"Testing all {len(EXAMPLES)} sample inputs through app.py process_hinglish()...\n")
    for idx, (inp, imp_flag, tr_flag) in enumerate(EXAMPLES, 1):
        native, improved, english, status = process_hinglish(inp, imp_flag, tr_flag)
        print(f"--- Example {idx} ---")
        print(f"Input:    {inp}")
        print(f"Native:   {native}")
        print(f"Improved: {improved}")
        print(f"English:  {english}")
        print(f"Status:   {status}\n")

if __name__ == "__main__":
    test_samples()
