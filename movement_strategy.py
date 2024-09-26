class MovementStrategy:
    def is_valid_move(self, x, y):
        raise NotImplementedError("This method should be overridden by subclasses.")


class MapMovementStrategy(MovementStrategy):
    def __init__(self, map_size):
        self.map_size = map_size

    def is_valid_move(self, x, y):
        """Vérifie si le mouvement vers la position (x, y) est valide en fonction de la taille de la carte."""
        return 0 <= x < self.map_size and 0 <= y < self.map_size
