import re
import math
from colorama import init, Fore, Style
from collections import Counter
from datetime import timedelta
from itertools import groupby
import nltk
from nltk.corpus import words

# Colorama'yı başlat
init()

# NLTK kelime listesini indir
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

# Sabitler
ATTEMPTS_PER_SECOND = 1_000_000_000  # Saniyede 1 milyar deneme
MIN_REPEAT_COUNT = 3  # Minimum tekrar sayısı

# Klavye desenleri
KEYBOARD_PATTERNS = [
    # QWERTY sıraları
    r'qwerty',
    r'asdfgh',
    r'zxcvbn',
    r'123456',
    r'qwertyuiop',
    r'asdfghjkl',
    r'zxcvbnm',
    r'qwerty123',
    r'asdfgh123',
    r'zxcvbn123',
    
    # QWERTY çapraz desenler
    r'1qaz',
    r'2wsx',
    r'3edc',
    r'4rfv',
    r'5tgb',
    r'6yhn',
    r'7ujm',
    r'8ik,',
    r'9ol.',
    r'0p;/',
    
    # QWERTY dikey desenler
    r'q1',
    r'w2',
    r'e3',
    r'r4',
    r't5',
    r'y6',
    r'u7',
    r'i8',
    r'o9',
    r'p0',
    
    # Sayı tuşu desenleri
    r'12345',
    r'23456',
    r'34567',
    r'45678',
    r'56789',
    r'67890',
    
    # Alfabetik sıralar
    r'abcdef',
    r'bcdefg',
    r'cdefgh',
    r'defghi',
    r'efghij',
    r'fghijk',
    r'ghijkl',
    r'hijklm',
    r'ijklmn',
    r'jklmno',
    r'klmnop',
    r'lmno',
    r'mnop',
    r'nopq',
    r'opqr',
    r'pqrs',
    r'qrst',
    r'rstu',
    r'stuv',
    r'tuvw',
    r'uvwx',
    r'vwxy',
    r'wxyz'
]

