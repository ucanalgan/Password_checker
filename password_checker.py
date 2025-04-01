import re
import math
from colorama import init, Fore, Style
from collections import Counter
from datetime import timedelta

# Colorama'yı başlat
init()

# Sabitler
ATTEMPTS_PER_SECOND = 1_000_000_000  # Saniyede 1 milyar deneme

# Yaygın parolalar listesi
COMMON_PASSWORDS = {
    # En yaygın parolalar
    "password", "123456", "12345678", "qwerty", "abc123", "monkey", "letmein", "dragon", "111111", "baseball",
    "iloveyou", "trustno1", "sunshine", "master", "welcome", "shadow", "ashley", "football", "jesus", "michael",
    "ninja", "mustang", "password1", "123456789", "1234567", "12345", "1234", "superman", "qwertyuiop", "121212",
    
    # Türkçe yaygın parolalar
    "şifre123", "123456789", "parola123", "istanbul", "ankara", "izmir", "türkiye", "atatürk", "fenerbahçe",
    "galatasaray", "beşiktaş", "trabzonspor", "merhaba", "hoşgeldin", "admin123", "sifre123", "parola123",
    
    # Klavye düzeni parolaları
    "qwerty123", "asdfgh", "zxcvbn", "qwertyuiop", "asdfghjkl", "zxcvbnm", "1qaz2wsx", "qwertyuiopasdfghjkl",
    
    # Yaygın isimler ve yıllar
    "ahmet123", "mehmet123", "ayşe123", "fatma123", "ali123", "can123", "deniz123", "emre123", "1990", "1991",
    "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004",
    
    # Yaygın kelimeler ve sayılar
    "admin", "administrator", "root", "toor", "test", "demo", "guest", "user", "pass", "pass123", "password123",
    "1234567890", "11111111", "22222222", "33333333", "44444444", "55555555", "66666666", "77777777", "88888888",
    "99999999", "00000000"
}

def calculate_entropy(password):
    """Parolanın Shannon Entropy değerini hesaplar."""
    if not password:
        return 0
    
    # Karakter frekanslarını hesapla
    char_freq = Counter(password)
    length = len(password)
    
    # Her karakter için olasılık hesapla
    probabilities = [count/length for count in char_freq.values()]
    
    # Shannon Entropy hesapla: -Σ p(x) * log2(p(x))
    entropy = -sum(p * math.log2(p) for p in probabilities)
    
    return entropy

def calculate_possible_combinations(password):
    """Parolanın olası kombinasyon sayısını hesaplar."""
    # Karakter setlerini belirle
    lowercase = bool(re.search(r'[a-z]', password))
    uppercase = bool(re.search(r'[A-Z]', password))
    numbers = bool(re.search(r'\d', password))
    special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    # Karakter seti boyutunu hesapla
    charset_size = 0
    if lowercase: charset_size += 26
    if uppercase: charset_size += 26
    if numbers: charset_size += 10
    if special: charset_size += 32
    
    # Eğer hiçbir karakter seti yoksa, minimum karakter seti boyutunu kullan
    if charset_size == 0:
        charset_size = 26  # Sadece küçük harfler
    
    # Olası kombinasyon sayısını hesapla: n^l
    length = len(password)
    combinations = charset_size ** length
    
    return combinations

def calculate_crack_time(combinations):
    """Parolanın kırılma süresini hesaplar."""
    # Ortalama olarak parolanın yarısında bulunacağını varsay
    attempts_needed = combinations / 2
    
    # Saniye cinsinden süre
    seconds = attempts_needed / ATTEMPTS_PER_SECOND
    
    # Süreyi daha anlaşılır formata çevir
    if seconds < 60:
        return f"{seconds:.1f} saniye"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} dakika"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f} saat"
    elif seconds < 31536000:
        days = seconds / 86400
        return f"{days:.1f} gün"
    else:
        years = seconds / 31536000
        return f"{years:.1f} yıl"

