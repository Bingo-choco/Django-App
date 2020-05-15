import datetime
import random

from django.shortcuts import render, get_object_or_404

from myapp.models import client, route, store, Choice, store_style, QandA, review
from myapp.plan_1 import work_out_rec
from myapp.plan_2 import GA
from myapp.question import Question


def index(request):
   # request.session.setdefault('user', 1)
    print('session里的user.id',request.session['user'])
    return render(request, 'myapp/index.html')

def login(request):



    if request.method == 'POST':
        uname = request.POST.get('user')
        pwd = request.POST.get('passwd')
        print(uname, pwd)
        if uname and pwd:
            uname=uname.strip()

            try:

                user = client.objects.get(name=uname)
                if user.password == pwd:
                    #这里需要session将用户id存储进来
                    request.session['username'] = user.name
                    request.session['userid'] = user.id
                    return render(request,'myapp/index.html',{'con':request.session['username']+"登录成功"})
                else:
                    return render(request,'myapp/login.html', {'error':'密码不正确'})
            except:
                return render(request,'myapp/login.html', {'error':'账号不存在'})
        else:
            return render(request, 'myapp/login.html', {'error': '账号或密码不为空'})

    else:
        print('no value')

    return render(request, 'myapp/login.html')

def register(request):

    if request.method == 'POST':
        uname = request.POST.get('user')
        pwd = request.POST.get('passwd')
        print(uname, pwd)
        print("come***********************come")

        if uname and pwd:
            uname = uname.strip()

            try:
                temp = client.objects.get(name=uname)
                return render(request, 'myapp/register.html', {'error': '该用户名已注册'})
            except:
                user = client()
                user.name = request.POST.get('user')
                user.password = request.POST.get('passwd')
                user.save()
                # 要实现所有choice的存储
                for i in store_style.objects.all():
                    Choice.objects.create(user_id = user.id , choice_kind_id= i.id , choice_about = i.name , choice_no = 3)
                return render(request, 'myapp/login.html', {'name': uname})
        else:
            return render(request, 'myapp/register.html', {'error': '账号或密码不为空'})
    return render(request, 'myapp/register.html',{'hi':"欢迎注册"})

def self_center(request):

    try:
        user_id = request.session['userid']
        user = client.objects.get(id=user_id)
        return render(request, 'myapp/myself.html', {'user': user})
    except:
        return render(request, 'myapp/login.html', {'error': '请先登录，再查看个人信息'})



def change_self(request):

    user_id = request.session['userid']

    user = client.objects.get(id=user_id)

    if request.method == 'POST':
        user.name = request.POST.get('user')
        user.password = request.POST.get('passwd')
        user.email = request.POST.get('email')
        user.mobile = request.POST.get('mobile')
        ans1 = request.POST.get('strength')
        print('体力下拉框：', ans1)
        user.strength = int(ans1)

        ans2 = request.POST.get('money')
        print('钱财下拉框：', ans2)
        user.money = int(ans2)

        user.save()

        for choice in user.choice_set.all():
            no = request.POST.get(choice.choice_about)

            if no == None:
                print('no值为空')
            else :
                choice.choice_no = int(no)
                choice.save()
            print('下拉框aaaaaaaaaaa', choice.choice_about, choice.choice_no )

        return render(request, 'myapp/myself.html', {'user': user})


    return render(request, 'myapp/self_change.html',{'user':user})


def plan_init(request):

    try:
        user_id = request.session['userid']

        user = client.objects.get(id=user_id)

        # 如果提交旅行内容
        if request.method == 'POST':
            print('到这里了')

            date_t = datetime.date.today()

            # 暂且默认为当前时间
            # date_t = request.POST.get('date_choose')

            hour_t = request.POST.get('hours')

            num = request.POST.get('people')

            road = route.objects.create(date=date_t, hours=hour_t, people_num=num, user_id=user_id)

            request.session['routeid'] = road.id

            print(road.date, road.hours, road.people_num, road.user_id)

            # 调用函数部分
            # print(route_get(1))
            global roads_no

            roads_no = road_plans(user, road, hour_t)

            global road_content

            road_content = deal_plan_ans(roads_no)

            return render(request, 'myapp/plan.html', {'user': user, 'road': road, 'content': road_content})
        # 第一步初始返回项
        return render(request, 'myapp/plan.html', {'user': user})
    except:

        return render(request, 'myapp/login.html', {'error': '请先登录，再进行行程规划'})



def road_plans(user ,inf , hours):

#地点编号存储（5，8）
    list = [[0 for col in range(6)] for row in range(5)]

    #店家价钱的数组
    price = []

    #用户对店家喜好程度
    like = []


    #用户体力值
    strength = user.strength*0.2

    #用户省钱度
    money = user.strength * 0.2


    for bus in store.objects.all():
        price.append(bus.cost)
        choice = Choice.objects.get(choice_kind_id = bus.style, user_id = user.id)
        like.append(choice.choice_no)

   
    # 函数传递
    for i in range(0, 5):

         places = work_out_rec(price , like , strength , money , float(hours))

         print('地点出炉' , places)

         k = 0

         for j in places :
             list[i][k] = j
             k = k+1

    return list

