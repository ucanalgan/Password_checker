from .base import PasswordAnalyzer
from colorama import Fore, Style
from typing import Dict, Any, List
import re

class CharacterAnalyzer(PasswordAnalyzer):
    """Karakter çeşitliliği analizi."""
    
    def __init__(self):
        self.messages = {
            'tr': {
                'has_uppercase': 'Büyük harf içeriyor! (+1 puan)',
                'needs_uppercase': 'Büyük harf kullanmanız önerilir.',
                'has_lowercase': 'Küçük harf içeriyor! (+1 puan)',
                'needs_lowercase': 'Küçük harf kullanmanız önerilir.',
                'has_number': 'Rakam içeriyor! (+1 puan)',
                'needs_number': 'Rakam kullanmanız önerilir.',
                'has_special': 'Özel karakter içeriyor! (+1 puan)',
                'needs_special': 'Özel karakter kullanmanız önerilir.',
            },
            'en': {
                'has_uppercase': 'Contains uppercase letters! (+1 point)',
                'needs_uppercase': 'Consider using uppercase letters.',
                'has_lowercase': 'Contains lowercase letters! (+1 point)',
                'needs_lowercase': 'Consider using lowercase letters.',
                'has_number': 'Contains numbers! (+1 point)',
                'needs_number': 'Consider using numbers.',
                'has_special': 'Contains special characters! (+1 point)',
                'needs_special': 'Consider using special characters.',
            }
        }
    
    def analyze(self, password: str) -> Dict[str, Any]:
        return {
            'has_uppercase': bool(re.search(r"[A-Z]", password)),
            'has_lowercase': bool(re.search(r"[a-z]", password)),
            'has_number': bool(re.search(r"\d", password)),
            'has_special': bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
        }
    
    def get_feedback(self, lang: str) -> List[str]:
        result = self.analyze(password)
        feedback = []
        
        if result['has_uppercase']:
            feedback.append(f"{Fore.GREEN}{self.messages[lang]['has_uppercase']}{Style.RESET_ALL}")
        else:
            feedback.append(f"{Fore.YELLOW}{self.messages[lang]['needs_uppercase']}{Style.RESET_ALL}")
            
        if result['has_lowercase']:
            feedback.append(f"{Fore.GREEN}{self.messages[lang]['has_lowercase']}{Style.RESET_ALL}")
        else:
            feedback.append(f"{Fore.YELLOW}{self.messages[lang]['needs_lowercase']}{Style.RESET_ALL}")
            
        if result['has_number']:
            feedback.append(f"{Fore.GREEN}{self.messages[lang]['has_number']}{Style.RESET_ALL}")
        else:
            feedback.append(f"{Fore.YELLOW}{self.messages[lang]['needs_number']}{Style.RESET_ALL}")
            
        if result['has_special']:
            feedback.append(f"{Fore.GREEN}{self.messages[lang]['has_special']}{Style.RESET_ALL}")
        else:
            feedback.append(f"{Fore.YELLOW}{self.messages[lang]['needs_special']}{Style.RESET_ALL}")
            
        return feedback
    
    def get_score_impact(self) -> int:
        result = self.analyze(password)
        return sum(1 for value in result.values() if value) 