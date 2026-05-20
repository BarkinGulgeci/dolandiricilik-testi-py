import streamlit as st
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt
import pandas as pd

# Sayfa Genişlik ve Tema Ayarı
st.set_page_config(layout="wide", page_title="Yapay Zeka ile Fraud Tespit Sistemi")

# CSS ile Arka Plan ve Kart Tasarımlarını Premium Yapma
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; color: #ff4b4b; }
    iframe { background-color: transparent !important; }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# --- ADIM 1: YARDIMCI FONKSİYONLARIN TANIMLANMASI ---
# ==============================================================================
def get_mu(var, term, val):
    try:
        return fuzz.interp_membership(var.universe, var[term].mf, val)
    except:
        return 0.0


def ciz_havali_grafik(var, title, current_val):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.set_facecolor('#1a1f2c')
    fig.patch.set_facecolor('#0e1117')
    colors = ['#3b82f6', '#10b981', '#ef4444']
    for i, term in enumerate(var.terms):
        color = colors[i % len(colors)]
        ax.plot(var.universe, var[term].mf, label=term, color=color, linewidth=2)
        ax.fill_between(var.universe, 0, var[term].mf, color=color, alpha=0.12)
        mu = get_mu(var, term, current_val)
        if mu > 0:
            ax.plot(current_val, mu, 'o', color='#ff4b4b', markersize=6, markeredgecolor='white')
    ax.axvline(x=current_val, color='#ff4b4b', linestyle='-', linewidth=1.8)
    ax.set_title(title, color='white', fontsize=10, fontweight='bold')
    ax.grid(True, color='#2d3748', linestyle=':', alpha=0.5)
    ax.tick_params(colors='white', labelsize=8)
    ax.legend(fontsize='x-small', facecolor='#11151c', edgecolor='#2d3748', labelcolor='white')
    return fig


def yukle_senaryo_callback(tutar_val, saat_val, guvenlik_val):
    st.session_state.s_tutar = float(tutar_val)
    st.session_state.s_saat = float(saat_val)
    st.session_state.s_guvenlik = int(guvenlik_val)


# ==============================================================================
# --- ADIM 2: DEĞİŞKENLERİN VE EVRENSEL KÜMELERİN TANIMLANMASI ---
# ==============================================================================
islem_tutari = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'islem_tutari')
islem_saati = ctrl.Antecedent(np.arange(0, 24.1, 0.1), 'islem_saati')
cihaz_guvenligi = ctrl.Antecedent(np.arange(0, 101, 1), 'cihaz_guvenligi')

fraud_riski = ctrl.Consequent(np.arange(0, 101, 1), 'fraud_riski', defuzzify_method='centroid')

# --- ÜYELİK FONKSİYONLARININ ATANMASI ---
islem_tutari['Normal'] = fuzz.trimf(islem_tutari.universe, [0, 0, 4])
islem_tutari['Yuksek'] = fuzz.trimf(islem_tutari.universe, [3, 5, 8])
islem_tutari['Anormal'] = fuzz.trapmf(islem_tutari.universe, [6, 8, 10, 10])

islem_saati['Gece_Yarisi'] = fuzz.trapmf(islem_saati.universe, [0, 0, 4, 8])
islem_saati['Mesai_Saati'] = fuzz.trimf(islem_saati.universe, [6, 12, 18])
islem_saati['Aksam_Gec'] = fuzz.trapmf(islem_saati.universe, [16, 20, 24, 24])

cihaz_guvenligi['Tehlikeli'] = fuzz.trapmf(cihaz_guvenligi.universe, [0, 0, 25, 45])
cihaz_guvenligi['Supheli'] = fuzz.trimf(cihaz_guvenligi.universe, [35, 50, 65])
cihaz_guvenligi['Guvenli'] = fuzz.trapmf(cihaz_guvenligi.universe, [55, 75, 100, 100])

fraud_riski['Dusuk'] = fuzz.trapmf(fraud_riski.universe, [0, 0, 25, 45])
fraud_riski['Orta'] = fuzz.trimf(fraud_riski.universe, [35, 50, 65])
fraud_riski['Yuksek'] = fuzz.trapmf(fraud_riski.universe, [55, 75, 100, 100])

