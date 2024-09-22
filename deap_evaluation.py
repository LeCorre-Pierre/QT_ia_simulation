from deap import base, creator, tools, algorithms
import functools
import random
import numpy as np


def generate_individual(IAs):
    """
    Génère un individu pour une population évolutive.

    Args:
        nb_ia_per_gen (int): Le nombre d'individus à générer.
        IAs (List[IAListWidgetItem]): Une liste d'éléments IAListWidgetItem représentant des IA.
            Si la liste est vide, un individu aléatoire sera généré.
            Si la liste contient des IA, l'individu sera rempli avec les valeurs de l'IA correspondante.

    Returns:
        List: Un individu représentant un vecteur de caractéristiques.
    """
    # Vérifier si la liste des IA est vide
    if not IAs:
        # Si la liste est vide, générer un individu avec des valeurs aléatoires
        return [random.uniform(-1, 1) for _ in range(58)]  # Remplissage aléatoire
    else:
        # Choisir une IA à partir de la liste, en utilisant modulo pour la répétition
        ia = IAs[random.randint(0, len(IAs) - 1)]  # Choisir aléatoirement une IA
        # Supposons que IAListWidgetItem a une méthode pour obtenir les valeurs sous forme de liste
        return ia


def evaluate_individual(individual, nb_turn_per_simulation, nb_characters, map_data):
    return random.randint(10, 1000),
    nn_controller = NeuralNetworkController(58, 32, 32, 5)

    # Initialiser le contrôleur de réseau de neurones avec les poids de l'individu
    nn_controller.update_weights(individual)

    # Exécuter la simulation et renvoyer le score de fitness
    fitness = nn_controller.evaluate(map_data, nb_turn_per_simulation, nb_characters)

    return fitness,


def run_evolution(nb_gener, nb_ia_per_gen, cxpb, mutpb, nb_turn_per_simulation, nb_characters, IAs, result_queue, map_data):
    global stop_evolution
    stop_evolution = False  # Réinitialiser le flag

    # Flag global pour arrêter l'algorithme
    stop_evolution = False

    # Définir la classe Fitness et Individu pour DEAP
    if not hasattr(creator, "FitnessMax"):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    if not hasattr(creator, "Individual"):
        creator.create("Individual", list, fitness=creator.FitnessMax)

    # Initialiser la toolbox DEAP
    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, functools.partial(generate_individual, IAs=IAs))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", functools.partial(evaluate_individual,
                                                   nb_turn_per_simulation=nb_turn_per_simulation,
                                                   nb_characters=nb_characters,
                                                   map_data=map_data))
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=4)

    # Initialiser la population
    population = toolbox.population(n=nb_ia_per_gen)

    # Algorithme d'évolution simple
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    popu = None
    try:
        popu, log = algorithms.eaSimple(population,
                                        toolbox,
                                        cxpb=cxpb,
                                        mutpb=mutpb,
                                        ngen=nb_gener,
                                        stats=stats,
                                        verbose=True)
    except StopIteration:
        print("Évolution stoppée par l'utilisateur.")

    result_queue.put(popu)  # Met le résultat dans la queue
