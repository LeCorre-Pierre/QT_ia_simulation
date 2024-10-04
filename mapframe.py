from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

import tilemanager

class MapFrame(QFrame):
    def __init__(self, map_data, tile_size=32, parent=None):
        super().__init__(parent)
        self.map_data = map_data  # Les données de la carte (tableau 2D représentant les cases)
        self.tile_size = tile_size  # Taille de chaque tuile (en pixels)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Exemple : afficher une tile de personnage à la position (x=0, y=0)
        character_tile = self.tile_manager.get_character_tile(0)
        if character_tile:
            painter.drawPixmap(0, 0, character_tile)

        # Exemple : afficher une tile de carte à la position (x=50, y=50)
        map_tile = self.tile_manager.get_map_tile(5)
        if map_tile:
            painter.drawPixmap(50, 50, map_tile)

    def draw_tile(self, painter, tile, x, y):
        """
        Dessine une tuile spécifique à la position donnée.
        """
        # Pour simplifier, nous utilisons des couleurs de base pour chaque type de tuile
        if tile == 0:  # Herbe
            painter.setBrush(QColor(34, 139, 34))  # Vert pour l'herbe
        elif tile == 1:  # Eau
            painter.setBrush(QColor(0, 191, 255))  # Bleu pour l'eau
        elif tile == 2:  # Mur
            painter.setBrush(QColor(139, 69, 19))  # Marron pour le mur
        else:
            painter.setBrush(QColor(255, 255, 255))  # Par défaut, blanc pour les cases inconnues

        painter.drawRect(x, y, self.tile_size, self.tile_size)
