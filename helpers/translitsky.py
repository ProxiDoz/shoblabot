import re
import json
import urllib.request as req

__my_dict__ = {}
__words__ = json.load(open('helpers/words.json'))

def __prepareDict():
    dict = {}
    en = "qwertyuiop[]\\asdfghjkl;'zxcvbnm,."
    ru = "йцукенгшщзхъёфывапролджэячсмитьбю"
    
    for i in range(len(en)):
        dict[ord(en[i])] = ord(ru[i])

    return dict

def __isAllEnglish(text):
    cleaned = re.sub(r'[^a-zа-я ]', '', text.lower())
    splitted = cleaned.split(' ')

    for word in splitted:
        for char in word:
            unicode = ord(char)
            if not (unicode > 96 and unicode < 123):
                return False, []

    return True, splitted

def __isWordExists(word):
    if word in __words__:
        return __words__[word]

    res = True
    try:
        r = req.Request("https://od-api.oxforddictionaries.com/api/v2/words/en-us?q={}".format(word), headers={'app_id' : '', 'app_key' : ''})
        req.urlopen(r).read()
    except:
        res = False
    
    __words__[word] = res
    with open('helpers/words.json', 'w') as outfile:
        json.dump(__words__, indent=4, fp=outfile)
    
    return res

def isTranslitsky(centence):
    flag, words = __isAllEnglish(centence)

    if not flag:
        return False

    total_accuracy = 0
    word_accuracy = 100 / len(words)
    
    for word in words:
        total_accuracy += 0 if __isWordExists(word) else word_accuracy
        if total_accuracy >= 65:
            return True
    
    return False

def doTranslitskyRollback(input):
    return input.lower().translate(__my_dict__)

__my_dict__ = __prepareDict()
