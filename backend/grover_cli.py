import sys
import json
from grover_engine import run_grover_process

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        counts, circuit_ascii = run_grover_process(target)
        
        # ÇÖZÜM: circuit_ascii nesnesini str() ile standart stringe çeviriyoruz
        output = {
            "counts": counts,
            "circuit": str(circuit_ascii)
        }
        print(json.dumps(output))