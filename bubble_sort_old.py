#Программа для прохожения игры Bubble Sort на Android

import copy
import random

def Settings(settings): #устанавливаем настройки ввода
    while True:
        print("""Вариант по умолчанию - 1
Выводит только порядок ходов.

Вариант 2:
Выводит ход, затем список пробирок после этого хода, затем снова ход и т.д.

Вариант 3:
Выводит список ходов, затем - как меняются пробирки в ходе решения.

Вариант 4:
Выводит только изменения пробирок без списка ходов.

Чтобы выбрать какой-либо вариант, введит его номер и нажмите Enter. Нажмите
Enter, чтобы оставить текущий вариант.""")
        print("Текущий вариант: "+str(settings))
        print()
        sett = int(input("Выберите вариант "))
        if sett in range (1, 5):
            print()
            return sett
        else:
            print()
            return settings

def MakeMove(ProbProb, hodi, LastMove, BannedMoves): #пробуем сделать ход
    popitki = 0 #определяем переменную для подсчёта попыток сделать ход, чтобы не уйти в бесконечный цикл
    BannedMoves = BannedMoves
    hodi = hodi
    if hodi>0: #если уже делали ход, то нельзя перемещать шарик из пробирки, куда его положили в прошлый ход
        Banned = [LastMove[1]]
    else:
        Banned = []
    for p in range (0, len(ProbProb)): #указываем, что пустые провирки не подлежат проверке
        if len (ProbProb[p]) == 0:
            Banned += [p]  
    NerasProb = NotSorted(ProbProb) #получаем список номеров не рассортированных пробирок        
    MaxTries = len(NerasProb) #получаем максимальное количество попыток сделать ход
    while popitki<=MaxTries: #Нам надо перебрать все нерассортированные пробирки, но не более того
        move = [] #определяем перемунную, в которую будем записывать движение.
        otkuda = Otkuda(NerasProb, ProbProb, hodi, Banned) #выбираем пробирку, из которой делаем ход
        if otkuda == "НетХода": #если такая пробирка не нашлась, перезапускаем сортировку
            return "restart"
        Banned += [otkuda] #добавляем выьранную побирку в список запрещённых, чтобы не проверять её ещё раз
        kuda = Kuda(otkuda, ProbProb, BannedMoves) #ищем, можем ли мы куда-то положить шарик из выбранной пробирки
        popitki +=1 #добавляем попытки к счётчику, чтобы, если ход невозможен, начать сортировку заново
        if kuda == "NoMove": #если шарик положить некуда, выбираем другую пробирку
            continue
        else:
            move += [otkuda] #Если всё хорошо, записываем, откуда перекладываем шарик.
            move += [kuda] #и куда перекладываем
            return move
    if popitki == MaxTries: #если превышен лимит попыток сделать ход, мы зашли в тупик
        return "restart" #начинаем сортировку заново


def NotSorted(ProbProb): #получаем список номеров не рассортированных пробирок
    NerasProb = [] #создаём список для номеров
    for i in range(0, len(ProbProb)): #считаем именно номера, не сами пробирки!
        if len(ProbProb[i]) == 0: #если пробирка пустая, её не считаем.
            continue
        elif len(ProbProb[i]) == 4 and SameColor(ProbProb[i]) == 1:
            continue #если в пробирке 4 шарика одного цвета, их тоже не считаем
        else:
            NerasProb += [i] #всё остальное считаем
    del i
    if len (NerasProb) == 0: #если в списке отсортированных ничего нет - отсортировано всё.
        return "Отсортировано!"
    else:
        return NerasProb