# Dil sözlükleri
LANGUAGES = {
    'tr': {
        'title': '=== Parola Güvenlik Kontrolü ===',
        'note_common': 'Not: Bu araç {} yaygın parola ile karşılaştırma yapar.',
        'note_metrics': 'Entropy, olası kombinasyon sayısı ve kırma süresi hesaplanır.',
        'note_attempts': 'Tahmin: Saniyede {} deneme yapan bir makine için.',
        'input_prompt': 'Kontrol etmek istediğiniz parolayı girin (çıkmak için \'q\'): ',
        'password_strength': 'Parola Gücü: {} (Puan: {}/6)',
        'feedback_title': 'Detaylı Geri Bildirim:',
        'too_short': 'Parola çok kısa! En az 8 karakter olmalı.',
        'good_length': 'Parola uzunluğu iyi! (+2 puan)',
        'has_uppercase': 'Büyük harf içeriyor! (+1 puan)',
        'needs_uppercase': 'Büyük harf kullanmanız önerilir.',
        'has_lowercase': 'Küçük harf içeriyor! (+1 puan)',
        'needs_lowercase': 'Küçük harf kullanmanız önerilir.',
        'has_number': 'Rakam içeriyor! (+1 puan)',
        'needs_number': 'Rakam kullanmanız önerilir.',
        'has_special': 'Özel karakter içeriyor! (+1 puan)',
        'needs_special': 'Özel karakter kullanmanız önerilir.',
        'common_password': 'Bu çok yaygın bir parola! Güvenli değil.',
        'similar_password': 'Parolanız yaygın bir parolaya çok benziyor. Daha benzersiz bir parola seçin.',
        'low_entropy': 'Entropy değeri çok düşük! ({:.2f}) Parola tahmin edilebilir.',
        'medium_entropy': 'Entropy değeri orta. ({:.2f}) Parola biraz tahmin edilebilir.',
        'high_entropy': 'Entropy değeri iyi! ({:.2f}) Parola tahmin edilmesi zor.',
        'low_combinations': 'Olası kombinasyon sayısı çok düşük! ({:,})',
        'medium_combinations': 'Olası kombinasyon sayısı orta. ({:,})',
        'high_combinations': 'Olası kombinasyon sayısı yüksek! ({:,})',
        'crack_time_weak': 'Tahmini kırma süresi: {} (Çok zayıf!)',
        'crack_time_medium': 'Tahmini kırma süresi: {} (Orta)',
        'crack_time_strong': 'Tahmini kırma süresi: {} (Güçlü)',
        'weak': 'Zayıf',
        'medium': 'Orta',
        'strong': 'Güçlü',
        'seconds': 'saniye',
        'minutes': 'dakika',
        'hours': 'saat',
        'days': 'gün',
        'years': 'yıl',
        'character_repeat': 'Çoklu tekrarlar tahmini kolaylaştırabilir.',
        'character_repeat_detail': '{} karakteri {} kez art arda tekrar ediyor.',
        'keyboard_pattern': 'Klavye düzeni tabanlı parola tespit edildi!',
        'keyboard_pattern_detail': 'Parola şu klavye desenini içeriyor: {}',
        'dictionary_word': 'Gerçek kelime içeriyor!',
        'dictionary_word_detail': 'Tespit edilen kelime: {}',
        'leetspeak_warning': 'Leetspeak kullanılan ama tahmin edilebilir parola!',
        'leetspeak_detail': 'Leetspeak dönüşümü: {} -> {}',
    },
    'en': {
        'title': '=== Password Security Check ===',
        'note_common': 'Note: This tool compares against {} common passwords.',
        'note_metrics': 'Entropy, possible combinations, and crack time are calculated.',
        'note_attempts': 'Estimate: For a machine that attempts {} passwords per second.',
        'input_prompt': 'Enter the password to check (press \'q\' to quit): ',
        'password_strength': 'Password Strength: {} (Score: {}/6)',
        'feedback_title': 'Detailed Feedback:',
        'too_short': 'Password is too short! Must be at least 8 characters.',
        'good_length': 'Password length is good! (+2 points)',
        'has_uppercase': 'Contains uppercase letters! (+1 point)',
        'needs_uppercase': 'Consider using uppercase letters.',
        'has_lowercase': 'Contains lowercase letters! (+1 point)',
        'needs_lowercase': 'Consider using lowercase letters.',
        'has_number': 'Contains numbers! (+1 point)',
        'needs_number': 'Consider using numbers.',
        'has_special': 'Contains special characters! (+1 point)',
        'needs_special': 'Consider using special characters.',
        'common_password': 'This is a very common password! Not secure.',
        'similar_password': 'Your password is very similar to a common password. Choose a more unique one.',
        'low_entropy': 'Entropy value is very low! ({:.2f}) Password is predictable.',
        'medium_entropy': 'Entropy value is medium. ({:.2f}) Password is somewhat predictable.',
        'high_entropy': 'Entropy value is good! ({:.2f}) Password is hard to predict.',
        'low_combinations': 'Possible combinations are very low! ({:,})',
        'medium_combinations': 'Possible combinations are medium. ({:,})',
        'high_combinations': 'Possible combinations are high! ({:,})',
        'crack_time_weak': 'Estimated crack time: {} (Very weak!)',
        'crack_time_medium': 'Estimated crack time: {} (Medium)',
        'crack_time_strong': 'Estimated crack time: {} (Strong)',
        'weak': 'Weak',
        'medium': 'Medium',
        'strong': 'Strong',
        'seconds': 'seconds',
        'minutes': 'minutes',
        'hours': 'hours',
        'days': 'days',
        'years': 'years',
        'character_repeat': 'Multiple character repetitions can make the password easier to guess.',
        'character_repeat_detail': 'Character \'{}\' repeats {} times in a row.',
        'keyboard_pattern': 'Keyboard pattern detected!',
        'keyboard_pattern_detail': 'Password contains this keyboard pattern: {}',
        'dictionary_word': 'Contains real words!',
        'dictionary_word_detail': 'Detected word: {}',
        'leetspeak_warning': 'Password uses leetspeak but is still predictable!',
        'leetspeak_detail': 'Leetspeak conversion: {} -> {}',
    }
}

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

def select_language():
    """Kullanıcıdan dil seçimini alır."""
    while True:
        print(f"{Fore.CYAN}Select Language / Dil Seçin:{Style.RESET_ALL}")
        print("1. English")
        print("2. Türkçe")
        choice = input("Choice / Seçim (1/2): ")
        if choice in ['1', '2']:
            return 'en' if choice == '1' else 'tr'
        print(f"{Fore.RED}Invalid choice. Please try again. / Geçersiz seçim. Lütfen tekrar deneyin.{Style.RESET_ALL}")

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

