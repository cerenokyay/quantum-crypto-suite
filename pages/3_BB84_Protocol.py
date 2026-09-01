import streamlit as st
import pandas as pd
import subprocess
import json

st.set_page_config(page_title="BB84 Protocol", page_icon="🛡️", layout="wide")

st.title("🛡️ BB84 Protokolü: Kırılamaz Kuantum Anahtarı")
st.markdown('''
Grover ve Shor algoritmaları mevcut sistemleri kırarken, BB84 protokolü kuantum mekaniğinin 
**Klonlamama Teoremi (No-Cloning Theorem)** sayesinde kırılamaz bir iletişim ağı kurar. 
Eğer hatta bir dinleyici (Eve) sızarsa, fotonların durumunu geri dönülemez şekilde çökertir 
ve hata oranı (QBER) fırlayarak korsanın varlığını anında ifşa eder.
''')

st.divider()

col_input, col_info = st.columns([1, 1])
with col_input:
    num_bits = st.slider("İletilecek Qubit Sayısı:", min_value=16, max_value=128, value=32, step=16)
    eve_present = st.toggle("Hacker (Eve) Ağı Dinlesin mi? 🕵️‍♀️", value=False)
    run_btn = st.button("Kuantum İletişimini Başlat 🚀", type="primary")

with col_info:
    if eve_present:
        st.error("🚨 Eve hatta sızdı! Kuantum durumlarını kopyalayamadığı için doğrudan ölçecek ve Alice'in gönderdiği orijinal fotonların bozulmasına neden olacak.")
    else:
        st.success("✅ Hat güvenli. Alice ve Bob arasında sadece doğa yasalarının koruduğu bir haberleşme gerçekleşecek.")

if run_btn:
    with st.spinner("Fotonlar iletiliyor ve bazlar karşılaştırılıyor..."):
        
        result = subprocess.run(
            ["python", "backend/bb84_cli.py", str(num_bits), str(eve_present)], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            
            st.subheader(f"QBER (Kuantum Hata Oranı): %{data['error_rate']:.2f}")
            if data['error_rate'] > 11:
                st.error("⚠️ HATA ORANI ÇOK YÜKSEK! İletişim derhal kesildi. Hatta kesinlikle bir dinleyici (Eve) var.")
            else:
                st.success("🔒 Anahtar başarıyla oluşturuldu! Hat güvenli.")
            
            st.markdown("### Ham Veri İletişim Tablosu")
            
            # Bazları sembollere çevirme
            basis_sym = {0: "✚ (Z)", 1: "✖ (X)"}
            
            df = pd.DataFrame({
                "Alice'in Biti": data["alice_bits"],
                "Alice'in Bazı": [basis_sym[b] for b in data["alice_bases"]],
                "Bob'un Bazı": [basis_sym[b] for b in data["bob_bases"]],
                "Bob'un Biti": data["bob_bits"]
            })
            
            # Sadece eşleşen bazları vurgula
            def highlight_matches(row):
                if row.name in data["matches"]:
                    return ['background-color: #173b22'] * len(row)
                return [''] * len(row)
                
            st.dataframe(df.style.apply(highlight_matches, axis=1), use_container_width=True)
            
            st.markdown("### Sonuç (Güvenli Şifreleme Anahtarı)")
            st.info(f"Oluşturulan Anahtar: **{''.join(map(str, data['key_alice']))}**")
            
        else:
            st.error("Kuantum süreci çalışırken bir hata oluştu.")
            st.code(result.stderr)