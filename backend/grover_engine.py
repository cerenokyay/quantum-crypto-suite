from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def get_grover_circuit(target_state: str, measure: bool = False) -> QuantumCircuit:
    n = len(target_state)
    qc = QuantumCircuit(n)

    qc.h(range(n))

    for i in range(n):
        if target_state[n - 1 - i] == '0':
            qc.x(i)
            
    qc.h(n-1)
    if n > 1:
        qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    
    for i in range(n):
        if target_state[n - 1 - i] == '0':
            qc.x(i)

    qc.h(range(n))
    qc.x(range(n))
    
    qc.h(n-1)
    if n > 1:
        qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    
    qc.x(range(n))
    qc.h(range(n))
    
    if measure:
        qc.measure_all()
        
    return qc

def run_grover_process(target_state: str):
    qc_no_measure = get_grover_circuit(target_state, measure=False)
    state = Statevector(qc_no_measure)
    probs = state.probabilities_dict()
    
    counts = {str(k): int(v * 1024) for k, v in probs.items() if v > 0.001}
    
    qc_measured = get_grover_circuit(target_state, measure=True)
    # Çizimi direkt burada ASCII text'e çevirip string olarak döndürüyoruz
    circuit_ascii = qc_measured.draw(output='text')
    
    return counts, circuit_ascii