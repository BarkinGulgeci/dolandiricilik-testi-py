 Bulanık Mantık Tabanlı Fraud (Dolandırıcılık) Tespit.

[![Python Sürümü](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Arayüz-Streamlit--Gelişmiş-FF4B4B.svg)](https://streamlit.io/)
[![Skfuzzy](https://img.shields.io/badge/Motor-Scikit--Fuzzy-orange.svg)](https://pythonhosted.org/scikit-fuzzy/)

Bu proje, geleneksel bankacılık sistemlerindeki katı kurallar yerine, insan muhakemesine ve esnek karar verme yeteneğine benzeyen **Bulanık Mantık (Fuzzy Logic)** teorisini kullanarak finansal işlemlerdeki dolandırıcılık (fraud) riskini gerçek zamanlı analiz eden akademik düzeyde bir karar destek sistemidir.

[1. GİRİŞLER] ➔ [2. BULANIKLAŞTIRMA] ➔ [3. ÇIKARIM MOTORU] ➔ [4. DURULAŞTIRMA] ➔ [5. SİSTEM ÇIKTISI]
Tutar, Saat,      Üyelik Fonksiyonları     15 Akademik Kural      Ağırlık Merkezi         Fraud Risk Skoru %
Güvenlik Skoru      (trimf / trapmf)         Mamdani (min)           (Centroid)          (Canlı Aksiyon Kararı)

<img width="1919" height="906" alt="Ekran görüntüsü 2026-05-20 220630" src="https://github.com/user-attachments/assets/81d04ee2-4d98-418b-a480-84f703a0b2c8" />
<img width="1919" height="907" alt="Ekran görüntüsü 2026-05-20 220622" src="https://github.com/user-attachments/assets/ef83606e-7717-4942-a8ea-9109b8d259d7" />

---

 Bulanık Mantık Motoru Sistem Mimarisi

Sistem, yapay zekanın en güçlü çıkarım modellerinden biri olan **Mamdani Bulanık Çıkarım Modeli** üzerine inşa edilmiştir. Kullanıcı panellerden girdileri değiştirdiğinde arka planda şu 5 aşamalı süreç reaktif olarak tetiklenir:

  1. Girdi Değişkenlerinin Analitiği (Antecedents)
Sistem, finans dünyasında siber güvenliğin "Altın Üçgeni" olarak kabul edilen 3 temel metrik üzerinden eş zamanlı girdi kabul etmektedir:

 A. İşlem Tutarı ($x_1 \in [0, 10]$)
Kart sahibinin geçmişe dönük harcama profili, lokasyon geçmişi ve sepet ortalamasının bir taban matrisi çıkarılmıştır. Gelen anlık harcama, bu ortalamanın kaç katı olduğuna göre `[0, 10]` aralığında ölçeklenir.
* **Normal Üyelik Fonksiyonu:** Yamuk küme $trap(0, 0, 2, 4)$. Müşterinin alışılagelmiş harcama limitlerini temsil eder.
* **Yüksek Üyelik Fonksiyonu:** Üçgen küme $tri(2, 5, 8)$. Alışveriş sepetindeki ani büyümeleri veya yüksek segmentli harcamaları gösterir.
* **Anormal Üyelik Fonksiyonu:** Yamuk küme $trap(6, 8, 10, 10)$. Kart limitlerinin aniden sonuna kadar zorlandığı durumları niteler.

 B. İşlem Saati ($x_2 \in [0, 24]$)
İşlemin günün hangi zaman diliminde (24 saatlik formatta) gerçekleştiğini denetler. Zaman dilimleri arasındaki geçişler katı saat sınırlarıyla değil, birbirinin içine geçen üyelik dereceleriyle tasarlanmıştır.
* **Gece Yarısı Üyelik Fonksiyonu:** Yamuk küme $trap(0, 0, 4, 7)$ ve $trap(21, 24, 24, 24)$. İstatistiki olarak fraud vakalarının en yoğun kümelendiği zaman dilimidir.
* **Mesai Saati Üyelik Fonksiyonu:** Yamuk küme $trap(6, 9, 17, 19)$. Standart insani harcama alışkanlıklarının zirve yaptığı güvenli bölgedir.
* **Akşam Geç Üyelik Fonksiyonu:** Üçgen küme $tri(16, 20, 22)$. Eğlence, sosyal aktiviteler veya gün sonu e-ticaret işlemlerini kapsar.

 C. Cihaz/Konum Güvenlik Skoru ($x_3 \in [0, 100]$)
İşlemin yapıldığı cihazın dijital parmak izini (Browser Fingerprint), daha önce bu kartla giriş yapılıp yapılmadığını, proxy/VPN kullanım durumunu ve IP adresi ile kartın kayıtlı olduğu lokasyon arasındaki coğrafi mesafeyi `%0 ile %100` arasında puanlar.
* **Tehlikeli Üyelik Fonksiyonu:** Yamuk küme $trap(0, 0, 20, 40)$. Bilinmeyen cihazlar, uzak ülkelerden gelen IP'ler, aktif VPN/Tor ağları.
* **Şüpheli Üyelik Fonksiyonu:** Üçgen küme $tri(30, 50, 70)$. Tanınan cihaz ancak alışılmamış tarayıcı güncellemeleri veya sınırda coğrafi konum değişimleri.
* **Güvenli Üyelik Fonksiyonu:** Yamuk küme $trap(60, 80, 100, 100)$. Kart sahibinin her gün kullandığı ev/iş yeri ağı ve kayıtlı mobil cihazı.

 2. Çıktı Değişkeni ve Aksiyon Sınırları (Consequent)
* **Fraud Risk Oranı ($y \in [0, 100]$):** İşlemin dolandırıcılık olasılığını belirten nihai matematiksel skordur.
  * **Dusuk Risk:** $trap(0, 0, 20, 40)$ ➔ İşlem sorunsuz onaylanır.
  * **Orta Risk:** $tri(30, 50, 70)$ ➔ İşlem beklemeye alınır, SMS veya Biyometrik Doğrulama (MFA) tetiklenir.
  * **Yuksek Risk:** $trap(60, 80, 100, 100)$ ➔ İşlem anında bloke edilir ve güvenlik operasyon merkezine (SOC) alarm düşer.

---

 Matematiksel ve Geometrik Modelleme

 Üyelik Fonksiyonlarının Geometrik Açılımı
Sistemdeki bulanık kümelerin sınır geçişlerinde doğrusal pürüzsüzlüğü sağlamak için matematiksel olarak aşağıdaki denklemler işletilir:

1. Üçgen Üyelik Fonksiyonu Açılımı:**
   $$\mu_A(x) = \begin{cases} 
   0, & x \le a \\
   \frac{x-a}{b-a}, & a < x \le b \\
   \frac{c-x}{c-b}, & b < x < c \\
   0, & x \ge c 
   \end{cases}$$

2. Yamuk Üyelik Fonksiyonu Açılımı:**
   $$\mu_A(x) = \begin{cases} 
   0, & x \le a \\
   \frac{x-a}{b-a}, & a < x \le b \\
   1, & b < x \le c \\
   \frac{d-x}{d-c}, & c < x < d \\
   0, & x \ge d 
   \end{cases}$$

 Durulaştırma (Defuzzification) Hesaplaması
Kural tabanından gelen ve aktifleşen bulanık alanların geometrik birleşimi, sayısal bir risk değerine dönüştürülürken **Centroid (Ağırlık Merkezi) yöntemi kullanılır. Ayrık evrenler üzerinde bu işlem şu formülle gerçekleştirilir.

---

 15 Gelişmiş Finansal Siber Güvenlik Kural Tabanı

Çıkarım motorumuz, finansal literatürdeki dolandırıcılık paternleri analiz edilerek yapılandırılmış **15 adet gelişmiş kuralı** eş zamanlı olarak tarar. Kurallardaki `VE` (AND) bağlaçları için 

<img width="942" height="387" alt="Senaryolar3" src="https://github.com/user-attachments/assets/927a6ad7-5381-4dd0-b628-e22cfaa1860a" />
<img width="962" height="416" alt="Senaryolar 2" src="https://github.com/user-attachments/assets/51f1bd22-14ec-4451-b920-357bd83ab889" />
<img width="946" height="377" alt="Senaryolar1" src="https://github.com/user-attachments/assets/12b18a6b-521c-4e52-b42f-8ec8f1c526f2" />


| Kural No | İşlem Tutarı | İşlem Saati | Cihaz Güvenliği | Karar Çıktısı (Risk) |

| Kural 1 | Anormal | Gece Yarısı | — | YÜKSEK (Anında Bloke)** |
| Kural 2 | Anormal | — | Tehlikeli | YÜKSEK (Anında Bloke)** |
| Kural 3 | — | Gece Yarısı | Tehlikeli | ÜKSEK (Anında Bloke)** |
| Kural 4 | Yüksek | Gece Yarısı | Şüpheli | YÜKSEK (Anında Bloke)** |
| Kural 5 | Anormal | Akşam Geç | Tehlikeli | YÜKSEK (Anında Bloke)** |
| Kural 6 | Yüksek | Mesai Saati | Şüpheli | ORTA (MFA / SMS Tetikle)** |
| Kural 7 | Normal | Gece Yarısı | Şüpheli | ORTA (MFA / SMS Tetikle)** |
| Kural 8 | Yüksek | Akşam Geç | Güvenli | ORTA (MFA / SMS Tetikle)** |
| Kural 9 | Normal | Mesai Saati | Tehlikeli | ORTA (MFA / SMS Tetikle)** |
| Kural 10| Anormal | Mesai Saati | Güvenli | ORTA (MFA / SMS Tetikle)** |
| Kural 11| Normal | Mesai Saati | Güvenli | DÜŞÜK (Doğrudan Onay)** |
| Kural 12| Normal | Akşam Geç | Güvenli | DÜŞÜK (Doğrudan Onay)** |
| Kural 13| Yüksek | Mesai Saati | Güvenli | DÜŞÜK (Doğrudan Onay)** |
| Kural 14| Normal | Mesai Saati | Şüpheli | DÜŞÜK (Doğrudan Onay)** |
| Kural 15| Normal | Akşam Geç | Şüpheli | DÜŞÜK (Doğrudan Onay)** |

---

 Reaktif Streamlit Kullanıcı Arayüzü Mimarisi

Uygulamanın arayüzü, akademik teorinin canlı ortamda test edilebilmesi amacıyla Python tabanlı **Streamlit** reaktif framework'ü kullanılarak tasarlanmıştır.

 Öne Çıkan Gelişmiş Arayüz Özellikleri:
1. Gerçek Zamanlı Risk İndikatörleri:** Girdi slider'ları hareket ettirildiği anda arka plandaki matematik motoru tetiklenir ve risk kartının rengi yeşilden sarıya, sarıdan kırmızıya dinamik olarak dönüşür.
2. Ateşlenen Kurallar Isı Haritası (Rule Matrix):** İşlem esnasında 15 kuraldan hangilerinin aktif olduğunu, hangi kuralın karar mekanizmasına yüzde kaçlık bir üyelik derecesiyle (alpha cut) etki ettiğini şeffaf bir reaktif tablo ile doğrular.
3. Grafiksel Bulanık Alan Analizi:** `scikit-fuzzy` ve `matplotlib` entegrasyonu sayesinde, durulaştırma aşamasındaki ağırlık merkezinin geometrik alanı ve kesim noktaları grafik üzerinde canlı olarak çizdirilir.

---

  Derinlemesine Simülasyon ve Validasyon Senaryoları

  Senaryo 1: Standart ve Güvenli Harcama (Sistem Doğrulaması)
 Girdi Seti:** Tutar = 1.2 Kat (Normal), Saat = 13.0 (Mesai Saati), Cihaz Güvenliği = %95 (Güvenli)
 Arka Plan Çıkarımı:** Kural 11 tam güçle ($\mu = 1.0$) ateşlenir. Diğer riskli kuralların üyelik dereceleri sıfıra pürüzsüzce indirgenir.
 Matematiksel Çıktı:** **%18 - %22 Fraud Riski** ➔ `Aksiyon: Onaylandı.` Müşteriye hiçbir engel çıkarılmadan pürüzsüz bir ödeme deneyimi sunulur.

  Senaryo 2: Gece Alışverişi ve Şüpheli Cihaz (Gri Alan Analizi)
 Girdi Seti:** Tutar = 4.5 Kat (Yüksek), Saat = 23.5 (Gece Yarısı), Cihaz Güvenliği = %50 (Şüpheli)
 Arka Plan Çıkarımı:** Sistem bu noktada ne tam güvenli ne de tam dolandırıcılık kararı verir. Kural 4, 7 ve 8 kısmi üyelik dereceleriyle aktifleşir. Centroid (ağırlık merkezi) grafiğin tam orta dilimine ($z^* = 50$) konumlanır.
 Matematiksel Çıktı:** **%50.0 Fraud Riski** ➔ `Aksiyon: MFA / 3D Secure Tetiklendi.` Kart tamamen engellenmez, müşteriye anlık SMS şifresi gönderilerek gri alan güvenle eritilir.

  Senaryo 3: Organize Fraud Tehdidi (Maksimum Tehdit Altında Reaksiyon)
 Girdi Seti:** Tutar = 9.5 Kat (Anormal), Saat = 03.15 (Gece Yarısı), Cihaz Güvenliği = %10 (Tehlikeli)
 Arka Plan Çıkarımı:** En kritik siber güvenlik kuralları olan Kural 1, Kural 2 ve Kural 3 maksimum üyelik dereceleriyle ($\mu = 1.0$) çıkarım motorunu domine eder. Bulanık küme alanı tamamen sağ taraftaki yamuk kümede kilitlenir.
 Matematiksel Çıktı:** **%84 - %89+ Fraud Riski** ➔ `Aksiyon: İşlem Bloke Edildi & Hesap Askıya Alındı.` Karttan para çıkışı saniyeler içinde engellenir.

---

 Yerel Kurulum ve Çalıştırma Kılavuzu

Sistemi bilgisayarınızda veya sunucunuzda çalıştırmak için aşağıdaki adımları takip edin:

 1. Depoyu Bilgisayarınıza Klonlayın
```bash
git clone [https://github.com/KullaniciAdiniz/fraud-detection-fuzzy-engine.git](https://github.com/KullaniciAdiniz/fraud-detection-fuzzy-engine.git)
cd fraud-detection-fuzzy-engine
cd dolandiricilik-testi-py

C:\Users\*Bilgisayar Kullanıcı Adınız\AppData\Local\Programs\Python\Python312\python.exe -m pip install -r requirements.txt
C:\Users\*Bilgisayar Kullanıcı Adınız\AppData\Local\Programs\Python\Python312\python.exe -m streamlit run fraud_testi.py
