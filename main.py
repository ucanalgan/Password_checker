from analyzer import PasswordAnalyzer
from colorama import Fore, Style

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

def main():
    # Dil seçimi
    lang = select_language()
    
    # Analizör oluştur
    analyzer = PasswordAnalyzer()
    
    # Başlık ve bilgileri göster
    print(f"{Fore.CYAN}{analyzer.messages[lang]['title']}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{analyzer.messages[lang]['note_metrics']}{Style.RESET_ALL}")
    
    while True:
        password = input(f"\n{analyzer.messages[lang]['input_prompt']}")
        if password.lower() == 'q':
            break
        
        # Analiz yap ve sonuçları göster
        analyzer.print_analysis(password, lang)
        
        # JSON olarak kaydet
        analyzer.save_analysis(password)

if __name__ == "__main__":
    main() 