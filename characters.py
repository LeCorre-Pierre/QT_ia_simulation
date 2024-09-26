import random

characters_debug = False


class Character:
    def __init__(self, role, x, y, movement_strategy, health=100, energy=10):
        self.role = role
        self.x = x
        self.y = y
        self.health = health
        self.energy = energy
        self.flowers = 0
        self.movement_strategy = movement_strategy
        self.last_moves = ["WAIT", "WAIT", "WAIT"]

    def reset_energy(self):
        self.energy = 10

    def clone(self):
        # Créer une copie profonde de cet objet Character
        c = Character(self.role, self.x, self.y, self.movement_strategy)
        c.health = self.health
        c.energy = self.energy
        c.flowers = self.flowers
        c.movement_strategy = self.movement_strategy
        c.last_moves = self.last_moves
        return c

    def get_pos(self):
        return self.x, self.y

    def is_full(self):
        if self.flowers >= 10:
            return True
        else:
            return False

    def collect_flower(self):
        self.flowers += 1

    def drop_flowers(self):
        self.flowers = 0

    def perform_action(self, action):
        self.last_moves.append(action)
        self.last_moves.pop(0)
        if self.energy <= 0:
            return
        """Déplace le personnage dans la direction spécifiée."""
        if action == 'UP':
            new_x, new_y = self.x, self.y - 1
        elif action == 'DOWN':
            new_x, new_y = self.x, self.y + 1
        elif action == 'LEFT':
            new_x, new_y = self.x - 1, self.y
        elif action == 'RIGHT':
            new_x, new_y = self.x + 1, self.y
        else:
            return

        self.energy -= 1
        if self.energy < 0:
            self.energy = 0
        # Vérifie si le nouveau mouvement est valide
        if self.is_valid_move(new_x, new_y):
            self.x, self.y = new_x, new_y
            if characters_debug:
                print(f"Moved to: ({self.x}, {self.y})")  # Debugging

    def is_valid_move(self, x, y):
        """Vérifie si le mouvement vers la position (x, y) est valide."""
        return self.movement_strategy.is_valid_move(x, y)
