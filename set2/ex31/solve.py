import math
import numpy
import random
import matplotlib.pyplot as plt
import string
import time
from Crypto.Util.number import long_to_bytes, bytes_to_long

# Implementazione dell'Algoritmo di Euclide Esteso (EEA)
# In input vengono forniti i due interi a, b di cui si vuole conoscere l'MCD e i valori x e y tc 
# MCD = x*a + y*b
# In output viene ritornata una tupla [MCD,x,y]
# In questa implementazione il vettore r[i] ha 3 componenti: 
#       - in r[i][0] il valore del resto al passo i-esimo
#       - in r[i][1] e r[i][2] i valori di x e y tali che r[i][0] = r[i][1]*a + r[i][2]*b
# Il calcolo del resto i-esimo viene svolto come r[i] = r[i-2] - q*r[i-1] fino a quando r[i][0] != 0
def EEA(a,b):
    r = {}
    # Inizialmente vengono ordinati a e b in modo che l'algoritmo possa funzionare (verranno considerati nella posizione corretta per i valori di ritorno)
    if(a > b):
        r[0] = numpy.array([a,1,0])
        r[1] = numpy.array([b,0,1])
    else:
        r[0] = numpy.array([b,1,0])
        r[1] = numpy.array([a,0,1])
    
    i=1
    while r[i][0] != 0:
        i += 1
        q = r[i-2][0]//r[i-1][0]
        r[i] = r[i-2] -q*r[i-1]
    
    if(a > b):
        return(r[i-1][0],r[i-1][1],r[i-1][2])
    else:
        return(r[i-1][0],r[i-1][2],r[i-1][1])

# Algoritmo di esponenziazione veloce che ritorna il valore a^m mod n
# L'esponente m viene scomposto in un vettore di bit, questo viene scansionato per eseguire certe operazioni su d e c
# d è il valore corrente della computazione, c è l'esponente corrente a cui è stato elevato il valore (a^c mod n = d ad ogni passo)
def fastExp(a,m,n):
    mBits = [int(k) for k in bin(m)[2:]]
    # c = 0
    d = 1
    for i in mBits:
        d = (d*d)%n
        # c = 2*c
        if(i == 1):
            d = (a*d)%n
            # c += 1
    return d

# Test di Compositness di Miller Rabin
def testMR(p): 
    NUM_TESTS = 5 # Numero di iterazioni del test. L'accuratezza del test sarà 1 - 4^(-NUM_TESTS) quindi = 0,9990
    # Calcolo la massima potenza del 2 r contenuta in p-1 e calcolo m come (p-1)/2^r
    r = ((p-1) & (~((p-1) - 1)))
    r = int(math.log2(r))
    m = (p-1)//(2**r)

    composite = False # Variabile booleana che verifica che p sia o meno composto
    j = 0
    while(j < NUM_TESTS and not composite): 
        x = random.randrange(1, p-1, 2) # Genero un numero casuale x dispari 
        # Vettore che contiene una sequenza di r numeri calcolati: al primo passo x^m mod p, 
        # quindi (chiamando il valore precedente calcolato come x_1) x_1^2 mod p
        xVec = [] 
        e = fastExp(x,m,p) #x^m mod p
        if(e - p == -1):
            xVec.append(-1)
        else:
            xVec.append(e)
        i = 0
        while(i < r):
            e = fastExp(xVec[-1],2,p) # x_1^2 mod p
            if(e - p == -1):
                xVec.append(-1)
            else:
                xVec.append(e)
            i += 1
        if(not (xVec[0] == 1 or -1 in xVec[:-1])): # Verifico l'esito del test di Miller Rabin 
            composite = True
        j += 1

    return composite

# Algoritmo di generazione di numeri primi
# Viene generato un nuovo numero intero randomico fino a quando tale valore risulta composto dal test di Miller Rabin
def primeGen(k):
    p = random.getrandbits(k)
    i = 1
    while(testMR(p)):
        p = random.getrandbits(k)
        i += 1
    # print(i)
    return p

