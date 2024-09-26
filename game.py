
from map import *
from characters import Character
from movement_strategy import *


class Game:
    def __init__(self, map_file, game_turn_number, characters_number=1):
        self.game_turn_number = game_turn_number
        self.map = Map()
        self.map.load_map_from_file(map_file)
        self.starting_points = self.map.get_starting_positions()
        self.characters = []
        self.score = 0
        movement_strategy = MapMovementStrategy(self.map.map_size)
        for i in range(characters_number):
            c = Character("paysan", 7, 7, movement_strategy)
            self.characters.append(c)
        self.turn_states = []

    def run(self, callback_action_selection, save=False):

        visited_positions = set()

        if save:
            self.save_state()  # état initial

        for i in range(self.game_turn_number):

            all_characters_out_of_energy = True

            self.map.update()

            for c in self.characters:
                if c.energy > 0:
                    all_characters_out_of_energy = False  # Si un personnage a encore de l'énergie
                    action = callback_action_selection(c, self.map, [], [], self.map.get_starting_positions())
                    c.perform_action(action)
                else:
                    c.perform_action("WAIT")
                x, y = c.get_pos()
                if self.map.is_flower(x, y) and not c.is_full():
                    self.map.cut_flower(x, y)
                    c.collect_flower()
                    self.score += 10
                else:
                    self.map.trample(x, y)

                if (x, y) not in visited_positions:
                    visited_positions.add((x, y))
                    self.score += 10  # Récompense pour avoir exploré une nouvelle position

                if self.map.is_on_starting_point(x, y):
                    "Reset de l'énergie du personnage et dépose des fleur contre des points"
                    c.reset_energy()
                    if c.flowers:
                        self.score += c.flowers * 100
                        c.drop_flowers()

            # Sauvegarder l'état après chaque tour
            if save:
                self.save_state()

            # Si tous les personnages sont à court d'énergie, on arrête la simulation
            if all_characters_out_of_energy:
                break
        # La fitness de l'individu est basée sur le score du jeu
        fitness = self.score

        return fitness,




        self.save_state() #état initial
        for i in range(self.game_turn_number):
            self.map.update()
            for c in self.characters:
                c.update()
                x, y = c.get_pos()
                if self.map.is_flower(x,y) and not c.is_full():
                    self.map.cut_flower(x, y)
                    c.collect_flower()
                else:
                    self.map.trample(x, y)

                if self.map.is_on_starting_point(x,y):
                    self.score += c.energy
                    c.drop_flowers()
            # Sauvegarder l'état après chaque tour
            self.save_state()

    def save_state(self, score, input_vector):
        """
        Sauvegarde l'état actuel de la carte et des personnages pour le rejouer plus tard.
        """
        # Sauvegarder une copie de la carte (en supposant que la classe Map a une méthode clone)
        map_state = self.map.clone()

        # Sauvegarder une copie de chaque personnage (en supposant que la classe Character a une méthode clone)
        characters_state = [c.clone() for c in self.characters]

        # Ajouter l'état actuel à la liste des états
        self.turn_states.append((map_state, characters_state, score, input_vector))

    def __str__(self):
        """Retourne une représentation sous forme de chaîne de caractères de l'état du jeu, incluant le score."""
        return f"Game Score: {self.score}"