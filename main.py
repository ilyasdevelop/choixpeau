from math import sqrt
from collections import Counter
import csv

class Student:
	"""
	Représente un étudiant dans le monde des sorciers, affecté à une maison en fonction de ses traits de personnalité.

	Attributs:
		name (str): Le nom de l'étudiant.
		courage (int): Le niveau de courage de l'étudiant.
		ambition (int): Le niveau d'ambition de l'étudiant.
		intelligence (int): Le niveau d'intelligence de l'étudiant.
		good (int): Le niveau de bonté de l'étudiant.
		distances (dict): Un dictionnaire contenant les distances entre l'étudiant et les autres personnages.
		closest (list): Une liste des personnages les plus proches triés par distance.
		house (str): La maison assignée à l'étudiant.

	Méthodes:
		__init__: Initialise une nouvelle instance de la classe Eleve.
		__str__: Retourne une représentation en chaîne de caractères de l'étudiant et de sa maison attribuée.
		distance: Calcule la distance euclidienne entre l'étudiant et un personnage donné en fonction de ses traits.
	"""
	def __init__(self, *args):
		"""
		Initialise un objet Student avec des attributs spécifiques et calcule les distances et voisins.

		Entrée:
		- args (tuple): Les caractéristiques de l'élève (nom, courage, ambition, intelligence, good).

		Sortie:
		Aucune.
		"""

		self.name, self.courage, self.ambition, self.intelligence, self.good = args
		self.distances = {ch['Name']: {"Distance": self.distance(ch), "House": ch["House"]} for ch in CHARACTERS}
		self.closests = sorted(self.distances.items(), key=lambda x: x[1]["Distance"])[:K]
		self.text_closests = '\n'.join([f'{BLUE}{name}{RESET} dans la maison {BLUE}{attr["House"]}{RESET}' for name, attr in self.closests])

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
		"""
		Formate l'objet Student en une chaîne de caractères.

		Entrée:
		Aucune.

		Sortie:
		- str: La représentation en chaîne de caractères de l'objet Student.
		"""
		return f"Élève {self.name} est envoyé à la maison {self.house.title()}{RESET}.\nSes 5 plus proches voisins sont, dans l'ordre:\n{self.text_closests}"

	def distance(self, character: dict) -> float:
		"""
		Calcule la distance euclidienne entre l'élève et un personnage donné.

		Entrée:
		- character (dict): Les caractéristiques du personnage.

		Sortie:
		- float: La distance euclidienne.
		"""
		return sqrt((int(self.courage) - int(character["Courage"])) ** 2
			+ (int(self.ambition) - int(character["Ambition"])) ** 2
			+ (int(self.intelligence) - int(character["Intelligence"])) ** 2
			+ (int(self.good) - int(character["Good"])) ** 2)


def read_csv(file: str) -> list[dict]:
	"""
	Fonction permettant simplement de lire un fichier csv et de former une table a partir de ce fichier

	Entrée:
	- file (str) : le nom du fichier qu'on souhaite ouvrir

	Sortie :
	- une table (dict) : le csv transformé en table
	"""
	with open(file, mode='r', encoding='utf-8') as f:
		reader = csv.DictReader(f, delimiter=";")
		return [{key : value.replace('\xa0', ' ') for key, value in element.items()} for element in reader]

def merge(characters: str, attributes: str) -> list[dict]:
	"""
	Fusionne les données de deux fichiers CSV en fonction du nom et retourne une liste de dictionnaires.

	Entrée:
	- characters (str): Le chemin du fichier CSV contenant les personnages.
	- attributes (str): Le chemin du fichier CSV contenant les caractéristiques des personnages.

	Sortie:
	- list[dict]: La liste des dictionnaires représentant les personnages avec leurs caractéristiques.
	"""
	poudlard_characters = []

	for poudlard_character in read_csv(attributes):
		for kaggle_character in read_csv(characters):
			if poudlard_character['Name'] == kaggle_character['Name']:
				poudlard_character.update(kaggle_character)
				poudlard_characters.append(poudlard_character)

	return poudlard_characters

def main():
	"""
	Fonction principale du programme qui gère l'interaction utilisateur.

	Entrée:
	Aucune.

	Sortie:
	Aucune.
	"""
	print(TEXTE_IHM, end="")
	student_id = input()

	while student_id in ('1', '2', '3', '4', '5') or len(student_id.split(" ")) == 4:
		print(students[int(student_id) - 1] if len(student_id) == 1 else Student("personnalisé", *student_id.split(" ")))
		student_id = input(f"{YELLOW}>>> Éleve n°")
	
	print("Au revoir!")

#          [Courage, Ambition, Intelligence, Good] -> index = Student_id - 1
STUDENTS = [[9, 2, 8, 9], [6, 7, 9, 7], [3, 8, 6, 3], [2, 3, 7, 8], [3, 4, 8, 8]]
CHARACTERS = merge("Characters.csv", "Caracteristiques_des_persos.csv")
IDX_CHARACTERS = {ch["Name"]: ch for ch in CHARACTERS}
BLUE, YELLOW, RED, RESET = '\033[94m', '\033[1;33m', '\033[1;31m', '\033[0m'
TEXTE_IHM = f"""
{RED} _______  __   __  _______  ___   __   __  _______  _______  _______  __   __ 
|       ||  | |  ||       ||   | |  |_|  ||       ||       ||   _   ||  | |  |
|       ||  |_|  ||   _   ||   | |       ||    _  ||    ___||  |_|  ||  | |  |
|       ||       ||  | |  ||   | |       ||   |_| ||   |___ |       ||  |_|  |
|      _||       ||  |_|  ||   |  |     | |    ___||    ___||       ||       |
|     |_ |   _   ||       ||   | |   _   ||   |    |   |___ |   _   ||       |
|_______||__| |__||_______||___| |__| |__||___|    |_______||__| |__||_______|
Par BEN GRINE Thibault, LALAUDE Martin, KASSAMALY Irwan, MARHRAOUI Ilyas{RESET}

Pour quel élève souhaitez vous connaitre la maison ?
Éleve {YELLOW}1{RESET} -> Courage : {BLUE}9{RESET}, Ambition : {BLUE}2{RESET}, Intelligence : {BLUE}8{RESET}, Good : {BLUE}9{RESET}
Éleve {YELLOW}2{RESET} -> Courage : {BLUE}6{RESET}, Ambition : {BLUE}7{RESET}, Intelligence : {BLUE}9{RESET}, Good : {BLUE}7{RESET}
Éleve {YELLOW}3{RESET} -> Courage : {BLUE}3{RESET}, Ambition : {BLUE}8{RESET}, Intelligence : {BLUE}6{RESET}, Good : {BLUE}3{RESET}
Éleve {YELLOW}4{RESET} -> Courage : {BLUE}2{RESET}, Ambition : {BLUE}3{RESET}, Intelligence : {BLUE}7{RESET}, Good : {BLUE}8{RESET}
Éleve {YELLOW}5{RESET} -> Courage : {BLUE}3{RESET}, Ambition : {BLUE}4{RESET}, Intelligence : {BLUE}8{RESET}, Good : {BLUE}8{RESET}
Vous pouvez aussi entrer des caractéristiques personnalisées sous cette forme: {YELLOW}x x x x{RESET}
Toute autre entrée terminera le programme
{YELLOW}>>> Éleve n°""" # Pas de reset pour garder la couleur pour l'entrée et jusqu'à la prochaine ligne
K = 5

if __name__ == '__main__':
	students = [Student(index + 1, *attr) for index, attr in enumerate(STUDENTS)]
	main()