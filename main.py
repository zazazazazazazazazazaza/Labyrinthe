import random
from collections import deque
import matplotlib.pyplot as plt

class Labyrinthe:
    def __init__(self, taille):
        self.taille = taille
        self.plateau = self.generer_plateau()
        self.depart, self.arrivee = self.trouver_points()

    def afficher_plateau(self):
        for ligne in self.plateau:
            print(''.join(ligne))

    def generer_plateau(self):
        # Initialiser le plateau avec des cases vides
        plateau = [['⬜' for _ in range(self.taille)] for _ in range(self.taille)]

        # On fait se déplacer un pointeur aléatoirement sur le plateau pour créer un chemin
        i, j = 3, 3
        p, max_steps = 0, 0
        
        while p < self.taille * 2 and max_steps < self.taille * self.taille:
            plateau[i][j] = '⬛' if p > 0 else '✅'
            direction = random.choices(['haut', 'bas', 'gauche', 'droite'], weights=[0.2, 0.8, 0.2, 0.8])[0]

            if direction == 'haut' and i > 0 and plateau[i - 1][j] == '⬜':
                i -= 1
                p += 1
            elif direction == 'bas' and i < self.taille - 1 and plateau[i + 1][j] == '⬜':
                i += 1
                p += 1
            elif direction == 'gauche' and j > 0 and plateau[i][j - 1] == '⬜':
                j -= 1
                p += 1
            elif direction == 'droite' and j < self.taille - 1 and plateau[i][j + 1] == '⬜':
                j += 1
                p += 1

            max_steps += 1
        
        plateau[i][j] = '✅'

        # Remplir le reste du plateau avec des murs ou des chemins
        for i in range(self.taille):
            for j in range(self.taille):
                if plateau[i][j] != '✅' and plateau[i][j] != '⬛':
                    plateau[i][j] = '⬜' if random.random() < 0.5 else '⬛'

        return plateau

    def trouver_points(self):
        """Trouve les deux points de départ et d'arrivée marqués '✅'."""
        points = []
        for i in range(self.taille):
            for j in range(self.taille):
                if self.plateau[i][j] == '✅':
                    points.append((i, j))
        return points[0], points[1]

    def sauvegarder_plateau(self):
        with open("plateaux.txt", 'a', encoding='utf-8') as fichier:
            fichier.write("--- Nouveau plateau ---\n")
            for ligne in self.plateau:
                fichier.write(''.join(ligne) + '\n')
            fichier.write("\n")


class Bot:
    def __init__(self, labyrinthe):
        self.labyrinthe = labyrinthe
        self.position = self.labyrinthe.depart  # Le bot commence au point de départ
        self.chemin = []

    def deplacements_possibles(self, position):
        """Retourne les mouvements possibles à partir de la position actuelle."""
        i, j = position
        mouvements = []
        
        if i > 0 and self.labyrinthe.plateau[i-1][j] in ['⬛', '✅']:  # Haut
            mouvements.append(('haut', (i-1, j)))
        if i < self.labyrinthe.taille - 1 and self.labyrinthe.plateau[i+1][j] in ['⬛', '✅']:  # Bas
            mouvements.append(('bas', (i+1, j)))
        if j > 0 and self.labyrinthe.plateau[i][j-1] in ['⬛', '✅']:  # Gauche
            mouvements.append(('gauche', (i, j-1)))
        if j < self.labyrinthe.taille - 1 and self.labyrinthe.plateau[i][j+1] in ['⬛', '✅']:  # Droite
            mouvements.append(('droite', (i, j+1)))
        return mouvements

    def deplacer_aleatoirement(self):
        """Le bot se déplace aléatoirement et compte le nombre de mouvements."""
        self.chemin = []
        self.position = self.labyrinthe.depart  # Réinitialise la position à chaque appel
        while self.position != self.labyrinthe.arrivee:
            mouvements = self.deplacements_possibles(self.position)
            if not mouvements:
                return float('inf')  # Bot bloqué, retour d'une valeur très élevée
            direction, nouvelle_position = random.choice(mouvements)
            self.position = nouvelle_position
            self.chemin.append(self.position)

        return len(self.chemin)  # Retourne le nombre de mouvements du bot

class Supervisor:
    def __init__(self):
        self.plateaux = []

    def generer_plateaux(self, n):
        labyrinthe = Labyrinthe(10)
        for _ in range(n):
            self.plateaux.append(labyrinthe)
            labyrinthe.sauvegarder_plateau()

    def evaluation(self):
        for labyrinthe in self.plateaux:
            bot = Bot(labyrinthe)
            bot.deplacer_aleatoirement()

class Enfant_meilleur_bot:
    def __init__(self, supervisor):
        self.supervisor = supervisor
        self.bots_scores = []

    def selectionner_meilleurs_bots(self):
        """Évalue les bots et sélectionne les deux meilleurs en fonction de leur performance."""
        self.bots_scores = []
        for labyrinthe in self.supervisor.plateaux:
            bot = Bot(labyrinthe)
            score = bot.deplacer_aleatoirement()  # On utilise ici le score de déplacement aléatoire
            self.bots_scores.append((bot, score))
        
        # Trier les bots par score (nombre de mouvements) croissant
        self.bots_scores.sort(key=lambda x: x[1])
        
        # Sélectionner les deux meilleurs
        meilleurs_bots = [self.bots_scores[0][0], self.bots_scores[1][0]]
        return meilleurs_bots, self.bots_scores[0][1]  # Retourne les meilleurs bots et leur meilleur score

    def relancer_meilleurs_bots(self, bots):
        """Relance les deux meilleurs bots 100 fois chacun avec 5% de modification aléatoire."""
        for bot in bots:
            for _ in range(100):
                if random.random() < 0.0001 and bot.chemin:
                    index_a_modifier = random.randint(0, len(bot.chemin) - 1)
                    mouvements_possibles = bot.deplacements_possibles(bot.chemin[index_a_modifier])
                    if mouvements_possibles:
                        _, nouvelle_position = random.choice(mouvements_possibles)
                        bot.chemin[index_a_modifier] = nouvelle_position
                
                bot.position = bot.labyrinthe.depart  # Réinitialiser la position du bot
                bot.deplacer_aleatoirement()
    
    def ameliorer_generation(self):
        """Effectue une génération d'amélioration avec les deux meilleurs bots."""
        meilleurs_bots, meilleur_score = self.selectionner_meilleurs_bots()
        self.relancer_meilleurs_bots(meilleurs_bots)
        return meilleur_score  # Retourne le meilleur score de cette génération

# Fonction pour exécuter et tracer les résultats
def run_genetic_algorithm(nb_generations):
    supervisor = Supervisor()
    supervisor.generer_plateaux(5)
    supervisor.evaluation()

    enfant_bot = Enfant_meilleur_bot(supervisor)

    generations = []
    meilleurs_scores = []

    # Améliorer les bots sur plusieurs générations
    for generation in range(nb_generations):
        print(f"--- Génération {generation + 1} ---")
        meilleur_score = enfant_bot.ameliorer_generation()
        generations.append(generation + 1)
        meilleurs_scores.append(meilleur_score)

    # Traçage des résultats
    plt.plot(generations, meilleurs_scores, marker='o')
    plt.xlabel('Numéro de la génération')
    plt.ylabel('Nombre de mouvements du meilleur bot')
    plt.title('Amélioration du nombre de mouvements par génération')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_genetic_algorithm(10000)
