# Description du réseau de neurone
## Entrées:     58
## 1er niveau:  32
## 2eme niveau: 16
## Sortie:      5
from characters import *
from map import *
import numpy as np
from game import *
from neural_network import *

NNC_INPUT_WEIGHT_NUMBER = 33
NNC_HIDDEN_LAYER_1_WEIGHT_NUMBER = 32
NNC_HIDDEN_LAYER_2_WEIGHT_NUMBER = 32
NNC_OUTPUT_WEIGHT_NUMBER = 5
NNC_BIAS_HIDDEN_LAYER_1 = 32
NNC_BIAS_HIDDEN_LAYER_2 = 32
NNC_BIAS_OUTPUT = 5
NNC_TOTAL_WEIGHT_NUMBER = (
        NNC_INPUT_WEIGHT_NUMBER * NNC_HIDDEN_LAYER_1_WEIGHT_NUMBER
        + NNC_HIDDEN_LAYER_1_WEIGHT_NUMBER * NNC_HIDDEN_LAYER_2_WEIGHT_NUMBER
        + NNC_HIDDEN_LAYER_2_WEIGHT_NUMBER * NNC_OUTPUT_WEIGHT_NUMBER
        + NNC_BIAS_HIDDEN_LAYER_1 + NNC_BIAS_HIDDEN_LAYER_2 + NNC_BIAS_OUTPUT
)

STATE_BUSH = 0
STATE_PATH = 1
STATE_GRASS = 2
STATE_PLANT = 3
STATE_FLOWER = 4
STATE_STARTPOINT = 5

STATE_CHAR_NO = 0
STATE_CHAR_ALLY = 1
STATE_CHAR_ENEMY = 2

actions = ["UP", "RIGHT", "DOWN", "LEFT", "WAIT"]


def to_map_state(m: Map, x: int, y: int):
    """
    This function considers the position of the character to return a subset of the map.
    This result is directly passed to the neural network.
    The following simplifications are applied:
        STATE_BUSH correspond to MAP_BUSH
        1 correspond to MAP_PATH
        2 correspond to MAP_GRASS_START to MAP_GRASS_END
        3 correspond to MAP_PLANT_START to MAP_PLANT_END
        4 correspond to MAP_FLOWER_0
        5 correspond to MAP_STARTPOINT
    :param m: The current map
    :param x: The x position of the character
    :param y: The y position of the character
    :return: The map state to be passed to the neural network
    """
    # Dimensions de la grille à extraire (5x5)
    grid_size = 5
    half_size = grid_size // 2

    map_state = []

    for i in range(-half_size, half_size + 1):
        for j in range(-half_size, half_size + 1):
            # Calculer les coordonnées dans la carte
            nx, ny = x + i, y + j

            # Si les coordonnées sont hors limites, ajouter une valeur par défaut (ex: obstacle/bord de la carte)
            if nx < 0 or nx >= m.map_size or ny < 0 or ny >= m.map_size:
                map_state.append(STATE_BUSH)  # Par exemple, 0 pour MAP_BUSH
            else:
                # Obtenir le type de tuile à cette position
                tile_type = m.get_tile_type(nx, ny)

                # Appliquer la simplification des états
                if tile_type == MAP_BUSH:
                    map_state.append(STATE_BUSH)
                elif tile_type == MAP_PATH:
                    map_state.append(STATE_PATH)
                elif MAP_GRASS_START <= tile_type <= MAP_GRASS_END:
                    map_state.append(STATE_GRASS)
                elif MAP_PLANT_START <= tile_type <= MAP_PLANT_END:
                    map_state.append(STATE_PLANT)
                elif tile_type == MAP_FLOWER_0:
                    map_state.append(STATE_FLOWER)
                elif tile_type == MAP_STARTPOINT:
                    map_state.append(STATE_BUSH)
                else:
                    map_state.append(STATE_BUSH)  # Valeur par défaut si aucune correspondance

    return map_state


def to_friends_enemies(x: int, y: int, allies, enemies):
    """
    This function considers the position of the character and returns a 5x5 subset of the map
    indicating the presence of allies and enemies.

    The following simplifications are applied:
        STATE_CHAR_NO corresponds to no character present
        STATE_CHAR_ALLY corresponds to an ally present
        STATE_CHAR_ENEMY corresponds to an enemy present
    :param x: The x position of the character
    :param y: The y position of the character
    :param allies: List of Character objects representing allies
    :param enemies: List of Character objects representing enemies
    :return: A list representing the 5x5 state of characters around the given position
    """

    grid_size = 5
    half_size = grid_size // 2

    # Initialiser la grille 5x5 avec 0 (aucun personnage)
    friends_enemies = [STATE_CHAR_NO] * (grid_size * grid_size)
    return friends_enemies

    # Remplir la grille avec les alliés et les ennemis
    for i in range(-half_size, half_size + 1):
        for j in range(-half_size, half_size + 1):
            # Calculer les coordonnées relatives dans la grille
            grid_x = i + half_size
            grid_y = j + half_size
            index = grid_y * grid_size + grid_x

            # Calculer les coordonnées absolues sur la carte
            nx, ny = x + i, y + j

            # Vérifier si un allié est présent à cette position
            if any((ally.get_pos() == (nx, ny)) for ally in allies):
                friends_enemies[index] = STATE_CHAR_ALLY
            # Vérifier si un ennemi est présent à cette position
            elif any((enemy.get_pos() == (nx, ny)) for enemy in enemies):
                friends_enemies[index] = STATE_CHAR_ENEMY
            # Sinon, laisser la valeur par défaut (aucun personnage)

    return friends_enemies


