import numpy as np

class NeuralNetwork:
    def __init__(self, input_size=33, hidden_size_1=32, hidden_size_2=32, output_size=5):
        """
        Initialise le réseau de neurones avec des poids aléatoires.
        :param input_size: Nombre de neurones en entrée.
        :param hidden_size_1: Nombre de neurones dans la première couche cachée.
        :param hidden_size_2: Nombre de neurones dans la deuxième couche cachée.
        :param output_size: Nombre de neurones en sortie.
        """
        self.input_size = input_size
        self.hidden_size_1 = hidden_size_1
        self.hidden_size_2 = hidden_size_2
        self.output_size = output_size

        # Initialiser les poids aléatoires
        self.W1 = np.random.uniform(-1.0, 1.0, (input_size, hidden_size_1))
        self.W2 = np.random.uniform(-1.0, 1.0, (hidden_size_1, hidden_size_2))
        self.W3 = np.random.uniform(-1.0, 1.0, (hidden_size_2, output_size))

        self.b1 = np.random.randn(hidden_size_1)
        self.b2 = np.random.randn(hidden_size_2)
        self.b3 = np.random.randn(output_size)

    def set_weights(self, weights):
        """
        Met à jour les poids du réseau de neurones.
        :param weights: Liste de matrices de poids [W1, W2, W3].
        """
        self.W1, self.W2, self.W3, self.b1, self.b2, self.b3 = weights

    def predict(self, inputs):
        """
        Exécute une passe avant (forward pass) dans le réseau de neurones.
        :param inputs: Entrée du réseau (vecteur).
        :return: Sortie du réseau (vecteur).
        """
        # Convertir inputs en tableau NumPy si ce n'est pas déjà le cas
        inputs = np.array(inputs, dtype=float)  # Assurez-vous que inputs est un tableau de floats

        # Vérifiez la forme des entrées
        if inputs.ndim == 1:
            inputs = inputs.reshape(1, -1)  # Assurez-vous que inputs est un tableau 2D (n_samples, n_features)

        # Vérifiez la forme des poids
        assert inputs.shape[1] == self.input_size, "La taille des entrées ne correspond pas à la taille attendue"

        # Calcul des activations pour chaque couche
        z1 = np.dot(inputs, self.W1) + self.b1
        a1 = self.activation(z1)
        z2 = np.dot(a1, self.W2) + self.b2
        a2 = self.activation(z2)
        z3 = np.dot(a2, self.W3) + self.b3
        output = self.softmax(z3)
        return output

    def activation(self, x):
        """
        Fonction d'activation (par exemple, ReLU, Sigmoid, etc.).
        Ici, nous utilisons la fonction ReLU pour les couches cachées.
        :param x: Entrée de la fonction d'activation.
        :return: Sortie de la fonction d'activation.
        """
        return np.maximum(0, x)

    def softmax(self, x):
        """
        Fonction softmax pour la couche de sortie.
        :param x: Entrée de la fonction softmax.
        :return: Sortie de la fonction softmax.
        """
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)
