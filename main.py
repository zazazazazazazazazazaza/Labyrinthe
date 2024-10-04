import random
from collections import deque

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
        
        # Vérifier les 4 directions et s'assurer que le bot ne sort pas du plateau
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
        """Le bot se déplace aléatoirement du nombre de mouvement minimum pour trouver l'arriver."""
        while self.position != self.labyrinthe.arrivee:
            mouvements = self.deplacements_possibles(self.position)
            if not mouvements:
                print("Le bot est bloqué, aucun mouvement possible.")
                return False
            
            # Choisir un mouvement aléatoire parmi les mouvements possibles
            direction, nouvelle_position = random.choice(mouvements)
            # print(f"Le bot se déplace {direction} vers {nouvelle_position}.")
            
            self.position = nouvelle_position
            self.chemin.append(self.position)
            
            # Afficher l'état du plateau après chaque mouvement
            # self.afficher_etat()

        print(f"Le bot a atteint l'arrivée en {len(self.chemin)} mouvements.")
        return True

    def afficher_etat(self):
        """Affiche l'état actuel du plateau avec la position du bot."""
        plateau_temporaire = [ligne[:] for ligne in self.labyrinthe.plateau]  # Copier le plateau
        i, j = self.position
        plateau_temporaire[i][j] = '🤖'  # Position actuelle du bot

        for ligne in plateau_temporaire:
            print(''.join(ligne))
        print()  # Ligne vide pour séparer les étapes

    def bfs_chemin_minimum(self):
        """Utilise BFS pour trouver le chemin le plus court entre les deux points '✅'."""
        file = deque([(self.labyrinthe.depart, [])])
        visite = set([self.labyrinthe.depart])
        
        while file:
            position_actuelle, chemin = file.popleft()
            
            if position_actuelle == self.labyrinthe.arrivee:
                print(f"Le chemin minimum trouvé est de {len(chemin)} mouvements.")
                return chemin

            for _, voisin in self.deplacements_possibles(position_actuelle):
                if voisin not in visite:
                    visite.add(voisin)
                    file.append((voisin, chemin + [voisin]))

        print("Aucun chemin trouvé.")
        return None
    
class Supervisor:
    def __init__(self):
        self.plateaux = []

    def generer_plateaux(self, n):
        labyrinthe = Labyrinthe(20)
        for _ in range(n):
            self.plateaux.append(labyrinthe)
            labyrinthe.sauvegarder_plateau()

    def afficher_plateaux(self):
        for labyrinthe in self.plateaux:
            labyrinthe.afficher_plateau()

    def lancer_jeu(self):
        for labyrinthe in self.plateaux:
            bot = Bot(labyrinthe)
            bot.deplacer_aleatoirement()
            chemin_minimum = bot.bfs_chemin_minimum()
            if chemin_minimum:
                print(f"Chemin minimum : {chemin_minimum}")
            print()
            
    def evaluation(self):
        pass


if __name__ == "__main__":
    supervisor = Supervisor()
    supervisor.generer_plateaux(5)
    supervisor.lancer_jeu()