def deal_plan_ans(roads):

   # roads = [[1, 3, 5, 7, 0], [4, 2, 8, 6, 0], [7, 2, 0, 0, 0], [9, 1, 0, 0, 0], [4, 2, 10, 0, 0]]

    list = []

    for i in range(len(roads)):
        # 如果为0就表示没有这条路径
        if roads[i][0] != 0:
            list.append("大连海事大学")
            for j in range(len(roads[i])):
                if roads[i][j] != 0:
                    dian = store.objects.get(id=roads[i][j])
                    #if j != 0:
                    list[i] += "  ,,,  "
                    list[i] += dian.name
            print('here---------------', list[i])
    return list

def change_plan(request):

    route_id = request.session['routeid']

    road = route.objects.get(id = route_id)

    user = client.objects.get(id = road.user_id)

    hour_t = road.hours

    global roads_no

    roads_no = road_plans(user, road, hour_t)

    global road_content

    road_content = deal_plan_ans(roads_no)

    return render(request, 'myapp/plan.html', {'user': user, 'road': road, 'content': road_content})

def plan_order(request):

    route_id = request.session['routeid']

    print('这里-----------------------------------')

    road = route.objects.get(id=route_id)

    user = client.objects.get(id=road.user_id)

    hour_t = road.hours

    if request.method == 'POST':

        num = request.POST.get('gender')

        print('nameaaaaa' , num)

        param = set()

        for i in roads_no[int(num)-1]:
            print('地点顺序',i)
            if i!=0:
               param.add(i)

        #插入TSP函数

        print('len' , len(param))

        list = "大连海事大学"

        #产生初始化的评论
        init_review(param , route_id)
        '''
        re = review.objects.get(id = 1)
        print('review.route_id' , re.route_id)
        re.route_id = 42;
        '''
        if len(param) != 1 :
            result = GA(param)

            print("GA的返回值",result)

            for j in range(1, len(result)):
                if result[j] != 0:
                    dian = store.objects.get(id=result[j])
                    # if j != 0:
                    list += "  ------->  "
                    list += dian.name
        else:
            dian = store.objects.get(id = roads_no[int(num)-1][0])
            list += "  ------->  "
            list += dian.name

        print('最后排序结果', list)

        road.store_route = list

        road.save()

    return render(request, 'myapp/plan.html', {'user': user, 'road': road, 'content': road_content })

def init_review(dian,road_id):
    #用于初始化评论
    road = route.objects.get(id = road_id)
    print('生成评论' , road_id)
    for i in dian:
        review.objects.create(date=road.date, route_id=road_id , store_id=i)
        print('route_id' , road_id ,'store_id',i)

def deal_satisfacation(add , before):
    if add == 1 and before < 5:
        return before+1
    elif add == 4 and before > 1:
        return before-1
    else:
        return before


def comment(request):

    try:
        user_id = request.session['userid']
        try:
            route_id = request.session['routeid']

            list = []

            name = []

            plan = route.objects.get(id=route_id)

            if request.method == 'POST':
                store_id = request.POST.get('select')
                sat = request.POST.get('sat')
                con = request.POST.get('con')
                dian = store.objects.get(id=store_id)
                user = client.objects.get(id=plan.user_id)
                re = review.objects.get(route_id=route_id, store_id=store_id)
                choice = Choice.objects.get(choice_kind=dian.style, user_id=user.id)
                print('商家id', store_id, '满意程度', sat, '想法与体会', con)

                # 处理顾客喜好程度
                choice.choice_no = deal_satisfacation(sat, choice.choice_no)
                choice.save()

                # 处理评论re
                re.is_reviewed = 1
                re.content = con
                re.save()

            for re in plan.review_set.all():
                # 没评论的加进来
                if re.is_reviewed == 0:
                    list.append(re)
                    dian = store.objects.get(id=re.store_id)
                    name.append(dian)

            return render(request, 'myapp/comment.html', {'store_list': name, 'route_id': route_id})
        except:
            return render(request, 'myapp/plan.html', {'con': "请先进行路程规划，再开始评论"})
    except:
        return render(request, 'myapp/login.html', {'error': '请先登录，才可以评论'})



#对满意度进行处理如果 非常满意+1（<= 5）
#                    拉入黑名单（>=1）

def diary(request):

    try:
        user_id = request.session['userid']
        try:
            route_id = request.session['routeid']

            road = route.objects.get(id=route_id)

            t = random.randint(1, 4)

            return render(request, 'myapp/diary.html', {'route': road, 'img': t})
        except:
            return render(request, 'myapp/plan.html', {'con': "请先进行路程规划，才能有日志哦！！！"})
    except:
        return render(request, 'myapp/login.html', {'error': '请先登录，才可以为你量身定做日志哦……'})


def question(request):

    if request.method == 'POST':
        s = request.POST.get("Question")
        print("问题为------------------" ,s)


        list = []

        # 问答函数
        ans = Question(s)

        print('ans' , ans)

        #先默认返回一条答案
        k = 0
        for i in range(0,1):
            q = QandA.objects.get(id = ans[i])
            list.append("Question: " + q.Q_content)
            list[k]+"\r\n"
            list.append("Answer: " + q.Q_answer)
            k = k+1
         #c_q为顾客初始化时提出的问题
        return render(request, 'myapp/QandA.html',{'c_q': s , 'ans':list })

    return render(request, 'myapp/QandA.html')

def re_ask(request):
    return render(request, 'myapp/QandA.html')

def delete(request):

    try:
        user_id = request.session['userid']

        try:
            route_id = request.session['routeid']
            del request.session['routeid']
        except:
           print('no route_id')

        del request.session['userid']
        return render(request, 'myapp/index.html', {'con': '注销成功,请重新登录'})
    except:
        return render(request, 'myapp/login.html', {'error': '请先登录，再说注销'})





