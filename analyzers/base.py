from abc import ABC, abstractmethod
from typing import Dict, Any

class PasswordAnalyzer(ABC):
    """Temel parola analiz sınıfı."""
    
    @abstractmethod
    def analyze(self, password: str) -> Dict[str, Any]:
        """Parolayı analiz eder ve sonuçları döndürür."""
        pass
    
    @abstractmethod
    def get_feedback(self, lang: str) -> list:
        """Analiz sonuçlarına göre geri bildirim mesajlarını döndürür."""
        pass
    
    @abstractmethod
    def get_score_impact(self) -> int:
        """Analiz sonucunun puan etkisini döndürür."""
        pass 