import random

map_debug = False

MAP_BUSH = 0
MAP_PATH = 1
MAP_GRASS_START = 2
MAP_GRASS_1 = 3
MAP_GRASS_2 = 4
MAP_GRASS_3 = 5
MAP_GRASS_4 = 6
MAP_GRASS_5 = 7
MAP_GRASS_6 = 8
MAP_GRASS_7 = 9
MAP_GRASS_8 = 10
MAP_GRASS_9 = 11
MAP_GRASS_10 = 12
MAP_GRASS_END = 13
MAP_PLANT_START = 14
MAP_PLANT_1 = 15
MAP_PLANT_2 = 16
MAP_PLANT_3 = 17
MAP_PLANT_4 = 18
MAP_PLANT_5 = 19
MAP_PLANT_6 = 20
MAP_PLANT_7 = 21
MAP_PLANT_8 = 22
MAP_PLANT_9 = 23
MAP_PLANT_10 = 24
MAP_PLANT_11 = 25
MAP_PLANT_END = 26
MAP_FLOWER_0 = 27
MAP_STARTPOINT = 28


class Map:
    def __init__(self, map_data=[]):
        self.map_size = 16
        if map_data:
            self.map_data = [row[:] for row in map_data]  # par exemple
        else:
            self.map_data = []
        self.starting_positions = None


    def clone(self):
        # Assurez-vous de copier profondément toutes les données nécessaires
        new_map = Map()
        new_map.map_data = [row[:] for row in self.map_data]  # par exemple
        return new_map

    def get_starting_positions(self):
        """
        Retourne une liste de tuples (x, y) représentant les positions de départ sur la carte.
        """
        if self.starting_positions is None:
            starting_positions = []
            for y, row in enumerate(self.map_data):
                for x, tile in enumerate(row):
                    if tile == MAP_STARTPOINT:  # MAP_STARTPOINT est la valeur qui désigne les points de départ
                        starting_positions.append((x, y))
            self.starting_positions = starting_positions
        return self.starting_positions

    def random_init(self):
        self.map_data = [[random.choice([MAP_GRASS_END, MAP_PLANT_START, MAP_PLANT_1, MAP_PLANT_2, MAP_PLANT_END, MAP_FLOWER_0]) for _ in range(self.map_size)] for _ in range(self.map_size)]

    def is_on_starting_point(self, x, y):
        """
        Vérifie si une position se trouve sur un point de départ.

        :param x: Position actuelle x
        :param y: Position actuelle y
        :return: True si la position est sur un point de départ, False sinon.
        """
        return (x, y) in self.starting_positions

    def get_tile_type(self, x, y):
        return self.map_data[y][x]

    def is_flower(self,x ,y):
        if self.map_data[y][x] == MAP_FLOWER_0:
            return True
        else:
            return False

    def cut_flower(self, x, y):
        """Coupe la fleur à la position (x, y) si elle existe et met à jour les données de la carte."""
        if self.map_data[y][x] == MAP_FLOWER_0:
            self.map_data[y][x] = MAP_GRASS_START
            if map_debug:
                print(f"Flower cut at: ({x}, {y})")  # Debugging
            return True
        return False

    def trample(self, x, y):
        """
        Réduit de 1 la valeur de la tuile si elle se trouve entre MAP_PLANT_FLOWER_0 et MAP_GRASS_0.
        :param map_data: La carte (liste 2D).
        :param row: La position de la tuile (ligne).
        :param col: La position de la tuile (colonne).
        :return: La nouvelle valeur de la tuile après piétinement.
        """
        # Vérifier si la tuile est dans la plage de valeurs concernée
        if MAP_GRASS_START <= self.map_data[y][x] <= MAP_FLOWER_0:
            self.map_data[y][x] = max(MAP_PATH, self.map_data[y][x] - 4)
            if map_debug:
                print(f"Trample at: ({x}, {y}: {max(MAP_PATH, self.map_data[y][x] - 4)})")  # Debugging

    def grow(self, map_value):
        """
        Incrémente map_value s'il est dans l'intervalle de croissance (MAP_GRASS_0 à MAP_PLANT_3).
        :param map_value: La valeur de la carte à vérifier et potentiellement incrémenter.
        :return: La nouvelle valeur de la carte après croissance.
        """
        if MAP_GRASS_START <= map_value < MAP_GRASS_END or MAP_PLANT_START <= map_value < MAP_FLOWER_0:
            return map_value + 1
        return map_value

    def grow_plant(self, row, col):
        """
        Fait pousser une plante si une tuile adjacente contient une plante entre MAP_PLANT_0 et MAP_PLANT_FLOWER_0.
        La tuile passe de MAP_GRASS_3 à MAP_PLANT_0.
        :param row: La position de la tuile (ligne).
        :param col: La position de la tuile (colonne).
        :return: La nouvelle valeur de la tuile après tentative de croissance.
        """
        # Vérifier que la tuile actuelle est bien MAP_GRASS_3
        if self.map_data[row][col] != MAP_GRASS_END:
            return self.map_data[row][col]  # Pas de changement si ce n'est pas MAP_GRASS_3

        # Définir les positions adjacentes (haut, bas, gauche, droite)
        neighbors = [
            (row - 1, col),  # haut
            (row + 1, col),  # bas
            (row, col - 1),  # gauche
            (row, col + 1)  # droite
        ]

        # Parcourir les voisins et vérifier s'il y a une plante
        for r, c in neighbors:
            if 0 <= r < len(self.map_data) and 0 <= c < len(self.map_data[0]):  # Vérifier les limites de la carte
                if self.map_data[r][c] == MAP_FLOWER_0:
                    # Si une plante est trouvée à proximité, faire pousser la tuile actuelle
                    if map_debug:
                        print(f"A new plant at: ({row}, {col}")  # Debugging
                    return MAP_PLANT_START

        # Si aucune plante n'est trouvée à proximité, ne rien changer
        return self.map_data[row][col]

    def update(self):
        """
        Itère sur toutes les cases de la carte et applique les fonctions grow et grow_plant.
        :return: La carte mise à jour.
        """
        # Créer une copie de la carte pour éviter de modifier la carte lors de l'itération
        new_map_data = [row[:] for row in self.map_data]

        for row in range(len(self.map_data)):
            for col in range(len(self.map_data[row])):
                # Appliquer grow_plant d'abord (car elle dépend des voisins)
                new_value = self.grow_plant(row, col)
                # Appliquer grow ensuite (si applicable)
                new_map_data[row][col] = self.grow(new_value)

        # Mettre à jour la carte avec les nouvelles valeurs
        self.map_data = new_map_data

    def export_map_to_file(self, file_path=""):
        """
        Exporte la carte actuelle dans un fichier texte.
        Chaque ligne du fichier texte représentera une ligne de la carte avec des valeurs séparées par des espaces.
        :param map_data: La carte à exporter (liste 2D).
        :param file_path: Chemin où le fichier texte sera sauvegardé.
        """
        # with open(file_path, 'w') as file:
        print("Export de la map courante")
        for row in self.map_data:
            # Convertir chaque ligne en chaîne de caractères avec des valeurs séparées par des espaces
            line = ' '.join(str(tile) for tile in row)
            # Écrire la ligne dans le fichier suivie d'un saut de ligne
            # file.write(line + '\n')
            print(line)

    def load_map_from_file(self, file_path):
        """
        Charge une carte depuis un fichier texte avec des valeurs séparées par des espaces et renvoie une liste 2D représentant la carte.
        Chaque ligne du fichier texte représente une ligne de la carte.
        :param file_path: Chemin vers le fichier texte.
        :return: Une liste 2D représentant la carte.
        """
        self.map_data = []

        with open(file_path, 'r') as file:
            for line in file:
                # Supprimer les espaces vides et les sauts de ligne
                line = line.strip()
                # Convertir la ligne en liste d'entiers, en séparant par des espaces
                row = [int(tile) for tile in line.split()]
                # Ajouter la ligne à la carte
                self.map_data.append(row)

