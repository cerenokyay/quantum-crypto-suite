from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

def c_amod15(a, power):
    """15 modunda kontrollü 'a' çarpım kapısı"""
    if a not in [2,7,8,11,13]:
        raise ValueError("'a' değeri 2,7,8,11 veya 13 olmalıdır")
    U = QuantumCircuit(4)
    for _ in range(power):
        if a in [2,13]:
            U.swap(0,1)
            U.swap(1,2)
            U.swap(2,3)
        if a in [7,8]:
            U.swap(2,3)
            U.swap(1,2)
            U.swap(0,1)
        if a in [11]:
            U.swap(1,3)
            U.swap(0,2)
        if a in [7,11,13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate(label=f"{a}^{power} mod 15")
    return U.control()

def qft_dagger(n):
    """Ters Kuantum Fourier Dönüşümü (QFT†)"""
    qc = QuantumCircuit(n)
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc.to_gate()

def get_shor_circuit(a=7):
    n_count = 3  # Sayıcı (counting) qubit sayısı
    qc = QuantumCircuit(n_count + 4, n_count)
    
    # 1. Tüm sayıcı qubitleri süperpozisyona al
    for q in range(n_count):
        qc.h(q)
        
    # Yardımcı (auxiliary) register'ı |1> durumuna getir
    qc.x(n_count)
    
    # 2. Kontrollü U kapılarını (Modüler Üs Alma) uygula
    for q in range(n_count):
        qc.append(c_amod15(a, 2**q), [q] + [i+n_count for i in range(4)])
        
    # 3. Ters QFT uygula
    qc.append(qft_dagger(n_count), range(n_count))
    
    # 4. Ölçüm
    qc.measure(range(n_count), range(n_count))
    return qc

def run_shor_process(a=7):
    qc = get_shor_circuit(a)
    
    # Simülasyon çökmesini engellemek için Statevector ile matematiksel analiz
    qc_no_meas = qc.copy()
    qc_no_meas.remove_final_measurements()
    
    state = Statevector(qc_no_meas)
    # Sadece ilk 3 (sayıcı) qubit'in olasılıklarını alıyoruz
    probs = state.probabilities_dict(qargs=[0,1,2])
    
    counts = {str(k): int(v * 1024) for k, v in probs.items() if v > 0.001}
    circuit_ascii = qc.draw(output='text')
    
    return counts, circuit_ascii