def check_password_strength(password):
    # Başlangıç puanı
    score = 0
    feedback = []

    # Uzunluk kontrolü
    if len(password) < 8:
        feedback.append(f"{Fore.RED}Parola çok kısa! En az 8 karakter olmalı.{Style.RESET_ALL}")
    else:
        score += 1
        if len(password) >= 12:
            score += 1
            feedback.append(f"{Fore.GREEN}Parola uzunluğu iyi! (+2 puan){Style.RESET_ALL}")

    # Büyük harf kontrolü
    if re.search(r"[A-Z]", password):
        score += 1
        feedback.append(f"{Fore.GREEN}Büyük harf içeriyor! (+1 puan){Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.YELLOW}Büyük harf kullanmanız önerilir.{Style.RESET_ALL}")

    # Küçük harf kontrolü
    if re.search(r"[a-z]", password):
        score += 1
        feedback.append(f"{Fore.GREEN}Küçük harf içeriyor! (+1 puan){Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.YELLOW}Küçük harf kullanmanız önerilir.{Style.RESET_ALL}")

    # Rakam kontrolü
    if re.search(r"\d", password):
        score += 1
        feedback.append(f"{Fore.GREEN}Rakam içeriyor! (+1 puan){Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.YELLOW}Rakam kullanmanız önerilir.{Style.RESET_ALL}")

    # Özel karakter kontrolü
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
        feedback.append(f"{Fore.GREEN}Özel karakter içeriyor! (+1 puan){Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.YELLOW}Özel karakter kullanmanız önerilir.{Style.RESET_ALL}")

    # Yaygın parola kontrolü
    if password.lower() in COMMON_PASSWORDS:
        score = 0
        feedback.append(f"{Fore.RED}Bu çok yaygın bir parola! Güvenli değil.{Style.RESET_ALL}")
    else:
        # Parolanın yaygın parolalara benzerliğini kontrol et
        for common in COMMON_PASSWORDS:
            if common in password.lower() or password.lower() in common:
                score -= 1
                feedback.append(f"{Fore.YELLOW}Parolanız yaygın bir parolaya çok benziyor. Daha benzersiz bir parola seçin.{Style.RESET_ALL}")
                break

    # Entropy hesaplama
    entropy = calculate_entropy(password)
    combinations = calculate_possible_combinations(password)
    
    # Entropy değerlendirmesi
    if entropy < 2:
        feedback.append(f"{Fore.RED}Entropy değeri çok düşük! ({entropy:.2f}) Parola tahmin edilebilir.{Style.RESET_ALL}")
    elif entropy < 3:
        feedback.append(f"{Fore.YELLOW}Entropy değeri orta. ({entropy:.2f}) Parola biraz tahmin edilebilir.{Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.GREEN}Entropy değeri iyi! ({entropy:.2f}) Parola tahmin edilmesi zor.{Style.RESET_ALL}")
    
    # Olası kombinasyon sayısı değerlendirmesi
    if combinations < 1000000:
        feedback.append(f"{Fore.RED}Olası kombinasyon sayısı çok düşük! ({combinations:,}){Style.RESET_ALL}")
    elif combinations < 100000000:
        feedback.append(f"{Fore.YELLOW}Olası kombinasyon sayısı orta. ({combinations:,}){Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.GREEN}Olası kombinasyon sayısı yüksek! ({combinations:,}){Style.RESET_ALL}")

    # Kırma süresi hesaplama
    crack_time = calculate_crack_time(combinations)
    if "saniye" in crack_time or "dakika" in crack_time:
        feedback.append(f"{Fore.RED}Tahmini kırma süresi: {crack_time} (Çok zayıf!){Style.RESET_ALL}")
    elif "saat" in crack_time:
        feedback.append(f"{Fore.YELLOW}Tahmini kırma süresi: {crack_time} (Orta){Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.GREEN}Tahmini kırma süresi: {crack_time} (Güçlü){Style.RESET_ALL}")

    # Sonuç değerlendirmesi
    if score <= 2:
        strength = f"{Fore.RED}Zayıf{Style.RESET_ALL}"
    elif score <= 4:
        strength = f"{Fore.YELLOW}Orta{Style.RESET_ALL}"
    else:
        strength = f"{Fore.GREEN}Güçlü{Style.RESET_ALL}"

    return strength, score, feedback

def main():
    print(f"{Fore.CYAN}=== Parola Güvenlik Kontrolü ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Not: Bu araç {len(COMMON_PASSWORDS)} yaygın parola ile karşılaştırma yapar.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Entropy, olası kombinasyon sayısı ve kırma süresi hesaplanır.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Tahmin: Saniyede {ATTEMPTS_PER_SECOND:,} deneme yapan bir makine için.{Style.RESET_ALL}")
    while True:
        password = input("\nKontrol etmek istediğiniz parolayı girin (çıkmak için 'q'): ")
        if password.lower() == 'q':
            break

        strength, score, feedback = check_password_strength(password)
        print(f"\nParola Gücü: {strength} (Puan: {score}/6)")
        print("\nDetaylı Geri Bildirim:")
        for msg in feedback:
            print(msg)

if __name__ == "__main__":
    main() 