def calculate_crack_time(combinations, lang):
    """Parolanın kırılma süresini hesaplar."""
    attempts_needed = combinations / 2
    seconds = attempts_needed / ATTEMPTS_PER_SECOND
    
    if seconds < 60:
        return f"{seconds:.1f} {LANGUAGES[lang]['seconds']}"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} {LANGUAGES[lang]['minutes']}"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f} {LANGUAGES[lang]['hours']}"
    elif seconds < 31536000:
        days = seconds / 86400
        return f"{days:.1f} {LANGUAGES[lang]['days']}"
    else:
        years = seconds / 31536000
        return f"{years:.1f} {LANGUAGES[lang]['years']}"

def check_character_repeats(password):
    """Paroladaki karakter tekrarlarını kontrol eder."""
    repeats = []
    for char, group in groupby(password):
        count = sum(1 for _ in group)
        if count >= MIN_REPEAT_COUNT:
            repeats.append((char, count))
    return repeats

def check_keyboard_patterns(password):
    """Paroladaki klavye desenlerini kontrol eder."""
    patterns_found = []
    password_lower = password.lower()
    
    for pattern in KEYBOARD_PATTERNS:
        if re.search(pattern, password_lower):
            patterns_found.append(pattern)
    
    return patterns_found

def check_dictionary_words(password):
    """Paroladaki gerçek kelimeleri kontrol eder."""
    word_list = set(words.words())
    found_words = []
    
    # Parolayı küçük harfe çevir
    password_lower = password.lower()
    
    # 4 karakterden uzun kelimeleri ara
    for i in range(len(password_lower)):
        for j in range(i + 4, len(password_lower) + 1):
            word = password_lower[i:j]
            if word in word_list:
                found_words.append(word)
    
    return found_words

def convert_leetspeak(text):
    """Leetspeak karakterlerini normal harflere dönüştürür."""
    leetspeak_map = {
        '0': 'o', '1': 'i', '2': 'z', '3': 'e', '4': 'a', '5': 's', '6': 'b', '7': 't', '8': 'b', '9': 'g',
        '@': 'a', '$': 's', '!': 'i', '+': 't', '#': 'h', '&': 'a', '*': 'a', '?': 'a', '^': 'a', '%': 'a'
    }
    
    converted = ''
    for char in text.lower():
        converted += leetspeak_map.get(char, char)
    return converted

def check_leetspeak(password):
    """Paroladaki leetspeak kullanımını kontrol eder."""
    word_list = set(words.words())
    found_words = []
    
    # Parolayı küçük harfe çevir
    password_lower = password.lower()
    
    # Leetspeak dönüşümü yap
    converted = convert_leetspeak(password_lower)
    
    # 4 karakterden uzun kelimeleri ara
    for i in range(len(converted)):
        for j in range(i + 4, len(converted) + 1):
            word = converted[i:j]
            if word in word_list:
                original = password_lower[i:j]
                found_words.append((original, word))
    
    return found_words

