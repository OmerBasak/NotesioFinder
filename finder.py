import requests, threading, sys, os
import time as t

def lower(string):
    string = r"{0}".format(string) 
    low = ""
    low = string.replace("I", "ı")
    low = low.replace("İ", "i")
    low = low.lower()
    return low

def converter(string):
    htmlSpecialCharacters = {'–': '&ndash;', '—': '&mdash;', '¡': '&iexcl;', '¿': '&iquest;', '"': '&quot;', '“': '&ldquo;', '”': '&rdquo;', '‘': '&lsquo;', '’': '&rsquo;', '«': '&laquo;', '»': '&raquo;', ' ': '&nbsp;', '&': '&amp;', '¢': '&cent;', '©': '&copy;', '÷': '&divide;', '>': '&gt;', '<': '&lt;', 'µ': '&micro;', '·': '&middot;', '¶': '&para;', '±': '&plusmn;', '€': '&euro;', '£': '&pound;', '®': '&reg;', '§': '&sect;', '™': '&trade;', '¥': '&yen;', 'á': '&aacute;', 'Á': '&Aacute;', 'à': '&agrave;', 'À': '&Agrave;', 'â': '&acirc;', 'Â': '&Acirc;', 'å': '&aring;', 'Å': '&Aring;', 'ã': '&atilde;', 'Ã': '&Atilde;', 'ä': '&auml;', 'Ä': '&Auml;', 'æ': '&aelig;', 'Æ': '&AElig;', 'ç': '&ccedil;', 'Ç': '&Ccedil;', 'é': '&eacute;', 'É': '&Eacute;', 'è': '&egrave;', 'È': '&Egrave;', 'ê': '&ecirc;', 'Ê': '&Ecirc;', 'ë': '&euml;', 'Ë': '&Euml;', 'í': '&iacute;', 'Í': '&Iacute;', 'ì': '&igrave;', 'Ì': '&Igrave;', 'î': '&icirc;', 'Î': '&Icirc;', 'ï': '&iuml;', 'Ï': '&Iuml;', 'ñ': '&ntilde;', 'Ñ': '&Ntilde;', 'ó': '&oacute;', 'Ó': '&Oacute;', 'ò': '&ograve;', 'Ò': '&Ograve;', 'ô': '&ocirc;', 'Ô': '&Ocirc;', 'ø': '&oslash;', 'Ø': '&Oslash;', 'õ': '&otilde;', 'Õ': '&Otilde;', 'ö': '&ouml;', 'Ö': '&Ouml;', 'ß': '&szlig;', 'ú': '&uacute;', 'Ú': '&Uacute;', 'ù': '&ugrave;', 'Ù': '&Ugrave;', 'û': '&ucirc;', 'Û': '&Ucirc;', 'ü': '&uuml;', 'Ü': '&Uuml;', 'ÿ': '&yuml;'}
    for k, v in htmlSpecialCharacters.items():
        if v in string:
            string = string.replace(v, k)
    return string

letters = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz"

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

keys = []

global counter
global found
counter, found = 0, 0

print("", file=open(r"Logs\finish.notes", "w"), end="")

speed = 2

