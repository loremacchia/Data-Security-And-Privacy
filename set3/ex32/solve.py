import math

# L'input è una lista di coppie (elemento, probabilità)
def huffman(input):
    nodes = {} # Dizionario contenente tutti i nodi dell'albero
    edge = [] # Lista di nodi da espolorare
    currentID = 0
    initial = {} # Foglie dell'albero

    # Inizializzazione dell'insieme dei nodi foglia con il vettore di input
    for inp in input:
        node = {}
        node["symbol"] = inp[0]
        node["probability"] = inp[1]
        node["value"] = None
        node["components"] = []
        initial[currentID] = node
        nodes[currentID] = node
        edge.append(node)
        currentID += 1

    # Ciclo per creare l'albero    
    while(len(edge) > 1): # Fino a quando non viene trovata la radice dell'albero
        # Albero binario, cerchiamo i due valori minimi delle probabilità nei nodi in edge e creo un nuovo nodo con la somma di queste due 
        min1 = 1
        min2 = 1
        el1 = None
        el2 = None
        for e in edge:
            if(e["probability"] < min2):
                el2 = e
                min2 = e["probability"]
                if(min2 < min1):
                    min1, min2 = min2, min1
                    el1, el2 = el2, el1
        # Creazione del nuovo nodo
        newNode = {}
        newNode["probability"] = round(min1 + min2, 4)
        newNode["components"] = [el1, el2]
        newNode["value"] = None
        # Aggiornamento di edge
        edge.remove(el1)
        edge.remove(el2)
        nodes[currentID] = newNode
        edge.append(newNode)
        currentID += 1
        
    # Inizializzazione della fase 2 dell'algoritmo
    edge[0]["value"] = ""
    toExpand = [edge[0]]
    # Ciclo fino a quando sono stati modificati i valori dei figli di tutti i nodi dell'albero 
    while(len(toExpand) != 0):
        currentExp = toExpand # toExpand non si modifica dinamicamente
        for el in currentExp:
            # Ad ogni figlio assegno il valore del padre a cui aggiungo 0 o 1
            for i in range(len(el["components"])):
                el["components"][i]["value"] = el["value"] + str(i)
                toExpand.append(el["components"][i])
            toExpand.remove(el)

    # print(nodes)
    # Creazione del dizionario per il codice ottenuto 
    retValue = {}
    retValue["chr_to_bin"] = {}
    retValue["bin_to_chr"] = {}
    for i in initial:
        retValue["bin_to_chr"][initial[i]["value"]] = initial[i]["symbol"]
        retValue["chr_to_bin"][initial[i]["symbol"]] = initial[i]["value"]
    # print(retValue)
    return retValue
            
# Funzione di codifica di una stringa con il relativo alfabeto da utilizzare
def encode(alphabet, string):
    encoded = ""
    for s in string:
        if(s in alphabet):
            encoded += alphabet[s]
    return encoded

# Funzione di decodifica di una stringa di bit con il relativo codice da utilizzare. Il codice deve essere prefix free
def decode(code, binary):
    finalString = ""
    currentString = ""
    for el in binary:
        if(currentString+el in code):
            finalString += code[currentString+el]
            currentString = ""
        else:
            currentString += el
    return finalString

# Funzione di calcolo dell'entropia di un alfabeto con l'uso della sua distribuzione di probabilità
def entropy(alphabet):
    value = 0
    for a in alphabet:
        value -= a[1]*math.log2(a[1])
    return value

# Lunghezza media del codice che in ingresso ottiene il codice da usare e la distribuzione delle probabilità dell'alfabeto
def meanLength(code, alphabet):
    value = 0
    for a in alphabet:
        if(a[0] in code):
            value += a[1]*len(code[a[0]])
    return value


# Tre tipi di alfabeto e relativa distribuzione per testare l'algoritmo di Huffman
engAlphabet = [('a', 0.08167), ('b', 0.01492), ('c', 0.02782), ('d', 0.04253), ('e', 0.12702), ('f', 0.02228), ('g', 0.02015), ('h', 0.06094), ('i', 0.06966), ('j', 0.00153), ('k', 0.00772), ('l', 0.04025), ('m', 0.02406), ('n', 0.06749), ('o', 0.07507), ('p', 0.01929), ('q', 0.00095), ('r', 0.05987), ('s', 0.06327), ('t', 0.09056), ('u', 0.02758), ('v', 0.00978), ('w', 0.0236), ('x', 0.0015), ('y', 0.01974), ('z', 0.00074)]
itAlphabet = [('a', 0.1174), ('b', 0.0092), ('c', 0.045), ('d', 0.0373), ('e', 0.1179), ('f', 0.0095), ('g', 0.0164), ('h', 0.0154), ('i', 0.1128), ('j', 0.0001), ('k', 0.0001), ('l', 0.0651), ('m', 0.0251), ('n', 0.0688), ('o', 0.0983), ('p', 0.0305), ('q', 0.0051), ('r', 0.0637), ('s', 0.0498), ('t', 0.0562), ('u', 0.0301), ('v', 0.021), ('w', 0.0001), ('x', 0.0001), ('y', 0.0001), ('z', 0.0049)]
fakeAlphabet = [("a",0.4),("b",0.2),("c",0.2),("o",0.2)]

# Test per gli algoritmi di encode e decode con generici codici prefix free
nonHuffCode = {'chr_to_bin': {'a': '0', 'b': '111', 'c': '110', 'd': '101'}, 'bin_to_chr': {'0': 'a', '111': 'b', '110': 'c', '101': 'd'}}
nonHuffCode1 = {'chr_to_bin': {'a': '00', 'b': '01', 'c': '10', 'd': '11'}, 'bin_to_chr': {'00': 'a', '01': 'b', '10': 'c', '11': 'd'}}

# Test degli algoritmi
usedAlphabet = itAlphabet
usedCode = huffman(usedAlphabet) # Test della generazione del codice con l'algoritmi di Huffman

# Verifica che lunghezza media del codice sia compresa fra entropia della distribuzione ed entropia della distribuzione+1
if(not(entropy(usedAlphabet) <= meanLength(usedCode["chr_to_bin"],usedAlphabet) < (entropy(usedAlphabet)+1))):
    print("Error in code generation")
else:
    # string = "abaco"
    string1 = "nellacrittoanalisilanalisidellefrequenzelostudiodellafrequenzadiutilizzodellelettereogruppidilettereinuntestocifratoquestometodoutilizzatoperviolareicifrariclassicileindaginiquantitativesuitestisiservonospessodiqualcheformadianalisidellefrequenze"
    # string2 = "incryptanalysisfrequencyanalysisalsoknownascountinglettersisthestudyofthefrequencyoflettersorgroupsoflettersinaciphertextthemethodisusedasanaidtobreakingclassicalciphers"

    encoded = encode(usedCode["chr_to_bin"],string1)
    print(encoded)

    print(decode(usedCode["bin_to_chr"],encoded))

        