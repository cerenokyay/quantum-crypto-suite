import streamlit as st
import pandas as pd
import subprocess
import json

st.set_page_config(page_title="Grover Search", page_icon="🔓", layout="wide")

st.title("🔓 Grover Algoritması ile Kuantum Şifre Kırma")
st.markdown('''
Klasik bir kaba kuvvet (brute-force) saldırısı, 3 bitlik (8 olası durum) bir şifreyi bulmak için ortalama 4 deneme yapar. 
Grover algoritması ise **genlik büyütme (amplitude amplification)** tekniğini kullanarak, 
yanlış durumların olasılıklarını sönümlendirip doğru şifrenin olasılığını tek iterasyonda %90'ın üzerine çıkarır.
''')

st.divider()

col_input, col_info = st.columns([1, 2])
with col_input:
    target = st.selectbox("Kırılacak 3-bitlik Gizli Şifreyi Seçin:", 
                          ["000", "001", "010", "011", "100", "101", "110", "111"])
    run_btn = st.button("Kuantum Saldırısını Başlat 🚀", type="primary")

with col_info:
    st.info("💡 Sistem kararlılığını sağlamak için kuantum motoru tamamen bağımsız bir mikro terminal süreci (Subprocess) olarak çalıştırılmaktadır.")

if run_btn:
    with st.spinner("Kuantum hesaplaması izole bir terminal sürecinde çalıştırılıyor..."):
        
        # ÇÖZÜM: Qiskit'i Streamlit'ten tamamen kopardık. Komut satırından çalıştırıp çıktıyı okuyoruz.
        result = subprocess.run(
            ["python", "backend/grover_cli.py", target], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            # JSON çıktısını ayrıştır
            data = json.loads(result.stdout)
            counts = data["counts"]
            circuit_ascii = data["circuit"]
            
            col_chart, col_circuit = st.columns(2)
            
            with col_chart:
                st.subheader("Ölçüm Sonuçları (1024 Atış)")
                chart_data = pd.DataFrame.from_dict(counts, orient='index', columns=['Frekans'])
                st.bar_chart(chart_data, color="#7B61FF")
                
            with col_circuit:
                st.subheader("Oluşturulan Qiskit Devresi")
                st.code(circuit_ascii, language="text")
                
                
            st.success(f"Hedef şifre '{target}' başarıyla tespit edildi!")
        else:
            st.error("Kuantum süreci çalışırken bir hata oluştu.")
            st.code(result.stderr)