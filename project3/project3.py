"""
Created on Sat Jan 23 12:11:50 2021

@author: mcaptain79
"""
#reading values line by line and saving them in the target list
#list containing ferdowsi poems
ferdowsiList = open('ferdowsi_train.txt',encoding='utf-8').readlines()
#list containing hafez poems
hafezList = open('hafez_train.txt',encoding='utf-8').readlines()
#list containing molavi poems
molaviList = open('molavi_train.txt',encoding='utf-8').readlines()
"""
now we should fill our test sets if starting with one its ferdowsi
                        if tow its hafez and three is for molavi
"""
ferdowsiTestList = []
hafezTestList = []
molaviTestList = []
for i in open('test_file.txt',encoding = 'utf-8'):
    number , text = i.split('\t')
    if number == '1':
        ferdowsiTestList.append(text)
    elif number == '2':
        hafezTestList.append(text)
    else:
        molaviTestList.append(text)
"""
function below calculates ocuurance of a word in list of texts
                this works in way that counts specific word occurance in list of texts
"""
def calculate_occurance(myList,word):
    occurence = 0
    for i in myList:
        for j in i.split():
            if word == j:
                occurence += 1
    return occurence
#function to calculate number of word in the list of Text
def calc_word_num(myList):
    res = 0
    for i in myList:
        res += len(i.split())
    return res
#saving these for each person in a variable
ferdowsiWordNum = calc_word_num(ferdowsiList)
hafezWordNum = calc_word_num(hafezList)
molaviWordNum = calc_word_num(molaviList)
wordNumList = [ferdowsiWordNum,hafezWordNum,molaviWordNum]
#function below calculates unigram for each word and saves them in dictionary
def unigram(myList,index):
    myDict = {}
    for i in myList:
        for j in i.split():
            if j not in myDict:
                myDict[j] = calculate_occurance(myList, j)/ wordNumList[index]
    return myDict
#filling ferdowsi and hafez and molavi unigram dictionaries with correct values
ferdowsiUnigramDict = unigram(ferdowsiList,0)
hafezUnigramDict = unigram(hafezList,1)
molaviUnigramDict = unigram(molaviList,2)
#this function calculates number of occurance of specific two consecutive words
def calculate_occurance_volume2(myList,sentence):
    res = 0
    for i in myList:
        res += i.count(sentence)
    return res
#function below calculates bigram for list of words
def bigram(myList,unigramDict,wordNum):
    myDict = {}
    for i in myList:
        tmp = i.split()
        for i in range(len(tmp)-1):
            if tmp[i]+' '+tmp[i+1] not in myDict:
                #for start and end character
                if i == 0 or i == len(tmp)-1:
                    myDict[tmp[i]] = (unigramDict[tmp[i]]*wordNum)/len(myList)
                else:
                    myDict[tmp[i]+' '+tmp[i+1]] = calculate_occurance_volume2(myList, tmp[i]+' '+tmp[i+1])/(unigramDict[tmp[i]]*wordNum)
        #we didnt calculate this in our loops
        myDict[tmp[0]+' '+tmp[1]] = calculate_occurance_volume2(myList, tmp[0]+' '+tmp[1])/(unigramDict[tmp[0]]*wordNum)            
    return myDict
#filling bugram dict for ferdowsi and hafez and molavi
ferdowsiBigramDict = bigram(ferdowsiList, ferdowsiUnigramDict, ferdowsiWordNum)
hafezBigramDict = bigram(hafezList, hafezUnigramDict, hafezWordNum)
molaviBigramDict = bigram(molaviList,molaviUnigramDict,molaviWordNum)                   
#testing our models
def backoff(testList,unigramDict,bigramDict,text,y1,y2,y3,e):
    res = 1
    tmp = text.split()
    for i in range(len(tmp)):
        uni = 0
        bi = 0
        if i == 0 or i == len(tmp)-1:
            if tmp[i] not in bigramDict:
                uni = 1
                bi = 0
            else:
                uni = 1
                bi = bigramDict[tmp[i]]
        else:
            value = tmp[i]+' '+tmp[i+1]
            if value in bigramDict and tmp[i] in unigramDict:
                uni = unigramDict[tmp[i]]
                bi = bigramDict[value]
            elif value in bigramDict and tmp[i] not in unigramDict:
                uni = 0
                bi = bigramDict[value]
            elif value not in bigramDict and tmp[i] in unigramDict:
                uni = unigramDict[tmp[i]]
                bi = 0
            else:
                uni = 0
                bi = 0
        res = res*(y3*bi+y2*uni+y1*e)
    """for index zero and one we should make specific calculation
                    because i didnt count them in calculation
    """
    u,b = 0,0
    value = tmp[0]+' '+tmp[1]
    if value in bigramDict and tmp[0] in unigramDict:
        u = unigramDict[tmp[0]]
        b = bigramDict[value]
    elif value in bigramDict and tmp[0] not in unigramDict:
        u = 0
        b = bigramDict[value]
    elif value not in bigramDict and tmp[0] in unigramDict:
        u = unigramDict[tmp[0]]
        b = 0
    else:
        u = 0
        b = 0
    res = res*(y3*b+y2*u+y1*e)
    return res
#function below calculates accuracy
def accurracy_score(y1,y2,y3,e):
    counter = 0
    for i in ferdowsiTestList:
        a1 = backoff(ferdowsiList, ferdowsiUnigramDict, ferdowsiBigramDict, i, y1, y2, y3, e)
        a2 = backoff(hafezList, hafezUnigramDict, hafezBigramDict, i, y1, y2, y3, e)
        a3 = backoff(molaviList, molaviUnigramDict, molaviBigramDict, i, y1, y2, y3, e)
        if a1 > a2 and a1 > a3:
            counter += 1
    for i in hafezTestList:
        a1 = backoff(ferdowsiList, ferdowsiUnigramDict, ferdowsiBigramDict, i, y1, y2, y3, e)
        a2 = backoff(hafezList, hafezUnigramDict, hafezBigramDict, i, y1, y2, y3, e)
        a3 = backoff(molaviList, molaviUnigramDict, molaviBigramDict, i, y1, y2, y3, e)
        if a2 > a1 and a2 > a3:
            counter += 1
    for i in molaviTestList:
        a1 = backoff(ferdowsiList, ferdowsiUnigramDict, ferdowsiBigramDict, i, y1, y2, y3, e)
        a2 = backoff(hafezList, hafezUnigramDict, hafezBigramDict, i, y1, y2, y3, e)
        a3 = backoff(molaviList, molaviUnigramDict, molaviBigramDict, i, y1, y2, y3, e)
        if a3 > a2 and a3 > a1:
            counter += 1
    return counter/(len(ferdowsiTestList)+len(hafezTestList)+len(molaviTestList))
res1 = accurracy_score(0.34, 0.33, 0.33, 0.2)
print(res1)
res2 = accurracy_score(0.34, 0.33, 0.33, 0.8)
print(res2)
res3 = accurracy_score(0.7, 0.1, 0.2, 0.8)
print(res3)
res4 = accurracy_score(0.1, 0.1, 0.8, 0.1)
print(res4)
res5 = accurracy_score(0.05, 0.05, 0.9, 0.0001)
print(res5)

                


    
    
    
    
    
    
    
    
    
    
    