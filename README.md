# Password Security Analyzer

A comprehensive password strength analysis tool that evaluates passwords based on multiple security criteria and provides detailed feedback in both English and Turkish.

## Features

### 1. Length Analysis
- Minimum length check (8 characters)
- Optimal length recommendation (12+ characters)
- Score impact based on length

### 2. Character Diversity Analysis
- Uppercase letters check
- Lowercase letters check
- Numbers check
- Special characters check
- Individual scoring for each character type

### 3. Entropy Analysis
- Shannon Entropy calculation
- Character set size evaluation
- Possible combinations calculation
- Estimated crack time based on:
  - 1 billion attempts per second
  - Average case scenario (50% of combinations)

### 4. Pattern Analysis
- Keyboard pattern detection (QWERTY layouts)
- Character repetition detection
- Leetspeak conversion and detection
- Common sequence detection

### 5. Dictionary Analysis
- English word detection
- Minimum word length check (4 characters)
- Case-insensitive matching

## Installation

1. Clone the repository:
```powershell
git clone https://github.com/yourusername/password-checker.git
cd password-checker
```

2. Create a virtual environment (recommended):
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Install required packages:
```powershell
pip install -r requirements.txt
```

## Usage

Run the program:
```powershell
python main.py
```

### Language Selection
The program supports both English and Turkish interfaces:
1. Select Language / Dil Seçin:
   - 1. English
   - 2. Türkçe

### Input
- Enter the password you want to analyze
- Press 'q' to quit the program

### Output
The program provides:
1. Overall password strength score (0-6)
2. Color-coded strength indicator (Red/Yellow/Green)
3. Detailed feedback for each analysis category
4. JSON report saved to 'analysis.json'

## Analysis Criteria

### Password Strength Score (0-6)
- 0-2: Weak (Red)
- 3-4: Medium (Yellow)
- 5-6: Strong (Green)

### Scoring Factors
- Length: +1 to +2 points
- Character types: +1 point each
- Entropy: -1 to +1 points
- Patterns: -1 point each
- Dictionary words: -1 point

## Technical Details

### Entropy Calculation
- Uses Shannon Entropy formula
- Evaluates character distribution
- Considers character set size

### Crack Time Estimation
Based on:
- Character set size
- Password length
- 1 billion attempts per second
- Average case scenario

### Pattern Detection
Includes:
- QWERTY keyboard patterns
- Sequential numbers
- Alphabetical sequences
- Character repetitions
- Leetspeak conversions

## Dependencies

- Python 3.6+
- colorama
- nltk

## File Structure

```
password_checker/
├── analyzers/
│   ├── __init__.py
│   ├── base.py
│   ├── length.py
│   ├── character.py
│   ├── entropy.py
│   ├── patterns.py
│   └── dictionary.py
├── analyzer.py
├── main.py
└── requirements.txt
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NLTK for English word list
- Colorama for colored terminal output
- Shannon Entropy formula for password strength evaluation 