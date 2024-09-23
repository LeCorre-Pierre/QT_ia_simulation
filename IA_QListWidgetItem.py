from PyQt5.QtWidgets import (
    QListWidgetItem
)
import ast  # Pour convertir la représentation string en liste ou autre structure

def load_from_file(filename):
    try:
        with open(filename, 'r') as f:
            ia_data = f.read()  # Lire le contenu du fichier

            # Convertir les données en une structure appropriée (par exemple, liste de poids)
            try:
                ia_values = ast.literal_eval(ia_data)  # Si c'est une liste de nombres dans le fichier
            except ValueError as ve:
                print(f"Erreur de conversion des données d'IA: {ve}")
                return None

            # Vérification de la validité des données
            if not isinstance(ia_values, (list, tuple)) or not all(isinstance(x, (int, float)) for x in ia_values):
                print(f"Les données de l'IA ne sont pas valides : {ia_values}")
                return None

            fitness = extract_fitness_from_filename(filename)  # Extraire le fitness du nom du fichier
            item = IAListWidgetItem(ia_values, fitness)  # Créer un nouvel item avec les données numériques
            return item

    except Exception as e:
        print(f"Erreur lors du chargement de l'IA depuis le fichier: {e}")
        return None


def extract_fitness_from_filename(filename):
    # Supposons que le nom du fichier a un format comme "ia_<fitness>.txt"
    base_name = filename.split('/')[-1]  # Extraire le nom de base
    fitness_str = base_name.split('_')[2].replace('.txt', '')  # Récupérer la partie du fitness
    return float(fitness_str)  # Convertir en float


class IAListWidgetItem(QListWidgetItem):
    def __init__(self, individual, fitness):
        # Initialiser l'élément avec un label "ia_58-32-32-5_<fitness_value>"
        super().__init__(f"ia_58-32-32-5_{fitness:.2f}")
        # Stocker l'individu dans l'objet
        self.individual = individual # Values as used by DEAP algorythm
        self.fitness = fitness

    def get_individual(self):
        """Retourner l'individu associé à cet item."""
        return self.individual

    def get_fitness(self):
        """Retourner le fitness associé à cet item."""
        return self.fitness

    def save_to_file(self):
        filename = f"ias/ia_58-32-32-5_{self.fitness:.2f}.txt"
        with open(filename, 'w') as f:
            f.write(str(self.individual))  # Sauvegarder les données de l'IA dans un fichier

