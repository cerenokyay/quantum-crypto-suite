import sys
import json
from shor_engine import run_shor_process

if __name__ == "__main__":
    a = 7
    if len(sys.argv) > 1:
        a = int(sys.argv[1])
        
    counts, circuit_ascii = run_shor_process(a)
    
    output = {
        "counts": counts,
        "circuit": str(circuit_ascii)
    }
    print(json.dumps(output))