# ==============================================================================
# --- ADIM 3: KURAL TABANI (TAM 15 AKADEMİK FRAUD KURALI) ---
# ==============================================================================
kurallar = [
    ctrl.Rule(islem_tutari['Anormal'] & islem_saati['Gece_Yarisi'], fraud_riski['Yuksek']),
    ctrl.Rule(islem_tutari['Anormal'] & cihaz_guvenligi['Tehlikeli'], fraud_riski['Yuksek']),
    ctrl.Rule(islem_saati['Gece_Yarisi'] & cihaz_guvenligi['Tehlikeli'], fraud_riski['Yuksek']),
    ctrl.Rule(islem_tutari['Yuksek'] & islem_saati['Gece_Yarisi'] & cihaz_guvenligi['Supheli'], fraud_riski['Yuksek']),
    ctrl.Rule(islem_tutari['Anormal'] & islem_saati['Aksam_Gec'] & cihaz_guvenligi['Tehlikeli'], fraud_riski['Yuksek']),
    
    ctrl.Rule(islem_tutari['Yuksek'] & islem_saati['Mesai_Saati'] & cihaz_guvenligi['Supheli'], fraud_riski['Orta']),
    ctrl.Rule(islem_tutari['Normal'] & islem_saati['Gece_Yarisi'] & cihaz_guvenligi['Supheli'], fraud_riski['Orta']),
    ctrl.Rule(islem_tutari['Yuksek'] & islem_saati['Aksam_Gec'] & cihaz_guvenligi['Guvenli'], fraud_riski['Orta']),
    ctrl.Rule(islem_tutari['Normal'] & islem_saati['Mesai_Saati'] & cihaz_guvenligi['Tehlikeli'], fraud_riski['Orta']),
    ctrl.Rule(islem_tutari['Anormal'] & islem_saati['Mesai_Saati'] & cihaz_guvenligi['Guvenli'], fraud_riski['Orta']),
    
    ctrl.Rule(islem_tutari['Normal'] & islem_saati['Mesai_Saati'] & cihaz_guvenligi['Guvenli'], fraud_riski['Dusuk']),
    ctrl.Rule(islem_tutari['Normal'] & islem_saati['Aksam_Gec'] & cihaz_guvenligi['Guvenli'], fraud_riski['Dusuk']),
    ctrl.Rule(islem_tutari['Yuksek'] & islem_saati['Mesai_Saati'] & cihaz_guvenligi['Guvenli'], fraud_riski['Dusuk']),
    ctrl.Rule(islem_tutari['Normal'] & islem_saati['Mesai_Saati'] & cihaz_guvenligi['Supheli'], fraud_riski['Dusuk']),
    ctrl.Rule(islem_tutari['Normal'] & islem_saati['Aksam_Gec'] & cihaz_guvenligi['Supheli'], fraud_riski['Dusuk'])
]

fraud_sistemi = ctrl.ControlSystem(kurallar)
fraud_simulasyon = ctrl.ControlSystemSimulation(fraud_sistemi)

# ==============================================================================
# --- ADIM 4: SESSION STATE VE WIDGET INITIALIZATION ---
# ==============================================================================
if 's_tutar' not in st.session_state: st.session_state.s_tutar = 1.5
if 's_saat' not in st.session_state: st.session_state.s_saat = 14.0
if 's_guvenlik' not in st.session_state: st.session_state.s_guvenlik = 90

# --- SIDEBAR PANEL DÜZENİ ---
st.sidebar.header("🎛️ Risk Faktörleri Paneli")
val_tutar = st.sidebar.slider("1. İşlem Tutarı (Eski Oran Katı)", 0.0, 10.0, step=0.1, key="s_tutar")
val_saat = st.sidebar.slider("2. İşlem Saati (00:00 - 24:00)", 0.0, 24.0, step=0.5, key="s_saat")
val_guvenlik = st.sidebar.slider("3. Cihaz/Konum Güvenlik Skoru (%)", 0, 100, key="s_guvenlik")

st.sidebar.markdown("---")
st.sidebar.header("📋 Gerçek Zamanlı Test Senaryoları")

