import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QListWidget, QLabel, QSlider,
    QComboBox, QTabWidget, QMessageBox, QMenu
)
import sys

import IA_QListWidgetItem
import searchwindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulation des IA")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        layout = QVBoxLayout(self.central_widget)

        # Liste des meilleures IA
        self.best_ia_list = QListWidget()
        self.best_ia_list.setContextMenuPolicy(3)  # Pour le clic droit
        self.best_ia_list.setSelectionMode(QListWidget.MultiSelection)
        self.best_ia_list.customContextMenuRequested.connect(self.context_menu)
        layout.addWidget(QLabel("Meilleures IA :"))
        layout.addWidget(self.best_ia_list)

        # Boutons pour les actions
        button_layout = QHBoxLayout()
        self.search_button = QPushButton("Rechercher")
        self.search_button.clicked.connect(self.open_search_window)
        button_layout.addWidget(self.search_button)

        self.observe_button = QPushButton("Observer")
        self.observe_button.clicked.connect(self.observe_ia)
        button_layout.addWidget(self.observe_button)

        layout.addLayout(button_layout)

        # Charger les IA sauvegardées
        self.load_saved_ias()

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

    def observe_ia(self):
        selected_ia = self.best_ia_list.currentItem()
        if not selected_ia:
            QMessageBox.warning(self, "Alerte", "Veuillez sélectionner une IA à observer.")
            return
        # Ouvrir une nouvelle fenêtre pour observer l'IA sélectionnée
        print(f"Observation de l'IA : {selected_ia.text()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
