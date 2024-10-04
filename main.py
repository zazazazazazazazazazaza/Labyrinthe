import random


def afficher_plateau(plateau):
    for ligne in plateau:
        print(''.join(ligne))


# Fonction pour generer un plateau de labyrinth valide
def generate_board(n):
    # Initialiser le plateau avec des cases vides
    plateau = [['⬜' for _ in range(n)] for _ in range(n)]

    # on fait se deplacer un pointeur aleatoirement sur le plateau pour creer un chemin
    i = 3
    j = 3
    p = 0
    max = 0
    while p < n*2 and max < n*n:
        if p > 0:
            plateau[i][j] = '⬛'
        else:
            plateau[i][j] = '✅'
        direction = random.choices(['haut', 'bas', 'gauche', 'droite'], weights=[
                                   0.2, 0.8, 0.2, 0.8])[0]
        if direction == 'haut':
            if i > 0 and plateau[i-1][j] == '⬜':
                i -= 1
                p += 1
        elif direction == 'bas':
            if i < n-1 and plateau[i+1][j] == '⬜':
                i += 1
                p += 1
        elif direction == 'gauche':
            if j > 0 and plateau[i][j-1] == '⬜':
                j -= 1
                p += 1
        elif direction == 'droite':
            if j < n-1 and plateau[i][j+1] == '⬜':
                j += 1
                p += 1
        max += 1
    plateau[i][j] = '✅'

    for i in range(n):
        for j in range(n):
            if plateau[i][j] != '✅' and plateau[i][j] != '⬛':
                if random.random() < 0.5:
                    plateau[i][j] = '⬜'
                else:
                    plateau[i][j] = '⬛'

    # on retourne le plateau
    return plateau


def sauvegarder_plateau(plateau):
    with open("plateaux.txt", 'w', encoding='utf-8') as fichier:
        for ligne in plateau:
            fichier.write(''.join(ligne) + '\n')


def recup_plateau():
    rep = input("ce plateau vous plait-il ? y or n")

    count = 0
    while count < 3:
        if rep == 'y':
            sauvegarder_plateau(plateau)
            break
        elif rep == 'n':
            plateau = generate_board(n)
            afficher_plateau(plateau)
            return recup_plateau()  # Add 'return' statement here
        else:
            rep = input("ce plateau vous plait-il ? y or n")
            count += 1


# on essaye de generer un plateau de labyrinth valide
n = 50
plateau = generate_board(n)
recup_plateau()
