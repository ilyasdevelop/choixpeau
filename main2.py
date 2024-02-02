from math import sqrt
from collections import Counter
import csv

class c:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[1;33m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Student:
	def __init__(self, *args):
		self.name, self.courage, self.ambition, self.intelligence, self.good = args
		self.distances = {ch['Name']: {"Distance": self.distance(ch), "House": ch["House"]} for ch in CHARACTERS}
		self.closests = sorted(self.distances.items(), key=lambda x: x[1]["Distance"])[:K]
		self.text_closests = '\n'.join([f'{c.BLUE}{name}{c.RESET} dans la maison {c.BLUE}{attr["House"]}{c.RESET}' for name, attr in self.closests])

		houses = Counter(attr["House"] for _, attr in self.closests)
		self.house = max(houses, key=houses.get)
		
		houses_has_equality = len(set(houses.values())) != len(houses.values())
		if houses_has_equality:
			house_count = {}
			for _, attr in self.closests:
				house_count[attr["House"]] = house_count.get(attr["House"], 0) + 1

				if house_count[attr["House"]] == houses[max(houses, key=houses.get)]:
					self.house = attr["House"]
					break

	def __str__(self) -> str:
		return f"Élève {self.name} est envoyé à la maison {c.YELLOW}{self.house.title()}{c.RESET}.\nSes 5 plus proches voisins sont, dans l'ordre:\n{self.text_closests}"

	def distance(self, character: dict) -> float:
		return sqrt((int(self.courage) - int(character["Courage"])) ** 2
			+ (int(self.ambition) - int(character["Ambition"])) ** 2
			+ (int(self.intelligence) - int(character["Intelligence"])) ** 2
			+ (int(self.good) - int(character["Good"])) ** 2)


def read_csv(file: str) -> list[dict]:
	with open(file, mode='r', encoding='utf-8') as f:
		reader = csv.DictReader(f, delimiter=";")
		return [{key : value.replace('\xa0', ' ') for key, value in element.items()} for element in reader]

def merge(characters: str, attributes: str) -> list[dict]:
	poudlard_characters = []

	for poudlard_character in read_csv(attributes):
		for kaggle_character in read_csv(characters):
			if poudlard_character['Name'] == kaggle_character['Name']:
				poudlard_character.update(kaggle_character)
				poudlard_characters.append(poudlard_character)

	return poudlard_characters

def main():
	student_id = input(TEXTE_IHM)

	while student_id in ('1', '2', '3', '4', '5') or len(student_id.split(" ")) == 4:
		print(students[int(student_id) - 1] if len(student_id) == 1 else Student("personnalisé", *student_id.split(" ")))
		student_id = input("Un autre élève? ")

#          [Courage, Ambition, Intelligence, Good] -> index = Student_id - 1
STUDENTS = [[9, 2, 8, 9], [6, 7, 9, 7], [3, 8, 6, 3], [2, 3, 7, 8], [3, 4, 8, 8]]
CHARACTERS = merge("Characters.csv", "Caracteristiques_des_persos.csv")
IDX_CHARACTERS = {ch["Name"]: ch for ch in CHARACTERS}
TEXTE_IHM = """Pour quel élève souhaitez vous connaitre la maison :
Éleve 1 -> Courage : 9, Ambition : 2, Intelligence : 8, Good : 9
Éleve 2 -> Courage : 6, Ambition : 7, Intelligence : 9, Good : 7
Éleve 3 -> Courage : 3, Ambition : 8, Intelligence : 6, Good : 3
Éleve 4 -> Courage : 2, Ambition : 3, Intelligence : 7, Good : 8
Éleve 5 -> Courage : 3, Ambition : 4, Intelligence : 8, Good : 8
Vous pouvez aussi entrer des caractéristiques personnalisées sous cette forme: x x x x
Toute autre entrée terminera le programme
"""
K = 5

if __name__ == '__main__':
	students = [Student(index + 1, *attr) for index, attr in enumerate(STUDENTS)]
	main()