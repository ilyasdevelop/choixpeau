from math import sqrt
from collections import Counter
import csv

class Eleve:
	def __init__(self, *args):
		self.name, self.courage, self.ambition, self.intelligence, self.good = args
		self.distances = {personnage['Name']: self.distance(personnage) for personnage in PERSONNAGES}
		self.closest = sorted(self.distances.items(), key=lambda x: x[1], reverse=True)[:K]
		houses = Counter(ch["House"] for slctd, _ in self.closest for ch in PERSONNAGES if ch["Name"] == slctd)
		self.house = max(houses, key=houses.get)

	def __str__(self):
		return f"Éleve {self.name} est envoyé à la maison {self.house.title()}."

	def distance(self, personnage):
		return sqrt((int(self.courage) - int(personnage["Courage"])) ** 2
			+ (int(self.ambition) - int(personnage["Ambition"])) ** 2
			+ (int(self.intelligence) - int(personnage["Intelligence"])) ** 2
			+ (int(self.good) - int(personnage["Good"])) ** 2)


def merge(table_perso, caracteristique_perso):
	with open(table_perso, mode='r', encoding='utf-8') as f:
		reader = csv.DictReader(f, delimiter=";")
		characters_tab = [{key : value.replace('\xa0', ' ') for key, value in element.items()} for element in reader]

	with open(caracteristique_perso, mode='r', encoding='utf-8') as f:
		reader = csv.DictReader(f, delimiter=';')
		characteristics_tab = [{key : value for key, value in element.items()} for element in reader]

	poudlard_characters = []

	for poudlard_character in characteristics_tab:
		for kaggle_character in characters_tab:
			if poudlard_character['Name'] == kaggle_character['Name']:
				poudlard_character.update(kaggle_character)
				poudlard_characters.append(poudlard_character)

	return poudlard_characters

def main():
	eleve_id = input(TEXTE_IHM)

	while eleve_id in ('1', '2', '3', '4', '5'):
		print(eleves[int(eleve_id) - 1])
		eleve_id = input("Un autre élève? ")

#        [Courage, Ambition, Intelligence, Good] -> index = eleve_id - 1
ELEVES = [[9, 2, 8, 9], [6, 7, 9, 7], [3, 8, 6, 3], [2, 3, 7, 8], [3, 4, 8, 8]]
PERSONNAGES = merge("Characters.csv", "Caracteristiques_des_persos.csv")
TEXTE_IHM = """Pour quel élève souhaitez vous connaitre la maison :
Éleve 1 -> Courage : 9, Ambition : 2, Intelligence : 8, Good : 9
Éleve 2 -> Courage : 6, Ambition : 7, Intelligence : 9, Good : 7
Éleve 3 -> Courage : 3, Ambition : 8, Intelligence : 6, Good : 3
Éleve 4 -> Courage : 2, Ambition : 3, Intelligence : 7, Good : 8
Éleve 5 -> Courage : 3, Ambition : 4, Intelligence : 8, Good : 8
"""
K = 5

if __name__ == '__main__':
	eleves = [Eleve(index + 1, *attr) for index, attr in enumerate(ELEVES)]
	main()