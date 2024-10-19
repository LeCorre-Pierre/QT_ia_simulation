from deap import base, creator, tools, algorithms
from neural_network_controller import *
import functools


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
        num_weights = NNC_TOTAL_WEIGHT_NUMBER
        return [random.uniform(-1, 1) for _ in range(num_weights)]  # Remplissage aléatoire
    else:
        # Choisir une IA à partir de la liste, en utilisant modulo pour la répétition
        ia = IAs[random.randint(0, len(IAs) - 1)]  # Choisir aléatoirement une IA
        # Supposons que IAListWidgetItem a une méthode pour obtenir les valeurs sous forme de liste
        return ia


def evaluate_individual(individual, nb_turn_per_simulation, nb_characters, map_data):

    nn_controller = NeuralNetworkController(58, 32, 32, 5)

    # Initialiser le contrôleur de réseau de neurones avec les poids de l'individu
    nn_controller.update_weights(individual)

    # Exécuter la simulation et renvoyer le score de fitness
    fitness = nn_controller.evaluate(map_data, nb_turn_per_simulation, nb_characters)

    return fitness,


def run_evolution(nb_gener, nb_ia_per_gen, cxpb, mutpb, nb_turn_per_simulation, nb_characters, IAs, result_queue, map_data, stop_event):
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
    popu, log = custom_eaSimple(population,
                                        toolbox,
                                        cxpb=cxpb,
                                        mutpb=mutpb,
                                        ngen=nb_gener,
                                        stats=stats,
                                        verbose=True,
                                        stop_event=stop_event)
    result_queue.put(popu)  # Met le résultat dans la queue


def custom_eaSimple(population, toolbox, cxpb, mutpb, ngen, stats=None, halloffame=None, verbose=__debug__, stop_event=None):
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Évaluer la population initiale
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(population), **record)
    if verbose:
        print(logbook.stream)

    # Boucle d'évolution
    for gen in range(1, ngen + 1):
        if stop_event.is_set():  # Vérifie si l'événement d'arrêt est déclenché
            print("Évolution stoppée par l'utilisateur.")
            break

        # Sélectionner les individus pour la prochaine génération
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        # Appliquer le croisement et la mutation
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Réévaluer les individus mutés
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Remplacer la population par les descendants
        population[:] = offspring

        # Mettre à jour le Hall of Fame
        if halloffame is not None:
            halloffame.update(population)

        # Compiler les statistiques et enregistrer le log
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

    return population, logbook
