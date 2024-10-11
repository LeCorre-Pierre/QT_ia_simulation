import os
from PyQt5.QtWidgets import QApplication, QMainWindow,QLabel, QSlider, QFrame, QVBoxLayout, QPushButton, QWidget, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt
from map import *
import sys


class TileCharacterManager:
    def __init__(self, file_name, tile_width, tile_height, spacing=1, scale_factor=10):
        self.tileset_image = QImage(file_name)
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.spacing = spacing
        self.scale_factor = scale_factor

        # Load prefab characters (row 0, column 5 to row 1, column 11) with lines and columns inverted
        self.prefab_characters = self.load_tiles(0, 5, 1, 11)

    def load_tiles(self, col_start, row_start, col_end, row_end):
        tiles = []
        for col in range(col_start, col_end + 1):
            for row in range(row_start, row_end + 1):
                x = col * (self.tile_width + self.spacing)
                y = row * (self.tile_height + self.spacing)
                tile = self.tileset_image.copy(x, y, self.tile_width, self.tile_height)

                # Scale the tile by the factor
                tile = tile.scaled(self.tile_width * self.scale_factor,
                                   self.tile_height * self.scale_factor,
                                   Qt.KeepAspectRatio)

                tiles.append(QPixmap.fromImage(tile))
        return tiles


class CharacterDisplayWidget(QLabel):
    def __init__(self, tile_manager, parent=None):
        super().__init__(parent)
        self.tile_manager = tile_manager
        self.current_index = 0
        self.update_character()

    def update_character(self):
        self.setPixmap(self.tile_manager.prefab_characters[self.current_index])

    def set_character(self, index):
        self.current_index = index
        self.update_character()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Prefab Character Viewer")
        self.setGeometry(200, 200, 640, 640)  # Ajuster la taille de la fenêtre

        # Tile Manager avec facteur d'agrandissement 10 et marge de 1 pixel
        self.tile_manager = TileCharacterManager("tiles/roguelikeChar_transparent.png", 16, 16, spacing=1, scale_factor=10)

        # Character Display Widget
        self.character_display = CharacterDisplayWidget(self.tile_manager)

        # Slider to change characters
        self.char_slider = QSlider(Qt.Horizontal)
        self.char_slider.setMaximum(len(self.tile_manager.prefab_characters) - 1)
        self.char_slider.valueChanged.connect(self.character_display.set_character)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.character_display)
        layout.addWidget(self.char_slider)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

