import utils_yahtzee
from math import *
from random import *

# Cette fonction renvoie une décision arbitraire, mais toujours valide.
# "nrelancers" est le nombre de fois qu'on a encore le droit de relancer les dés ;
# "feuilleScore" est notre feuille de score ; "valeursDes" sont les valeurs affichées par les dés ;
# "feuilleScoreAdv" est la feuille de score de l'adversaire (qui n'est en réalité pas utilisée).

def decisionArbitraire(valeursDes, nrelancers, feuilleScore, feuilleScoreAdv):
    # S'il faut de prononcer sur les dés à garder…
    if nrelancers > 0:
        # … on choisit au hasard de garder, ou pas, chaque dé
        return [2 * random() > 1 for de in range(utils_yahtzee.NDES)]
    # Si c'est la case à remplir qu'il faut décider…
    else:
        # On traite d'abord le cas de base, où la règle du joker ne s'applique pas.
        # Dans ce cas, tout ce qui compte est de prendre une décision existante et qui n'ait pas encore été prise.
        if feuilleScore['Yahtzee'] is None or any([valeursDes[de] != valeursDes[0] for de in range(1, utils_yahtzee.NDES)]):
            # On regarde l'ensemble des décisions qu'on a le droit de prendre…
            decisionsPossibles = set()
            for decision in utils_yahtzee.ENSDECISIONS:
                if feuilleScore[decision] is None:
                    decisionsPossibles.add(decision)
            # … et on en choisit une uniformément au hasard.
            return list(decisionsPossibles)[floor(len(decisionsPossibles) * random())]
        # Le cas où on joue avec la règle du joker est plus complexe…
        else:
            # Par défaut, on doit jouer le chiffre du yahtzee obtenu, s'il est disponible
            chiffre = utils_yahtzee.ENLETTRES[valeursDes[0]]
            if feuilleScore[chiffre] is None:
                return chiffre
            # Sinon, on doit jouer une décision de la section inférieure de la grille encore disponible,
            # s'il y en a une, qu'on sélectionne au hasard le cas échéant.
            else:
                decisionsPossibles = set()
                for decision in utils_yahtzee.SECTINF:
                    if feuilleScore[decision] is None:
                        decisionsPossibles.add(decision)
                if len(decisionsPossibles) > 0:
                    return list(decisionsPossibles)[floor(len(decisionsPossibles) * random())]
                # Sinon, il faut jouer une décision non encore prise quelconque,
                # nécessairement dans la section supérieure de la grille.
                else:
                    decisionsPossibles = set()
                    for decision in utils_yahtzee.SECTSUP:
                        if feuilleScore[decision] is None:
                            decisionsPossibles.add(decision)
                    return list(decisionsPossibles)[floor(len(decisionsPossibles) * random())]

# "decisionStupide" prend sa décision complètement au hasard,
# sans même regarder si la case qu'il joue est libre.
def decisionStupide(valeursDes, nrelancers, feuilleScore, feuilleScoreAdv):
    if nrelancers > 0:
        return [2 * random() > 1 for de in range(utils_yahtzee.NDES)]
    else:
        return list(utils_yahtzee.ENSDECISIONS)[floor(len(utils_yahtzee.ENSDECISIONS) * random())]

# "decisionManuelle" demande à l'humain son choix.
# Cette fonction peut être utilisée pour les phases de test du code.
# À noter que le temps pendant lequel on attend la réponse de l'humain
# n'est pas décompté au chronomètre.
def decisionManuelle(valeursDes, nrelancers, feuilleScore, feuilleScoreAdv):
    if nrelancers > 0:
        decision_texte = input('Veuillez dire quels dés vous souhaitez garder : ')
        # Si vous souhaitez p. ex. garder les premier et la quatrième dé, et relancer les autres,
        # répondez « ONNON ».
        if len(decision_texte) < utils_yahtzee.NDES:
            print('Décision invalide ! Je vais faire comme si vous aviez répondu \'OOOOO\'')
            decision = [True for de in range(utils_yahtzee.NDES)]
        else:
            decision = [decision_texte[de] == 'O' for de in range(utils_yahtzee.NDES)]
    else:
        decision = input('Veuillez indiquez la case que vous souhaitez jouer : ')
        # Attention, vous devez utiliser exactement la même graphie que dans le code-source !'
        if decision not in utils_yahtzee.ENSDECISIONS:
            print('Décision invalide ! Je vais faire comme si vous aviez répondu \'As\'')
            decision = 'As'
    return decision
