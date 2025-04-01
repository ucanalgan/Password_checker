from .base import PasswordAnalyzer
from colorama import Fore, Style
from typing import Dict, Any, List
import nltk
from nltk.corpus import words

class DictionaryAnalyzer(PasswordAnalyzer):
    """Sözlük kelimesi analizi."""
    
    def __init__(self):
        try:
            nltk.data.find('corpora/words')
        except LookupError:
            nltk.download('words')
            
        self.messages = {
            'tr': {
                'dictionary_word': 'Gerçek kelime içeriyor!',
                'dictionary_word_detail': 'Tespit edilen kelime: {}',
            },
            'en': {
                'dictionary_word': 'Contains real words!',
                'dictionary_word_detail': 'Detected word: {}',
            }
        }
    
    def analyze(self, password: str) -> Dict[str, Any]:
        word_list = set(words.words())
        found_words = []
        password_lower = password.lower()
        
        for i in range(len(password_lower)):
            for j in range(i + 4, len(password_lower) + 1):
                word = password_lower[i:j]
                if word in word_list:
                    found_words.append(word)
        
        return {
            'found_words': found_words
        }
    
    def get_feedback(self, lang: str) -> List[str]:
        result = self.analyze(password)
        feedback = []
        
        if result['found_words']:
            feedback.append(f"{Fore.YELLOW}{self.messages[lang]['dictionary_word']}{Style.RESET_ALL}")
            for word in result['found_words']:
                feedback.append(f"{Fore.YELLOW}{self.messages[lang]['dictionary_word_detail'].format(word)}{Style.RESET_ALL}")
        
        return feedback
    
    def get_score_impact(self) -> int:
        result = self.analyze(password)
        return -1 if result['found_words'] else 0 