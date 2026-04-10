import streamlit as st
import numpy as np

# Sayfa Ayarları
st.set_page_config(page_title="Veri Bilimi İşe Alım Simülatörü", layout="wide")

# Sigmoid Fonksiyonu (Yüzde Hesaplama için)
def get_hire_probability(score):
    return 1 / (1 + np.exp(-(score - 50) / 10)) * 100

# Başlık
st.title("📊 Veri Bilimi & İstatistik İşe Alım Simülatörü")
st.markdown("Yetkinliklerinizi seçin, işe alınma potansiyelinizi anlık olarak görün.")

st.divider()

# Arayüzü İki Sütuna Bölelim
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🛠 Teknik Yetkinlikler (0-5)")
    python = st.slider("Python Seviyesi", 0, 5, 2)
    sql = st.slider("SQL Seviyesi", 0, 5, 2)
    ml = st.slider("Makine Öğrenmesi (ML)", 0, 5, 1)
    stats = st.slider("İstatistik Teorisi", 0, 5, 3)
    viz = st.slider("Veri Görselleştirme (Tableau/PowerBI/Matplotlib)", 0, 5, 2)

    st.header("🎓 Eğitim & Deneyim")
    exp_years = st.number_input("Deneyim Yılı", 0, 20, 0)
    gpa = st.slider("Mezuniyet Not Ortalaması (GPA)", 0.0, 4.0, 2.5)
    uni_tier = st.selectbox("Üniversite Grubu", 
                            options=[1.0, 0.8, 0.6, 0.4], 
                            format_func=lambda x: "Tier 1 (ODTÜ, İTÜ, Boğaziçi vb.)" if x == 1.0 else 
                                          ("Tier 2 (Hacettepe, YTÜ, Ankara vb.)" if x == 0.8 else "Diğer"))

with col2:
    st.header("🌟 Ekstra Sinyaller")
    english = st.slider("İngilizce Seviyesi", 0, 5, 2)
    github_active = st.checkbox("Aktif bir GitHub portfolyom var")
    kaggle_score = st.checkbox("Kaggle yarışma derecem veya projelerim var")
    reference = st.checkbox("Güçlü bir referansım var")
    internship = st.checkbox("Staj tecrübem var")
    master_degree = st.checkbox("Yüksek Lisans / Doktora yapıyorum/yaptım")

# --- HESAPLAMA MOTORU ---
# 1. Teknik Skor (Max 30 Puan)
tech_score = (python*0.25 + sql*0.15 + ml*0.25 + stats*0.20 + viz*0.15) * 20

# 2. Deneyim Skor (Max 20 Puan)
exp_katsayi = 0.2 if exp_years == 0 else (0.5 if exp_years < 3 else (0.8 if exp_years < 5 else 1.0))
exp_score = exp_katsayi * 100

# 3. Proje Skor (Max 20 Puan)
proje_score = (github_active*0.4 + kaggle_score*0.4 + internship*0.2) * 100

# 4. Eğitim Skor (Max 15 Puan)
edu_score = (uni_tier*0.5 + (gpa/4.0)*0.3 + master_degree*0.2) * 100

# 5. Soft Sinyaller (Max 15 Puan)
soft_score = ((english/5)*0.6 + reference*0.4) * 100

# Ağırlıklı Toplam
final_weighted_score = (tech_score * 0.30 + exp_score * 0.20 + proje_score * 0.20 + 
                        edu_score * 0.15 + soft_score * 0.15)

# Yüzdeye Dönüştür
probability = get_hire_probability(final_weighted_score)

# --- SONUÇ EKRANI ---
st.divider()
st.header("🎯 Analiz Sonucu")

col_res1, col_res2 = st.columns([1, 2])

with col_res1:
    st.metric(label="İşe Alınma Olasılığı", value=f"%{probability:.1f}")

with col_res2:
    st.progress(int(probability))
    if probability > 80:
        st.success("Harika! Bu profille mülakata çağrılma şansınız çok yüksek. 🚀")
    elif probability > 50:
        st.info("İyi bir profilsiniz. Teknik projelerinizi artırarak şansınızı %80 üzerine çıkarabilirsiniz. 📈")
    else:
        st.warning("Gelişime açık alanlarınız var. Özellikle Python ve SQL üzerine yoğunlaşmanızı öneririz. 📚")
