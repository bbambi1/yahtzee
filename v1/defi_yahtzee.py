from math import *
from random import *
from copy import *
from time import process_time
from utils_yahtzee import *
import decisions_yahtzee
import boss.boss

## La fonction "partie" simule une partie et renvoie son résultat.
# "decisionA" et "decisionB" sont les fonctions utilisées par chaque joueur pour prendre sa décision.
# "DELAI" est le temps total imparti à chaque joueur pour prendre l'ensemble de ses décisions.
# "MODEBAVARD" dit si on veut afficher le détail de ce qui se passe.

def partie(decisionA=decisions_yahtzee.decisionStupide, decisionB=decisions_yahtzee.decisionArbitraire, DELAI=39.0, MODEBAVARD=True):
    # Initialisation des feuilles de scores
    feuilleScoreA = deepcopy(FEUILLESCOREVIERGE)
    feuilleScoreB = deepcopy(FEUILLESCOREVIERGE)
    # Temps de réflexion cumulé pour chaque joueur
    tempsreflexion = [0.0 for i in range(2)]
    # La partie se joue en 13 tours
    for tour in range(NTOURS):
        if MODEBAVARD:
            print('Début du tour # {:d}'.format(tour))
        # À chaque tour, on fait successivement jouer chaque joueur
        for joueur in range(2):
            if joueur == 0:
                if MODEBAVARD:
                    print('Au joueur A de jouer !')
                idJoueur = 'A'
                feuilleScore = feuilleScoreA
                feuilleScoreAdv = deepcopy(feuilleScoreB)
                fonctionDeDecision = decisionA
            else:
                if MODEBAVARD:
                    print('Au joueur B de jouer !')
                idJoueur = 'B'
                feuilleScore = feuilleScoreB
                feuilleScoreAdv = deepcopy(feuilleScoreA)
                fonctionDeDecision = decisionB
            # Tirage initial des dés
            valeursDes = [ceil(NFACES * random()) for de in range(NDES)]
            if MODEBAVARD:
                print('Résultat du lancer de dés initial : {:s}'.format(str(valeursDes)))
            # Décision du joueur pour le premier relancer
            topchrono = process_time()
            decision = fonctionDeDecision(deepcopy(valeursDes), 2, deepcopy(feuilleScore), feuilleScoreAdv)
            tempsreflexion[joueur] += process_time() - topchrono
            # Contrôle de la validité de la décision
            if decision is None or len(decision) < NDES:
                decision = [True for de in range(NDES)]
                if MODEBAVARD:
                    print('Décision sur le choix des dés à garder invalide :' +
                          'on va garder tous les dés')
            if MODEBAVARD:
                print('Première décision du joueur {:s} concernant les dés à garder : {:s}'.format(idJoueur, str(decision)))
            # On relance les dés que le joueur n'a pas sélectionnés
            for de in range(NDES):
                if not decision[de]:
                    valeursDes[de] = ceil(NFACES * random())
            if MODEBAVARD:
                print('Valeurs des dés à l\'issue du premier relancer : {:s}'.format(str(valeursDes)))
            # Décision du joueur pour le second relancer
            topchrono = process_time()
            decision = fonctionDeDecision(deepcopy(valeursDes), 1, deepcopy(feuilleScore), feuilleScoreAdv)
            tempsreflexion[joueur] += process_time() - topchrono
            # Contrôle de la validité de la décision
            if decision is None or len(decision) < NDES:
                decision = [True for de in range(NDES)]
                if MODEBAVARD:
                    print('Décision sur le nombre de dés à relancer invalide :' +
                          'on ne va relancer aucun dé')
            if MODEBAVARD:
                print('Seconde décision du joueur {:s} concernant les dés à garder : {:s}'.format(idJoueur, str(decision)))
            # On relance les dés que le joueur n'a pas sélectionnés
            for de in range(NDES):
                if not decision[de]:
                    valeursDes[de] = ceil(NFACES * random())
            if MODEBAVARD:
                print('Valeurs terminales des dés : {:s}'.format(str(valeursDes)))
            # On regarde si le résultat est éligible au joker et éventuellement à la prime yahtzee
            joker = False
            primeYahtzee = False
            ilYAYahtzee = all([valeursDes[i] == valeursDes[0] for i in range(1, NDES)])
            if ilYAYahtzee:
                if feuilleScore['Yahtzee'] is not None:
                    joker = True
                    if MODEBAVARD:
                        print('Le joueur {:s} a obtenu un Yahtzee '.format(idJoueur) +
                              'alors que sa case \'Yahtzee\' est déjà remplie : '
                              'il doit donc jouer selon la règle du joker !')
                if feuilleScore['Yahtzee'] == VALEURYAHTZEE:
                    if MODEBAVARD:
                        print('En outre, comme le joueur avait déjà remporté la case \'Yahtzee\', il marque ' +
                              '{:d} points de prime !'.format(VALEURPRIMEYAHTZEE))
                    primeYahtzee = True
            # Décision d'assignation du joueur
            topchrono = process_time()
            decision = fonctionDeDecision(deepcopy(valeursDes), 0, deepcopy(feuilleScore), feuilleScoreAdv)
            tempsreflexion[joueur] += process_time() - topchrono
            if MODEBAVARD:
                print('Le joueur {:s} a choisi de jouer la case {:s}'.format(idJoueur, decision))
            # On regarde si la décision prise respecte les règles ; sinon, on la remplace par une décision respectueuse arbitraire
            if not rulesRespected(decision, feuilleScore, joker=joker, valeursDes=valeursDes):
                decision = decisions_yahtzee.decisionArbitraire(deepcopy(valeursDes), 0, deepcopy(feuilleScore), feuilleScoreAdv)
                if MODEBAVARD:
                    print('La décision du joueur étant irrégulière, on l\'a remplacée par ' +
                          'une décision arbitraire, à savoir, {:s}'.format(decision))
            # On remplit la case appropriée dans la feuille de score
            feuilleScore[decision] = computeScore(valeursDes, decision, joker=joker)
            if primeYahtzee:
                feuilleScore['PrimeYahtzee'] += VALEURPRIMEYAHTZEE
            if MODEBAVARD:
                print('Voici la nouvelle feuille de score pour le joueur {:s} : {:s}'.format(idJoueur, str(feuilleScore)))
    # Calcul des scores
    scoreA = totalScore(feuilleScoreA)
    scoreB = totalScore(feuilleScoreB)
    print('Score final :\n\tJoueur A : {:3d}\n\tJoueur B : {:3d}'.format(scoreA, scoreB))
    if scoreA > scoreB:
        print('Victoire de A')
        bilan = [1, 0]
    elif scoreB > scoreA:
        print('Victoire de B')
        bilan = [0, 1]
    else:
        print('Match nul')
        bilan = [1 / 2, 1 / 2]
    if MODEBAVARD:
        print('Temps total de réflexion pour le joueur A : {:.2f} s.'.format(tempsreflexion[0]))
        print('Temps total de réflexion pour le joueur B : {:.2f} s.'.format(tempsreflexion[1]))
    depassementTempsA = tempsreflexion[0] - DELAI
    depassementTempsB = tempsreflexion[1] - DELAI
    if depassementTempsA > 0:
        penalite = depassementTempsA / DELAI
        bilan[0] -= penalite
        print('Le joueur A reçoit une pénalité de {:.2f}'.format(penalite) +
              'pour dépassement de temps')
    if depassementTempsB > 0:
        penalite = depassementTempsB / DELAI
        bilan[1] -= penalite
        print('Le joueur B reçoit une pénalité de {:.2f}'.format(penalite) +
              'pour dépassement de temps')
    return bilan

partie()