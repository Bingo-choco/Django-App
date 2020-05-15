from json import load

import numpy as np
import random

from django.contrib import staticfiles


def read_data():
    N=19
    Mat=[[0,21.6,6.1,23.7,9.9,13.1,0.9,8.7,8.2,4.1,16.7,12,2.8,9,6.6,9.4,23.3,1.1,3.5], [21.6,0,13.3,9.4,14.2,8.6,21.1,12.7,15.6,16.9,24,10.6,16.8,13.8,13.6,12,8.9,21,17.7], [6.1,13.3,0,10.9,3.1,8.6,6.6,4.4,7.5,3.6,15.9,7.4,3.4,6,0.9,4.8,12.1,6.7,5.8], [23.7,9.4,10.9,0,12.7,3.3,21.9,10.6,13.6,13.5,17.3,4.8,13.3,10.2,13.3,9.8,2.1,21.8,17.2], [9.9,14.2,3.1,12.7,0,9.9,9.2,6,9,6.5,17.5,10.1,6.4,7.4,2.7,6.4,12.4,9.1,8.7], [13.1,8.6,8.6,3.3,9.9,0,13.2,5.5,9.4,10.2,15.6,1.6,10.1,5.5,7.3,4.9,4.3,15.9,10.6], [0.9,21.1,6.6,21.9,9.2,13.2,0,8.4,8.6,4.5,17,15.1,3.2,9.4,7,9.7,18.7,1,4], [8.7,12.7,4.4,10.6,6,5.5,8.4,0,3.6,6.6,12.9,4,6.3,1.9,4,0.9,11.2,8.8,5.9], [8.2,15.6,7.5,13.6,9,9.4,8.6,3.6,0,7,10.5,7.5,6.9,4.4,7.4,4.5,14,9.3,6.4], [4.1,16.9,3.6,13.5,6.5,10.2,4.5,6.6,7,0,14.2,9.7,0.5,6.5,4.4,6.6,14.4,3.8,2.9],[16.7,24,15.9,17.3,17.5,15.6,17,12.9,10.5,14.2,0,14.5,14.6,12,16.1,12.6,18.3,17.1,14.2],[12,10.6,7.4,4.8,10.1,1.6,15.1,4,7.5,9.7,14.5,0,9.1,4.4,6.3,3.9,6.2,12.3,9.6],[2.8,16.8,3.4,13.3,6.4,10.1,3.2,6.3,6.9,0.5,14.6,9.1,0,6.9,3.8,6.6,13.9,4.4,3.6],[9,13.8,6,10.2,7.4,5.5,9.4,1.9,4.4,6.5,12,4.4,6.9,0,4.3,2.1,10.5,9.8,6.2],[6.6,13.6,0.9,13.3,2.7,7.3,7,4,7.4,4.4,16.1,6.3,3.8,4.3,0,4.1,11.9,7.4,6.5],[9.4,12,4.8,9.8,6.4,4.9,9.7,0.9,4.5,6.6,12.6,3.9,6.6,2.1,4.1,0,8.5,13.1,6.9],[23.3,8.9,12.1,2.1,12.4,4.3,18.7,11.2,14,14.4,18.3,6.2,13.9,10.5,11.9,8.5,0,19,17.5],[1.1,21,6.7,21.8,9.1,15.9,1,8.8,9.3,3.8,17.1,12.3,4.4,9.8,7.4,13.1,19,0,3.9],[3.5,17.7,5.8,17.2,8.7,10.6,4,5.9,6.4,2.9,14.2,9.6,3.6,6.2,6.5,6.9,17.5,3.9,0]]
    return N, Mat


def calpathValue(path,Mat):
    #global Mat
    temp = Mat[0][path[0]]
    for i in range(len(path) - 1):
        temp += Mat[path[i]][path[i + 1]]
    temp += Mat[path[-1]][0]
    return temp


def initial(N,LEN,Mat):
    #global N
    init = list(range(1, N, 1))
    pack = [0] * LEN
    packValue = [0] * LEN
    for i in range(LEN):
        random.shuffle(init)
        data = init
        pack[i] = data.copy()
        packValue[i] = calpathValue(pack[i],Mat)
    indexes = np.argsort(packValue)
    pack = np.array(pack)[indexes]
    packValue = np.sort(packValue)
    return packValue, pack


def preserve(i,packValue,tempPackValue,tempIndex,pack,tempPack):
    #global tempPack, tempPackValue, pack, packValue, tempIndex
    tempPackValue[tempIndex] = packValue[i]
    tempPack[tempIndex] = pack[i].copy()
    tempIndex += 1


