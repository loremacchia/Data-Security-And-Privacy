import math
import numpy as np
import matplotlib.pyplot as plt

# Costruisco il set di parole contenute nel testo mobydick.txt non considerando i caratteri speciali e gli spazi
f = open("mobydick.txt", "r")
wordSet = []
for line in f:
    currentWord = ""
    for letter in line:
        if letter.isalpha():
            currentWord += letter
        else:
            if currentWord != "":
                wordSet.append(currentWord)
                currentWord = ""
f.close() 
print(wordSet)

# Dal set di parole estraggo per ogni n da 1 a 4:
#   - il set di n-grams (ngrams[n]["set"])
#   - le occorrenze di ogni n-gram (ngrams[n]["set"][gram])
#   - il numero totale di n-grams (ngrams[n]["totalNum"])
ngrams = {}
for n in range(1,5):
    ngrams[n] = {}
    ngrams[n]["totalNum"] = 0
    ngrams[n]["set"] = {}
    for word in wordSet:
        i = 0
        while i+n <= len(word):
            gram = word[i:i+n]
            if gram not in ngrams[n]["set"]:
                ngrams[n]["set"][gram] = 0
            ngrams[n]["set"][gram] += 1
            i += 1
            ngrams[n]["totalNum"] += 1

# Funzione per stampare un istrogramma delle frequenze delle lettere all'interno del testo
# I colori dell'istogramma sono più scuri a seconda se la frequenza è maggiore o meno
fig, ax = plt.subplots()
c = ax.bar(sorted(ngrams[1]["set"].keys()), ngrams[1]["set"].values(), 1.0,edgecolor="white", color='b')
lista = []
for i in c:
    lista.append(i.get_height())
for i in c:
    i.set_color((0.76,0.15,0,0.4 + i.get_height()*0.5/(max(lista)-min(lista))))
ax.set_ylabel('Frequenza')
ax.set_xlabel('Lettere')
ax.set_title('Istogramma della frequenza delle 26 lettere')
plt.show()

# Per ogni m da 1 a 4 calcolo quindi:
#   - gli indici di coincidenza calcolati come sum([fi*(fi-1)]/[tot*(tot-1)]) con fi le occorrenze dell'm-gram i-esimo
#   - l'entropia di Shannon calcolata come sum(-[fi/tot]*lg(fi/tot)) con fi le occorrenze dell'm-gram i-esimo
for n in range(1,5):
    ngrams[n]["indexCoincidence"] = 0
    ngrams[n]["shannonEntropy"] = 0
    for val in ngrams[n]["set"]:
        ngrams[n]["indexCoincidence"] += ((ngrams[n]["set"][val])*(ngrams[n]["set"][val]-1))/((ngrams[n]["totalNum"])*(ngrams[n]["totalNum"]-1))
        ngrams[n]["shannonEntropy"] -= (ngrams[n]["set"][val]/ngrams[n]["totalNum"])*math.log2(ngrams[n]["set"][val]/ngrams[n]["totalNum"])
print(ngrams)