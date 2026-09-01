from backend.grover_engine import run_grover

print("Qiskit motoru başlatılıyor...")
counts, qc = run_grover("010")
print("Hesaplama başarılı:", counts)
print("Devre çiziliyor...")
print(qc.draw(output='text'))
print("İşlem sorunsuz tamamlandı.")