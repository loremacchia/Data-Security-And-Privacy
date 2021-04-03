def allFactors(x):
    factors = []
    for i in range(1, x + 1):
        if x % i == 0:
            factors.append(i)
    return factors




ct = "EIVDMAOHSVVUPXYSAYMNAAOMWOGKHKTECDYTDRIBRPLECHWJQLBELWTCGWIJTECXBTPIGTBTBACXVFIHIRBDOGGZXYHSEEFBNDMRGQOXRWIINSMHXNOVPBXQIXYDYTDHNAROWKWLLPWYXPMPSZUXKCPHFGNBNMQARYPREDSEBLXTXVRVPOMFPXKTYKELWBRTMTJEIIEIGEGLIEKVZRWVFGAAAETHUQAXYGFZFLTRRKVNPOXQNSLDYFEFJSEAWNPHICRSHUUMZVGDXWDYIQIGEIMFFQVPFNGRXFBTTXFRVMGQTMKENAEMZIGJJNRXHFZNUEEQSIGQMYCCDALXETKVCGZLMCMTDYTTXQGFVIFNTHNUNATAMWYNCLGDRFRMMIETPRKVZRWMJUGTGBVOEABAGCKTMFEEWUSOWBMFPXJZIKETTDNTBHDILVULBDXVHVVGBRHEUUMMRTKHVQVTQDYIOYHFVWBSWABMCXYQLXSGWFRCAHLISBQYIOGLCVPOBRDVKAGTKXBVRUMLCEEIMNXPXWDYGNHJASNQUVHHBVRTQGRXQVXYMTAMANNTEGKIKAAXTAMFZGMMCPGYANAEKSSRRGHSRSDBUGYDIHRIZBNEIUTCFBRBVRUPHSAHVDMTNWTCBMMWFXQZZNAEXGSLQCVYCXSQWHMXBVRUWEGEWZENGAMQCAVPTRHRFZMXNLMWGUZACISIUWYRHUOAQTWNAEPMFEIMECHNLFCPRZEXRIGOHUGXXMEPVFBXSHNHJCZXAGIRFYLWAMBLQCKCVSEQQHNMJSLQCBLPRPIURTAMMYNJXFPTGKQHNMBVRANKMBXZYYMOMQARHWKRWIZDIPNLBFNPOXPTEJAHLYXAPHVBAYIWRXFBAFVCJVPTRHECXNAAMLSSKVXQBIJAQAEGBVRAZXFPTGKNAERTZOGUX".lower()
engFreq = {0: 0.08167, 1: 0.01492, 2: 0.02782, 3: 0.04253, 4: 0.12702, 5: 0.02228, 6: 0.02015, 7: 0.06094, 8: 0.06966, 9: 0.00153, 10: 0.00772, 11: 0.04025, 12: 0.02406, 13: 0.06749, 14: 0.07507, 15: 0.01929, 16: 0.00095, 17: 0.05987, 18: 0.06327, 19: 0.09056, 20: 0.02758, 21: 0.00978, 22: 0.0236, 23: 0.0015, 24: 0.01974, 25: 0.00074}

ngramsAppearances = {}
i = 0
while i+3 <= len(ct):
    gram = ct[i:i+3]
    # print(gram)
    if(gram not in ngramsAppearances):
        ngramsAppearances[gram] = []
        j = i+3
        while j+3 <= len(ct):
            # print(ct[j:j+3])
            if(gram == ct[j:j+3]):
                ngramsAppearances[gram].append(j-i)
            j += 1
        if(len(ngramsAppearances[gram]) == 0):
            ngramsAppearances.pop(gram)
    i += 1

# print(ngramsAppearances)

factors = {}
for gram in ngramsAppearances:
    for val in ngramsAppearances[gram]:
        currentFactors = allFactors(val)
        for fac in currentFactors:
            if(fac not in factors):
                factors[fac] = 0
            factors[fac] += 1
# print(factors)
okFactors = {}
for i in range(2,30):
    if(i in factors):
        okFactors[i] = factors[i]
    else:
        okFactors[i] = 0

# print(okFactors) #TODO fare il grafico

highestVal = sorted(okFactors, key=okFactors.get, reverse=True)
# for v in highestVal:
#     print(v, okFactors[v])


m = 15
cols = len(ct)//m if len(ct)%m == 0 else 1+(len(ct)//m)
txt = {}
for i in range(m):
    txt[i] = []
    for j in range(cols):
        if i+j*m < len((ct)):
            txt[i].append(ct[i+j*m])
# print(txt)

coincIndex = {}
for i in range(m):
    freq = {j:txt[i].count(j) for j in txt[i]}
    coincIndex[i] = 0
    for j in freq:
        coincIndex[i] += freq[j]*(freq[j]-1)/(len(txt[i])*(len(txt[i])-1))
# print(coincIndex)

key = []
for i in range(m):
    distr = {ord(j)-97:txt[i].count(j)/len(txt[i]) for j in txt[i]}
    # print(distr)
    scalarProds = []
    for k in range(26):
        scal = 0
        newDistr = {}
        for j in range(26):
            if((j+k)%26 in distr):
                newDistr[j] = distr[(j+k)%26]
            else: 
                newDistr[j] = 0
        for j in range(26):
            scal += newDistr[j]*engFreq[j]
        scalarProds.append(scal)
    key.append(chr(scalarProds.index(max(scalarProds))+97))
            
print(key)
pt = ""

i = 0
for char in ct:
    pt += chr(((ord(char)-ord(key[i%len(key)]))%26)+97)
    i+=1
print(pt)