def Otkuda(NerasProb, ProbProb, hodi, Banned): #выбираем конкретную пробирку из списка нерасоортированных
    if len(Banned)>0: #проверяем наличие пробирок в списке запрещённых
        for b in Banned: #удаляем те варианты, откуда нельзя переложить шарик
            if b in NerasProb:
                NerasProb.remove(b)
    for p in NerasProb:
        if len(ProbProb[p]) == 3 and SameColor(ProbProb[p]) == 1:
            NerasProb.remove(p) #если есть пробирка, в которой 3 шарика одного цвета, её не трогать, так как это бессмысленно
    if len(NerasProb) == 0: #если в итоге у нас нет пробирок, из которых можно сделать ход
        return "НетХода" #возвращаем, что хода нет
    if hodi >2: #Если уже перекладывали шарики минимум 2 раза, ищем, нельзя ли закончить какую-нибудь пробирку
        for i in NerasProb:
            if len (ProbProb[i]) == 1 and len(Same(i, ProbProb))>0: #Если у нас один шарик в пробирке, ищем, не можем ли мы положить его к другим, все из которых того же цвета
                return i     
            if len (ProbProb[i]) == 2 and ProbProb[i][0]==ProbProb[i][1] and len(Same(i, ProbProb))>0: #проверяем то же самое для 2 шариков
                return i
    for p in NerasProb:
        if len(ProbProb[p]) == 4 and ProbProb[p][0] == ProbProb[p][1] and ProbProb[p][1] == ProbProb[p][2]:
            for b in range (0, len(ProbProb)):
                if len(ProbProb[b]) == 1 and ProbProb[b][0] == ProbProb[p][0]:
                    return p #если у нас есть пробирка из 4 шариков, 3 из которых одного цвета, и одиночкий шарик того це цвета, перекладываем из пробирки с 4
        elif len(ProbProb[p])>2 and ProbProb[p][0] == ProbProb[p][1]:
            for b in range(0, len(ProbProb)):
                if len(ProbProb[b]) == 2 and ProbProb[b][0] == ProbProb[b][1] and ProbProb[b][0] == ProbProb[p][0]:
                    return p #если есть два одинаковых шарика в пробирке, где их 3 или 4, и два в полупостой, перекладываем в полупустую
    i = int(random.choice(NerasProb)) #если никаких "логичных" вариантов нет, берём случайную нерасфасованную пробирку
    return i

def Kuda(otkuda, ProbProb, BannedMoves): #Ищем, куда можно положить шарик
    proverka = [] #создаём список проверки. Именно список, т.к. потом проверяем, есть там какие-то варианты или нет
    if len(BannedMoves)>0: #если есть запрещённые движения, проверяем, можно ли сделать такое из выьранной ранее пробирки
        for b in range(0, len(BannedMoves)):
            if BannedMoves[b][0] == otkuda:
                proverka += [otkuda] #если да, записываем номер побирки, откуда пытаемся сделать ход, в проверку
            else:
                continue
    if len(ProbProb[otkuda]) == 1: #если перекладываем из пробирки, где 1 шарик
        if len(Same(otkuda, ProbProb))>0: #ищем, не можем ли мы закончить
            kuda = int(Same(otkuda, ProbProb)[0]) #какую-либо пробирку
            return kuda
    kuda = [] #если не можем, создаём список возможных ходов
    for p in range (0, len(ProbProb)):
        if p == otkuda: #запрещаем делать ход в ту же пробирку, откуда берём шарик
            continue
        if len (ProbProb[p]) == 0: #не перекладываем шарики в пустую пробирку
            if SameColor(ProbProb[otkuda]) == 1: #если в текущей пробирке
                continue #они все и так уже одного цвета
            else:
                kuda +=[p] #если нет, то добавляем пустые пробирки в список
        elif len(ProbProb[p])<4: #проверяем, чтобы в целевой пробирке было меньше 4 шариков
            if ProbProb[p][0] == ProbProb[otkuda][0]: #проверяем совпадение цветов верхних шариков
                if SameColor(ProbProb[p]) == 1: #если в целевой пробирке все шарики того же цвета
                    return p #кладём в неё без вариантов
                else:
                    kuda += [p] #если нет, добавляем её к списку возможных целевых
    if len(proverka)>0: #проверяем, нужна ли проверка на попытку сделать запретный ход
        for k in kuda:
            proverka1 = [] #моделируем предполагаемые ходы
            proverka1 += [otkuda]
            proverka1 += [k]
            if proverka1 in BannedMoves: #если предполагаемый ход запрещён
                kuda.remove(k) #удаляем его
            else:
                continue
    if len (kuda) == 0: #если после этого у нас нет вариантов, куда положить шарик
        return "NoMove" #возвращаем это и ищем другую исходную пробирку
    else:
        i = int(random.choice(kuda)) #если варианты есть, выбираем случайный
        return i
    
        

