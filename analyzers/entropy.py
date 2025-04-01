from .base import PasswordAnalyzer
from colorama import Fore, Style
from typing import Dict, Any, List
from collections import Counter
import math

class EntropyAnalyzer(PasswordAnalyzer):
    """Entropy ve kombinasyon analizi."""
    
    def __init__(self):
        self.attempts_per_second = 1_000_000_000
        self.messages = {
            'tr': {
                'low_entropy': 'Entropy değeri çok düşük! ({:.2f}) Parola tahmin edilebilir.',
                'medium_entropy': 'Entropy değeri orta. ({:.2f}) Parola biraz tahmin edilebilir.',
                'high_entropy': 'Entropy değeri iyi! ({:.2f}) Parola tahmin edilmesi zor.',
                'low_combinations': 'Olası kombinasyon sayısı çok düşük! ({:,})',
                'medium_combinations': 'Olası kombinasyon sayısı orta. ({:,})',
                'high_combinations': 'Olası kombinasyon sayısı yüksek! ({:,})',
                'crack_time_weak': 'Tahmini kırma süresi: {} (Çok zayıf!)',
                'crack_time_medium': 'Tahmini kırma süresi: {} (Orta)',
                'crack_time_strong': 'Tahmini kırma süresi: {} (Güçlü)',
            },
            'en': {
                'low_entropy': 'Entropy value is very low! ({:.2f}) Password is predictable.',
                'medium_entropy': 'Entropy value is medium. ({:.2f}) Password is somewhat predictable.',
                'high_entropy': 'Entropy value is good! ({:.2f}) Password is hard to predict.',
                'low_combinations': 'Possible combinations are very low! ({:,})',
                'medium_combinations': 'Possible combinations are medium. ({:,})',
                'high_combinations': 'Possible combinations are high! ({:,})',
                'crack_time_weak': 'Estimated crack time: {} (Very weak!)',
                'crack_time_medium': 'Estimated crack time: {} (Medium)',
                'crack_time_strong': 'Estimated crack time: {} (Strong)',
            }
        }
    
    def calculate_entropy(self, password: str) -> float:
        if not password:
            return 0
        
        char_freq = Counter(password)
        length = len(password)
        probabilities = [count/length for count in char_freq.values()]
        return -sum(p * math.log2(p) for p in probabilities)
    
    def calculate_combinations(self, password: str) -> int:
        charset_size = 0
        if re.search(r'[a-z]', password): charset_size += 26
        if re.search(r'[A-Z]', password): charset_size += 26
        if re.search(r'\d', password): charset_size += 10
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): charset_size += 32
        
        if charset_size == 0:
            charset_size = 26
        
        return charset_size ** len(password)
    
    def calculate_crack_time(self, combinations: int) -> str:
        attempts_needed = combinations / 2
        seconds = attempts_needed / self.attempts_per_second
        
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.1f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.1f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.1f} days"
        else:
            return f"{seconds/31536000:.1f} years"
    
    def analyze(self, password: str) -> Dict[str, Any]:
        entropy = self.calculate_entropy(password)
        combinations = self.calculate_combinations(password)
        crack_time = self.calculate_crack_time(combinations)
        
        return {
            'entropy': entropy,
            'combinations': combinations,
            'crack_time': crack_time
        }
    
    def get_feedback(self, lang: str) -> List[str]:
        result = self.analyze(password)
        feedback = []
        
        # Entropy değerlendirmesi
        if result['entropy'] < 2:
            feedback.append(f"{Fore.RED}{self.messages[lang]['low_entropy'].format(result['entropy'])}{Style.RESET_ALL}")
        elif result['entropy'] < 3:
            feedback.append(f"{Fore.YELLOW}{self.messages[lang]['medium_entropy'].format(result['entropy'])}{Style.RESET_ALL}")
        else:
            feedback.append(f"{Fore.GREEN}{self.messages[lang]['high_entropy'].format(result['entropy'])}{Style.RESET_ALL}")
        
        # Kombinasyon değerlendirmesi
        if result['combinations'] < 1000000:
            feedback.append(f"{Fore.RED}{self.messages[lang]['low_combinations'].format(result['combinations'])}{Style.RESET_ALL}")
        elif result['combinations'] < 100000000:
            feedback.append(f"{Fore.YELLOW}{self.messages[lang]['medium_combinations'].format(result['combinations'])}{Style.RESET_ALL}")
        else:
            feedback.append(f"{Fore.GREEN}{self.messages[lang]['high_combinations'].format(result['combinations'])}{Style.RESET_ALL}")
        
        # Kırma süresi değerlendirmesi
        if "seconds" in result['crack_time'] or "minutes" in result['crack_time']:
            feedback.append(f"{Fore.RED}{self.messages[lang]['crack_time_weak'].format(result['crack_time'])}{Style.RESET_ALL}")
        elif "hours" in result['crack_time']:
            feedback.append(f"{Fore.YELLOW}{self.messages[lang]['crack_time_medium'].format(result['crack_time'])}{Style.RESET_ALL}")
        else:
            feedback.append(f"{Fore.GREEN}{self.messages[lang]['crack_time_strong'].format(result['crack_time'])}{Style.RESET_ALL}")
        
        return feedback
    
    def get_score_impact(self) -> int:
        result = self.analyze(password)
        if result['entropy'] < 2:
            return -1
        elif result['entropy'] < 3:
            return 0
        return 1 