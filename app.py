import streamlit as st

st.set_page_config(
    page_title="Quantum Cryptography Suite",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚛️ Quantum Cryptography Suite")
st.markdown('''
Bu laboratuvar, modern kriptografik sistemlerin kuantum algoritmaları karşısındaki zafiyetlerini ve kuantum mekaniğinin doğa yasalarıyla kurulan kırılamaz iletişim protokollerini simüle eden uçtan uca bir yazılım mühendisliği projesidir.

Apple Silicon mimarilerinde Qiskit'in derlenmiş C++/Rust çekirdekleri ile asenkron web sunucuları arasında yaşanan donanımsal çakışmaları (segfault) kökünden çözmek amacıyla, tüm kuantum motoru **işletim sistemi seviyesinde izole edilmiş alt süreçler (subprocess)** olarak çalışacak bir mikro terminal mimarisinde tasarlanmıştır.

### 🔬 Laboratuvar Modülleri

*   **[ 🔓 Grover Search ] - Kaba Kuvvetin Yıkımı:** Genlik büyütme (amplitude amplification) tekniği kullanılarak, klasik sistemlerin $O(N)$ sürede çözdüğü arama problemlerinin $O(\sqrt{N})$ karmaşıklığıyla kuantum Statevector uzayında nasıl tek adımda çözüldüğünü gösterir.
*   **[ 🗝️ Shor RSA ] - Matematiğin Yıkımı:** İnternet şifrelemesinin temelini oluşturan büyük sayıları asal çarpanlara ayırma problemini, Kuantum Fourier Dönüşümü (QFT) ve faz tahmini (phase estimation) devresi inşa ederek polinom zamanda çözer. 
*   **[ 🛡️ BB84 Protokolü ] - Kuantum Savunması:** Klonlamama Teoremi (No-Cloning Theorem) üzerine inşa edilmiş mutlak güvenli bir ağ simülasyonudur. İletişime sızan korsanların (Eve) fotonların dalga fonksiyonunu çökertmesi sonucu artan QBER (Kuantum Hata Oranı) ile anında ifşa edilmesini sağlar.

---
*Geliştirme Notu: Standart simülatörlerin bellek (RAM) limitlerini aşarak AES veya RSA-2048 ölçeğinde testler yapabilmek adına, arka plandaki matris hesaplamalarının Apple Accelerate framework'ü ve C++ (PyBind11) tabanlı SVD tensör daraltma modülleriyle optimize edilmesi projenin bir sonraki fazıdır.*
''')

st.info("Sol menüden bir algoritma seçerek kuantum simülasyonlarını başlatabilirsiniz.")