def Same(i, ProbProb): #Ищем, есть ли пробирка, в которой все щарики того же цвета, что в данной(i).
    tsvet = ProbProb[i][0] #определяем, какой верхний цвет в исходной пробирке
    kuda = [] #здесь список, т.к. вышестоящие функции работают с наличие значения
    for p in range (0, len(ProbProb)):
        if p!=i and len(ProbProb[p])>0 and len(ProbProb[p]) == (4-len(ProbProb[i])) and SameColor(ProbProb[p]) == 1 and ProbProb[p][0] == tsvet:
            kuda = [p] #номер искомой пробирки не совпадает с номером данной. В них суммарно не более 4 шариков. В целевой все шарики одного цвета, и они совпадают с данной
    return kuda
        

def SameColor(Prob): #проверка, что все шарики в пробирке одного цвета
    SameC = 0
    for p in range (0, len(Prob)):
        if Prob[p] == Prob[int(p+1)%len(Prob)]:
            SameC +=1 #Если цвет шарика совпадает со следующим, прибавляем 1
    if SameC == len(Prob): #Если количество шариков с совпадающим цветом
        return 1 #равно длине пробирки, значит, они все одного цвета.
    else:
        return 0
        
def Banned(move, BannedMoves): #составляет/обновляет список "запрещённых" ходов
    PrevMove = [] #создаём переменную, создержающую "перевёрнутый" последний ход
    PrevMove += [int(move[1])] #чтобы программа не перекладывала шарики между 2 пробирками
    PrevMove += [int(move[0])] #пока в них что-то не изменится
    if len(BannedMoves) >0: #если у нас есть какие-то запрещённые ходы
        for b in (BannedMoves): #проверяем, не перестали ли они такими быть
            if int(move[0]) in b: #удаляем из списка все ходы, содержащие номер
                BannedMoves.remove(b) #пробирки, из которой мы сделали ход
        for b in (BannedMoves): #теперь удаляем, опираясь на то, куда сделали ход
            if int(move[1]) in b:
                BannedMoves.remove(b)
        BannedMoves += [PrevMove] #записываем в список отзеркаленный посдений ход
    else:
        BannedMoves = [PrevMove] #если у нас нет запрещённых ходов, просто добавляем последнее
    return BannedMoves
        
    

def Sortirovka(probirki, settings): #сортируем шарики
    ProbProb = copy.deepcopy(probirki) #Делаем черновую копию пробирок
    hodi = 0 #создаём счётчик ходов
    Logi = "" #создаём список ходов в формате строки
    while True:
        if hodi == 0: #если ещё не ходили
            LastMove = [] #последнего хода нет
            BannedMoves = [] #запрещённых ходов нет
        else:
            LastMove = move #если уже ходили, то записываем ход в последний
        move = MakeMove(ProbProb, hodi, LastMove, BannedMoves) #получаем ход
        hodi +=1 #увеличиваем счётчик ходов
        if move == "restart": #если ход вернул перезапуск, начинаем сортировку заново
            return "restart"
        else:
            tsvet = ProbProb[int(move[0])][0] #определяем цвет шарика, который перемещаем
            ProbProb[int(move[1])].insert(0, tsvet) #вставляем его в целевую пробирку
            ProbProb[int(move[0])].remove(tsvet) #удаляем из исходной
            BannedMoves = Banned(move, BannedMoves) #обновляем список запрещённых ходов
            if settings == 1:
                Logi += str(hodi)+". "+str(tsvet)+" из пробирки " +str(int(move[0])+1)+" в пробирку "+str(int(move[1])+1)+"\n" #добавляем ход в список ходов
            elif settings == 2:
                Logi += str(hodi)+". "+str(tsvet)+" из пробирки " +str(int(move[0])+1)+" в пробирку "+str(int(move[1])+1)+"\n"
                for p in range(0, len(ProbProb)):
                    Logi += "Пробирка номер "+str(p+1)+":"+"\n"
                    if len(ProbProb[p])>0:
                        for s in range(0, len(ProbProb[p])):
                            Logi += str(ProbProb[p][s])+" "
                    else:
                        Logi +="Пустая"
                    Logi +="\n"
                Logi += "\n"
            elif settings == 3:
                Logi += str(hodi)+". "+str(tsvet)+" из пробирки " +str(int(move[0])+1)+" в пробирку "+str(int(move[1])+1)+"\n"
                if hodi ==1:
                    Probirochki = ""
                for p in range(0, len(ProbProb)):
                    Probirochki += "Пробирка номер "+str(p+1)+":"+"\n"
                    if len(ProbProb[p])>0:
                        for s in range(0, len(ProbProb[p])):
                            Probirochki += str(ProbProb[p][s])+" "
                    else:
                        Probirochki +="Пустая"
                    Probirochki +="\n"
                Probirochki +="\n"
            else:
                for p in range(0, len(ProbProb)):
                    Logi += "Пробирка номер "+str(p+1)+":"+"\n"
                    if len (ProbProb[p])>0:
                        for s in range(0, len(ProbProb[p])):
                            Logi += str(ProbProb[p][s])+" "
                    else:
                        Logi +="Пустая"
                    Logi +="\n"
                Logi += "\n"
                del p
                del s
                Logi += "\n"
            if (NotSorted(ProbProb)) == "Отсортировано!": #проверяем, не завершена ли сортировка
                if settings == 3:
                    Logi += "\n"
                    Logi += Probirochki
                return Logi #если да, возвращаем список ходов
        
    
        

