from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicSimulator
import numpy as np

def run_bb84_process(num_bits=32, eve_present=False):
    # 0: Z bazı (Dikey/Yatay), 1: X bazı (Çapraz)
    alice_bits = np.random.randint(2, size=num_bits)
    alice_bases = np.random.randint(2, size=num_bits) 
    bob_bases = np.random.randint(2, size=num_bits)
    
    bob_bits = []
    backend = BasicSimulator()
    
    for i in range(num_bits):
        # 1 Qubit ve 2 Klasik bit (biri Eve, biri Bob için) içeren devre
        qc = QuantumCircuit(1, 2)
        
        # 1. Alice qubit'i hazırlar
        if alice_bits[i] == 1:
            qc.x(0)
        if alice_bases[i] == 1:
            qc.h(0)
            
        # 2. Eve hatta sızıp ölçüm yapar (Opsiyonel)
        if eve_present:
            eve_basis = np.random.randint(2)
            if eve_basis == 1:
                qc.h(0)
            qc.measure(0, 0) # Eve'in ölçümü durumu çökertir (Wavefunction collapse)
            if eve_basis == 1:
                qc.h(0) # Bob'a göndermek için tekrar baz değiştirir
                
        # 3. Bob qubit'i ölçer
        if bob_bases[i] == 1:
            qc.h(0)
        qc.measure(0, 1)
        
        t_qc = transpile(qc, backend)
        job = backend.run(t_qc, shots=1)
        counts = job.result().get_counts(t_qc)
        
        # Sonuç 'Bob_biti Eve_biti' formatında gelir (örn: '1 0')
        measured_str = list(counts.keys())[0]
        bob_bits.append(int(measured_str[0]))
        
    # 4. Anahtar Eleme (Sifting) - Alice ve Bob sadece aynı bazları kullandıkları bitleri tutar
    key_alice = []
    key_bob = []
    match_indices = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            match_indices.append(i)
            key_alice.append(int(alice_bits[i]))
            key_bob.append(int(bob_bits[i]))
            
    # QBER (Kuantum Hata Oranı) Hesaplama
    errors = sum(1 for a, b in zip(key_alice, key_bob) if a != b)
    error_rate = (errors / len(key_alice)) * 100 if key_alice else 0
    
    return {
        "alice_bits": alice_bits.tolist(),
        "alice_bases": alice_bases.tolist(),
        "bob_bases": bob_bases.tolist(),
        "bob_bits": bob_bits,
        "key_alice": key_alice,
        "key_bob": key_bob,
        "error_rate": error_rate,
        "matches": match_indices
    }