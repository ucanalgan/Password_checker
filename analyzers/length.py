from .base import PasswordAnalyzer
from colorama import Fore, Style
from typing import Dict, Any, List

class LengthAnalyzer(PasswordAnalyzer):
    """Parola uzunluğu analizi."""
    
    def __init__(self):
        self.min_length = 8
        self.good_length = 12
        self.messages = {
            'tr': {
                'too_short': 'Parola çok kısa! En az 8 karakter olmalı.',
                'good_length': 'Parola uzunluğu iyi! (+2 puan)',
            },
            'en': {
                'too_short': 'Password is too short! Must be at least 8 characters.',
                'good_length': 'Password length is good! (+2 points)',
            }
        }
    
    def analyze(self, password: str) -> Dict[str, Any]:
        length = len(password)
        return {
            'length': length,
            'is_valid': length >= self.min_length,
            'is_good': length >= self.good_length
        }
    
    def get_feedback(self, lang: str) -> List[str]:
        result = self.analyze(password)
        feedback = []
        
        if not result['is_valid']:
            feedback.append(f"{Fore.RED}{self.messages[lang]['too_short']}{Style.RESET_ALL}")
        elif result['is_good']:
            feedback.append(f"{Fore.GREEN}{self.messages[lang]['good_length']}{Style.RESET_ALL}")
            
        return feedback
    
    def get_score_impact(self) -> int:
        result = self.analyze(password)
        if not result['is_valid']:
            return 0
        return 2 if result['is_good'] else 1 