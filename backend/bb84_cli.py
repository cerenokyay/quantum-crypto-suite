import sys
import json
from bb84_engine import run_bb84_process

if __name__ == "__main__":
    num_bits = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    eve_present = sys.argv[2].lower() == 'true' if len(sys.argv) > 2 else False
    
    result = run_bb84_process(num_bits, eve_present)
    print(json.dumps(result))