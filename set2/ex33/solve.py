import random
from TimingAttackModule import TimingAttack

# Funzione che calcola il bit i-esimo corretto dell'esponente privato sulla base dei tempi di esecuzione registrati nelle varie versioni. 
# In input vengono forniti i tempi di esecuzione della vittima (correct) e delle due versioni testate in cui i primi 
# i-1 bit più significativi sono corretti mentre il bit i-esimo assume i valori 0 (zero) e 1 (one) al variare delle due versioni.
# Il test si basa sul calcolare le varianze del valore T-T', ovvero la differenza fra i tempi dell'algoritmo che usa l'esponente corretto e 
# quelli dell'algoritmo che usa le due versioni dell'esponente. 
# In output viene restituito il bit i-esimo corretto in base a quale delle due versioni genera il valore di varianza minore.
def getCorrectBit(correct, zero, one):
    # Variabili temporanee in cui salvare la somma dei quadrati delle differenze (in [0]) e la somma delle differenze (in [1])
    varianceZero = [0,0] 
    varianceOne = [0,0]
    # Calcolo delle varianze che vengono quindi salvate in varZero e varOne
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
    # Comparazione di quale delle due varianze è la minore
    if(varZero < varOne):
        return 0
    return 1


NUM_TESTS = 10000 # Numero di ciphertext casuali generati. All'aumentare del numero migliora la precisione della stima della varianza
EXPONENT_LEN = 64 # Lunghezza dell'esponente privato da trovare
# Generazione dei ciphertext casuali
ciphertexts = []
for i in range(NUM_TESTS):
    ciphertexts.append(random.getrandbits(100))

ta = TimingAttack()
# Vengono calcolati i tempi di esecuzione della decifratura dei ciphertexts eseguita dalla "vittima" (non variano durante l'esecuzione dell'attacco)
correctTimes = []
for i in range(len(ciphertexts)):
    correctTimes.append(ta.victimdevice(ciphertexts[i]))

dFound = [] # Lista di bit aggiornata con i valori dei bit corretti trovati
dFound.append(1) # Il primo valore dell'esponente è 1

# Ciclo sui bit ancora da trovare dell'esponente 
for i in range(0,EXPONENT_LEN-1):
    # Vettori che hanno i primi i-1 bit uguali a quelli di dFound e hanno posto il bit i-esimo rispettivamente a 0 e 1
    dZero = []
    dOne = []
    for j in range(len(dFound)):
        dZero.append(dFound[j])
        dOne.append(dFound[j])
    dZero.append(0)
    dOne.append(1)
    # Vengono presi i tempi di computazione su tutti i ciphertexts testati utilizzando le due versioni della chiave privata ipotizzate
    zeroTime = []
    oneTime = []
    for j in range(len(ciphertexts)):
        zeroTime.append(ta.attackerdevice(ciphertexts[j],dZero))
        oneTime.append(ta.attackerdevice(ciphertexts[j],dOne))
    dFound.append(getCorrectBit(correctTimes,zeroTime,oneTime)) # Viene quindi aggiunto alla chiave privata dFound il valore corretto del bit i-esimo 
print(ta.test(dFound)) # Verifichiamo che l'algoritmo abbia trovato la chiave privata corretta