def one():
    global counter
    global found

    def finder(string, task):
        global counter
        global found
        work = True

        letter = string
        
        try: 
            last = open("Logs\{0}.notes".format(task), "r").read()
            if last != "":
                if last == string[-1]: work = False
                else: letter = letter[letter.find(last)+1:]
        except FileNotFoundError: 
            print("", file=open("Logs\{0}.notes".format(task), "w"), end="")
        
        if work:
            for let in letter: 
                while True:
                    try: response = requests.get("https://notes.io/{0}".format(let), headers = headers).text
                    except requests.exceptions.ConnectionError:
                        while True:
                            t.sleep(30)
                            try:
                                response = requests.get("https://notes.io/{0}".format(let), headers = headers).text
                                break
                            except requests.exceptions.ConnectionError: print("Error")
                    if "<title>Notes" in response: break
                    else:
                        print("Title error: {0}".format(let))
                        t.sleep(15)
                f, l = response.find("</script></center>"), response.rfind('''<ins class="adsbygoogle"''')
                text = converter(response[f+9:l])[9:-9]
                low = lower(text)
                exist = False
                for key in keys:
                    if key in low:
                        exist = True
                        break
                counter+=1
                if exist == True: 
                    print(let, file=open("Logs\hey", "a"), flush=True, end=",")
                    found+=1
                print("{0} | {1}".format(counter, found))

                print(let, file=open(r"Logs\{0}.notes".format(task), "w"), flush=True, end="")
        print("{0}".format(task), file=open(r"Logs\finish.notes", "a"), flush=True, end=",")

    checkList = {}
    if speed == 3:
        for i in range(0,57,3):
            word = letters[i:i+3]
            keyX = "1_{0}".format(i)
            checkList[keyX] = word
            threading.Thread(target=finder, args=(word, keyX, )).start()
            
    elif speed == 2:
        for i in range(0,57,19):
            word = letters[i:i+19]
            keyX = "1_{0}".format(i)
            checkList[keyX] = word
            threading.Thread(target=finder, args=(word, keyX, )).start()
    elif speed == 1:
        word = letters
        keyX = "1_1"
        checkList[keyX] = word
        threading.Thread(target=finder, args=(word, keyX, )).start()
    else:
        print("Yazılımsal hata!")
        sys.exit()

    while True:
        for cList in list(checkList):
            if cList in open(r"Logs\finish.notes", "r").read(): 
                del checkList[cList]
                os.remove("Logs\{0}.notes".format(cList))
        if len(checkList) == 0: 
            break
        else: 
            temp = {}
            for cList in list(checkList): temp[cList] = open("Logs\{0}.notes".format(cList), "r").read()

            t.sleep(90)

            for cList in list(checkList):
                if temp[cList] == open("Logs\{0}.notes".format(cList), "r").read():
                    threading.Thread(target=finder, args=(checkList[cList], cList, )).start()
    return "ok"

def two():
    global counter
    global found

    def finder(string, task):
        global counter
        global found
        work = True

        letter0 = string
        letter1 = letters

        try: 
            last = open("Logs\{0}.notes".format(task), "r").read()
            if last != "": # ??
                if last == string[-1] + letters[-1]: work = False
                else: # ??
                    if last[1] == letters[-1]: # ?+z
                        letter0 = string[string.find(last[0])+1:]
                        letter1 = letters
                    else: # ?+z
                        letter0 = string[string.find(last[0]):]
                        letter1 = letter1[letter1.find(last[1])+1:]
        except FileNotFoundError: 
            print("", file=open("Logs\{0}.notes".format(task), "w"), end="")

        if work:
            for a in letter0:
                for b in letter1:
                    let = a+b
                    while True:
                        try: response = requests.get("https://notes.io/{0}".format(let), headers = headers).text
                        except requests.exceptions.ConnectionError:
                            while True:
                                t.sleep(30)
                                try:
                                    response = requests.get("https://notes.io/{0}".format(let), headers = headers).text
                                    break
                                except requests.exceptions.ConnectionError: print("Error")
                        if "<title>Notes" in response: break
                        else:
                            if let == "js": let = "jh"
                            else:
                                print("Title error: {0}".format(let))
                                t.sleep(15)
                    f, l = response.find("</script></center>"), response.rfind('''<ins class="adsbygoogle"''')
                    text = converter(response[f+9:l])[9:-9]
                    low = lower(text)
                    exist = False
                    for key in keys:
                        if key in low:
                            exist = True
                            break
                    counter+=1
                    if exist == True: 
                        print(let, file=open("Logs\hey", "a"), flush=True, end=",")
                        found+=1
                    print("{0} | {1}".format(counter, found))

                    print(let, file=open(r"Logs\{0}.notes".format(task), "w"), flush=True, end="")
        print("{0}".format(task), file=open(r"Logs\finish.notes", "a"), flush=True, end=",")

    checkList = {}
    if speed == 3:
        for i in range(0,57,3):
            word = letters[i:i+3]
            keyX = "2_{0}".format(i)
            checkList[keyX] = word
            threading.Thread(target=finder, args=(word, keyX, )).start()
    elif speed == 2:
        for i in range(0,57,19):
            word = letters[i:i+19]
            keyX = "2_{0}".format(i)
            checkList[keyX] = word
            threading.Thread(target=finder, args=(word, keyX, )).start()
    elif speed == 1:
        word = letters
        keyX = "2_1"
        checkList[keyX] = word
        threading.Thread(target=finder, args=(word, keyX, )).start()
    else:
        print("Yazılımsal hata!")
        sys.exit()


    while True:
        for cList in list(checkList):
            if cList in open(r"Logs\finish.notes", "r").read(): 
                del checkList[cList]
                os.remove("Logs\{0}.notes".format(cList))
        if len(checkList) == 0: break
        else: 
            temp = {}
            for cList in list(checkList): temp[cList] = open("Logs\{0}.notes".format(cList), "r").read()

            t.sleep(150) # 2.5m

            for cList in list(checkList):
                if temp[cList] == open("Logs\{0}.notes".format(cList), "r").read():
                    threading.Thread(target=finder, args=(checkList[cList], cList, )).start()

    return "ok"