class TileMapManager:
    def __init__(self, tilesheet_path, tile_size=16, spacing=1, scale_factor=6):
        self.tile_size = tile_size
        self.spacing = spacing
        self.tilesheet = QImage(tilesheet_path)
        self.scale_factor = scale_factor
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

                # Scale the tile by the factor
                tile = tile.scaled(self.tile_size * self.scale_factor,
                                   self.tile_size * self.scale_factor,
                                   Qt.KeepAspectRatio)

                tiles.append(QPixmap.fromImage(tile))
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
    def __init__(self, game_map, tile_manager, scale_factor=6):
        super().__init__()
        self.game_map = game_map
        self.tile_manager = tile_manager
        self.border_size = 3
        self.intertilespace_size = 1
        tile_size = self.tile_manager.tile_size * scale_factor
        map_cell_nb_width = len(self.game_map.map_data[0])
        map_cell_nb_height = len(self.game_map.map_data)
        self.map_width = map_cell_nb_width * tile_size + (map_cell_nb_width - 1 ) * self.intertilespace_size + self.border_size * 2
        self.map_height = map_cell_nb_height * tile_size + (map_cell_nb_height - 1 ) * self.intertilespace_size + self.border_size * 2
        self.setMinimumSize(self.map_width, self.map_height)  # Taille minimum du widget
        self.setMaximumSize(self.map_width, self.map_height)
        self.scale_factor = scale_factor

    def paintEvent(self, event):
        painter = QPainter(self)
        tile_size = self.tile_manager.tile_size * self.scale_factor
        # Size = nb cell * size + interline nb * size + 2 borders

        # Dessiner le fond
        painter.fillRect(event.rect(), Qt.lightGray)  # Remplir le fond en blanc

        # Dessiner le tour
        pen = QPen(Qt.black, self.border_size, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(1, 1, self.map_width-1, 1)
        painter.drawLine(1, 1, 1, self.map_height-1)
        painter.drawLine(self.map_width-1, 1, self.map_width-1, self.map_height-1)
        painter.drawLine(1, self.map_height-1, self.map_width-1, self.map_height-1)

        # Dessiner les tuiles de la carte
        for row_index, row in enumerate(self.game_map.map_data):
            for col_index, map_value in enumerate(row):
                tile_index = tile_mapping.get(map_value)
                tile = self.tile_manager.get_tile(tile_index)
                if tile:
                    x = 4 + col_index * (tile_size + 1)
                    y = 4 + row_index * (tile_size + 1 )
                    painter.drawPixmap(x, y, tile)  # Dessiner la tuile

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Afficher la carte")
        self.setGeometry(100, 100, 600, 600)
        self.scale_factor = 2
        self.map = Map()
        self.map.load_map_from_file("maps/map_0.txt")
        self.tile_manager = TileMapManager("tiles/tilemap.png", tile_size=16, spacing=1, scale_factor=self.scale_factor)  # Chargement du tileset

        self.map_widget = MapWidget(self.map, self.tile_manager, self.scale_factor)  # Passer le TileManager

        self.load_map()

        layout = QVBoxLayout()
        layout.addWidget(self.map_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_map(self):
        self.map.load_map_from_file("maps/map_0.txt")
        self.map_widget.repaint()  # Redessiner le widget avec la nouvelle carte

TILE_GRASS_0 = 0
TILE_GRASS_1 = 1
TILE_GRASS_2 = 2
TILE_PATH = 43
TILE_BUSH = 102 # 6 + 8 x 12
TILE_START = 107 # 11 + 8 x 12

tile_mapping = {
    MAP_BUSH: TILE_BUSH,
    MAP_PATH: TILE_PATH,

    # Les différentes tuiles d'herbe
    MAP_GRASS_START: TILE_GRASS_0,
    MAP_GRASS_1: TILE_GRASS_0,
    MAP_GRASS_2: TILE_GRASS_0,
    MAP_GRASS_3: TILE_GRASS_0,  # Ajoutez si TILE_GRASS_0 est la bonne tuile pour toutes ces valeurs
    MAP_GRASS_4: TILE_GRASS_0,  # Ajoutez si TILE_GRASS_0 est la bonne tuile pour toutes ces valeurs
    MAP_GRASS_5: TILE_GRASS_0,
    MAP_GRASS_6: TILE_GRASS_0,
    MAP_GRASS_7: TILE_GRASS_0,
    MAP_GRASS_8: TILE_GRASS_0,
    MAP_GRASS_9: TILE_GRASS_0,
    MAP_GRASS_10: TILE_GRASS_0,
    MAP_GRASS_END: TILE_GRASS_0,

    # Les différentes tuiles de plantes
    MAP_PLANT_START: TILE_GRASS_1,
    MAP_PLANT_1: TILE_GRASS_1,
    MAP_PLANT_2: TILE_GRASS_1,
    MAP_PLANT_3: TILE_GRASS_1,  # Ajoutez si TILE_GRASS_1 est la bonne tuile pour toutes ces valeurs
    MAP_PLANT_4: TILE_GRASS_1,
    MAP_PLANT_5: TILE_GRASS_1,
    MAP_PLANT_6: TILE_GRASS_1,
    MAP_PLANT_7: TILE_GRASS_1,
    MAP_PLANT_8: TILE_GRASS_1,
    MAP_PLANT_9: TILE_GRASS_1,
    MAP_PLANT_10: TILE_GRASS_1,
    MAP_PLANT_11: TILE_GRASS_1,
    MAP_PLANT_END: TILE_GRASS_1,

    MAP_FLOWER_0: TILE_GRASS_2,
    MAP_STARTPOINT: TILE_START
}

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window1 = MainWindow()
    window1.show()

    window2 = MapWindow()
    window2.show()
    app.exec_()
