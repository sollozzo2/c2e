import csv
from nltk.corpus import cmudict
import itertools
from difflib import SequenceMatcher
import jellyfish
import re

allCh = {}
with open("allPinyin.txt", encoding='utf-8') as fd:
    st = set()
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    for row in rd:
        nut = row[1].strip('[]ʰㄥɿ̯ㄩ')
        for char in nut:
            st.add(char)
        allCh[row[0]] = nut
    #print(st)

toStrip = 'ʰㄥɿ̯ㄩ' 
#get doubles in here - we fucking need them.
doubles = {'tɕ':['JH'], 'aɪ':['AY'],'ɑʊ':['AW'],'eɪ':['EY'],'ɤʊ':['OW'], 'tʂ':['ZH', 'JH'], 'ɯʌ':['UH', 'AH', 'AA']} #ch, ao, ou, ia, etc.

allphons = {'m':['M'], 'ʐ':['R'], 'f':['F'], 'ʊ':['UH'], 'ɪ':['IH'], 'ə':['AH', 'UH', 'AO'], 'o':['AA','AO'],
            'y':['IY','UW','Y','IH'],'ɛ':['EH'], 'ɑ':['AH', 'AA','AO', 'AW'], 't':['T','D'], 'ɤ':['AW','OW'], 'ɕ':['SH'],
            'ɻ':['R'], 'e':['EH'], 'a':['AA'], 'k':['G', 'K'], 'ɯ':['AH','UH'], 'ŋ':['NG'],
            'ɔ':['AA','AH','AO'], 'ʂ':['CH','SH'], 'n':['N'], 'x':['HH'], 'l':['L'],
            'i':['IY', 'IH', 'Y'], 'ʌ':['AH'], 'h':['HH'], 'u':['UW','W'], 'œ':['EH','EY'], 'p':['P','B'], 'ʅ':['UHR',''], 's':['S']}
d = cmudict.dict()

#jiang
#[['JH', 'IY']]
#[['Y', 'AH', 'NG']]
# ignore starting phoneme of second word if it's already covered in the first.

def e2c(word):
    global d
    prons = d[word]
    prons = [[x.strip('012') for x in y] for y in prons]
    tmp = []
    for pron in prons:
        tmp += [''.join(pron)]
    prons = tmp
    print(prons)
    vowels = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW']
    cons = ['B', 'CH', 'D', 'DH', 'DR', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N', 'NG', 'P', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH']
    #convert to pinyin directly? there are only so many anyway.
    #split by consonants. if a word ends in consonant, or a consonant is followed by another consnant,
    #then just make it -'e' by default. or -i? i.e. chi, alice -> ai li si
    #then pinyin to characters.
    
    toSkip = 0
    allIndices = []
    for pron in prons:
        consIndices = []
        for i in range(len(pron)):
            if toSkip > 0:
                toSkip -= 1
                continue
            if i < len(pron) - 2:
                single = pron[i]
                double = pron[i:i+2]
                #print(single, double)
                if double in cons:
                    consIndices += [pron.find(double)]
                    toSkip = 1
                    continue
                else:
                    if single in cons:
                        consIndices += [pron.find(double)]
        allIndices += [consIndices]
    for i in range(len(allIndices)):
        for j in range(len(allIndices[i])):
            if j < len(allIndices[i]) - 1:
                #print(prons[i], allIndices[i], allIndices[i][j], allIndices[i][j+1])
                print(prons[i][allIndices[i][j]:allIndices[i][j+1]])
            else:
                #print(prons[i], allIndices[i], allIndices[i][j])
                print(prons[i][allIndices[i][j]:])
    
                
    


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def cutOrNot(a, b):
    for i in range(len(a)):
        if a[i] == b[i]:
            if i < len(a) - 1:
                continue
            else:
                return True
        else:
            return False

def p2combs(pinyin):
    global toStrip
    global d
    #raw phonemes
    cphons = allCh[pinyin].strip(toStrip)
    cphons = re.sub('['+toStrip+']', '', cphons)
    print(cphons)
    cmuphons = []
    #list of lists
    #for phoneme in cphons:
    #    cmuphons += [allphons[phoneme]]
    #print(cmuphons)

    skip = False

    for i in range(len(cphons)):
        if skip:
            skip = False
            continue
        if i <= len(cphons) - 2 and len(cphons) >= 2:
            if cphons[i:i+2] in doubles:
                possibles = doubles[cphons[i:i+2]]
                cmuphons += [possibles]
                print('double spotted:', possibles, cphons[i:i+2])
                skip = True
                continue
        cmuphons += [allphons[cphons[i]]]
    
    combs = list(itertools.product(*cmuphons))
    combs = [list(x) for x in combs]
    combs = [''.join(x) for x in combs]
    return combs

def c2e(pinyin):
    combs = p2combs(pinyin)
    
    #pinyin: jiang -> gee-young
    res = ''
    curscore = 999
    curword = ''
    print(combs)
    for word in d:
        pronunciations = d[word]
        pronunciations = [[x.strip('012') for x in y] for y in pronunciations]
        pronunciations = [''.join(x) for x in pronunciations]
        #pronunciations = ['NIH', 'XXX', ...]
        #pronunciations = [y for y in pronunciations if y in combs]
        
        
        for pron in pronunciations:
            for comb in combs:
                #recursion?
                if comb[:len(pron)] == pron and len(pron) < len(comb):
                    #lists of possibles are ordered by similarity, so go with the earliest.
                    print('substring found!', comb)
                    print('calling c2w:', [comb[len(pron):]])
                    print(word + '-' + combs2word([comb[len(pron):]]))
                    break
                if comb == pron:
                    print(word)
                else:
                    continue
                score = jellyfish.levenshtein_distance(pron, comb)
                if score < curscore:
                    print(curword)
                    curscore = score
                    curword = word
    return curword

def combs2word(combs):
    global d
    for word in d:
        pronunciations = d[word]
        pronunciations = [[x.strip('012') for x in y] for y in pronunciations]
        pronunciations = [''.join(x) for x in pronunciations]
        for pron in pronunciations:
            for comb in combs:
                if comb == pron:
                    return word
                    #print(word)
    return ''
