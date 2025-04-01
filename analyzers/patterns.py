from .base import PasswordAnalyzer
from colorama import Fore, Style
from typing import Dict, Any, List
import re
from itertools import groupby

class PatternAnalyzer(PasswordAnalyzer):
    """Desen analizi (klavye desenleri, tekrarlar, leetspeak)."""
    
    def __init__(self):
        self.min_repeat_count = 3
        self.keyboard_patterns = [
            # QWERTY sıraları
            r'qwerty', r'asdfgh', r'zxcvbn', r'123456',
            r'qwertyuiop', r'asdfghjkl', r'zxcvbnm',
            r'qwerty123', r'asdfgh123', r'zxcvbn123',
            
            # QWERTY çapraz desenler
            r'1qaz', r'2wsx', r'3edc', r'4rfv', r'5tgb',
            r'6yhn', r'7ujm', r'8ik,', r'9ol.', r'0p;/',
            
            # QWERTY dikey desenler
            r'q1', r'w2', r'e3', r'r4', r't5',
            r'y6', r'u7', r'i8', r'o9', r'p0',
            
            # Sayı tuşu desenleri
            r'12345', r'23456', r'34567', r'45678', r'56789', r'67890',
            
            # Alfabetik sıralar
            r'abcdef', r'bcdefg', r'cdefgh', r'defghi', r'efghij',
            r'fghijk', r'ghijkl', r'hijklm', r'ijklmn', r'jklmno',
            r'klmnop', r'lmno', r'mnop', r'nopq', r'opqr',
            r'pqrs', r'qrst', r'rstu', r'stuv', r'tuvw',
            r'uvwx', r'vwxy', r'wxyz'
        ]
        
        self.leetspeak_map = {
            '0': 'o', '1': 'i', '2': 'z', '3': 'e', '4': 'a', '5': 's',
            '6': 'b', '7': 't', '8': 'b', '9': 'g',
            '@': 'a', '$': 's', '!': 'i', '+': 't', '#': 'h',
            '&': 'a', '*': 'a', '?': 'a', '^': 'a', '%': 'a'
        }
        
        self.messages = {
            'tr': {
                'character_repeat': 'Çoklu tekrarlar tahmini kolaylaştırabilir.',
                'character_repeat_detail': '{} karakteri {} kez art arda tekrar ediyor.',
                'keyboard_pattern': 'Klavye düzeni tabanlı parola tespit edildi!',
                'keyboard_pattern_detail': 'Parola şu klavye desenini içeriyor: {}',
                'leetspeak_warning': 'Leetspeak kullanılan ama tahmin edilebilir parola!',
                'leetspeak_detail': 'Leetspeak dönüşümü: {} -> {}',
            },
            'en': {
                'character_repeat': 'Multiple character repetitions can make the password easier to guess.',
                'character_repeat_detail': 'Character \'{}\' repeats {} times in a row.',
                'keyboard_pattern': 'Keyboard pattern detected!',
                'keyboard_pattern_detail': 'Password contains this keyboard pattern: {}',
                'leetspeak_warning': 'Password uses leetspeak but is still predictable!',
                'leetspeak_detail': 'Leetspeak conversion: {} -> {}',
            }
        }
    
    def check_character_repeats(self, password: str) -> List[tuple]:
        repeats = []
        for char, group in groupby(password):
            count = sum(1 for _ in group)
            if count >= self.min_repeat_count:
                repeats.append((char, count))
        return repeats
    
    def check_keyboard_patterns(self, password: str) -> List[str]:
        patterns_found = []
        password_lower = password.lower()
        
        for pattern in self.keyboard_patterns:
            if re.search(pattern, password_lower):
                patterns_found.append(pattern)
        
        return patterns_found
    
    def convert_leetspeak(self, text: str) -> str:
        converted = ''
        for char in text.lower():
            converted += self.leetspeak_map.get(char, char)
        return converted
    
    def check_leetspeak(self, password: str) -> List[tuple]:
        word_list = set(words.words())
        found_words = []
        password_lower = password.lower()
        converted = self.convert_leetspeak(password_lower)
        
        for i in range(len(converted)):
            for j in range(i + 4, len(converted) + 1):
                word = converted[i:j]
                if word in word_list:
                    original = password_lower[i:j]
                    found_words.append((original, word))
        
        return found_words
    
    def analyze(self, password: str) -> Dict[str, Any]:
        return {
            'repeats': self.check_character_repeats(password),
            'keyboard_patterns': self.check_keyboard_patterns(password),
            'leetspeak_words': self.check_leetspeak(password)
        }
    
    def get_feedback(self, lang: str) -> List[str]:
        result = self.analyze(password)
        feedback = []
        
        # Karakter tekrarı kontrolü
        if result['repeats']:
            feedback.append(f"{Fore.YELLOW}{self.messages[lang]['character_repeat']}{Style.RESET_ALL}")
            for char, count in result['repeats']:
                feedback.append(f"{Fore.YELLOW}{self.messages[lang]['character_repeat_detail'].format(char, count)}{Style.RESET_ALL}")
        
        # Klavye deseni kontrolü
        if result['keyboard_patterns']:
            feedback.append(f"{Fore.YELLOW}{self.messages[lang]['keyboard_pattern']}{Style.RESET_ALL}")
            for pattern in result['keyboard_patterns']:
                feedback.append(f"{Fore.YELLOW}{self.messages[lang]['keyboard_pattern_detail'].format(pattern)}{Style.RESET_ALL}")
        
        # Leetspeak kontrolü
        if result['leetspeak_words']:
            feedback.append(f"{Fore.YELLOW}{self.messages[lang]['leetspeak_warning']}{Style.RESET_ALL}")
            for original, converted in result['leetspeak_words']:
                feedback.append(f"{Fore.YELLOW}{self.messages[lang]['leetspeak_detail'].format(original, converted)}{Style.RESET_ALL}")
        
        return feedback
    
    def get_score_impact(self) -> int:
        result = self.analyze(password)
        score_impact = 0
        
        if result['repeats']:
            score_impact -= 1
        if result['keyboard_patterns']:
            score_impact -= 1
        if result['leetspeak_words']:
            score_impact -= 1
            
        return score_impact 