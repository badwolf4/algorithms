import csv
import math
import random

train_data = []

test_data = []

with open('data_train.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        train_data.append([float(row[0]),float(row[1]),float(row[2]),float(row[3]),int(row[4])])

with open('data_test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        test_data.append([float(row[0]),float(row[1]),float(row[2]),float(row[3]),int(row[4])])


choice = 1
while (choice!=2) and (choice!=3): 
    choice = int(input("Enter how many columns to compare( 2 or 3): "))

print(choice)

columns = []
for i in range(0,choice):
    a = int(input("Enter number of column(1-4): "))
    while a<1 or a>4:
        a = int(input("Enter number of column(1-4): "))
    a-=1
    columns.append(a)

print(columns)

neighbors = int(input("Enter how many neighbours: "))

while neighbors<=0 or neighbors>len(train_data):
    neighbours = int(input("Enter how many neighbours: "))

#print("Dlugosc train_data: ", len(train_data))
#print("Dlugosc test_data: ", len(test_data))

###################################################################################################################################
mistake = 0
# obliczamy odleglosc do wszystkich sasiadow dla pojedynczej probki testu
for k in range(0,len(test_data)):
    #print("Iteration: ",k)
    distance = []
    for i in range(0,len(train_data)):
        if choice == 2:
            d = math.sqrt( (test_data[k][columns[0]]-train_data[i][columns[0]])**2 + (test_data[k][columns[1]]-train_data[i][columns[1]])**2)
            distance.append([d,train_data[i][4]])
        if choice == 3:
            d = math.sqrt( (test_data[k][columns[0]]-train_data[i][columns[0]])**2 + (test_data[k][columns[1]]-train_data[i][columns[1]])**2 +(test_data[k][columns[2]]-train_data[i][columns[2]])**2)
            distance.append([d,train_data[i][4]])

    #print(distance)

    #print("Koniec")

#sortujemy wedlug odleglosci
    distance.sort()

    #print(distance)

    neighbor_list = []

# wybieramy ile nam potrzeba sasiadow
    for i in range(0,neighbors):
        neighbor_list.append(distance[i])

    count0 = 0
    count1 = 0
    count2 = 0

    for i in range(0,len(neighbor_list)):
        if neighbor_list[i][1]==0:
            count0+=1
        if neighbor_list[i][1]==1:
            count1+=1
        if neighbor_list[i][1]==2:
            count2+=1

    result = -1

    if count0 > count1 and count0 > count2:
        result = 0
    elif count1 > count0 and count1 > count2:
        result = 1
    elif count2 > count1 and count2 > count0:
        result = 2
    else:
        d0=0
        d1=0
        d2=0
        for i in range(0,len(neighbor_list)):
            if neighbor_list[i][1]==0:
                d+=neighbor_list[i][0]
            if neighbor_list[i][1]==1:
                d+=neighbor_list[i][0]
            if neighbor_list[i][1]==2:
                d+=neighbor_list[i][0]
        if d0>d1 and d0>d2:
            result=0
        elif d1>d2 and d1>d0:
            result=1
        elif d2>d1 and d2>d0:
            result=2
        else:
            if d0 == d1:
                result = random.randint(0,1)
            if d1==d2:
                result = random.randint(1,2)
            if d0 == d2:
                result = random.randrange(0,2,2)



    #print (neighbor_list)

    #print("Result: ", result)

    distance[:]=[]
    neighbor_list[:]=[]

    if result!=test_data[k][4]:
        mistake+=1
    #print("End of iteration: ", k)

print("Mistakes: ", mistake)