def select(N, pack, tempPack, tempPackValue, tempIndex, LEN, packValue):
    #global N, pack, tempPack, tempPackValue, tempIndex, LEN, packValue

    tpk = tempPack[:tempIndex]
    tpkv = tempPackValue[:tempIndex]

    indexes = np.argsort(tpkv)
    tpk = np.array(tpk)[indexes]
    tpkv = np.sort(tpkv)

    pack = tpk[:LEN]
    packValue = tpkv[:LEN]


def crossover(i, j, N, pack, tempPack, tempPackValue, tempIndex,Mat):
    #global N, pack, tempPack, tempPackValue, tempIndex
    times = random.randint(1, N - 2)
    indexes = [0] * times
    for t in range(times):
        if t == 0:
            indexes[t] = random.randint(0, N - times - 1)
        else:
            indexes[t] = random.randint(indexes[t - 1] + 1, N - times + t - 1)
    tempPack[tempIndex] = pack[i].copy()
    pack_j_reindex = pack[j].copy()[indexes]
    count = 0
    for v in range(N - 1):
        if count >= times: break
        if tempPack[tempIndex][v] in pack_j_reindex:
            tempPack[tempIndex][v] = pack_j_reindex[count]
            count += 1
    tempPackValue[tempIndex] = calpathValue(tempPack[tempIndex], Mat)

    tempIndex += 1
    tempPack[tempIndex] = pack[j].copy()
    pack_i_reindex = pack[i].copy()[indexes]
    count = 0
    for v in range(N - 1):
        if count >= times: break
        if tempPack[tempIndex][v] in pack_i_reindex:
            tempPack[tempIndex][v] = pack_i_reindex[count]
            count += 1
    tempPackValue[tempIndex] = calpathValue(tempPack[tempIndex], Mat)

    tempIndex += 1


def mutation(i,N, pack, tempPack, tempPackValue, tempIndex,Mat):
    #global N, pack, tempPack, tempPackValue, tempIndex
    times = random.randint(1, N - 2)
    indexes = [0] * times
    for t in range(times):
        if t == 0:
            indexes[t] = random.randint(0, N - times - 1)
        else:
            indexes[t] = random.randint(indexes[t - 1] + 1, N - times + t - 1)
    origin_indexes = indexes.copy()
    random.shuffle(indexes)
    tempPack[tempIndex] = pack[i].copy()

    for t in range(times):
        tempPack[tempIndex][indexes[t]] = pack[i][origin_indexes[t]]
    tempPackValue[tempIndex] = calpathValue(tempPack[tempIndex],Mat)
    tempIndex += 1

def GA(places):

    place_choose = places#此处为输入
    N = len(place_choose) + 1
    n, dis_table = read_data()

    place_choose.add(0)
    place_choose = list(place_choose)
    Mat = np.zeros((N, N))
    for i in range(0, N):
        for j in range(0, N):
            Mat[i][j] = dis_table[place_choose[i]][place_choose[j]]
    #print(Mat)

    LEN = 20
    pc, pm = 0.7, 0.6
    NOTMORETHANstayINGV = 10

    packValue, pack = initial(N,LEN,Mat)

    tempLEN = LEN * LEN
    tempPack = [[0] * N] * tempLEN
    tempPackValue = [0] * tempLEN

    tempIndex = 0

    global_Value = packValue[0]
    stayinGV = 0

    while True:
        tempIndex = 0
        for i in range(LEN):
            preserve(i,packValue,tempPackValue,tempIndex,pack,tempPack)
            if random.random() < pm:
                mutation(i,N, pack, tempPack, tempPackValue, tempIndex,Mat)
            if i == LEN - 1: break
            for j in range(i + 1, LEN):
                if tempIndex >= tempLEN: break
                if random.random() < pc:
                    crossover(i, j, N, pack, tempPack, tempPackValue, tempIndex, Mat)
        select(N, pack, tempPack, tempPackValue, tempIndex, LEN, packValue)
        if packValue[0] < global_Value:
            global_Value = packValue[0]
            stayinGV = 0
        elif packValue[0] == global_Value:
            stayinGV += 1
        else:
            print("Something wrong")
            break
        if stayinGV == NOTMORETHANstayINGV:
            break
    a = {}
    a[0]=0
    for i in range(0,len(pack[0])):
        a[i+1] = place_choose[pack[0][i]]
    a[0] = global_Value
    return(a)
