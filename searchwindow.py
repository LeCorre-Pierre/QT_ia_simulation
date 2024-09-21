from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QSpinBox,
    QPushButton, QListWidget, QMenu, QMessageBox, QTextEdit
)
import sys


class SearchWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recherche IA")
        self.setGeometry(200, 200, 600, 400)  # Élargi pour inclure la liste et les logs
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Section principale
        top_layout = QHBoxLayout()

        # Layout gauche pour les paramètres de la recherche
        param_layout = QVBoxLayout()

        # Taux de mutation
        param_layout.addWidget(QLabel("Taux de mutation (0 à 1):"))
        self.mutation_rate = QDoubleSpinBox()
        self.mutation_rate.setRange(0, 1)
        self.mutation_rate.setValue(0.5)
        param_layout.addWidget(self.mutation_rate)

        # Taux de croisement
        param_layout.addWidget(QLabel("Taux de croisement (0 à 1):"))
        self.crossover_rate = QDoubleSpinBox()
        self.crossover_rate.setRange(0, 1)
        self.crossover_rate.setValue(0.5)
        param_layout.addWidget(self.crossover_rate)

        # Nombre d'IA par génération
        param_layout.addWidget(QLabel("Nombre d'IA par génération:"))
        self.num_ia = QSpinBox()
        self.num_ia.setRange(1, 10000)
        self.num_ia.setValue(100)
        param_layout.addWidget(self.num_ia)

        # Nombre de tours par simulation
        param_layout.addWidget(QLabel("Nombre de tours par simulation:"))
        self.num_turns = QSpinBox()
        self.num_turns.setRange(1, 10000)
        self.num_turns.setValue(100)
        param_layout.addWidget(self.num_turns)

        # Nombre de personnes sur la même carte en simultané
        param_layout.addWidget(QLabel("Nombre de personnes sur la même carte:"))
        self.num_players = QSpinBox()
        self.num_players.setRange(1, 10)
        self.num_players.setValue(1)
        param_layout.addWidget(self.num_players)

        # Bouton pour lancer la recherche
        self.start_button = QPushButton("Lancer la recherche")
        self.start_button.clicked.connect(self.start_search)
        param_layout.addWidget(self.start_button)

        # Bouton pour arrêter la recherche
        self.stop_button = QPushButton("Arrêter la recherche")
        self.stop_button.clicked.connect(self.stop_search)
        param_layout.addWidget(self.stop_button)

        top_layout.addLayout(param_layout)

        # Layout droit pour la liste des IA
        ia_layout = QVBoxLayout()

        # Liste des IA
        self.ia_list = QListWidget()
        self.ia_list.setContextMenuPolicy(3)  # Pour le clic droit
        self.ia_list.customContextMenuRequested.connect(self.context_menu)
        ia_layout.addWidget(QLabel("Liste des IA :"))
        ia_layout.addWidget(self.ia_list)

        # Ajouter des IA fictives pour l'illustration
        for i in range(3):
            self.ia_list.addItem(f"IA {i+1}")

        top_layout.addLayout(ia_layout)

        main_layout.addLayout(top_layout)

        # Affichage des logs en bas
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)  # Les logs sont en lecture seule
        main_layout.addWidget(QLabel("Logs :"))
        main_layout.addWidget(self.log_output)

    def context_menu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("Supprimer")
        save_action = menu.addAction("Sauvegarder")

        action = menu.exec_(self.ia_list.viewport().mapToGlobal(position))

        if action == delete_action:
            selected_items = self.ia_list.selectedItems()
            for item in selected_items:
                self.ia_list.takeItem(self.ia_list.row(item))
            self.log_output.append("IA supprimée.")

        elif action == save_action:
            selected_item = self.ia_list.currentItem()
            if selected_item:
                self.log_output.append(f"IA {selected_item.text()} sauvegardée.")
            else:
                QMessageBox.warning(self, "Erreur", "Aucune IA sélectionnée.")

    def start_search(self):
        # Lancer la simulation de recherche ici
        self.log_output.append("Recherche lancée avec les paramètres:")
        self.log_output.append(f"Taux de mutation: {self.mutation_rate.value()}")
        self.log_output.append(f"Taux de croisement: {self.crossover_rate.value()}")
        self.log_output.append(f"Nombre d'IA: {self.num_ia.value()}")
        self.log_output.append(f"Nombre de tours: {self.num_turns.value()}")
        self.log_output.append(f"Nombre de personnes: {self.num_players.value()}")
        # Code pour démarrer la simulation ici

    def stop_search(self):
        # Arrêter la simulation de recherche
        self.log_output.append("Recherche arrêtée")
        # Code pour stopper la simulation ici


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchWindow()
    window.show()
    sys.exit(app.exec_())
