import os
import random
from TimingAttackModule import TimingAttack


def getCorrectBit(correct, zero, one):
    varianceZero = [0,0]
    varianceOne = [0,0]
    for i in range(len(correct)):
        varianceZero[0] += (correct[i] - zero[i])**2
        varianceZero[1] += correct[i] - zero[i]
        varianceOne[0] += (correct[i] - one[i])**2
        varianceOne[1] += correct[i] - one[i]

    varianceZero[0] /= len(correct)
    varianceZero[1] /= len(correct)
    varianceZero[1] = varianceZero[1]**2
    varZero = varianceZero[0] - varianceZero[1]

    varianceOne[0] /= len(correct)
    varianceOne[1] /= len(correct)
    varianceOne[1] = varianceOne[1]**2
    varOne = varianceOne[0] - varianceOne[1]
    print(varZero,varOne)
    if(varZero < varOne):
        return 0
    return 1

NUM_TESTS = 10000
EXPONENT_LEN = 64
ciphertexts = []
for i in range(NUM_TESTS):
    ciphertexts.append(random.getrandbits(100))
ta = TimingAttack()
correctTimes = []
for i in range(len(ciphertexts)):
    correctTimes.append(ta.victimdevice(ciphertexts[i]))

dFound = []

dFound.append(1)
print(ta.test(dFound))

for i in range(0,EXPONENT_LEN-1):
    dZero = []
    dOne = []
    for j in range(len(dFound)):
        dZero.append(dFound[j])
        dOne.append(dFound[j])
    dZero.append(0)
    zeroTime = []
    dOne.append(1)
    oneTime = []
    for j in range(len(ciphertexts)):
        zeroTime.append(ta.attackerdevice(ciphertexts[j],dZero))
        oneTime.append(ta.attackerdevice(ciphertexts[j],dOne))
    dFound.append(getCorrectBit(correctTimes,zeroTime,oneTime))
    print(ta.test(dFound))
