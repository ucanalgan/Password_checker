# Parola Güvenlik Kontrolü

Bu araç, girilen parolanın güvenlik seviyesini değerlendirir ve detaylı geri bildirim sağlar.

## Özellikler

- Parola uzunluğu kontrolü
- Büyük/küçük harf kullanımı kontrolü
- Rakam kullanımı kontrolü
- Özel karakter kullanımı kontrolü
- Yaygın parola kontrolü
- Renkli ve detaylı geri bildirim

## Kurulum

1. Gerekli paketleri yükleyin:
```powershell
pip install -r requirements.txt
```

2. Programı çalıştırın:
```powershell
python password_checker.py
```

## Kullanım

1. Programı başlattığınızda, kontrol etmek istediğiniz parolayı girin
2. Program parolanızı analiz edip detaylı geri bildirim verecektir
3. Çıkmak için 'q' tuşuna basın

## Puanlama Sistemi

- 0-2 puan: Zayıf
- 3-4 puan: Orta
- 5-6 puan: Güçlü

Her kriter için 1 puan verilir, uzunluk için ekstra 1 puan daha verilir. 