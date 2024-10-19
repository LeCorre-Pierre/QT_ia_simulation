from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QSpinBox,
    QPushButton, QListWidget, QMenu, QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer
import sys
import threading
from IA_QListWidgetItem import *
from deap_evaluation import *
import queue
from map import *


class SearchWindow(QDialog):
    def __init__(self, ias):
        super().__init__()
        self.setWindowTitle("Recherche IA")
        self.setGeometry(200, 200, 600, 400)  # Élargi pour inclure la liste et les logs
        self.initUI()

        self.search_thread = None
        self.running = False  # Variable pour contrôler le thread

        # Ajout des IA à la liste
        for ia in ias:
            # Vérifiez que ia est un IAListWidgetItem avant de l'ajouter
            if isinstance(ia, IAListWidgetItem):
                # Créer une copie de l'élément
                ia_copy = IAListWidgetItem(ia.individual, ia.fitness)
                self.ia_list.addItem(ia_copy)
                print(f"Adding : {ia_copy} ")
            else:
                print(f"Erreur : {ia} n'est pas une IAListWidgetItem valide.")

    def get_ia_list_items(self):
        ia_list = []
        for index in range(self.ia_list.count()):
            ia_item = self.ia_list.item(index)  # Récupère l'IAListWidgetItem
            ia_list.append(ia_item.individual)
        return ia_list

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Section principale
        top_layout = QHBoxLayout()

        # Layout gauche pour les paramètres de la recherche
        param_layout = QVBoxLayout()

        # Nombre de générations
        param_layout.addWidget(QLabel("Nombre de générations:"))
        self.num_generation = QSpinBox()
        self.num_generation.setRange(1, 10000)
        self.num_generation.setValue(50)  # Valeur par défaut
        param_layout.addWidget(self.num_generation)

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
        self.ia_list.setSelectionMode(QListWidget.MultiSelection)
        self.ia_list.customContextMenuRequested.connect(self.context_menu)
        ia_layout.addWidget(QLabel("Liste des IA :"))
        ia_layout.addWidget(self.ia_list)

        top_layout.addLayout(ia_layout)

        main_layout.addLayout(top_layout)

        # Affichage des logs en bas
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)  # Les logs sont en lecture seule
        main_layout.addWidget(QLabel("Logs :"))
        main_layout.addWidget(self.log_output)

    def start_search(self):
        global stop_evolution
        if self.search_thread is not None and self.search_thread.is_alive():
            QMessageBox.warning(self, "Alerte", "La recherche est déjà en cours.")
            return

        # Logs pour les paramètres
        self.log_output.append("Recherche lancée avec les paramètres:")
        self.log_output.append(f"Nombre de générations: {self.num_generation.value()}")
        self.log_output.append(f"Taux de mutation: {self.mutation_rate.value()}")
        self.log_output.append(f"Taux de croisement: {self.crossover_rate.value()}")
        self.log_output.append(f"Nombre d'IA: {self.num_ia.value()}")
        self.log_output.append(f"Nombre de tours: {self.num_turns.value()}")
        self.log_output.append(f"Nombre de personnes: {self.num_players.value()}")

        # Récupérer les valeurs des paramètres
        nb_gener = self.num_generation.value()
        nb_ia_per_gen = self.num_ia.value()
        mutpb = self.mutation_rate.value()
        cxpb = self.crossover_rate.value()
        nb_turn_per_simulation = self.num_turns.value()
        nb_characters = self.num_players.value()
        IAs = self.get_ia_list_items()
        m = Map()
        m.load_map_from_file("maps/map_0.txt")

        result_queue = queue.Queue()
        self.stop_event = threading.Event()  # Créer l'événement pour l'arrêt
        # Démarrer le thread
        self.running = True
        self.search_thread = threading.Thread(
            target=run_evolution,
            args=(
            nb_gener, nb_ia_per_gen, cxpb, mutpb, nb_turn_per_simulation, nb_characters, IAs, result_queue, m.map_data, self.stop_event)
        )
        self.search_thread.start()

        # Utiliser un timer pour vérifier si le thread a terminé sans bloquer l'interface
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.check_thread_completion(result_queue))
        self.timer.start(100)  # Vérifier toutes les 100 millisecondes

    def check_thread_completion(self, result_queue):
        if not self.search_thread.is_alive():
            self.timer.stop()
            self.log_output.append("Recherche terminée.")

            # Récupérer les résultats (si la recherche n'a pas été arrêtée prématurément)
            try:
                results = result_queue.get_nowait()
                self.callback_per_gen_search_window(results)
            except queue.Empty:
                self.log_output.append("Aucun résultat disponible (recherche arrêtée ou aucun IA générée).")

    def stop_search(self):
        if self.search_thread and self.search_thread.is_alive():
            # Logique pour arrêter la recherche
            self.log_output.append("Demande d'arrêt de la recherche...")
            self.stop_event.set()  # Déclenche l'événement d'arrêt

            # Attendre que le thread se termine
            self.search_thread.join()
            self.log_output.append("Recherche arrêtée.")

    def callback_per_gen_search_window(self, population):
        # Sélectionner les 10 meilleurs individus
        best_inds = tools.selBest(population, 10)

        # Ajouter chaque meilleur individu à la liste
        for best_ind in best_inds:
            fitness = best_ind.fitness.values[0]
            item = IAListWidgetItem(best_ind, fitness)
            self.ia_list.addItem(item)

    def sort_ia_list(self):
        # Récupérer tous les items dans une liste
        items = []
        for index in range(self.ia_list.count()):
            item = self.ia_list.item(index)
            # Créer une copie de l'IAListWidgetItem pour éviter la suppression après clear()
            new_item = IAListWidgetItem(item.individual, item.fitness)
            items.append(new_item)

        # Trier les items par fitness
        items.sort(key=lambda x: x.fitness, reverse=True)  # Tri décroissant par fitness

        # Vider la liste
        self.ia_list.clear()

        # Ajouter les items triés à la liste
        for sorted_item in items:
            self.ia_list.addItem(sorted_item)

    def context_menu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("Supprimer")
        save_action = menu.addAction("Sauvegarder")

        action = menu.exec_(self.ia_list.viewport().mapToGlobal(position))

        if action == delete_action:
            selected_items = self.ia_list.selectedItems()  # Récupère les éléments sélectionnés
            if not selected_items:
                return

            for item in selected_items:
                self.ia_list.takeItem(self.ia_list.row(item))  # Supprime chaque élément

        elif action == save_action:
            selected_items = self.ia_list.selectedItems()
            if not selected_items:
                return

            for item in selected_items:
                self.log_output.append(f"IA {item.text()} sauvegardée.")
                item.save_to_file()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchWindow(())
    window.show()
    sys.exit(app.exec_())
