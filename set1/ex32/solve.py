import sys
import numpy as np
from sympy import Matrix
import math

lenAlphabet = 26 # Lunghezza dell'alfabeto, nel nostro caso solamente con lettere minuscole
m = 10 # Dimensione dei blocchi

# Funzione per generare in modo randomico la chiave
# La chiave ottenuta deve avere determinante coprimo con lenAlphabet, altrimenti la matrice non sarà invertibile modulo lenAlphabet
def generateKey():
    k = np.random.randint(lenAlphabet, size=(m, m)) 
    while (math.gcd(int(round(np.linalg.det(k))), lenAlphabet) != 1):
        k = np.random.randint(lenAlphabet, size=(m, m)) 
    return k
    
# Funzione per cifrare un plaintext pt con la chiave k usando l'algoritmo di Hill
# La cifratura consiste nel prodotto scalare fra pt e k modulo len alphabet
def encryptHill(pt, k):
    ct = np.dot(k, pt)%lenAlphabet
    return ct

# Funzione per decifrare un ciphertext ct con la chiave k usando l'algoritmo di Hill
# La decifratura consiste nel prodotto scalare fra l'inversa della matrice della chiave k e ct modulo lenAlphabet
# La funzione in questo caso permette di prendere in ingresso anche k1, l'inversa della matrice della chiave k
def decryptHill(ct, k, k1 = None):
    if(k1 is decryptHill.__defaults__[0]):
        k1 = np.array(Matrix(k).inv_mod(lenAlphabet))
    pt = np.dot(k1, ct)
    return pt%lenAlphabet

# Funzione che permette di attaccare il cifrario di Hill ottenendo la chiave a partire da un set di coppie plaintext ciphertext
# In ingresso vengono fornite tutte le coppie plaintext-ciphertext ottenute
# La funzione è divisa in due parti:
#   1. Fra tutti i plaintext ne vengono scelti m che generano una matrice P* invertibile modulo lenAlplabet
#   2. Viene invertita la matrice P* e ottenuta k facendo il prodotto scalare fra P*^(-1) e la matrice di ciphertext
def attackHill(ptBlocks, ctBlocks):
    pt = np.zeros(shape=(m, m), dtype = np.int32)
    ct = np.zeros(shape=(m,m), dtype = np.int32)
    for i in range(m):
        for j in range(m):
            pt[i][j] = ptBlocks[j][i]
            ct[i][j] = ctBlocks[j][i]
    i = m
    while(math.gcd(int(round(np.linalg.det(pt))), lenAlphabet) != 1 and i < len):
        for j in range(m):
            pt[j][i%m] = ptBlocks[i][j]
            ct[j][i%m] = ctBlocks[i][j]
        i += 1
    if not i < len:
        return None
    ptInv = np.array(Matrix(pt).inv_mod(lenAlphabet))
    
    k = np.dot(ptInv,ct)%lenAlphabet
    return k



#
# Inizio del main
#
ptText = "peershookhisheadwhathaveibecomealreadyanendlessseriesofpeopleallhappyfortheirownprivatereasonslinkedtogetherbythefaintestthreadofmemorywhykeepthemspreadoutintimewhygoonpretendingthattheresonerealpersonenduringthroughallthosearbitrarychangesyourememberyourselfyoubelieveyoureonepersonwhycallitapretenseitsthetruthbutidontbelieveitanymoreeachpersonicreateisstampedwiththeillusionofstillbeingthisimaginarythingcalledmebutthatsnorealpartoftheiridentityitsadistractionasourceofconfusiontheresnoreasontokeepondoingitortomaketheseseparatepeoplefolloweachotherintimeletthemalllivetogethermeeteachotherkeepyoucompanykategrippedhimbytheshouldersandlookedhimintheeyeyoucantbecomethesolipsistnationthatsnonsenseitsrhetoricfromanoldplayallitwouldmeanisdyingthepeoplethesoftwarecreateswhenyouregonewontbeyouinanywaytheyllbehappywonttheyfromtimetotimefortheirownstrangereasonsyesbutthatsalliamnowthatsallthatdefinesmesowhentheyrehappytheyllbeme"

k = generateKey()
print(k)

# Aggiungo del padding al testo in modo che la lunghezza sia multipla di m
while(len(ptText) % m != 0):
    ptText+="a"
print(ptText)
len = len(ptText)//m 

# Divido il testo in blocchi da m caratteri poi convertiti ad interi minori di 26 
ptBlocks = np.zeros(shape=(len, m), dtype = np.int32)
for i in range(len):
    for j in range(m):
        ptBlocks[i][j] = ord(ptText[i*m+j])-97
print(ptBlocks)

# Cifro tutti i blocchi del plaintext
ctBlocks = np.zeros(shape=(len,m), dtype = np.int32)
for i in range(len):
    ctBlocks[i] = encryptHill(ptBlocks[i], k)
print(ctBlocks)
# Stampo la cifratura
ctFoundTxt = ""
for i in range(len):
    for j in range(m):
        ctFoundTxt += chr(ctBlocks[i][j]+97)
print(ctFoundTxt)

# Decifro tutti i blocchi di ciphertext con la matrice k invertita (k1)
k1 = np.array(Matrix(k).inv_mod(lenAlphabet))
ptFound = np.zeros(shape=(len, m), dtype = np.int32)
for i in range(len):
    ptFound[i] = decryptHill(ctBlocks[i], k, k1)
print(ptFound)

# Converto a string tutti i valori interi ottenuti con la decifratura e stampo il testo ottenuto
ptFoundTxt = ""
for i in range(len):
    for j in range(m):
        ptFoundTxt += chr(ptFound[i][j]+97)
print(ptFoundTxt)

# Test dell'algoritmo di attacco al cifrario fornendo in ingresso tutti i blocchi di plaintext e ciphertext che abbiamo
kFound = attackHill(ptBlocks, ctBlocks)
print(kFound)