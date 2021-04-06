import math

# Costruisco il set di parole contenute nel testo mobydick.txt non considerando i caratteri speciali e gli spazi
wordSet = []
f = open("mobydick.txt", "r")
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

# Dal set di parole estraggo per ogni m da 1 a 4:
#   - il set di m-grams (ngrams[m]["set"])
#   - le occorrenze di ogni m-gram (ngrams[m]["set"][gram])
#   - il numero totale di m-grams (ngrams[m]["totalNum"])
ngrams = {}
for m in range(1,5):
    ngrams[m] = {}
    ngrams[m]["totalNum"] = 0
    ngrams[m]["set"] = {}
    for word in wordSet:
        i = 0
        while i+m <= len(word):
            gram = word[i:i+m]
            if gram not in ngrams[m]["set"]:
                ngrams[m]["set"][gram] = 0
            ngrams[m]["set"][gram] += 1
            i += 1
            ngrams[m]["totalNum"] += 1

# Per ogni m da 1 a 4 calcolo quindi:
#   - gli indici di coincidenza calcolati come sum([fi*(fi-1)]/[tot*(tot-1)]) con fi le occorrenze dell'm-gram i-esimo
#   - l'entropia di Shannon calcolata come sum(-[fi/tot]*lg(fi/tot)) con fi le occorrenze dell'm-gram i-esimo
for m in range(1,5):
    ngrams[m]["indexCoincidence"] = 0
    ngrams[m]["shannonEntropy"] = 0
    for val in ngrams[m]["set"]:
        ngrams[m]["indexCoincidence"] += ((ngrams[m]["set"][val])*(ngrams[m]["set"][val]-1))/((ngrams[m]["totalNum"])*(ngrams[m]["totalNum"]-1))
        ngrams[m]["shannonEntropy"] -= (ngrams[m]["set"][val]/ngrams[m]["totalNum"])*math.log2(ngrams[m]["set"][val]/ngrams[m]["totalNum"])
print(ngrams)