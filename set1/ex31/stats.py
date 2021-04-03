import math

wordSet = []
ngrams = {}
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

for m in range(1,5):
    ngrams[m]["indexCoincidence"] = 0
    ngrams[m]["shannonEntropy"] = 0
    for val in ngrams[m]["set"]:
        ngrams[m]["indexCoincidence"] += ((ngrams[m]["set"][val])*(ngrams[m]["set"][val]-1))/((ngrams[m]["totalNum"])*(ngrams[m]["totalNum"]-1))
        ngrams[m]["shannonEntropy"] -= (ngrams[m]["set"][val]/ngrams[m]["totalNum"])*math.log2(ngrams[m]["set"][val]/ngrams[m]["totalNum"])

print(ngrams)
