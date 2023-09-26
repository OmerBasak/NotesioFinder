import finder, os

os.mkdir("Logs")

def lower(string):
    string = r"{0}".format(string) 
    low = ""
    low = string.replace("I", "ı")
    low = low.replace("İ", "i")
    low = low.lower()
    return low

addKeys = []
while True:
    while True:
        try:
            key = lower(input("Aranacak kelime (e: Ok): "))
            if key == "": break
            elif key == "e": break
            elif key == "ok": break
            elif len(key) < 4:
                print("Aranacak kelime en az 4 karakter olmalıdır!")
            else: addKeys.append(key)
        except KeyboardInterrupt: break
    speed = 3

    if len(addKeys) == 0: print("Lütfen aranacak kelimeleri giriniz!")
    else: break

for key in addKeys:
    finder.keys.append(key) 

os.system("cls") # Linux sistemlerde clear denmesi gerekiyor. Os tespiti yapılabilir.

textKeys = ""
for key in addKeys: textKeys+=key+", "
textKeys = textKeys[:-2]

print("Aranacak kelimeler: {0}\n".format(textKeys))

while True:
    thread = input("Hız belirtiniz (1, 2, 3): ").replace(" ", "")
    if thread.isdigit():
        thread = int(thread)
        if thread == 3: break
        elif thread == 2: 
            speed = 2
            break
        elif thread == 1:
            speed = 1
            break
        else: 
            print("Lütfen 1, 2 veya 3 sayılarından birini giriniz.")
    else: print("1, 2 veya 3 cinsinden sayı belirtiniz.")


finder.speed = speed

fromFinder = finder.one()
if fromFinder == "ok":
    print("+ Tek basamaklı tarama tamamlandı !")
    fromFinder = finder.two()
    if fromFinder == "ok":
        print("+ İki basamaklı tarama tamamlandı")
        fromFinder = finder.three()
        if fromFinder == "ok":
            print("+ Üç basamaklı tarama tamamlandı")
            fromFinder = finder.four()
            if fromFinder == "ok":
                print("+ Dört basamaklı tarama tamamlandı")