import math
import numpy

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
        q = int(math.floor(r[i-2][0]/r[i-1][0]))
        r[i] = r[i-2] -q*r[i-1]
        # r[i] = [r[i-2][0]-q*r[i-1][0],r[i-2][1] - q*r[i-1][1], r[i-2][2] - q*r[i-1][2]]
    if(a > b):
        return(r[i-1][0],r[i-1][1],r[i-1][2])
    else:
        return(r[i-1][0],r[i-1][2],r[i-1][1])
    

a = pow(11,100)-12345677
b = pow(10,100) + 1234567898765467890876543456789087654345678908765432345678904323456789876543456788
mcd, x, y = EEA(a,b)
print("The MCD between "+str(a)+" and "+str(b)+" is: "+str(mcd))
print("They are decomposed as: ("+str(x)+" x "+str(a)+") + ("+str(y)+" x "+str(b)+") = "+str(mcd))