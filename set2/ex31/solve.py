import math
import numpy
import random
import string
import time
from Crypto.Util.number import long_to_bytes, bytes_to_long

def EEA(a,b):
    r = {}
    if(a > b):
        r[0] = numpy.array([a,1,0])
        r[1] = numpy.array([b,0,1])
    else:
        r[0] = numpy.array([b,1,0])
        r[1] = numpy.array([a,0,1])
    i=1
    while r[i][0] != 0:
        i += 1
        q = r[i-2][0]//r[i-1][0] #todo check validità int(math.floor)
        r[i] = r[i-2] -q*r[i-1]
        # r[i] = [r[i-2][0]-q*r[i-1][0],r[i-2][1] - q*r[i-1][1], r[i-2][2] - q*r[i-1][2]]
    if(a > b):
        return(r[i-1][0],r[i-1][1],r[i-1][2])
    else:
        return(r[i-1][0],r[i-1][2],r[i-1][1])

# a^m mod n
def fastExp(a,m,n):
    # print(m)
    mBits = [int(k) for k in bin(m)[2:]]
    c = 0
    d = 1
    for i in mBits:
        d = (d*d)%n
        c = 2*c
        if(i == 1):
            d = (a*d)%n
            c += 1
    # print(c)
    return d

def testMR(p): # 16/4 1
    r = ((p-1) & (~((p-1) - 1)))
    r = int(math.log2(r))
    m = (p-1)//(2**r)

    composite = False
    j = 0
    while(j < 5 and not composite):
        x = random.randrange(1, p-1, 2)
        xVec = []
        e = fastExp(x,m,p)
        if(e - p == -1):
            xVec.append(-1)
        else:
            xVec.append(e)
        i = 0
        while(i < r):
            e = fastExp(xVec[-1],2,p)
            if(e - p == -1):
                xVec.append(-1)
            else:
                xVec.append(e)
            i += 1
        if(not (xVec[0] == 1 or -1 in xVec[:-1])): #or (xVec[-1] == 1 and (xVec[0] == 1 or 1 not in xVec[:-1] or -1 in xVec[:-1]))
            composite = True
        j += 1
        # if(composite == True):
        #     print(xVec)
        #     print(sympy.isprime(p), composite)
        #     print(p)
        #     print()

    return composite

def primeGen(k):
    p = random.getrandbits(k)
    i = 1
    while(testMR(p)):
        p = random.getrandbits(k)
        i += 1
    print(i)
    return p

class RSA:
    def __init__(self, k):
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
        self.cp = self.q*(EEA(self.q,self.p)[1] % self.p)
        self.cq = self.p*(EEA(self.p,self.q)[1] % self.q)

    def encrypt(self, m):
        while(EEA(self.n, bytes_to_long(m.encode()))[0] != 1):
            m += " "
        m = bytes_to_long(m.encode())
        return fastExp(m,self.e,self.n)
    
    def decrypt(self, c):
        # return long_to_bytes(fastExp(c,self.d,self.n)).decode()
        return fastExp(c,self.d,self.n)

    def decryptCRT(self, c):
        dp = fastExp(c%self.p,self.d%(self.p-1),self.p)
        dq = fastExp(c%self.q,self.d%(self.q-1),self.q)
        # return long_to_bytes((dp*self.cp + dq*self.cq )% self.n).decode()
        return (dp*self.cp + dq*self.cq )% self.n
        

def id_generator(size, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


# for i in range(1000):
#     p = primeGen(1024)
# print(p)

noCRT = []
CRT = []
start_time = time.time()
r = RSA(1024)
for i in range(100):
    pt = id_generator(random.getrandbits(8)) # plaintext di dimensione 2^8 chars
    
    ct = r.encrypt(pt)

    start_time = time.time()
    dt = r.decrypt(ct)
    noCRT.append(time.time() - start_time)

    start_time = time.time()
    dtCRT = r.decryptCRT(ct)
    CRT.append(time.time() - start_time)

    if(dt != dtCRT):
        print(dt)
        print(dtCRT)
print(CRT)
print(noCRT)