# Classe che implementa l'algoritmo RSA
class RSA:
    # Inizializzazione dell'algoritmo in cui 
    #   - vengono generati p e q primi di lunghezza k (preso in ingresso)
    #   - vengono calcolati n e il totiente di n
    #   - preso e = 65537 si verifica se è coprimo con il totiente e si calcola d come inverso moltiplicativo di e
    #   - si predispone l'utilizzo dell'algoritmo di decryption con il teorema cinese del resto calcolando cp e cq
    def __init__(self, k = 1024):
        self.p = primeGen(k)
        self.q = primeGen(k)
        self.n = self.p*self.q
        self.totn = (self.p-1)*(self.q-1)
        self.e = 65537
        while(EEA(self.e, self.totn)[0] != 1):
            self.e = primeGen(16)
        self.d = EEA(self.e, self.totn)[1]
        if(self.d < 0):
            self.d += self.totn
        self.cp = self.q*(EEA(self.q,self.p)[1] % self.p) # q * inverso moltiplicativo di q modulo p
        self.cq = self.p*(EEA(self.p,self.q)[1] % self.q) # p * inverso moltiplicativo di p modulo q

    # Fase di encryption di un messaggio m:
    #   - Il messaggio viene decodificato da stringa a intero, viene verificato che l'm ottenuto sia coprimo con n
    #   - Viene svolta la codifica utilizzando la funzione di esponenziazione veloce implementata che ritorna m^e mod n
    def encrypt(self, m):
        while(bytes_to_long(m.encode()) >= self.n):
            m = m[:-1]
        while(EEA(self.n, bytes_to_long(m.encode()))[0] != 1):
            m += " "
        m = bytes_to_long(m.encode())
        return fastExp(m,self.e,self.n)
    
    # Fase di decryption del ciphertext c:
    #   - Il ciphertext in ingresso si presume che sia un numero intero
    #   - Viene svolta la decodifica utilizzando la funzione di esponenziazione veloce implementata che ritorna c^d mod n
    def decrypt(self, c):
        # return fastExp(c,self.d,self.n)
        return long_to_bytes(fastExp(c,self.d,self.n)).decode()

    # Fase di decryption del ciphertext c utilizzando il teorema cinese del resto:
    #   - cp e cq sono già stati calcolati in precedenza
    #   - vengono calcolati dp e dq
    #   - viene ritornato il valore [((c mod p)^(d mod p-1) mod p) * q * (q^-1 mod p)] + [((c mod q)^(d mod q-1) mod q) * p * (p^-1 mod q)]
    def decryptCRT(self, c):
        dp = fastExp(c%self.p,self.d%(self.p-1),self.p) # (c mod p)^(d mod p-1) mod p
        dq = fastExp(c%self.q,self.d%(self.q-1),self.q) # (c mod q)^(d mod q-1) mod q
        # return (dp*self.cp + dq*self.cq )% self.n 
        return long_to_bytes((dp*self.cp + dq*self.cq )% self.n).decode()
        
# Funzione di supporto che genera stringhe casuali di dimensione size
def id_generator(size, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


noCRT = []
CRT = []
start_time = time.time()
r = RSA(1024) # Inizializzazione di RSA generando chiavi private da 1024 bit ciascuna 
for i in range(1): # Ciclo su 100 plaintext diversi per testare le versioni di decryption RSA con e senza l'utilizzo del Teorema Cinese del Resto
    pt = id_generator(random.getrandbits(8)) # plaintext di dimensione 2^8 chars
    ct = r.encrypt(pt)

    start_time = time.time()
    dt = r.decrypt(ct)
    noCRT.append(time.time() - start_time)
    # print(dt)
    start_time = time.time()
    dtCRT = r.decryptCRT(ct)
    CRT.append(time.time() - start_time)

# print(CRT)
# print(noCRT)
# Calcolo della media di CRT e noCRT
length = len(CRT)
mCRT = sum(CRT)/length
mnoCRT = sum(noCRT)/length
# Stampa del grafico relativo al run corrente
fig, ax = plt.subplots()
ax.plot(range(length), CRT, '#ff7f0e', label='CRT')
ax.plot(range(length), [mCRT for i in range(length)], '#ff7f0e', linestyle='dashed',markersize=2, label='CRT avg')
ax.plot(range(length), noCRT, '#1f77b4', label='no CRT')
ax.plot(range(length), [mnoCRT for i in range(length)], '#1f77b4', linestyle='dashed', markersize=2, label='no CRT avg')
plt.xlabel('Test ID')
plt.ylabel('Execution Time (s)')
leg = ax.legend()
plt.show()