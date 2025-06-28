from mafia import *
import collections
import numpy as np

iter = 100000 ## number of iterations
targetRole = 'Mayor [U]'
hitCount = np.zeros(iter)
fakeRate = .18 ## Subjective value determining how likely someone is to fake this claim

## This code is wildly inefficient, don't judge me idc

for i in range(iter):
    gameVar = game('game_setup.txt') ## Place setup text file here

    roles = (['Jailor', 'Godfather'] + gameVar.TI.roles + gameVar.TS.roles + gameVar.TP_TK.roles + gameVar.RT.roles + gameVar.RM.roles +
    gameVar.NK.roles + gameVar.NE.roles + gameVar.NB.roles + gameVar.ANY.roles)

    known_list = [''.join(x) for x in gameVar.known_list]

    roleCounts = collections.Counter(roles)
    knownCounts = collections.Counter(known_list)

    numHits = roleCounts[targetRole] - knownCounts[targetRole]
    hitCount[i] = numHits > 0

N = gameVar.total_players - gameVar.known_players
priorProbability = (sum(hitCount) / iter) / N
bayesProbability = priorProbability / (priorProbability + fakeRate * (1 - priorProbability))

print("Claim to be evaluated: ",targetRole)
print("The probability this role exists in this game is: ", f'{priorProbability * N:.2f}')
print("The prior probability of this claim is: ",  f'{priorProbability:.2f}')
print("Probability of this claim is: ", f'{bayesProbability:.2f}')