def get_delta_to_closest_start(x, y, starting_positions):
    """
    Retourne le delta (dx, dy) vers le point de départ le plus proche.
    Optimisé pour les cas où il y a un seul point de départ.

    :param x: Position actuelle x du personnage.
    :param y: Position actuelle y du personnage.
    :param starting_positions: Liste des positions de départ sous forme de tuples (x, y).
    :return: Tuple (dx, dy) représentant la différence entre la position actuelle et la position de départ la plus proche.
    """
    # Si la liste contient un seul point de départ
    if len(starting_positions) == 1:
        start_x, start_y = starting_positions[0]
        return start_x - x, start_y - y

    # Sinon, on cherche le point de départ le plus proche
    closest_start = None
    min_distance = float('inf')

    for start_x, start_y in starting_positions:
        distance = (start_x - x) ** 2 + (start_y - y) ** 2  # Utiliser la distance au carré (évite l'appel à sqrt)
        if distance < min_distance:
            min_distance = distance
            closest_start = (start_x, start_y)

    if closest_start:
        dx = closest_start[0] - x
        dy = closest_start[1] - y
        return dx, dy
    else:
        return None  # Aucun point de départ trouvé


def get_input_vector(c: Character, m: Map, starting_positions):
    (x, y) = c.get_pos()
    map_state = to_map_state(m, x, y)
    #friends_enemies = to_friends_enemies(x, y, allies, enemies)
    dx, dy = get_delta_to_closest_start(x, y, starting_positions)
    flower_stock = c.flowers
    health = 0
    energy = c.energy
    action_indices = [actions.index(action) for action in c.last_moves]
    # Construire le vecteur d'entrée pour le réseau de neurones
    #return map_state + friends_enemies + [dx, dy] + [flower_stock] + [health, energy] + action_indices
    return map_state + [dx, dy] + [flower_stock] + [health, energy] + action_indices


def map_action(action_index):
    """
    Mappe la sortie du réseau neuronal à une action concrète.
    """
    return actions[action_index]


class NeuralNetworkController:
    def __init__(self, input_layer_size=33, hidden_layer_1_size=32, hidden_layer_2_size=32, output_layer_size=5):
        self.neural_network = NeuralNetwork(input_layer_size, hidden_layer_1_size, hidden_layer_2_size, output_layer_size)
        self.input_size = input_layer_size
        self.hidden_size_1 = hidden_layer_1_size
        self.hidden_size_2 = hidden_layer_2_size
        self.output_size = output_layer_size

    def update_weights(self, weights):
        input_size = self.input_size
        hidden_size_1 = self.hidden_size_1
        hidden_size_2 = self.hidden_size_2
        output_size = self.output_size

        end_w1 = input_size * hidden_size_1
        end_w2 = end_w1 + hidden_size_1 * hidden_size_2
        end_w3 = end_w2 + hidden_size_2 * output_size

        # Assurez-vous que les longueurs sont correctes
        assert len(weights) == end_w3 + hidden_size_1 + hidden_size_2 + output_size

        W1 = np.array(weights[:end_w1]).reshape((input_size, hidden_size_1))
        W2 = np.array(weights[end_w1:end_w2]).reshape((hidden_size_1, hidden_size_2))
        W3 = np.array(weights[end_w2:end_w3]).reshape((hidden_size_2, output_size))

        b1 = np.array(weights[end_w3:end_w3 + hidden_size_1]).reshape((hidden_size_1,))
        b2 = np.array(weights[end_w3 + hidden_size_1:end_w3 + hidden_size_1 + hidden_size_2]).reshape((hidden_size_2,))
        b3 = np.array(weights[end_w3 + hidden_size_1 + hidden_size_2:]).reshape((output_size,))

        self.neural_network.set_weights([W1, W2, W3, b1, b2, b3])

    def decide_action(self, c: Character, m: Map, starting_positions):
        input_vector = get_input_vector(c, m, starting_positions)
        # Obtenir l'action du réseau de neurones
        output_vector = self.neural_network.predict(input_vector)
        # Trouver l'index de l'action avec la valeur la plus élevée (argmax)
        action_index = np.argmax(output_vector)
        # Mapper l'index à une action
        action = actions[action_index]
        return action

    def randomize_map(self, map_data):
        return map.randomize(map_data)

    def evaluate(self, map_data, nb_turn_per_simulation, nb_characters, callback_action_selection=decide_action, start_pos=(7,7)):
        """
        Évalue un individu en simulant une partie et en calculant un score basé sur la performance.
        """

        # Créer une instance de la classe Game avec les paramètres donnés
        game = Game(map_data, nb_turn_per_simulation, nb_characters, start_pos)

        # Exécuter la simulation du jeu
        fitness = game.run(self, callback_action_selection)

        return fitness

if __name__ == "__main__":
    m = Map()
    m.load_map_from_file("maps/map_0.txt")
    state_1 = to_map_state(m, 0, 0)
    state_2 = to_map_state(m, 6, 6)
    state_3 = to_map_state(m, 0, 12)
    state_4 = to_map_state(m, 4, 4)
    print("State4")
    print(str(state_4))
    # Création d'exemples de personnages
    allies = [Character("Ally1", 4, 5, None), Character("Ally2", 6, 6, None)]
    enemies = [Character("Enemy1", 5, 6, None), Character("Enemy2", 7, 7, None)]

    # Position du personnage central
    c = Character("Paysan", 5, 5, None)
    x, y = c.get_pos()

    input_vector = get_input_vector(c, m, [(5,7)])
    print(input_vector)
