import sys
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QSlider, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import character_gui
import tilemanager
import map

class SimulationViewer(QFrame):
    def __init__(self):
        super().__init__()

        # Définir la taille initiale de la fenêtre
        self.setFixedSize(800, 600)
        self.setWindowTitle("Simulation Viewer")

        # Layout principal
        self.main_layout = QVBoxLayout()

        # Section pour le score
        self.score_label = QLabel("Score : 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.score_label)

        # Section pour le numéro du tour
        self.turn_label = QLabel("Tour : 0")
        self.turn_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.turn_label)

        # Ajouter un espace vide pour le futur usage (la partie graphique avec la carte, etc.)
        self.scale_factor = 2
        self.map = map.Map()
        self.map.load_map_from_file("maps/map_0.txt")
        self.tile_manager = character_gui.TileMapManager("tiles/tilemap.png", tile_size=16, spacing=1, scale_factor=self.scale_factor)  # Chargement du tileset

        self.map_widget = character_gui.MapWidget(self.map, self.tile_manager, self.scale_factor)  # Passer le TileManager

        self.map.load_map_from_file("maps/map_0.txt")
        self.map_widget.repaint()  # Redessiner le widget avec la nouvelle carte

        self.main_layout.addWidget(self.map_widget)

        # Slider pour naviguer entre les tours (de 0 à 200)
        self.turn_slider = QSlider(Qt.Horizontal)
        self.turn_slider.setMinimum(0)
        self.turn_slider.setMaximum(200)
        self.turn_slider.setValue(0)  # Tour actuel à 0
        self.turn_slider.setTickInterval(1)
        self.turn_slider.setTickPosition(QSlider.TicksBelow)

        # Ajouter le slider à la disposition principale
        self.main_layout.addWidget(self.turn_slider)

        # Appliquer la disposition au cadre principal
        self.setLayout(self.main_layout)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    window1 = SimulationViewer()
    window1.show()

    app.exec_()
