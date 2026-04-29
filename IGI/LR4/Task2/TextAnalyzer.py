import re

class TextAnalyzer:
    def __init__(self, input_file: str = "Task2/data/input.txt"):
        self.input_file = input_file
        self.text = ""
        self.results = {}

    def read_text(self) -> None:
        """Reading text from input file"""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as file:
                self.text = file.read()
            print(f"Текст успешно считан из файла {self.input_file}")
        except FileNotFoundError:
            print(f"Файл {self.input_file} не найден!")
            raise    

    def analyze_sentences(self) -> None:
        """Sentences analyze"""
        sentence_endings = re.finditer(r'[.!?]+', self.text)
        
        declarative = 0
        interrogative = 0
        imperative = 0
        
        for match in sentence_endings:
            punctuation = match.group()
            if '?' in punctuation:
                interrogative += 1
            elif '!' in punctuation:
                imperative += 1
            else:  # '.'
                declarative += 1
        
        total_sentences = declarative + interrogative + imperative
        
        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        all_words = re.findall(r'\b\w+\b', self.text)
        total_chars = sum(len(word) for word in all_words)
        avg_sentence_length = total_chars / total_sentences if total_sentences > 0 else 0
        
        self.results['sentences'] = {               # print()
            'total': total_sentences,
            'declarative': declarative,
            'interrogative': interrogative,
            'imperative': imperative,
            'avg_length': round(avg_sentence_length, 2)
        }
    
    def analyze_words(self) -> None:
        words = re.findall(r"\b\w+\b", self.text)
        avg_world_length = round(sum(len(word) for word in words) / len(words), 2)
        self.results['avg_words_length'] = avg_world_length                # print

    def analyze_smiles(self) -> None:
        smiles = re.findall(r"[:;]-*[()\[\]]+", self.text)
        self.results['smiles_count'] = len(smiles)
        print(*smiles, sep=' | ')
        
    def print_words_start_with_lower(self) -> None:
        words = re.findall(r"\b[a-z]\w*\b", self.text)
        print(*words, sep=', ')

    def print_puncts(self) -> None:
        puncts = re.findall(r"[.!?]+|,|[:;](?=[\s\w])", self.text)         # (?=[\s\w]) - проверка на то, что это не смайлик
        print(*puncts, sep=' -> ')

    def validate_mac_address(self, mac_string: str = "aE:dC:cA:56:76:54"):
        """MAC-Address check"""
        # Формат: xx:xx:xx:xx:xx:xx, где x - hex-цифра (0-9, a-f, A-F)
        pattern = r'^[\da-fA-F]{2}:[\da-fA-F]{2}:[\da-fA-F]{2}:[\da-fA-F]{2}:[\da-fA-F]{2}:[\da-fA-F]{2}$'
        is_valid = bool(re.match(pattern, mac_string))
        print(f"MAC-адрес {mac_string} является валидным") if is_valid else print(f"MAC-адрес {mac_string} является невалидным")

    def count_words_start_with_consonant(self):
        """Counts words in text that starting with consonant letter"""
        words = re.findall(r"\b[^\saeuioy]\w*\b", self.text.lower())
        print(*words, sep=', ')

    def find_words_with_identical_letters(self, c: int = 2):
        """Finds words with `c` identical letters and their IDs"""
        all_words = re.findall(r"\b\w+\b", self.text)
        words = []
        for i, word in enumerate(all_words):
            if re.search(r"(.)\1", word):
                words.append((word, i))
        print(*words, sep='; ')

    def print_sorted_words(self):
        """Prints words sorted in alphabet"""
        all_words = re.findall(r"\b\w+\b", self.text)
        sorted_words = sorted(set(all_words), key=lambda x: x.lower())
        print(*sorted_words, sep=', ')

# ta = TextAnalyzer()
# ta.read_text()
# ta.analyze_sentences()
# ta.analyze_words()
# ta.analyze_smiles()
# ta.print_words_start_with_lower()
# ta.print_puncts()
# ta.validate_mac_address()
# ta.count_words_start_with_consonant()
# ta.find_words_with_identical_letters()
# ta.print_sorted_words()
# print(ta.results['sentences'], '\n', ta.results['avg_words_length'], '\n', ta.results['smiles_count'])    