# Paramètres de base pour le Yahtzee

NDES = 5
NFACES = 6

# Décision possibles, &c.

SECTSUP = {'As', 'Deux', 'Trois', 'Quatre', 'Cinq', 'Six'} # Section supérieure
SECTINF = {'Brelan', 'Carre', 'Full', 'PetiteSuite', 'GrandeSuite', 'Yahtzee', 'Chance'} # Section inférieure
ENSDECISIONS = set().union(SECTSUP, SECTINF) # Ensemble des décisions
NTOURS = len(SECTSUP) + len(SECTINF) # Nombre de tours dans une partie. Vaut 13
FEUILLESCOREVIERGE = {'As': None, 'Deux': None, 'Trois': None, 'Quatre': None,
    'Cinq': None, 'Six': None, 'Brelan': None, 'Carre': None, 'Full': None,
    'PetiteSuite': None, 'GrandeSuite': None, 'Yahtzee': None, 'Chance': None,
    'PrimeYahtzee': 0} # Feuille de score vierge
ENLETTRES = {1: 'As', 2: 'Deux', 3: 'Trois', 4: 'Quatre', 5: 'Cinq', 6: 'Six'} # Pour convertir les chiffres en lettres
ENCHIFFRES = {'As': 1, 'Deux': 2, 'Trois': 3, 'Quatre': 4, 'Cinq': 5, 'Six': 6} # Pour convertir les lettres en chiffres

# Nombre de points associés à différentes choses

SEUILPRIMESUP = 63
VALEURPRIMESUP = 35
VALEURFULL = 25
VALEURPETITESUITE = 30
VALEURGRANDESUITE = 40
VALEURYAHTZEE = 50
VALEURPRIMEYAHTZEE = 100

# Cette fonction détermine si une décision respecte les règles autorisées.
# "decision" est la décision prose par le joueur ; "feuilleScore" l'état actuel de sa feuille de score ;
# "joker" dit s'il est dans la situation d'utiliser le Yahtzee comme joker ;
# "valeursDes" est la valeur affichée par les dés.

def rulesRespected(decision, feuilleScore, joker=False, valeursDes=None):
    if feuilleScore[decision] is not None:
        return False
    # Les règles en cas de joker sont un peu compliquées…
    if joker:
        chiffre = ENLETTRES[valeursDes[0]]
        if feuilleScore[chiffre] is None:
            return decision == chiffre
        elif any(feuilleScore[dec] is None for dec in SECTINF):
            return (decision in SECTINF)
        else:
            return (decision in SECTSUP)
    else:
        return True

# Cette fonction calcule le score obtenu à la fin d'un coup.
# "valeursDes" est la valeur affichée par les dés ; "decision" est la case jouée ;
# "joker" dit si on est en situation d'utiliser le yahtzee comme joker.

def computeScore(valeursDes, decision, joker=False):
    occurrences = [0 for chiffre in range(NFACES)]
    for de in range(NDES):
        occurrences[valeursDes[de] - 1] += 1
    if decision in SECTSUP:
        chiffre = ENCHIFFRES[decision]
        return occurrences[chiffre - 1] * chiffre
    else:
        totalDes = sum(valeursDes)
        if decision == 'Brelan':
            return (max(occurrences) >= 3) * totalDes
        elif decision == 'Carre':
            return (max(occurrences) >= 4) * totalDes
        elif decision == 'Full':
            return ((any([occurrences[j] == 3 for j in range(6)])
                    and any([occurrences[j] == 2 for j in range(6)]))
                    or joker) * VALEURFULL
        elif decision == 'PetiteSuite':
            return (all([occurrences[j] > 0 for j in range(0, 4)])
                    or all([occurrences[j] > 0 for j in range(1, 5)])
                    or all([occurrences[j] > 0 for j in range(2, 6)])
                    or joker) * VALEURPETITESUITE
        elif decision == 'GrandeSuite':
            return (all([occurrences[j] > 0 for j in range(0, 5)])
                    or all([occurrences[j] > 0 for j in range(1, 6)])
                    or joker) * VALEURGRANDESUITE
        elif decision == 'Yahtzee':
            return (max(occurrences) >= 5) * VALEURYAHTZEE
        else:
            return totalDes

# Cette fonction calcule le score total d'un joueur,
# à partir de sa feuille de score (supposée finale) "feuilleScore"

def totalScore(feuilleScore):
    sommeSup = sum([feuilleScore[case] for case in SECTSUP])
    if sommeSup >= SEUILPRIMESUP:
        sommeSup += VALEURPRIMESUP
    sommeInf = sum([feuilleScore[case] for case in SECTINF])
    return sommeSup + sommeInf + feuilleScore['PrimeYahtzee']
