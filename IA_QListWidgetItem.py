from PyQt5.QtWidgets import (
    QListWidgetItem
)


class IAListWidgetItem(QListWidgetItem):
    def __init__(self, individual, fitness):
        # Initialiser l'élément avec un label "ia_58-32-32-5_<fitness_value>"
        super().__init__(f"ia_58-32-32-5_{fitness:.2f}")
        # Stocker l'individu dans l'objet
        self.individual = individual # Values as used by DEAP algorythm
        self.fitness = fitness

    def get_individual(self):
        """Retourner l'individu associé à cet item."""
        return self.individual

    def get_fitness(self):
        """Retourner le fitness associé à cet item."""
        return self.fitness
