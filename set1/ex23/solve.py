# Funzione che stampa tutti i fattori di un intero (sia numeri primi che non)
def allFactors(x):
    factors = []
    for i in range(1, x + 1):
        if x % i == 0:
            factors.append(i)
    return factors

# Testo cifrato con l'algoritmo di Vigenere, deve essere decifrato (viene usato in lowercase)
ct = "EIVDMAOHSVVUPXYSAYMNAAOMWOGKHKTECDYTDRIBRPLECHWJQLBELWTCGWIJTECXBTPIGTBTBACXVFIHIRBDOGGZXYHSEEFBNDMRGQOXRWIINSMHXNOVPBXQIXYDYTDHNAROWKWLLPWYXPMPSZUXKCPHFGNBNMQARYPREDSEBLXTXVRVPOMFPXKTYKELWBRTMTJEIIEIGEGLIEKVZRWVFGAAAETHUQAXYGFZFLTRRKVNPOXQNSLDYFEFJSEAWNPHICRSHUUMZVGDXWDYIQIGEIMFFQVPFNGRXFBTTXFRVMGQTMKENAEMZIGJJNRXHFZNUEEQSIGQMYCCDALXETKVCGZLMCMTDYTTXQGFVIFNTHNUNATAMWYNCLGDRFRMMIETPRKVZRWMJUGTGBVOEABAGCKTMFEEWUSOWBMFPXJZIKETTDNTBHDILVULBDXVHVVGBRHEUUMMRTKHVQVTQDYIOYHFVWBSWABMCXYQLXSGWFRCAHLISBQYIOGLCVPOBRDVKAGTKXBVRUMLCEEIMNXPXWDYGNHJASNQUVHHBVRTQGRXQVXYMTAMANNTEGKIKAAXTAMFZGMMCPGYANAEKSSRRGHSRSDBUGYDIHRIZBNEIUTCFBRBVRUPHSAHVDMTNWTCBMMWFXQZZNAEXGSLQCVYCXSQWHMXBVRUWEGEWZENGAMQCAVPTRHRFZMXNLMWGUZACISIUWYRHUOAQTWNAEPMFEIMECHNLFCPRZEXRIGOHUGXXMEPVFBXSHNHJCZXAGIRFYLWAMBLQCKCVSEQQHNMJSLQCBLPRPIURTAMMYNJXFPTGKQHNMBVRANKMBXZYYMOMQARHWKRWIZDIPNLBFNPOXPTEJAHLYXAPHVBAYIWRXFBAFVCJVPTRHECXNAAMLSSKVXQBIJAQAEGBVRAZXFPTGKNAERTZOGUX".lower()
# Frequenze delle lettere nella lingua inglese (le lettere sono state convertite ad interi per una più semplice gestione)
engFreq = {0: 0.08167, 1: 0.01492, 2: 0.02782, 3: 0.04253, 4: 0.12702, 5: 0.02228, 6: 0.02015, 7: 0.06094, 8: 0.06966, 9: 0.00153, 10: 0.00772, 11: 0.04025, 12: 0.02406, 13: 0.06749, 14: 0.07507, 15: 0.01929, 16: 0.00095, 17: 0.05987, 18: 0.06327, 19: 0.09056, 20: 0.02758, 21: 0.00978, 22: 0.0236, 23: 0.0015, 24: 0.01974, 25: 0.00074}

# Cerchiamo i trigrammi che si ripetono all'interno del ciphertext e ne analizziamo le distanze per applicare il Test di Kasiski
ngramsAppearances = {} # Dizionario che conterrà i trigrammi che si ripetono più di una volta con le relative distanze
i = 0
while i+3 <= len(ct):
    gram = ct[i:i+3]
    if(gram not in ngramsAppearances):
        ngramsAppearances[gram] = [] # Ad ogni trigramma è associato il vettore delle distanze delle apparizioni
        j = i+3
        while j+3 <= len(ct):
            if(gram == ct[j:j+3]):
                ngramsAppearances[gram].append(j-i)
            j += 1
        if(len(ngramsAppearances[gram]) == 0):
            ngramsAppearances.pop(gram)
    i += 1
print(ngramsAppearances)

# Analizzo quali sono i fattori che compaiono più volte nelle distanze fra trigrammi per poi testare queste come lunghezze possibili della chiave
factors = {}
for gram in ngramsAppearances:
    for val in ngramsAppearances[gram]: # Scompongo ogni distanza in fattori (non per forza primi) e aggiungo 1, nel vettore dei fattori, in corrispondenza del fattore trovato
        currentFactors = allFactors(val) 
        for fac in currentFactors:
            if(fac not in factors):
                factors[fac] = 0
            factors[fac] += 1
# print(factors)

# Restringo il range dei fattori e li ordino secondo il loro valore
okFactors = {}
for i in range(2,30):
    if(i in factors):
        okFactors[i] = factors[i]
    else:
        okFactors[i] = 0
print(okFactors) 
highestVal = sorted(okFactors, key=okFactors.get, reverse=True)
for v in highestVal:
    print(v, okFactors[v])

# Scelgo manualmente il valore corretto della chiave, 15, ed inizio il vero e proprio attacco
m = 15

# Dispongo il testo in colonne formando una matrice che chiamiamo txt
cols = len(ct)//m if len(ct)%m == 0 else 1+(len(ct)//m) 
txt = {}
for i in range(m):
    txt[i] = []
    for j in range(cols):
        if i+j*m < len((ct)):
            txt[i].append(ct[i+j*m])
# print(txt)

# Per ogni riga della matrice calcolo l'indice di coincidenza
coincIndex = {}
for i in range(m):
    freq = {j:txt[i].count(j) for j in txt[i]}
    coincIndex[i] = 0
    for j in freq:
        coincIndex[i] += freq[j]*(freq[j]-1)/(len(txt[i])*(len(txt[i])-1))

# Viene costruita la chiave carattere per carattere: per ogni riga della matrice del testo estraggo la distribuzione dei caratteri e la confronto con 
# la distribuzione della lingua inglese shiftandola da 1 a 25 volte. Il numero di shift fatti corrisponde al valore numerico della lettera della chiave.
# Quindi scelgo la distribuzione che fra queste rende massimo il prodotto scalare con la distribuzione della lingua inglese.
key = []
scalProds = []
for i in range(m):
    distr = {ord(j)-97:txt[i].count(j)/len(txt[i]) for j in txt[i]}
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
    scalProds.append(max(scalarProds))
print(key)
print(scalProds)

# Infine stampo il plaintext ottenuto dalla decifratura del ciphertext con la chiave ottenuta
pt = ""
i = 0
for char in ct:
    pt += chr(((ord(char)-ord(key[i%len(key)]))%26)+97)
    i+=1
print(pt)