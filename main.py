import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QListWidget, QLabel, QSlider,
    QComboBox, QTabWidget, QMessageBox, QMenu, QFrame
)
from PyQt5.QtCore import pyqtSignal
import sys

import IA_QListWidgetItem
import infinitegameframe
import searchwindow


class MainWindow(QMainWindow):
    ia_selected_signal = pyqtSignal(IA_QListWidgetItem.IAListWidgetItem)  # Signal pour envoyer la liste des IA sélectionnées

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulation des IA")
        self.setGeometry(100, 100, 800, 600)    # Connexion du signal pour sélectionner une IA
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal avec un QHBoxLayout pour séparer la liste des IA et le QFrame à droite
        main_layout = QHBoxLayout(self.central_widget)

        # Partie gauche avec la liste des meilleures IA
        left_layout = QVBoxLayout()

        # Liste des meilleures IA
        self.best_ia_list = QListWidget()
        self.best_ia_list.setContextMenuPolicy(3)  # Pour le clic droit
        self.best_ia_list.setSelectionMode(QListWidget.MultiSelection)
        self.best_ia_list.customContextMenuRequested.connect(self.context_menu)
        left_layout.addWidget(QLabel("Meilleures IA :"))
        left_layout.addWidget(self.best_ia_list)

        # Boutons pour les actions
        button_layout = QHBoxLayout()
        self.search_button = QPushButton("Rechercher")
        self.search_button.clicked.connect(self.open_search_window)
        button_layout.addWidget(self.search_button)

        left_layout.addLayout(button_layout)

        # Ajout de la partie gauche (liste des IA et boutons) au layout principal
        main_layout.addLayout(left_layout)

        # Partie droite avec un QFrame pour afficher des informations supplémentaires
        self.infinitegame_frame = infinitegameframe.InfiniteGameFrame()

        # Ajout de la frame au layout principal
        main_layout.addWidget(self.infinitegame_frame)

        # Charger les IA sauvegardées
        self.load_saved_ias()
        self.best_ia_list.itemSelectionChanged.connect(self.on_selection_changed)
        self.ia_selected_signal.connect(self.infinitegame_frame.set_selected_ia)

    def load_saved_ias(self):
        self.best_ia_list.clear()  # On vide d'abord la liste actuelle
        directory = "ias"  # Répertoire contenant les IA
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):  # Vérifiez le format du fichier
                item = IA_QListWidgetItem.load_from_file(os.path.join(directory, filename))  # Charger l'IA
                if item:  # Si l'élément est valide, l'ajouter à la liste
                    self.best_ia_list.addItem(item)

    def context_menu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("Supprimer")
        save_action = menu.addAction("Sauvegarder")

        action = menu.exec_(self.best_ia_list.viewport().mapToGlobal(position))

        if action == delete_action:
            selected_items = self.best_ia_list.selectedItems()
            for item in selected_items:
                self.best_ia_list.takeItem(self.best_ia_list.row(item))
            print("IA supprimée.")

        elif action == save_action:
            selected_items = self.best_ia_list.selectedItems()
            for item in selected_items:
                item.save_to_file()  # Sauvegarder l'IA sélectionnée
                print(f"IA {item.text()} sauvegardée.")
            else:
                QMessageBox.warning(self, "Erreur", "Aucune IA sélectionnée.")

    def open_search_window(self):
        selected_items = self.best_ia_list.selectedItems()
        self.search_window = searchwindow.SearchWindow(selected_items)
        self.search_window.exec_()
        self.load_saved_ias()

    def on_selection_changed(self):
        # Vérifier si un élément est sélectionné
        selected_items = self.best_ia_list.selectedItems()

        if selected_items:  # Si quelque chose est sélectionné
            # Récupérer le premier élément sélectionné
            first_selected_item = selected_items[0]

            # Émettre le signal avec l'IA sélectionnée
            self.ia_selected_signal.emit(first_selected_item)  # Émettre l'IA ou un autre objet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
