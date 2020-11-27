import sys
import time

# Jeu du taquin avec 8 cases.
# Classe montrant l'état du  plateau
class Status:
    # constructeur initialisant les variables nécessaires
    def __init__(self, row1, row2, row3):
        # l'etat initial est donné avec le clavier et passé au constructeur
        self.state = [[int(s) for s in row1.split(' ')], [int(s) for s in row2.split(' ')],
                      [int(s) for s in row3.split(' ')]]
        # aucune etape n'a encore été effectuée
        self.steps = []
        # les états suivants n'ont pas encore été initialisés
        self.nextStates = []

    # fonction de calcul des états suivants
    def calculEtatsSuivants(self):
        self.nextStates = []
        # localisation des indexes de la case vide représentée par 0
        for row in self.state:
            if 0 in row:
                row0 = self.state.index(row)
                location0 = row.index(0)
                break
        # verifie si on peut déplacer la case au-dessus du zero dans la case du 0
        # c'est possible si la ligne n'est pas la toute première du plateau
        # même principe pour les autres if
        if row0 > 0:
            newRow = row0 - 1
            self.createNextState(newRow, row0, location0, location0, "up")
        if row0 < 2:
            newRow = row0 + 1
            self.createNextState(newRow, row0, location0, location0, "down")
        if location0 > 0:
            newLoc = location0 - 1
            self.createNextState(row0, row0, newLoc, location0, "left")
        if location0 < 2:
            newLoc = location0 + 1
            self.createNextState(row0, row0, newLoc, location0, "right")

    # fonction de création du prochain état, prend l'état, les coordonnées de la case
    # vide et ses nouvelles coordonnées, ainsi que la direction du pas dans "steps"
    def createNextState(self, row1, row2, location1, location2, step):
        newState = Status("0 0 0", "0 0 0", "0 0 0")
        newState.state = []
        for i, ii in enumerate(self.state):
            newState.state.append([])
            for j, jj in enumerate(ii):
                newState.state[i].append(jj)
        newState.nextStates = []
        newState.state[row1][location1], newState.state[row2][location2] = newState.state[row2][location2], newState.state[row1][location1]
        for s in self.steps:
            newState.steps.append(s)
        newState.steps.append(step)
        self.nextStates.append(newState)

    # Fonction permettant d'afficher la matrice de l'état
    def afficherMatrice(self):
        for row in self.state:
            print(row[0], " ", row[1], " ", row[2])

    # Fonction permettant de vérifier si un problème peut être résolu ou non
    # C'est fait en comptant le nombre d'inversions, c'est à dire pour chaque case, 
	# combien de cases suivantes ont une valeur inférieure. La somme donne le nombre d'inversions.
    def check_solvability(self):
        inversions = 0
        array = [j for sub in self.state for j in sub]
        for index, n in enumerate(array):
            for m in array[index + 1:]:
                if m and n and n > m:
                    inversions += 1
        if inversions % 2 == 1:
            print("La solution n'existe pas")
            return 0
        return 1

# declaration des heuristiques
# nombre de pieces mal placees
def h1(etatCourant, etatFinal):
    h = 0
    for rowNumber, row in enumerate(etatCourant.state):
        for index, n in enumerate(row):
            if (n != 0) and (n != etatFinal.state[rowNumber][index]):
                h += 1
    return h


# somme distances de chaque piece a sa position finale
def h2(etatCourant, etatFinal):
    h = 0
    for rowNumber, row in enumerate(etatCourant.state):
        for index, n in enumerate(row):
            if n != 0:
                for efrow in etatFinal.state:
                    if n in efrow:
                        rowf = etatFinal.state.index(efrow)
                        indexf = efrow.index(n)
                        break
                # distance manhattan
                h += abs(rowf - rowNumber) + abs(indexf - index)
    return h


def get_best_node(open_set):
    return min(open_set.keys(), key=(lambda k: open_set[k]))

def g(state):
    return len(state.steps)


def aetoile(initial_state, final_state, h) :
    open_set = {initial_state : 1000000}
    closed_set = set()
    done = 0
    print("calculating path...")
    while (done != 1) and bool(open_set):
        chosen_state = get_best_node(open_set)
        del open_set[chosen_state]
        if str(chosen_state.state) not in closed_set:
            closed_set.add(str(chosen_state.state))
        if chosen_state.state == final_state.state:
            done = 1
        else:
            chosen_state.calculEtatsSuivants()
            for state in chosen_state.nextStates:
                f_value = g(state) + h(state, final_state)
                if f_value > 31:
                    closed_set.add(str(state.state))
                else:
                    if str(state.state) not in closed_set:
                        open_set[state] = f_value
    if done == 1:
        print("les déplacements de l'espace vide durant l'execution:")
        print(chosen_state.steps)
        print("nombre d'états visités :" + str(len(closed_set)+len(open_set)))
        print("profondeur :" + str(len(chosen_state.steps)))
    else :
        print("la solution n'existe pas")


etatFinal = Status("0 1 2", "3 4 5", "6 7 8")
# instructions au joueur
print(
    "Nous commençons par montrer la création des états suivants, et l'application des heuristiques, à un exemple que vous donnerez:")
print(
    "Ecrivez chaque ligne de votre état initial, séparant chaque nombre par un espace et représentant l'espace vide par un 0:")
print("Exemple:\n1 2 0\n3 4 6\n5 7 8\n")
row1 = input()
row2 = input()
row3 = input()
# creation de l'état initial
etatInitial = Status(row1, row2, row3)
# calcul des états suivants:
etatInitial.calculEtatsSuivants()

# reinitialisation pour pouvoir utiliser l'algorithme:
etatInitial.nextStates = []
etatInitial.steps = []

print("\n_________________________________________________________________________________\n")

if etatInitial.check_solvability() == 0:
    input()
    exit()

sys.setrecursionlimit(10000)

print("Execution de l'algorithme A* avec l'heuristique h1: nombre de pieces mal placées:")
etatInitial.afficherMatrice()
start = time.time()
aetoile(etatInitial, etatFinal,h1)
end = time.time()
print(f"Temps d'exécution : {end - start}")
print("press 'enter' key to procede to calculating path to final state with h2")
input()
# reinitialisation des états suivants:
etatInitial.nextStates = []
etatInitial.steps = []

print("\n_________________________________________________________________________\n")
print("Execution de l'algorithme a* avec l'heuristique h2: somme des distances de chaque piece a sa bonne place:")
etatInitial.afficherMatrice()
start = time.time()

aetoile(etatInitial, etatFinal, h2)
end = time.time()
print(f"Temps d'exécution : {end - start}")
input()