def three():
    global counter
    global found

    def finder(string, task):
        global counter
        global found
        work = True

        letter0 = string
        letter1 = letters
        letter2 = letters

        try: 
            last = open("Logs\{0}.notes".format(task), "r").read()
            if last != "":
                if last == string[-1] + letters[-1] + letters[-1]: work = False
                else: # ?+?+?
                    if last[2] == letters[-1]: # ?+?+z
                        letter2 = letters
                        if last[1] == letters[-1]: # ?+z+z
                            letter0 = string[string.find(last[0])+1:]
                            letter1 = letters
                        else: # ?+(?: not z)+z
                            letter0 = string[string.find(last[0]):]
                            letter1 = letter1[letter1.find(last[1])+1:]

                    else: # ?+?+(?: not z)
                        letter0 = string[string.find(last[0]):]
                        letter1 = letter1[letter1.find(last[1]):]
                        letter2 = letter2[letter2.find(last[2])+1:]
        except FileNotFoundError: 
            print("", file=open("Logs\{0}.notes".format(task), "w"), end="")


        if work:
            for a in letter0:
                for b in letter1:
                    for c in letter2:
                        let = a+b+c
                        while True:
                            try: response = requests.get("https://notes.io/{0}".format(let), headers = headers).text
                            except requests.exceptions.ConnectionError:
                                while True:
                                    t.sleep(30)
                                    try:
                                        response = requests.get("https://notes.io/{0}".format(let), headers = headers).text
                                        break
                                    except requests.exceptions.ConnectionError: print("Error")
                            if "<title>Notes" in response: break
                            else:
                                if let == "inc": let = "iab"
                                else:
                                    print("Title error: {0}".format(let))
                                    t.sleep(15)
                        f, l = response.find("</script></center>"), response.rfind('''<ins class="adsbygoogle"''')
                        text = converter(response[f+9:l])[9:-9]
                        low = lower(text)
                        exist = False
                        for key in keys:
                            if key in low:
                                exist = True
                                break
                        counter+=1
                        if exist == True: 
                            print(let, file=open("Logs\hey", "a"), flush=True, end=",")
                            found+=1
                        print("{0} | {1}".format(counter, found))

                        print(let, file=open(r"Logs\{0}.notes".format(task), "w"), flush=True, end="")
        print("{0}".format(task), file=open(r"Logs\finish.notes", "a"), flush=True, end=",")
        

    checkList = {}
    if speed == 3:
        for i in range(0,57,3):
            word = letters[i:i+3]
            keyX = "3_{0}".format(i)
            checkList[keyX] = word
            threading.Thread(target=finder, args=(word, keyX, )).start()
    elif speed == 2:
        for i in range(0,57,11):
            word = letters[i:i+11]
            keyX = "3_{0}".format(i)
            checkList[keyX] = word
            threading.Thread(target=finder, args=(word, keyX, )).start()
    elif speed == 1:
        for i in range(0,57,19):
            word = letters[i:i+19]
            keyX = "3_{0}".format(i)
            checkList[keyX] = word
            threading.Thread(target=finder, args=(word, keyX, )).start()
    else:
        print("Yazılımsal hata!")
        sys.exit()

    while True:
        for cList in list(checkList):
            if cList in open(r"Logs\finish.notes", "r").read(): 
                del checkList[cList]
                os.remove("Logs\{0}.notes".format(cList))
        if len(checkList) == 0: break
        else: 
            temp = {}
            for cList in list(checkList): temp[cList] = open("Logs\{0}.notes".format(cList), "r").read()

            t.sleep(210) # 3.5m

            for cList in list(checkList):
                if temp[cList] == open("Logs\{0}.notes".format(cList), "r").read():
                    threading.Thread(target=finder, args=(checkList[cList], cList, )).start()

    return "ok"
    

