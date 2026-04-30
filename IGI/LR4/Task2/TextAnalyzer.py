import re
import zipfile
import os
from datetime import datetime

class TextAnalyzer:
    def __init__(self, input_file: str = "Task2/data/input.txt"):
        self.input_file = input_file
        self.text = ""
        self.results = {}
        self.output_file = "Task2/data/results.txt"

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
        
        all_words = re.findall(r'\b\w+\'?\b', self.text)
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
        words = re.findall(r"\b\w+\'?[a-zA-Z]+\b", self.text)
        avg_world_length = round(sum(len(word) for word in words) / len(words), 2)
        self.results['avg_words_length'] = avg_world_length                # print

    def analyze_smiles(self) -> None:
        pattern = r'[:;]-*([()\[\]])\1*'
    
        matches = re.finditer(pattern, self.text)
        smiles = [m.group() for m in matches]  
        
        self.results['smiles_count'] = len(smiles)
        self.results['smiles_list'] = smiles
        
    def print_words_start_with_lower(self) -> None:
        words = re.findall(r"\b[a-z]\w*\'?[a-zA-Z]+\b", self.text)
        self.results['lowercase_words'] = words

    def print_puncts(self) -> None:
        puncts = re.findall(r"[.!?]+|,|[:;](?=[\s\w])", self.text)         # (?=[\s\w]) - проверка на то, что это не смайлик
        self.results['punctuation'] = puncts

    def validate_mac_address(self, mac_string: str = "aE:dC:cA:56:76:54"):
        """MAC-Address check"""
        # Формат: xx:xx:xx:xx:xx:xx, где x - hex-цифра (0-9, a-f, A-F)
        pattern = r'^[\da-fA-F]{2}:[\da-fA-F]{2}:[\da-fA-F]{2}:[\da-fA-F]{2}:[\da-fA-F]{2}:[\da-fA-F]{2}$'
        is_valid = bool(re.match(pattern, mac_string))
        if is_valid:
            self.results['mac_address'] = {
                'address': mac_string,
                'is_valid': is_valid
            }
        

    def count_words_start_with_consonant(self):
        """Counts words in text that starting with consonant letter"""
        words = re.findall(r"\b[^\saeuioy]\w*\b", self.text.lower())
        self.results['consonant_words'] = words
        self.results['consonant_words_count'] = len(words)

    def find_words_with_identical_letters(self, c: int = 2):
        """Finds words with `c` identical letters and their IDs"""
        all_words = re.findall(r"\b[a-zA-Z]+'?[a-zA-Z]+\b", self.text)
        words = []
        for i, word in enumerate(all_words):
            if re.search(r"(.)\1", word):
                words.append((word, i))
        self.results['double_letter_words'] = words
        

    def print_sorted_words(self):
        """Prints words sorted in alphabet"""
        all_words = re.findall(r"\b[a-zA-Z]+'?[a-zA-Z]+\b", self.text)
        sorted_words = sorted(set(all_words), key=lambda x: x.lower())
        self.results['sorted_words'] = sorted_words

    def save_results_to_file(self) -> None:
        """Сохраняет все результаты в файл"""
        # Создаем директорию, если её нет
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("РЕЗУЛЬТАТЫ АНАЛИЗА ТЕКСТА\n")
            f.write(f"Дата и время анализа: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            # Предложения
            f.write("1. АНАЛИЗ ПРЕДЛОЖЕНИЙ:\n")
            f.write(f"   - Общее количество предложений: {self.results['sentences']['total']}\n")
            f.write(f"   - Повествовательных (.): {self.results['sentences']['declarative']}\n")
            f.write(f"   - Вопросительных (?): {self.results['sentences']['interrogative']}\n")
            f.write(f"   - Побудительных (!): {self.results['sentences']['imperative']}\n")
            f.write(f"   - Средняя длина предложения: {self.results['sentences']['avg_length']} символов\n\n")
            
            # Слова
            f.write("2. АНАЛИЗ СЛОВ:\n")
            f.write(f"   - Средняя длина слова: {self.results['avg_words_length']} символов\n")
            f.write(f"   - Слова, начинающиеся со строчной буквы: {', '.join(self.results['lowercase_words'][:20])}\n")
            f.write(f"   - Количество слов, начинающихся с согласной: {self.results['consonant_words_count']}\n")
            f.write(f"   - Слова, начинающиеся с согласной: {', '.join(self.results['consonant_words'][:20])}\n\n")
            
            # Смайлики
            f.write("3. СМАЙЛИКИ:\n")
            f.write(f"   - Количество смайликов: {self.results['smiles_count']}\n")
            if self.results['smiles_list']:
                f.write(f"   - Найденные смайлики: {', '.join(self.results['smiles_list'])}\n")
            f.write("\n")
            
            # Знаки препинания
            f.write("4. ЗНАКИ ПРЕПИНАНИЯ:\n")
            f.write(f"   - Последовательность: {' -> '.join(self.results['punctuation'])}\n\n")
            
            # MAC-адрес
            f.write("5. ПРОВЕРКА MAC-АДРЕСА:\n")
            f.write(f"   - Адрес: {self.results['mac_address']['address']}\n")
            f.write(f"   - Статус: {'КОРРЕКТНЫЙ' if self.results['mac_address']['is_valid'] else 'НЕКОРРЕКТНЫЙ'}\n\n")
            
            # Слова с повторяющимися буквами
            f.write("6. СЛОВА С ДВУМЯ ОДИНАКОВЫМИ БУКВАМИ ПОДРЯД:\n")
            if self.results['double_letter_words']:
                for idx, word in self.results['double_letter_words'][:30]:
                    f.write(f"   - Порядковый номер {idx}: {word}\n")
            else:
                f.write("   - Такие слова не найдены\n")
            f.write("\n")
            
            # Слова в алфавитном порядке
            f.write("7. СЛОВА В АЛФАВИТНОМ ПОРЯДКЕ:\n")
            alphabetical = self.results['sorted_words']
            for word in alphabetical[:50]:
                f.write(f"   {word}\n")
            if len(alphabetical) > 50:
                f.write(f"   ... и еще {len(alphabetical) - 50} слов\n")
        
        print(f"\n✅ Результаты сохранены в файл: {self.output_file}")
    
    def archive_results(self, archive_name: str = "Task2/data/results.zip") -> None:
        """Архивирует файл с результатами"""
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(self.output_file, arcname=os.path.basename(self.output_file))
            
            print(f"\n📦 Архив создан: {archive_name}")
            print("\n" + "="*60)
            print("ИНФОРМАЦИЯ О ФАЙЛЕ В АРХИВЕ:")
            print("="*60)
            
            for info in zipf.infolist():
                print(f"  📄 Имя файла: {info.filename}")
                print(f"  📏 Исходный размер: {info.file_size:,} байт")
                print(f"  📦 Сжатый размер: {info.compress_size:,} байт")
                compression_ratio = (1 - info.compress_size / info.file_size) * 100 if info.file_size > 0 else 0
                print(f"  💾 Степень сжатия: {compression_ratio:.1f}%")
                print(f"  📅 Дата/время: {info.date_time}")
                print(f"  🔒 CRC-32: {info.CRC:08X}")
        
        print(f"\n✅ Файл {os.path.basename(self.output_file)} заархивирован в {archive_name}")

ta = TextAnalyzer()
ta.read_text()
ta.analyze_sentences()
ta.analyze_words()
ta.analyze_smiles()
ta.print_words_start_with_lower()
ta.print_puncts()
ta.validate_mac_address()
ta.count_words_start_with_consonant()
ta.find_words_with_identical_letters()
ta.print_sorted_words()
ta.save_results_to_file()
ta.archive_results()