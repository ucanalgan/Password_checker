from colorama import init, Fore, Style
from typing import Dict, Any, List, Tuple
import json
from analyzers.length import LengthAnalyzer
from analyzers.character import CharacterAnalyzer
from analyzers.entropy import EntropyAnalyzer
from analyzers.patterns import PatternAnalyzer
from analyzers.dictionary import DictionaryAnalyzer

# Colorama'yı başlat
init()

class PasswordAnalyzer:
    """Parola güvenlik analizi ana sınıfı."""
    
    def __init__(self):
        self.analyzers = [
            LengthAnalyzer(),
            CharacterAnalyzer(),
            EntropyAnalyzer(),
            PatternAnalyzer(),
            DictionaryAnalyzer()
        ]
        
        self.messages = {
            'tr': {
                'title': '=== Parola Güvenlik Kontrolü ===',
                'note_common': 'Not: Bu araç {} yaygın parola ile karşılaştırma yapar.',
                'note_metrics': 'Entropy, olası kombinasyon sayısı ve kırma süresi hesaplanır.',
                'note_attempts': 'Tahmin: Saniyede {} deneme yapan bir makine için.',
                'input_prompt': 'Kontrol etmek istediğiniz parolayı girin (çıkmak için \'q\'): ',
                'password_strength': 'Parola Gücü: {} (Puan: {}/6)',
                'feedback_title': 'Detaylı Geri Bildirim:',
                'weak': 'Zayıf',
                'medium': 'Orta',
                'strong': 'Güçlü',
            },
            'en': {
                'title': '=== Password Security Check ===',
                'note_common': 'Note: This tool compares against {} common passwords.',
                'note_metrics': 'Entropy, possible combinations, and crack time are calculated.',
                'note_attempts': 'Estimate: For a machine that attempts {} passwords per second.',
                'input_prompt': 'Enter the password to check (press \'q\' to quit): ',
                'password_strength': 'Password Strength: {} (Score: {}/6)',
                'feedback_title': 'Detailed Feedback:',
                'weak': 'Weak',
                'medium': 'Medium',
                'strong': 'Strong',
            }
        }
    
    def analyze_password(self, password: str, lang: str = 'tr') -> Tuple[str, int, List[str]]:
        """Parolayı analiz eder ve sonuçları döndürür."""
        score = 0
        feedback = []
        
        # Her analizörü çalıştır
        for analyzer in self.analyzers:
            analyzer_feedback = analyzer.get_feedback(lang)
            score_impact = analyzer.get_score_impact()
            
            feedback.extend(analyzer_feedback)
            score += score_impact
        
        # Sonuç değerlendirmesi
        if score <= 2:
            strength = f"{Fore.RED}{self.messages[lang]['weak']}{Style.RESET_ALL}"
        elif score <= 4:
            strength = f"{Fore.YELLOW}{self.messages[lang]['medium']}{Style.RESET_ALL}"
        else:
            strength = f"{Fore.GREEN}{self.messages[lang]['strong']}{Style.RESET_ALL}"
        
        return strength, score, feedback
    
    def analyze_password_json(self, password: str) -> Dict[str, Any]:
        """Parolayı analiz eder ve sonuçları JSON formatında döndürür."""
        results = {}
        
        for analyzer in self.analyzers:
            analyzer_name = analyzer.__class__.__name__.replace('Analyzer', '').lower()
            results[analyzer_name] = analyzer.analyze(password)
        
        return results
    
    def print_analysis(self, password: str, lang: str = 'tr'):
        """Analiz sonuçlarını ekrana yazdırır."""
        strength, score, feedback = self.analyze_password(password, lang)
        
        print(f"\n{self.messages[lang]['password_strength'].format(strength, score)}")
        print(f"\n{self.messages[lang]['feedback_title']}")
        for msg in feedback:
            print(msg)
    
    def save_analysis(self, password: str, filename: str = 'analysis.json'):
        """Analiz sonuçlarını JSON dosyasına kaydeder."""
        results = self.analyze_password_json(password)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        
        print(f"\nAnaliz sonuçları {filename} dosyasına kaydedildi.") 