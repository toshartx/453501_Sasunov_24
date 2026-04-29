import csv
import pickle

class StudentInfo():
    def __init__(self, is_needed: bool, work_experience: int, institute: str, language: str):
        self.__is_needed_in_dormitory = is_needed
        self.__work_experience = work_experience
        self.__institute = institute
        self.__language = language

    def is_needed(self) -> bool:
        return self.__is_needed_in_dormitory

    def work_experience(self) -> int:
        return self.__work_experience

    def institute(self) -> str:
        return self.__institute

    def language(self) -> str:
        return self.__language

    def __repr__(self):
        return f"{self.__is_needed_in_dormitory}, {self.__work_experience}, {self.__institute}, {self.__language}"



class UniversityController():
    def __init__(self):
        self.__dictionary = {}

    def add_student(self, surname: str, info: StudentInfo) -> None:
        """Adding student to dictionary"""
        self.__dictionary[surname] = info

    def count_destitute_students(self) -> int:
        destitutes = [student for student in self.__dictionary.values() if student.is_needed() == False]
        return len(destitutes)

    def experience_bigger_than(self, work_experience: int = 2) -> list:
        return [key for key, value in self.__dictionary.items() if value.work_experience() > work_experience]

    def ended_technicume(self) -> list:
        return [key for key, value in self.__dictionary.items() if value.institute() == "Техникум"]

    def language_groups(self) -> dict:
        groups: dict = {}
        for key, value in self.__dictionary.items():
            if value.language() not in groups:
                groups[value.language()] = []
            groups[value.language()].append(key)
        
        return groups

    def csv_serialize(self) -> None:
        with open(file="Task1/data/students.csv", mode="w+") as f:
            writer = csv.writer(f)
            for key, value in self.__dictionary.items():
                writer.writerow([key, value.is_needed(), value.work_experience(), value.institute(), value.language()])

    def csv_deserialize(self) -> None:
        with open(file="Task1/data/students.csv", mode="r") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:  
                    continue

                is_needed = row[1].lower() == "true"
                work_experience = int(row[2])
                institute = row[3]
                language = row[4]
                st = StudentInfo(is_needed, work_experience, institute, language)

                self.__dictionary[row[0]] = st 
        print(f"{self.__dictionary}")        

    def pickle_serialize(self) -> None:
        with open(file="Task1/data/students.bin", mode="wb+") as f:
            pickle.dump(self.__dictionary, f)

    def pickle_deserialize(self) -> None:
        with open(file="Task1/data/students.bin", mode="rb") as f:
            self.__dictionary = pickle.load(f)
                
                


        

        
# unvsty = UniversityController()
# unvsty.csv_deserialize()
# unvsty.pickle_serialize()
# unvsty.pickle_deserialize()
# print(unvsty.count_destitute_students())
# print(unvsty.experience_bigger_than())
# print(unvsty.ended_technicume())
# print(unvsty.language_groups())

