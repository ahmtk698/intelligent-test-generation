import streamlit as st
import os
import time
import subprocess
import shutil  
from src.analyzer import analyze_file
from src.test_generator import generate_tests_with_ai

st.set_page_config(layout="wide", page_title="SEN0414 Final")

st.markdown("## SEN0414 - Advanced Programming Final Project")
st.markdown("**Student:** Ahmet Kaya (2100005631) | **Project:** Intelligent Test Generation System")
st.write("---")

with st.sidebar:
    st.header("Dosya Yükleme Paneli")
    st.write("Test edilecek Python (.py) dosyalarını buraya yükleyin.")
    
    uploaded_files = st.file_uploader("Dosya Seç", type=['py'], accept_multiple_files=True)
    
    TARGET_DIR = "uploaded_samples"
    active_files = []

    if uploaded_files:
        if os.path.exists(TARGET_DIR):
            shutil.rmtree(TARGET_DIR)
        
        os.makedirs(TARGET_DIR)

        st.success(f"✅ {len(uploaded_files)} dosya yüklendi.")
        for f in uploaded_files:
            file_path = os.path.join(TARGET_DIR, f.name)
            with open(file_path, "wb") as w:
                w.write(f.getbuffer())
            active_files.append(f.name)
            
    else:
        if os.path.exists(TARGET_DIR):
            shutil.rmtree(TARGET_DIR)
        st.info("Lütfen dosya yükleyiniz.")


if not active_files:
    st.warning("⬅️ Başlamak için sol taraftan dosya yükleyin.")

else:
    st.subheader("1. Kaynak Kod İncelemesi")
    st.write("Sisteme yüklenen dosyaların içeriği aşağıdadır:")
    
    cols = st.columns(len(active_files))
    for i, filename in enumerate(active_files):
        with cols[i]:
            st.info(f" {filename}")
            path = os.path.join(TARGET_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                st.code(f.read(), language="python")

    st.write("---")

    st.subheader("2. AI Test Üretimi (Generation)")
    st.write("Bu aşamada Agent, kodu analiz eder ve test senaryoları yazar.")
    
    col_btn, col_status = st.columns([1, 4])
    
    with col_btn:
        generate_btn = st.button("Testleri Oluştur", type="primary")
    
    if generate_btn:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        full_test_code = "import pytest\nimport math\nfrom hypothesis import given, strategies as st\n"
        
        for f in active_files:
            mod = f.replace(".py", "")
            full_test_code += f"from {TARGET_DIR}.{mod} import *\n"
        full_test_code += "\n"

        for idx, filename in enumerate(active_files):
            status_text.text(f"İşleniyor: {filename}...")
            path = os.path.join(TARGET_DIR, filename)
            
            funcs = analyze_file(path)
            for func in funcs:
                ai_code = generate_tests_with_ai(func['name'], func['code'])
                if "# Error" not in ai_code:
                    full_test_code += f"# Tests for {func['name']}\n{ai_code}\n\n"
            
            progress_bar.progress((idx + 1) / len(active_files))
            time.sleep(0.5)

        if not os.path.exists("tests"): os.makedirs("tests")
        with open("tests/test_generated.py", "w", encoding="utf-8") as f:
            f.write(full_test_code)
        
        status_text.success("Test dosyası oluşturuldu! (tests/test_generated.py)")
        st.session_state['tests_done'] = True

    if 'tests_done' in st.session_state:
        with st.expander("AI Tarafından Oluşturulan Test Kodunu Gör"):
            with open("tests/test_generated.py", "r", encoding="utf-8") as f:
                st.code(f.read(), language="python")

    st.write("---")

    st.subheader("3. Doğrulama ve Kapsama (Coverage)")
    st.write("Oluşturulan testler Pytest ile çalıştırılır.")
    
    run_btn = st.button("Testleri Çalıştır")
    
    if run_btn:
        if 'tests_done' not in st.session_state:
            st.error("Önce testleri oluşturmalısınız.")
        else:
            with st.spinner("Testler koşuluyor..."):
                cmd = ["pytest", f"--cov={TARGET_DIR}", "--cov-report=term-missing"]
                res = subprocess.run(cmd, capture_output=True, text=True)
                
                st.text("Terminal Çıktısı:")
                st.code(res.stdout)
                
                if res.returncode == 0:
                    st.success("SONUÇ: Tüm testler başarıyla geçti.")
                    if "100%" in res.stdout:
                        st.balloons()
                        st.success("MÜKEMMEL: %100 Kod Kapsama Oranına Ulaşıldı!")
                else:
                    st.error("Bazı testler başarısız oldu.")

st.write("---")
st.caption("Istanbul Kültür Üniversitesi")