def Vvod(polnie, pustie, numbers): #создаём пробирки без шариков
    probirki = []
    for i in range (1, polnie+pustie+1):
        probirki += [[0]]
    for i in range(0, len(probirki)):
        if i in numbers:
            probirki[i] = []
    return probirki

def Pravka(probirki): #позволяет исправить ошибку ввода
    while True:
        print()
        prob = 0
        while prob == 0:
            try:
                print("Введите номер пробирки, где нужно сделать правку.")
                prob = int(input())
            except:
                print("Ошибка ввода. Повторите ввод.")
                print()
                continue
            if prob >len(probirki):
                print("Вы ввели сликшом большое число. Такой пробирки нет.")
                print()
                prob = 0
                continue
        prob -=1    
        sharik = 0
        while sharik == 0:
            try:
                print()
                print("Введите номер шарика, который нужно заменить.")
                sharik = int(input())
            except:
                print("Ошибка ввода. Повторите ввод.")
                print()
                continue
            if sharik >4:
                print("Вы ввели сликшом большое число. В пробирке не может быть больше 4 шариков.")
                print()
                prob = 0
                continue
        sharik -=1
        print()
        print("Какой цвет у нового щарика?")
        tsvet = str(input())
        probirki[prob][sharik] = tsvet
        print()
        print("Теперь пробирки сожерат шарики следующих цветов:")
        for i in range (0, len(probirki)):
            print("Пробирка номер "+str(i+1)+":")
            if len(probirki[i])>0:
                print(*probirki[i])  
            else:
                print("Пустая")
        tsveta = Tsveta(probirki)
        proverka = Check(tsveta)
        if str(proverka) == "ошибка":
            print("Требуются ещё правки")
            print()
            print("""Нажмите Enter, чтобы продолжить правки. Введите "Выход"
и нажмите Enter, чтобы начать ввод заново.""")
            ask = input()
            if ask.lower().startswith("в"):
                return "Повтор"
            else:
                continue
        print("Чтобы закончить правку, нажмите Enter.")
        print("Чтобы исправить ещё один шарик, введите Повтор и нажмите Enter.")
        check = input()
        if check.lower().startswith("п"):
            continue
        else:
            return probirki
            
def Tsveta(probirki): #считаем количество шариков разного цвета
    tsveta = {}
    for s in range(0, len(probirki)):
        if len(probirki[s]) ==0:
            continue
        for i in range (0, 4):
            tsvet = probirki[s][i]
            if tsvet in tsveta:
                num = int(tsveta[tsvet])+1
                tsveta[tsvet] = num
            else:
                tsveta[tsvet] = 1
    return tsveta
            