def four():
    global counter
    global found

    def finder(string, task):
        global counter
        global found
        work = True

        letter0 = string
        letter1 = letters
        letter2 = letters
        letter3 = letters

        try: 
            last = open("Logs\{0}.notes".format(task), "r").read()
            if last != "":
                if last == string[-1] + letters[-1] + letters[-1] + letters[-1]: work = False
                else: # ?+?+?+?
                    if last[3] == letters[-1]: # ?+?+?+z
                        letter3 = letters
                        if last[2] == letters[-1]: # ?+?+z+z
                            letter2 = letters
                            if last[1] == letters[-1]: # ?+z+z+z
                                letter1 = letters
                                letter0 = string[string.find(last[0])+1:]
                            else: # ?+?+z+z
                                letter0 = string[string.find(last[0]):]
                                letter1 = letter1[letter1.find(last[1])+1:]
                        else: # ?+?+?+z
                            letter0 = string[string.find(last[0]):]
                            letter1 = letter1[letter1.find(last[1]):]
                            letter2 = letter2 = letter2[letter2.find(last[2])+1:]
                    else:
                        letter0 = string[string.find(last[0]):]
                        letter1 = letter1[letter1.find(last[1]):]
                        letter2 = letter2[letter2.find(last[2]):]
                        letter3 = letter3[letter3.find(last[3])+1:]
        except FileNotFoundError: 
            print("", file=open("Logs\{0}.notes".format(task), "w"), end="")


        if work:
            for a in letter0:
                for b in letter1:
                    for c in letter2:
                        for d in letter3:
                            let = a+b+c+d
                            while True:
                                try: response = requests.get("https://notes.io/{0}".format(let), headers = headers).text
                                except requests.exceptions.ConnectionError:
                                    while True:
                                        t.sleep(30)
                                        try:
                                            response = requests.get("https://notes.io/{0}".format(let), headers = headers).text
                                            break
                                        except requests.exceptions.ConnectionError: print("Error")
                                if "<title>Notes" in response: break
                                else:
                                    print("Title error: {0}".format(let))
                                    t.sleep(15)
                            f, l = response.find("</script></center>"), response.rfind('''<ins class="adsbygoogle"''')
                            text = converter(response[f+9:l])[9:-9]
                            low = lower(text)
                            exist = False
                            for key in keys:
                                if key in low:
                                    exist = True
                                    break
                            counter+=1
                            if exist == True: 
                                print(let, file=open("Logs\hey", "a"), flush=True, end=",")
                                found+=1
                            print("{0} | {1}".format(counter, found))

                            print(let, file=open(r"Logs\{0}.notes".format(task), "w"), flush=True, end="")
        print("{0}".format(task), file=open(r"Logs\finish.notes", "a"), flush=True, end=",")


    checkList = {}
    if speed == 3:
        for i in range(0,57,2):
            word = letters[i:i+2]
            keyX = "4_{0}".format(i)
            checkList[keyX] = word
            threading.Thread(target=finder, args=(word, keyX, )).start()
    elif speed == 2:
        for i in range(0,57,3):
            word = letters[i:i+3]
            keyX = "4_{0}".format(i)
            checkList[keyX] = word
            threading.Thread(target=finder, args=(word, keyX, )).start()
    elif speed == 1:
        for i in range(0,57,11):
            word = letters[i:i+11]
            keyX = "4_{0}".format(i)
            checkList[keyX] = word
            threading.Thread(target=finder, args=(word, keyX, )).start()
    else:
        print("Yazılımsal hata!")
        sys.exit()


    while True:
        for cList in list(checkList):
            if cList in open(r"Logs\finish.notes", "r").read(): 
                del checkList[cList]
                os.remove("Logs\{0}.notes".format(cList))
        if len(checkList) == 0: break
        else: 
            temp = {}
            for cList in list(checkList): temp[cList] = open("Logs\{0}.notes".format(cList), "r").read()

            t.sleep(7*60) # 6m

            for cList in list(checkList):
                if temp[cList] == open("Logs\{0}.notes".format(cList), "r").read():
                    threading.Thread(target=finder, args=(checkList[cList], cList, )).start()

    return "ok"