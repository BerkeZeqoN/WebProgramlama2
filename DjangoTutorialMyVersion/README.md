# Django Polls Uygulaması (Gelişmiş Versiyon)

Bu proje, standart Django eğitim projesinin baştan sona genişletilerek premium özelliklerle donatılmış gelişmiş bir anket uygulamasıdır. İçerisinde yetkilendirme, gelişmiş anket filtreleri, modern arayüz (UI) iyileştirmeleri, yorum sistemi ve kullanıcı profil özellikleri bulunmaktadır.

## Yeni Eklenen Özellikler

1. **Gelişmiş Görsel Anket Sonuçları:**
   Sonuç ekranında her anket seçeneğinin aldığı oy oranı yüzdelik değerleri CSS barları (progress bar) yardımıyla dinamik olarak gösterilir.
2. **Taslak Modu (Draft):**
   Anketler `is_published` özelliğine sahiptir. `is_published=False` olan yöneticilerin taslak anketleri listelerde gösterilmez.
3. **Trend/Popüler Anketler:**
   Ana ekranda en çok oy alan 3 uygulamanın yer aldığı özel bir "Günün Popüler Anketleri" vitrini sunulmaktadır.
4. **Anket Fotoğrafları:**
   Anketlere görsel içerik zenginliği katmak için `image_url` sistemi kullanılarak fotoğraf ekleme şansı verilmiştir. Olası kütüphane kısıtlamalarına karşı URL kullanılmıştır.
5. **Kullanıcı Profil Resmi (Avatar):**
   Kullanıcıların profil ekranında avatar kullanması desteklenmiştir. `UserProfile` modeli sayesinde kullanıcı fotoğraf linkleri alınır ve sunulur.
6. **Kapsamlı Yorum & Kategori Sistemi:**
   Anketler için kategori belirlenebilir ve detay sayfasında yorum yapılabilir.

## Kurulum ve Çalıştırma

Projeyi bilgisayarınızda kurmak ve çalıştırmak için aşağıdaki komutları sırasıyla terminalinizde çalıştırabilirsiniz:

1. **Sanallaştırma Kurulumu (İsteğe Bağlı):**
   ```bash
   python -m venv env
   env\Scripts\activate  # Windows için
   ```

2. **Gerekli Paketler:**
   Proje dahili Django standartlarını kullanır, fazladan kütüphane gerekmez. (Django'nun yüklü olması yeterlidir).
   ```bash
   pip install django
   ```

3. **Veritabanı Hazırlıkları:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Süper Kullanıcı (Admin) Oluşturma:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Sunucuyu Başlatma:**
   ```bash
   python manage.py runserver
   ```
   Kurulum tamamlandıktan sonra tarayıcınızdan `http://127.0.0.1:8000/polls/` adresine giderek uygulamayı inceleyebilir veya `/admin/` adresinden yönetim paneline erişebilirsiniz.

## Testler

Proje üzerinde yapılan değişikliklerin veritabanı kurgusunu ve sayfa görünümlerini bozmadığının doğrulanabilmesi adına tüm temel unit-test işlemleri sağlanmıştır. Çalıştırmak için:
```bash
python manage.py test polls
```