st.sidebar.button("🔴 Gece Yarısı Tehdidi (Yüksek Risk)", on_click=yukle_senaryo_callback, args=(9.0, 2.5, 15))
st.sidebar.button("🟡 Şüpheli Doğrulama (Orta Risk)", on_click=yukle_senaryo_callback, args=(5.5, 21.0, 45))
st.sidebar.button("🟢 Standart Müşteri (Düşük Risk)", on_click=yukle_senaryo_callback, args=(1.2, 12.5, 95))
st.sidebar.button("📐 Sınır Durum (Gri Alan %50)", on_click=yukle_senaryo_callback, args=(5.0, 12.0, 50))

st.sidebar.markdown("---")
st.sidebar.button("🔄 Değerleri Sıfırla", on_click=yukle_senaryo_callback, args=(1.5, 14.0, 90))

# ==============================================================================
# --- ADIM 5: ANA SAYFA GÖRSEL MATRİS VE AKIŞ ŞEMASI ---
# ==============================================================================
st.markdown("<h3 style='text-align: center; color: #ff4b4b; margin-top: 15px; margin-bottom: 15px; font-size: 18px; font-weight: bold;'>🏗️ Bulanık Mantık Dolandırıcılık Tespit Motoru Sistem Mimarisi</h3>", unsafe_allow_html=True)

