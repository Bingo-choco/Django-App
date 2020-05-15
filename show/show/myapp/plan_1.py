import math
import random
place_price = [5,4,3,2,1,2,3,4,5,4,5,3,3,4,5,4,4,3,5,4] #每一处平均消费{1，2，3，4，5}
place_enjoy = [3,4,5,3,4,2,1,3,2,4,3,2,5,3,4,2,3,1,3,4] #用户对每一处的喜好程度{1，2，3，4，5}
E = 0.6 #用户体力值{0.2，0.4，0.6，0.8，1}
W = 0.4 #用户省钱程度{0.1，0.2，0.3，0.4，0.5}

def work_out_rec(pp,pe,energy,weight,time):#几个参数分别为 地点价格、地点喜爱度、体力值、省钱度、时间，返回推荐地点编号集合
    place_result = []
    place_up = math.ceil(energy*time)
    place_down = int(energy*time)#算出游玩地方总数的上下限

    for i in range(0 , len(pp)):
        place_result.append((pe[i] - weight * pp[i] , i+1))
    place_result= sorted(place_result, key=lambda x: x[0])
    place_result.reverse()#算出每一个地方的收获值

    temp_p={}
    temp_p[0]=place_result[0][0]
    for i in range(1, len(pp)):
        temp_p[i] = temp_p[i-1]+place_result[i][0]
    for i in range(0, len(pp)):
        temp_p[i] = temp_p[i] / temp_p[len(pp)-1]
    #print(temp_p)#计算出每一个地方累计概率

    decide_number1 = random.uniform(0, 1)
    if decide_number1 > 0.5:
        place_number = place_up
    else:
        place_number = place_down
    #确定去几个地方

    places=set()
    while len(places) < place_number :
        decide_number2 = random.uniform(0, 1)
        for i in range(0, len(pp)):
            if temp_p[i] >= decide_number2:
                break
        places.add(place_result[i][1])
    return places


'''
for i in range(0,10):#随便推荐几种行程
    print(work_out_rec(place_price,place_enjoy,E,W,6))
'''