def Shariki(probirki): #заполняем пробирки шариками
    while True:
        for i in range (0, len(probirki)):
            if len(probirki[i])>0:
                tsvet = []
                print("Пробирка "+str(i+1))
                print("Введите цвета от верхнего к нижнему.")
                for s in range (1,5):
                    tsvet1 = input("Цвет "+str(s)+" шарика: ")
                    tsvet += [tsvet1]
                probirki[i] = tsvet
                del(s)
                print()
            else:
                continue
        pravki = 0
        while True:
            tsveta = Tsveta(probirki) #проверяем корректность заполнения
            proverka = Check(tsveta)
            if proverka == "ошибка":
                print("""Чтобы начать ввод заново, нажмите Enter.
Чтобы исправить конкретную ошибку, введите "Исправить" и нажмите Enter.""")
                ask = input()
                if ask.lower().startswith("и"):
                    probirki = Pravka(probirki)
                    pravki +=1    
                else:
                    break
            elif pravki >0: #если уже правили пробирки, нам не нужно выводить сообщение о том, какие там шарики
                return probirki
            else:
                print("Пробирки содержат шарики следующих цветов:")
                for i in range (0, len(probirki)):
                    print("Пробирка номер "+str(i+1)+":")
                    if len(probirki[i])>0:
                        print(*probirki[i])
                    else:
                        print("Пустая")
                print()
                print("""Если всё правильно, нажмите Enter. Для повторного заполнения
введите "Повтор" и нажмите Enter. Для, того, чтобы исправить конкретное место,
введите "Исправить" и нажмите Enter.""")
                check = str(input())
                if check.lower().startswith("п"):
                    return "Повтор"
                elif check.lower().startswith("и"):
                    probirki = Pravka(probirki)
                    return probirki
                else:
                    return probirki
                

def Check(tsveta): #проверяем корректность заполнения пробирок
    for t in tsveta:
        if tsveta[t] >4: #если больше 4 шариков какого-либо цвета, повторяем ввод
            print("Указано больше 4 шариков одного цвета.")
            print("Слишком много шариков цвета "+str(t))
            return "ошибка"
        elif tsveta[t] < 4:
            print("Указано меньше 4 шариков одного цвета.")
            print("Слишком мало шариков цвета "+str(t))
            return "ошибка"
    return "ОК"


    
        
settings = 1
while True:
    print("""Введите 0 и нажмите Enter, чтобы перейти в меню вывода результата.
Нажмите Enter, чтобы перейти к вводу исходных данных.""")
    sett = str(input())
    if sett == "0":
        try:
            settings = Settings(settings)
            settings = int(settings)
        except:
            settings = 1
    while True:
        try:
            polnie = int(input("Введите количество полных пробирок: "))
            break
        except:
            print()
            print("Ошибка ввода. Пожалуйста, введите целое число.")
            print()
            continue
    while True:
        try:
            pustie = int(input("Введите количество пустых пробирок: "))
            print()
            break
        except:
            print()
            print("Ошибка ввода. Пожалуйста, введите целое число.")
            print()
            continue
    print("""Если расположение пустых пробирок стандартное (в конце), нажмите
Enter. Если нет, введите "Номера" и нажмите Enter. Если есть ошибка, введите
слово "Повтор" и нажмите Enter""")
    check = input()
    numbers = []
    if check.lower().startswith("п"):
        continue
    if check.lower().startswith("н"):
        for i in range (0, pustie):
            while True:
                try:
                    number = int(input("Введите номер "+str(i+1)+" пустой пробирки: "))
                    numbers += [number-1]
                    print()
                    break
                except:
                    print()
                    print("Ошибка ввода. Пожалуйста, введите целое число.")
    else:
        for i in range (polnie, int(polnie+pustie)):
            numbers += [i]
    probirki = Vvod(polnie, pustie, numbers)
    if probirki == "Повтор":
        print()
        continue
    probirki = Shariki(probirki)
    print()
    s = 0
    popitki = 0
    while s == 0:
        logi = Sortirovka(probirki, settings)
        if logi == "restart":
            popitki += 1
            print("Нет хода. Попытка %s закончена" %(popitki))
            continue
        else:
            popitki +=1
            if popitki >1:
                print() #Делаем отступ от счётчика попыток, если решилось не с 1
            print(logi)
            print()
            print("Завершено с %s попытки" %(popitki))
            print()
            s = 1
    print("""Запустить новую сортировку? Введите "Да" и нажмите Enter для
запуска, или нажмите Enter, чтобы завершить работу программы.""")
    check = input()
    if str(check).lower().startswith("д"):
        print()
        continue
    else:
        break
    
    