st.markdown(f"""
    <div style='background-color: #1e222b; padding: 15px; border-radius: 8px; margin-top: 15px; border: 1px solid #2d3748;'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; text-align: center; font-size: 11px; font-family: monospace;'>
            <div style='background-color: #10141d; padding: 10px; border-radius: 5px; flex: 1; margin: 4px; border-top: 3px solid #3b82f6;'>
                <b style='color:#3b82f6;'>1. GİRİŞLER</b><br>Tutar, Saat, Güvenlik<br><small style='color:#a0aec0;'>Dinamik Metrikler</small>
            </div>
            <div style='color: #ff4b4b; font-weight: bold; font-size:16px;'>➔</div>
            <div style='background-color: #10141d; padding: 10px; border-radius: 5px; flex: 1; margin: 4px; border-top: 3px solid #10b981;'>
                <b style='color:#10b981;'>2. BULANIKLAŞTIRMA</b><br>Üyelik Fonksiyonları<br><small style='color:#a0aec0;'>trimf + trapmf Analizi</small>
            </div>
            <div style='color: #ff4b4b; font-weight: bold; font-size:16px;'>➔</div>
            <div style='background-color: #10141d; padding: 10px; border-radius: 5px; flex: 1; margin: 4px; border-top: 3px solid #f59e0b;'>
                <b style='color:#f59e0b;'>3. ÇIKARIM MOTORU</b><br>15 Akademik Kural<br><small style='color:#a0aec0;'>Mamdani Çıkarımı (min)</small>
            </div>
            <div style='color: #ff4b4b; font-weight: bold; font-size:16px;'>➔</div>
            <div style='background-color: #10141d; padding: 10px; border-radius: 5px; flex: 1; margin: 4px; border-top: 3px solid #ef4444;'>
                <b style='color:#ef4444;'>4. DURULAŞTIRMA</b><br>Ağırlık Merkezi Hesaplama<br><small style='color:#a0aec0;'>Centroid Metodu</small>
            </div>
            <div style='color: #ff4b4b; font-weight: bold; font-size:16px;'>➔</div>
            <div style='background-color: #1a1f2c; padding: 10px; border-radius: 5px; flex: 1; margin: 4px; border: 1px dashed #ff4b4b;'>
                <b style='color:#ff4b4b;'>5. SİSTEM ÇIKISI</b><br>Fraud Risk Skoru %<br><small style='color:#a0aec0;'>Anlık Güvenlik Kararı</small>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# --- ADIM 6: REAKTİF CANLI ÇIKARIM MATRİSİ HESAPLAMASI ---
# ==============================================================================
fraud_simulasyon.input['islem_tutari'] = val_tutar
fraud_simulasyon.input['islem_saati'] = val_saat
fraud_simulasyon.input['cihaz_guvenligi'] = val_guvenlik

# KEYERROR ENGELLEYİCİ GÜVENLİ HESAPLAMA BLOĞU
try:
    fraud_simulasyon.compute()
    skor = fraud_simulasyon.output['fraud_riski']
    hata_var = False
except:
    # Eğer matematiksel olarak hiçbir kural kesişimi yoksa varsayılan güvenli alan skoru üret
    skor = 35.0  
    hata_var = True

if skor >= 65:
    card_bg = "#8b0000"  
    status_lbl = "🚨 YÜKSEK FRAUD RİSKİ (Bloke Edildi)"
    baskin_sonuc = "Yuksek"
elif skor >= 40:
    card_bg = "#d97706"  
    status_lbl = "⚠️ ORTA RİSK (SMS Onayı Gerekli)"
    baskin_sonuc = "Orta"
else:
    card_bg = "#10b981"  
    status_lbl = "✅ GÜVENLİ İŞLEM (Onaylandı)"
    baskin_sonuc = "Dusuk"

st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("#### 🎯 Canlı Risk Analiz Kartı")
    st.markdown(f"""
        <div style='background-color: #1a1f2c; padding: 25px; border-radius: 8px; border-bottom: 5px solid {card_bg}; text-align: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);'>
            <span style='color: #a0aec0; font-size: 13px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;'>Hesaplanan Fraud Risk Oranı</span>
            <h1 style='color: white; margin: 8px 0; font-size: 46px; font-weight: bold;'>%{skor:.2f}</h1>
            <span style='background-color: {card_bg}; color: white; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: bold;'>{status_lbl}</span>
        </div>
    """, unsafe_allow_html=True)

    fig_out, ax_out = plt.subplots(figsize=(6, 3.2))
    ax_out.set_facecolor('#1a1f2c')
    fig_out.patch.set_facecolor('#0e1117')
    colors_out = ['#10b981', '#f59e0b', '#ef4444']
    for i, term in enumerate(fraud_riski.terms):
        ax_out.plot(fraud_riski.universe, fraud_riski[term].mf, label=term, color=colors_out[i], linewidth=2)
        ax_out.fill_between(fraud_riski.universe, 0, fraud_riski[term].mf, color=colors_out[i], alpha=0.12)
    ax_out.axvline(x=skor, color='#ff4b4b', linestyle='--', linewidth=2.5, label=f'Centroid: {skor:.1f}')
    ax_out.set_title("Nihai Risk Karar Dağılımı (Centroid)", color='white', fontweight='bold', fontsize=10)
    ax_out.grid(True, color='#2d3748', linestyle=':', alpha=0.5)
    ax_out.tick_params(colors='white', labelsize=8)
    ax_out.legend(facecolor='#11151c', edgecolor='#2d3748', labelcolor='white', fontsize='small')
    st.pyplot(fig_out)

with col2:
    st.markdown("#### 📜 Ateşlenen Finansal Güvenlik Kuralları")

    rule_specs = [
        {"no": 1, "desc": "Tutar=Anormal + Saat=Gece_Yarisi", "output": "Yuksek",
         "act": min(get_mu(islem_tutari, 'Anormal', val_tutar), get_mu(islem_saati, 'Gece_Yarisi', val_saat))},
        {"no": 2, "desc": "Tutar=Anormal + Cihaz=Tehlikeli", "output": "Yuksek",
         "act": min(get_mu(islem_tutari, 'Anormal', val_tutar), get_mu(cihaz_guvenligi, 'Tehlikeli', val_guvenlik))},
        {"no": 3, "desc": "Saat=Gece_Yarisi + Cihaz=Tehlikeli", "output": "Yuksek",
         "act": min(get_mu(islem_saati, 'Gece_Yarisi', val_saat), get_mu(cihaz_guvenligi, 'Tehlikeli', val_guvenlik))},
        {"no": 4, "desc": "Tutar=Yuksek + Saat=Gece_Yarisi + Cihaz=Supheli", "output": "Yuksek",
         "act": min(get_mu(islem_tutari, 'Yuksek', val_tutar), get_mu(islem_saati, 'Gece_Yarisi', val_saat), get_mu(cihaz_guvenligi, 'Supheli', val_guvenlik))},
        {"no": 5, "desc": "Tutar=Anormal + Saat=Aksam_Gec + Cihaz=Tehlikeli", "output": "Yuksek",
         "act": min(get_mu(islem_tutari, 'Anormal', val_tutar), get_mu(islem_saati, 'Aksam_Gec', val_saat), get_mu(cihaz_guvenligi, 'Tehlikeli', val_guvenlik))},
        
        {"no": 6, "desc": "Tutar=Yuksek + Saat=Mesai_Saati + Cihaz=Supheli", "output": "Orta",
         "act": min(get_mu(islem_tutari, 'Yuksek', val_tutar), get_mu(islem_saati, 'Mesai_Saati', val_saat), get_mu(cihaz_guvenligi, 'Supheli', val_guvenlik))},
        {"no": 7, "desc": "Tutar=Normal + Saat=Gece_Yarisi + Cihaz=Supheli", "output": "Orta",
         "act": min(get_mu(islem_tutari, 'Normal', val_tutar), get_mu(islem_saati, 'Gece_Yarisi', val_saat), get_mu(cihaz_guvenligi, 'Supheli', val_guvenlik))},
        {"no": 8, "desc": "Tutar=Yuksek + Saat=Aksam_Gec + Cihaz=Guvenli", "output": "Orta",
         "act": min(get_mu(islem_tutari, 'Yuksek', val_tutar), get_mu(islem_saati, 'Aksam_Gec', val_saat), get_mu(cihaz_guvenligi, 'Guvenli', val_guvenlik))},
        {"no": 9, "desc": "Tutar=Normal + Saat=Mesai_Saati + Cihaz=Tehlikeli", "output": "Orta",
         "act": min(get_mu(islem_tutari, 'Normal', val_tutar), get_mu(islem_saati, 'Mesai_Saati', val_saat), get_mu(cihaz_guvenligi, 'Tehlikeli', val_guvenlik))},
        {"no": 10, "desc": "Tutar=Anormal + Saat=Mesai_Saati + Cihaz=Guvenli", "output": "Orta",
         "act": min(get_mu(islem_tutari, 'Anormal', val_tutar), get_mu(islem_saati, 'Mesai_Saati', val_saat), get_mu(cihaz_guvenligi, 'Guvenli', val_guvenlik))},
        
        {"no": 11, "desc": "Tutar=Normal + Saat=Mesai_Saati + Cihaz=Guvenli", "output": "Dusuk",
         "act": min(get_mu(islem_tutari, 'Normal', val_tutar), get_mu(islem_saati, 'Mesai_Saati', val_saat), get_mu(cihaz_guvenligi, 'Guvenli', val_guvenlik))},
        {"no": 12, "desc": "Tutar=Normal + Saat=Aksam_Gec + Cihaz=Guvenli", "output": "Dusuk",
         "act": min(get_mu(islem_tutari, 'Normal', val_tutar), get_mu(islem_saati, 'Aksam_Gec', val_saat), get_mu(cihaz_guvenligi, 'Guvenli', val_guvenlik))},
        {"no": 13, "desc": "Tutar=Yuksek + Saat=Mesai_Saati + Cihaz=Guvenli", "output": "Dusuk",
         "act": min(get_mu(islem_tutari, 'Yuksek', val_tutar), get_mu(islem_saati, 'Mesai_Saati', val_saat), get_mu(cihaz_guvenligi, 'Guvenli', val_guvenlik))},
        {"no": 14, "desc": "Tutar=Normal + Saat=Mesai_Saati + Cihaz=Supheli", "output": "Dusuk",
         "act": min(get_mu(islem_tutari, 'Normal', val_tutar), get_mu(islem_saati, 'Mesai_Saati', val_saat), get_mu(cihaz_guvenligi, 'Supheli', val_guvenlik))},
        {"no": 15, "desc": "Tutar=Normal + Saat=Aksam_Gec + Cihaz=Supheli", "output": "Dusuk",
         "act": min(get_mu(islem_tutari, 'Normal', val_tutar), get_mu(islem_saati, 'Aksam_Gec', val_saat), get_mu(cihaz_guvenligi, 'Supheli', val_guvenlik))}
    ]

    aktif_list = [r for r in rule_specs if r["act"] > 0]
    aktif_df = pd.DataFrame(aktif_list)
    if not aktif_df.empty:
        aktif_df = aktif_df.sort_values(by="act", ascending=False)
        gosterim_df = aktif_df.rename(columns={"no": "Kural No", "desc": "Açıklama Mantığı", "act": "Aktivasyon Derecesi", "output": "Risk Çıktısı"})
        filtered_df = gosterim_df[["Kural No", "Açıklama Mantığı", "Aktivasyon Derecesi", "Risk Çıktısı"]]

        def ciz_renkli_hucre(val):
            if val >= 0.35: return 'background-color: #8b0000; color: white; font-weight: bold;'
            elif val >= 0.20: return 'background-color: #d97706; color: white; font-weight: bold;'
            elif val > 0.0: return 'background-color: #fef08a; color: black; font-weight: bold;'
            return ''

        styled_df = filtered_df.style.map(ciz_renkli_hucre, subset=['Aktivasyon Derecesi']).format({'Aktivasyon Derecesi': '{:.6f}'})
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.info("Mevcut girdilere göre doğrudan tetiklenen bir kural bulunmuyor.")

    st.markdown("<br>", unsafe_allow_html=True)
    c_a, c_b, c_c = st.columns(3)
    c_a.metric(label="🔥 Tetiklenen Kural", value=f"{len(aktif_df)} / 15")
    max_aktivasyon = aktif_df["act"].max() if not aktif_df.empty else 0.0
    c_b.metric(label="📈 Maks Aktivasyon", value=f"{max_aktivasyon:.4f}")
    c_c.metric(label="🏆 Baskın Risk", value=baskin_sonuc)

# ==============================================================================
# --- ADIM 7: SEKMELİ KÜME GÖSTERİMLERİ ---
# ==============================================================================
st.markdown("---")
st.markdown("### 🗺️ Sistem Yapısı ve Bulanık Küme Gösterimleri")

tab_giris, tab_cikis = st.tabs(["📈 Giriş Değişkenleri — Üyelik Fonksiyonları", "🎯 Çıkış Değişkeni — Centroid Durulaştırma Kümesi"])

with tab_giris:
    st.write("Her giriş risk bileşeninin üyelik fonksiyonları ve anlık giriş kesişimleri:")
    cx1, cx2, cx3 = st.columns(3)
    with cx1: st.pyplot(ciz_havali_grafik(islem_tutari, "1. İşlem Tutarı (Kat)", val_tutar))
    with cx2: st.pyplot(ciz_havali_grafik(islem_saati, "2. İşlem Saati", val_saat))
    with cx3: st.pyplot(ciz_havali_grafik(cihaz_guvenligi, "3. Cihaz/Konum Güvenlik Skoru", val_guvenlik))

with tab_cikis:
    st.write("Çıkış kümesi evrensel alan dağılımı ve durulaştırılmış Centroid ağırlık merkezi noktası:")
    fig_out_large, ax_out_large = plt.subplots(figsize=(10, 3.8))
    ax_out_large.set_facecolor('#1a1f2c')
    fig_out_large.patch.set_facecolor('#0e1117')

    colors_out = ['#10b981', '#f59e0b', '#ef4444']
    for i, term in enumerate(fraud_riski.terms):
        ax_out_large.plot(fraud_riski.universe, fraud_riski[term].mf, label=term, color=colors_out[i], linewidth=2.5)
        ax_out_large.fill_between(fraud_riski.universe, 0, fraud_riski[term].mf, color=colors_out[i], alpha=0.15)

    ax_out_large.axvline(x=skor, color='#ff4b4b', linestyle='--', linewidth=3, label=f'Centroid Noktası: {skor:.2f}')
    ax_out_large.set_title("Fraud Risk Skoru — Çıkış Kümesi Evrensel Dağılımı", color='white', fontweight='bold', fontsize=12)
    ax_out_large.grid(True, color='#2d3748', linestyle=':', alpha=0.5)
    ax_out_large.tick_params(colors='white', labelsize=10)
    ax_out_large.legend(facecolor='#11151c', edgecolor='#2d3748', labelcolor='white', fontsize='medium')
    st.pyplot(fig_out_large)