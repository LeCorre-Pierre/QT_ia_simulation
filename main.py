import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QListWidget, QLabel, QSlider,
    QComboBox, QTabWidget, QMessageBox
)
from searchwindow import SearchWindow


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
            selected_item = self.best_ia_list.currentItem()
            if selected_item:
                print(f"IA {selected_item.text()} sauvegardée.")
            else:
                QMessageBox.warning(self, "Erreur", "Aucune IA sélectionnée.")

    def open_search_window(self):
        self.search_window = SearchWindow()
        self.search_window.exec_()

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
