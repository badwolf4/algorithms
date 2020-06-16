import random as r
import csv
import math
import copy

#TODO  poprawic obliczenie bledu kwantyzacji, przejrzec zmienne globalne


dane = []
centra = []
najlepszeGrupowanie = []
najlepszeCentra = []



def readData():
    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            dane.append([float(row[0]), float(row[1]), -1])


def forgy(iloscCentra):
    crand = []
    while len(centra)!=iloscCentra:
        c = r.randrange(0,len(dane),1)
        if c not in crand:
            crand.append(c)
            centra.append([dane[c][0], dane[c][1]])


def randomPartition(iloscCentra):
    for i in range(0,len(dane)):
        c = r.randrange(0,iloscCentra,1)
        dane[i][2] = c


def uniform(iloscCentra):
    xmin = dane[0][0]
    xmax = dane[0][0]
    ymin = dane[0][1]
    ymax = dane[0][1]

    for i in range(0,len(dane)):
        if dane[i][0] < xmin:
            xmin = dane[i][0]
    for i in range(0,len(dane)):
        if dane[i][0] > xmax:
            xmax = dane[i][0]
    for i in range(0,len(dane)):
        if dane[i][1] < ymin:
            ymin = dane[i][1]
    for i in range(0,len(dane)):
        if dane[i][1] > ymax:
            ymax = dane[i][1]
    while len(centra)!=iloscCentra:
        centra.append([r.uniform(xmin,xmax), r.uniform(ymin,ymax)])


def algorytmKSrednich():
    it = 0
    count = 0
    while count!=len(dane):
        count = 0
        #przydzielanie prob do najblizszych centra
        for i in range(0,len(dane)):
            d = []
            for j in range(0,len(centra)):
                d.append( math.sqrt((dane[i][0] - centra[j][0])**2 + (dane[i][1] - centra[j][1])**2 ) )
            for j in range(0,len(d)):
                if min(d) == d[j]:
                    if dane[i][2]==j:
                        count+=1
                    dane[i][2]=j
                    break
        #obliczanie nowych centra
        for i in range(0,len(centra)):
            ile = 0
            sumx = 0.0
            sumy = 0.0
            for j in range(0,len(dane)):
                if(dane[j][2]==i):
                    sumx += dane[j][0]
                    sumy += dane[j][1]
                    ile += 1
            if ile == 0:
                continue
            centra[i][0] = sumx/ile
            centra[i][1] = sumy/ile
        it += 1
    return it

def obliczCentra(ile):
    for i in range(0,ile):
            ile = 0
            sumx = 0.0
            sumy = 0.0
            for j in range(0,len(dane)):
                if(dane[j][2]==i):
                    sumx += dane[j][0]
                    sumy += dane[j][1]
                    ile += 1
            if ile == 0:
                continue
            centra.append([sumx/ile, sumy/ile])


def bladKwantyzacji():
    blad = 0.0
    if(len(dane)==0):
        return blad
    for i in range(0, len(dane)):
        blad += (dane[i][0] - centra[ dane[i][2] ][0])**2 + (dane[i][1] - centra[ dane[i][2] ][1])**2 
    blad /= len(dane)
    return blad


def wyczyscWynikiZDanych():
    for i in range(0,len(dane)):
        dane[i][2] = -1
    

def srednieZnaczenie(tablica):
    s = 0.0
    if len(tablica) == 0:
        return s
    for i in tablica:
        s += i
    s /= len(tablica)
    return s


def odchylenieStandardowe(tablica):
    s = srednieZnaczenie(tablica)
    odchylenie = 0.0
    if len(tablica)==0:
        return odchylenie
    for i in tablica:
        odchylenie += (i - s)**2
    odchylenie /= len(tablica)
    return math.sqrt(odchylenie)


def kopiujDoNajlepszego(tablica):
    for i in range(0, len(tablica)):
        najlepszeGrupowanie.append([tablica[i][0], tablica[i][1], tablica[i][2]])


def kopiujDoNajlepszegoCentra(tablica):
    for i in range(0, len(tablica)):
        najlepszeCentra.append([tablica[i][0], tablica[i][1]])


readData()
wybor = int(input("Wprowadz numer metody(1-3): "))
ilosc = int(input("Wprowadz ilosc grup: "))
powtorz = 12
wszystkieBledy = []
wszystkieIteracje = []
w = 0

while powtorz!=0:
    if wybor == 1:
        forgy(ilosc)
    if wybor == 2:
        randomPartition(ilosc)
        obliczCentra(ilosc)
    if wybor == 3:
        uniform(ilosc)
    w+=1
    wszystkieIteracje.append(algorytmKSrednich())
    b = bladKwantyzacji()
    wszystkieBledy.append(b)
    if b == min(wszystkieBledy):
        najlepszeGrupowanie.clear()
        kopiujDoNajlepszego(dane)
        najlepszeCentra.clear()
        kopiujDoNajlepszegoCentra(centra)
    centra.clear()
    wyczyscWynikiZDanych()
    powtorz -= 1
    
fileName = 'raport'
if wybor == 1:
    fileName+='_forgy_'
if wybor == 2:
    fileName+='_random_partition_'
if wybor == 3:
    fileName+='_uniform_'
fileName+=str(ilosc)
fileName+='.csv'
print(fileName)
with open(fileName, mode='w', newline='') as raport_file:
    raport_writer = csv.writer(raport_file, delimiter=',')

    raport_writer.writerow([srednieZnaczenie(wszystkieBledy), odchylenieStandardowe(wszystkieBledy)])
    raport_writer.writerow([srednieZnaczenie(wszystkieIteracje), odchylenieStandardowe(wszystkieIteracje)])
    for i in range (0, len(najlepszeCentra)):
        raport_writer.writerow([najlepszeCentra[i][0], najlepszeCentra[i][1]])
    for i in range (0, len(najlepszeGrupowanie)):
        raport_writer.writerow([najlepszeGrupowanie[i][0], najlepszeGrupowanie[i][1], najlepszeGrupowanie[i][2]])
    


