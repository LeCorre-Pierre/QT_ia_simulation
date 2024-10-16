from PyQt5.QtWidgets import (
    QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QFileDialog, QMessageBox
)
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QMouseEvent, QPen
import random
import map
import character_gui
import os
import characters
import neural_network_controller
from movement_strategy import *
from neural_network_controller import *

class InfiniteGameFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Variables de jeu
        self.map = map.Map()
        self.map.load_map_from_file("maps/map_0.txt")
        self.characters = []  # Liste des personnages ajoutés par l'utilisateur
        self.selected_ia = None  # IA sélectionnée pour contrôler les personnages
        self.is_paused = False  # Etat de pause
        self.grid_size = 16

        # Gestion du temps de défilement
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_map)
        self.timer_interval = 500  # Intervalle initial (500ms)
        self.timer.start(self.timer_interval)

        self.scale_factor = 2
        self.tile_manager = character_gui.TileMapManager("tiles/tilemap.png", tile_size=16, spacing=1, scale_factor=self.scale_factor)  # Chargement du tileset
        self.tilechar_manager = character_gui.TileCharacterManager("tiles/roguelikeChar_transparent.png", 16, 16, spacing=1, scale_factor=self.scale_factor)
        self.tick_count = 0  # Compteur pour les ticks du timer
        self.characters = []
        self.movement_strategy = MapMovementStrategy(self.map.map_size)

        # Initialisation des composants
        self.initUI()
        self.nn_controller = neural_network_controller.NeuralNetworkController(58, 32, 32, 5)

    def initUI(self):
        # Layout principal
        layout = QVBoxLayout(self)

        # Haut de la fenêtre : Boutons et slider
        top_layout = QHBoxLayout()

        # Bouton Reset
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_map)
        top_layout.addWidget(self.reset_button)

        # Bouton pour sélectionner une carte
        self.select_map_button = QPushButton("Sélectionner Carte")
        self.select_map_button.clicked.connect(self.select_map)
        top_layout.addWidget(self.select_map_button)

        # Slider pour régler la vitesse
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(100)
        self.speed_slider.setMaximum(1000)
        self.speed_slider.setTickInterval(200)
        self.speed_slider.setValue(self.timer_interval)
        self.speed_slider.valueChanged.connect(self.change_speed)

        # Label pour afficher la vitesse actuelle en millisecondes
        self.speed_label = QLabel(f"Vitesse : {self.timer_interval} ms")
        top_layout.addWidget(self.speed_label)
        top_layout.addWidget(self.speed_slider)

        # Bouton Pause/Resume
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.toggle_pause)
        top_layout.addWidget(self.pause_button)

        # Ajouter la layout du haut au layout principal
        layout.addLayout(top_layout)

        # Partie basse : Affichage de la carte (jeu infini)
        self.map_frame = character_gui.MapWidget(self.map, self.tile_manager,
                                                  self.scale_factor)  # Passer le TileManager
        self.map_frame.clicked_on_map.connect(self.add_character)  # Connecte le signal à la méthode
        layout.addWidget(self.map_frame)

        # Label pour afficher le nombre de ticks
        self.tick_label = QLabel(f"Ticks: {self.tick_count}")
        layout.addWidget(self.tick_label)

    def set_selected_ia(self, ia_item):
        """ Met à jour l'IA sélectionnée avec l'IA venant de MainWindow. """
        self.selected_ia = ia_item
        self.update_nn_controller()  # Mettez à jour le contrôleur de réseau de neurones avec la nouvelle IA

    def update_nn_controller(self):
        """ Met à jour le contrôleur de réseau de neurones avec l'IA sélectionnée. """
        if self.selected_ia:
            self.nn_controller.update_weights(self.selected_ia.individual)

    def add_character(self, grid_pos: QPoint):
        if grid_pos:  # Si la position est valide
            character = characters.Character("paysan", grid_pos.x(), grid_pos.y(), self.movement_strategy)
            self.characters.append(character)  # Ajoute le personnage à la liste
        self.update()  # Redessiner la carte avec les personnages

    def reset_map(self):
        """ Réinitialise la carte à son état par défaut. """
        self.map.load_map_from_file("maps/map_0.txt")
        self.characters.clear()  # Supprimer tous les personnages
        self.tick_count = 0
        self.characters.clear()  # Supprime les personnages de la carte
        self.update()  # Redessiner la carte

    def select_map(self):
        """ Permet de sélectionner une nouvelle carte via un explorateur de fichiers. """
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner une carte", "maps/", "Text Files (*.txt)")
        if file_path:
            try:
                self.map.load_map_from_file("maps/map_0.txt")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de charger la carte : {str(e)}")

    def change_speed(self, value):
        # Change la vitesse du timer et met à jour le label de la vitesse
        self.timer_interval = value
        self.timer.setInterval(self.timer_interval)
        self.speed_label.setText(f"Vitesse : {self.timer_interval} ms")  # Met à jour le label de la vitesse
        self.update()  # Redessiner la carte avec les personnages

    def toggle_pause(self):
        """ Met en pause ou relance le défilement de la carte. """
        if self.is_paused:
            self.timer.start(self.timer_interval)
            self.pause_button.setText("Pause")
        else:
            self.timer.stop()
            self.pause_button.setText("Resume")
        self.is_paused = not self.is_paused

    def update_map(self):
        """ Met à jour la carte et les personnages à chaque tick du timer. """
        self.tick_label.setText(f"Ticks: {self.tick_count}")
        self.tick_count += 1
        if not self.is_paused:
            self.map.update()
            self.characters = [character for character in self.characters if character.energy > 0]
            for c in self.characters:
                action = self.nn_controller.decide_action(c, self.map, [], [], self.map.get_starting_positions())
                c.perform_action(action)
                x, y = c.get_pos()
                if self.map.is_flower(x, y) and not c.is_full():
                    self.map.cut_flower(x, y)
                    c.collect_flower()
                else:
                    self.map.trample(x, y)

                if self.map.is_on_starting_point(x, y):
                    "Reset de l'énergie du personnage et dépose des fleur contre des points"
                    c.reset_energy()
                    if c.flowers:
                        c.drop_flowers()
        self.update()  # Redessiner la carte avec les personnages

    def paintEvent(self, event):
        painter = QPainter(self)

        # Dessiner la carte (en utilisant map_frame)
        self.map_frame.draw(painter)

        # Obtenir la position de map_frame pour ajuster la position des personnages
        map_pos = self.map_frame.pos()  # Position de map_frame dans InfiniteGameFrame
        offset_x = map_pos.x()
        offset_y = map_pos.y()

        # Dessiner les personnages par-dessus la carte
        for character in self.characters:
            # Calculer la position ajustée du personnage
            x, y = self.map_frame.convert_to_pixel(character.x, character.y)

            # Dessiner le personnage en utilisant tilechar_manager
            self.tilechar_manager.draw(painter, x, y)

        painter.end()  # Terminer le QPainter





