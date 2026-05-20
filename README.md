 Bulanık Mantık Tabanlı Fraud (Dolandırıcılık) Tespit.

[![Python Sürümü](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Arayüz-Streamlit--Gelişmiş-FF4B4B.svg)](https://streamlit.io/)
[![Skfuzzy](https://img.shields.io/badge/Motor-Scikit--Fuzzy-orange.svg)](https://pythonhosted.org/scikit-fuzzy/)

Bu proje, geleneksel bankacılık sistemlerindeki katı kurallar yerine, insan muhakemesine ve esnek karar verme yeteneğine benzeyen **Bulanık Mantık (Fuzzy Logic)** teorisini kullanarak finansal işlemlerdeki dolandırıcılık (fraud) riskini gerçek zamanlı analiz eden akademik düzeyde bir karar destek sistemidir.
<img width="1919" height="906" alt="Ekran görüntüsü 2026-05-20 220630" src="https://github.com/user-attachments/assets/81d04ee2-4d98-418b-a480-84f703a0b2c8" />
<img width="1919" height="907" alt="Ekran görüntüsü 2026-05-20 220622" src="https://github.com/user-attachments/assets/ef83606e-7717-4942-a8ea-9109b8d259d7" />

---

 Bulanık Mantık Motoru Sistem Mimarisi

Sistem, yapay zekanın en güçlü çıkarım modellerinden biri olan **Mamdani Bulanık Çıkarım Modeli** üzerine inşa edilmiştir. Kullanıcı panellerden girdileri değiştirdiğinde arka planda şu 5 aşamalı süreç reaktif olarak tetiklenir:

 Girdi Değişkenleri 
1. **İşlem Tutarı (0 - 10 Kat): Müşterinin geçmiş harcama alışkanlıklarına oranla anlık harcama büyüklüğü. *(Normal, Yüksek, Anormal)*
2. **İşlem Saati (00:00 - 24:00): İşlemin yapıldığı zaman dilimi. *(Gece Yarısı, Mesai Saati, Akşam Geç)*
3. **Cihaz/Konum Güvenlik Skoru (%0 - %100): Kullanılan cihazın tanınırlığı, VPN durumu ve konum doğruluğu. *(Tehlikeli, Şüpheli, Güvenli)*

 Çıktı Değişkeni 
Fraud Risk Oranı (%0 - %100): İşlemin dolandırıcılık olasılığını gösteren nihai skor. Matematiksel hesaplamada **Centroid (Ağırlık Merkezi)** durulaştırma metodu kullanılmıştır.

---

 15 Akademik Finansal Güvenlik Kuralı

Sistem, finans dünyasındaki risk senaryolarını kapsayan tam 15 adet kural kombinasyonunu eş zamanlı olarak denetler...

* **Kural 1-5 (Yüksek Risk): Anormal tutarların gece yarısı yapılması veya tehlikeli cihazlardan denenmesi durumunda doğrudan sistemi bloke eder.
* **Kural 6-10 (Orta Risk): Şüpheli durumları tespit ederek işleme SMS/MFA onayı şartı getirir.
* **Kural 11-15 (Düşük Risk): Güvenli cihazlardan mesai saatlerinde yapılan normal harcamalara anında onay verir.

<img width="591" height="306" alt="Risk1" src="https://github.com/user-attachments/assets/0de3c9d5-4cbf-4780-a274-6521e728ba0c" />
<img width="590" height="312" alt="Risk2" src="https://github.com/user-attachments/assets/535f1f5a-38c2-4c39-86d4-478fd5104830" />
<img width="589" height="313" alt="Risk3" src="https://github.com/user-attachments/assets/4ea73acd-bae0-4749-b368-a49e992adaa8" />


---

 Kurulum ve Yerel Çalıştırma

Projeyi bilgisayarınızda sorunsuzca ayağa kaldırmak için aşağıdaki adımları uygulayınız:

 1. Depoyu Klonlayın veya İndirin
```bash
git clone [https://github.com/BarkinGulgeci/dolandiricilik-testi-py.git](https://github.com/BarkinGulgeci/dolandiricilik-testi-py.git)
cd dolandiricilik-testi-py

C:\Users\*Bilgisayar Kullanıcı Adınız\AppData\Local\Programs\Python\Python312\python.exe -m pip install -r requirements.txt
C:\Users\*Bilgisayar Kullanıcı Adınız\AppData\Local\Programs\Python\Python312\python.exe -m streamlit run fraud_testi.py
