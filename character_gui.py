import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QPushButton, QWidget, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt

class TileManager:
    def __init__(self, tilesheet_path, tile_size=16, spacing=1):
        self.tile_size = tile_size
        self.spacing = spacing
        self.tilesheet = QImage(tilesheet_path)
        self.tiles = self.load_tiles()

    def load_tiles(self):
        """Charge toutes les tuiles à partir du tileset."""
        tiles = []
        tilesheet_width = self.tilesheet.width()
        tilesheet_height = self.tilesheet.height()

        # Calculer le nombre de colonnes et de rangées
        cols = (tilesheet_width + self.spacing) // (self.tile_size + self.spacing)
        rows = (tilesheet_height + self.spacing) // (self.tile_size + self.spacing)

        for row in range(rows):
            for col in range(cols):
                x = col * (self.tile_size + self.spacing)
                y = row * (self.tile_size + self.spacing)
                tile = self.tilesheet.copy(x, y, self.tile_size, self.tile_size)
                tiles.append(QPixmap(tile))  # Utiliser QPixmap pour une meilleure performance
        return tiles

    def get_tile(self, index):
        """Renvoie la tuile correspondant à l'index."""
        return self.tiles[index] if 0 <= index < len(self.tiles) else None

class Map:
    def __init__(self, map_data=None):
        self.map_size = 16
        self.map_data = map_data if map_data is not None else []
        self.starting_positions = None

    def load_map_from_file(self, file_path):
        """Charge la carte à partir d'un fichier."""
        with open(file_path, 'r') as file:
            self.map_data = [list(map(int, line.strip().split())) for line in file.readlines()]

class MapWidget(QFrame):
    def __init__(self, game_map, tile_manager):
        super().__init__()
        self.game_map = game_map
        self.tile_manager = tile_manager
        self.setMinimumSize(400, 400)  # Taille minimum du widget

    def paintEvent(self, event):
        painter = QPainter(self)
        border_size = 2
        tile_size = self.tile_manager.tile_size
        map_width = len(self.game_map.map_data[0]) * tile_size
        map_height = len(self.game_map.map_data) * tile_size

        # Dessiner le fond
        painter.fillRect(event.rect(), Qt.white)  # Remplir le fond en blanc

        # Dessiner les tuiles de la carte
        for row_index, row in enumerate(self.game_map.map_data):
            for col_index, map_value in enumerate(row):
                tile_index = map_value  # Supposer que la valeur correspond à l'index de la tuile
                tile = self.tile_manager.get_tile(tile_index)
                if tile:
                    x = col_index * tile_size
                    y = row_index * tile_size
                    painter.drawPixmap(x, y, tile)  # Dessiner la tuile

        # Dessiner les lignes de la grille
        grid_color = Qt.lightGray
        for i in range(len(self.game_map.map_data) + 1):
            painter.setPen(grid_color)
            painter.drawLine(i * tile_size, 0, i * tile_size, map_height)
            painter.drawLine(0, i * tile_size, map_width, i * tile_size)

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Afficher la carte")
        self.setGeometry(100, 100, 600, 600)

        self.map = Map()
        self.tile_manager = TileManager("tiles/tilemap.png", tile_size=16, spacing=1)  # Chargement du tileset

        self.map_widget = MapWidget(self.map, self.tile_manager)  # Passer le TileManager

        self.load_map()

        layout = QVBoxLayout()
        layout.addWidget(self.map_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_map(self):
        self.map.load_map_from_file("maps/map_0.txt")
        self.map_widget.repaint()  # Redessiner le widget avec la nouvelle carte

if __name__ == "__main__":
    app = QApplication([])
    window = MapWindow()
    window.show()
    app.exec_()
