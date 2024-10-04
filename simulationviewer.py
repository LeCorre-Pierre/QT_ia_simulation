import sys
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QSlider, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

import tilemanager

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
        #self.game_frame = mapframe.MapFrame(self)
        #self.game_frame.setFrameShape(QFrame.StyledPanel)  # Un cadre simple pour l'instant
        #self.game_frame.setFixedSize(600, 400)  # Ajuste la taille selon tes besoins
        #self.main_layout.addWidget(self.game_frame)

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
    global_tilemanager = tilemanager.TileManager()
    global_tilemanager.load_character_tiles("tiles/roguelikeChar_transparent.png")
    global_tilemanager.load_map_tiles("tiles/roguelikeMap_transparent.png")
    app = QApplication(sys.argv)
    viewer = SimulationViewer()
    viewer.show()
    sys.exit(app.exec_())