def check_password_strength(password, lang):
    score = 0
    feedback = []

    # Uzunluk kontrolü
    if len(password) < 8:
        feedback.append(f"{Fore.RED}{LANGUAGES[lang]['too_short']}{Style.RESET_ALL}")
    else:
        score += 1
        if len(password) >= 12:
            score += 1
            feedback.append(f"{Fore.GREEN}{LANGUAGES[lang]['good_length']}{Style.RESET_ALL}")

    # Klavye deseni kontrolü
    patterns = check_keyboard_patterns(password)
    if patterns:
        score -= 1
        feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['keyboard_pattern']}{Style.RESET_ALL}")
        for pattern in patterns:
            feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['keyboard_pattern_detail'].format(pattern)}{Style.RESET_ALL}")

    # Karakter tekrarı kontrolü
    repeats = check_character_repeats(password)
    if repeats:
        score -= 1
        feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['character_repeat']}{Style.RESET_ALL}")
        for char, count in repeats:
            feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['character_repeat_detail'].format(char, count)}{Style.RESET_ALL}")

    # Büyük harf kontrolü
    if re.search(r"[A-Z]", password):
        score += 1
        feedback.append(f"{Fore.GREEN}{LANGUAGES[lang]['has_uppercase']}{Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['needs_uppercase']}{Style.RESET_ALL}")

    # Küçük harf kontrolü
    if re.search(r"[a-z]", password):
        score += 1
        feedback.append(f"{Fore.GREEN}{LANGUAGES[lang]['has_lowercase']}{Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['needs_lowercase']}{Style.RESET_ALL}")

    # Rakam kontrolü
    if re.search(r"\d", password):
        score += 1
        feedback.append(f"{Fore.GREEN}{LANGUAGES[lang]['has_number']}{Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['needs_number']}{Style.RESET_ALL}")

    # Özel karakter kontrolü
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
        feedback.append(f"{Fore.GREEN}{LANGUAGES[lang]['has_special']}{Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['needs_special']}{Style.RESET_ALL}")

    # Yaygın parola kontrolü
    if password.lower() in COMMON_PASSWORDS:
        score = 0
        feedback.append(f"{Fore.RED}{LANGUAGES[lang]['common_password']}{Style.RESET_ALL}")
    else:
        for common in COMMON_PASSWORDS:
            if common in password.lower() or password.lower() in common:
                score -= 1
                feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['similar_password']}{Style.RESET_ALL}")
                break

    # Sözlük kelimesi kontrolü
    dictionary_words = check_dictionary_words(password)
    if dictionary_words:
        score -= 1
        feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['dictionary_word']}{Style.RESET_ALL}")
        for word in dictionary_words:
            feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['dictionary_word_detail'].format(word)}{Style.RESET_ALL}")

    # Leetspeak kontrolü
    leetspeak_words = check_leetspeak(password)
    if leetspeak_words:
        score -= 1
        feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['leetspeak_warning']}{Style.RESET_ALL}")
        for original, converted in leetspeak_words:
            feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['leetspeak_detail'].format(original, converted)}{Style.RESET_ALL}")

    # Entropy hesaplama
    entropy = calculate_entropy(password)
    combinations = calculate_possible_combinations(password)
    
    # Entropy değerlendirmesi
    if entropy < 2:
        feedback.append(f"{Fore.RED}{LANGUAGES[lang]['low_entropy'].format(entropy)}{Style.RESET_ALL}")
    elif entropy < 3:
        feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['medium_entropy'].format(entropy)}{Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.GREEN}{LANGUAGES[lang]['high_entropy'].format(entropy)}{Style.RESET_ALL}")
    
    # Olası kombinasyon sayısı değerlendirmesi
    if combinations < 1000000:
        feedback.append(f"{Fore.RED}{LANGUAGES[lang]['low_combinations'].format(combinations)}{Style.RESET_ALL}")
    elif combinations < 100000000:
        feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['medium_combinations'].format(combinations)}{Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.GREEN}{LANGUAGES[lang]['high_combinations'].format(combinations)}{Style.RESET_ALL}")

    # Kırma süresi hesaplama
    crack_time = calculate_crack_time(combinations, lang)
    if "seconds" in crack_time or "minutes" in crack_time:
        feedback.append(f"{Fore.RED}{LANGUAGES[lang]['crack_time_weak'].format(crack_time)}{Style.RESET_ALL}")
    elif "hours" in crack_time:
        feedback.append(f"{Fore.YELLOW}{LANGUAGES[lang]['crack_time_medium'].format(crack_time)}{Style.RESET_ALL}")
    else:
        feedback.append(f"{Fore.GREEN}{LANGUAGES[lang]['crack_time_strong'].format(crack_time)}{Style.RESET_ALL}")

    # Sonuç değerlendirmesi
    if score <= 2:
        strength = f"{Fore.RED}{LANGUAGES[lang]['weak']}{Style.RESET_ALL}"
    elif score <= 4:
        strength = f"{Fore.YELLOW}{LANGUAGES[lang]['medium']}{Style.RESET_ALL}"
    else:
        strength = f"{Fore.GREEN}{LANGUAGES[lang]['strong']}{Style.RESET_ALL}"

    return strength, score, feedback

def main():
    # Dil seçimi
    lang = select_language()
    
    print(f"{Fore.CYAN}{LANGUAGES[lang]['title']}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{LANGUAGES[lang]['note_common'].format(len(COMMON_PASSWORDS))}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{LANGUAGES[lang]['note_metrics']}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{LANGUAGES[lang]['note_attempts'].format(ATTEMPTS_PER_SECOND)}{Style.RESET_ALL}")
    
    while True:
        password = input(f"\n{LANGUAGES[lang]['input_prompt']}")
        if password.lower() == 'q':
            break

        strength, score, feedback = check_password_strength(password, lang)
        print(f"\n{LANGUAGES[lang]['password_strength'].format(strength, score)}")
        print(f"\n{LANGUAGES[lang]['feedback_title']}")
        for msg in feedback:
            print(msg)

if __name__ == "__main__":
    main() 