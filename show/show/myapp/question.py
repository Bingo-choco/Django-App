# -*- coding: utf-8 -*-
import MySQLdb #引入pymssql模块
import jieba
import operator
import sys
# reload(sys)
import jieba.posseg as pseg #词性标注
import jieba.analyse as anls #关键词提取



def Question(Q):
    conn = MySQLdb.connect("localhost", "root", "Aptx4869", "route", charset='utf8' )
    if conn:
        print("连接成功!")
    cur = conn.cursor()
    sqlstr = 'select * from myapp_qanda'
    cur.execute(sqlstr)
    data = cur.fetchall()
    cur.close()
    conn.close()
    # print('表中的原始数据:')
    # print data      #表中原始数据 data
    len_row = len(data)  # 表中的行数 len_row
    # print ('表中的行数：%d',len_row)

    # print '***列表化的数据data：', data

    len_col = len(data[0])  # 表中的列数 len_col
    # print ('表中的列数',len_col)

    # for i in range(len_row):        #展示问题的内容
    #     print '表中第',i+1,'行'
    #      print data[i]
    #     for j in range(len_col):
    #          print(data[i][j])

    # t1=list()
    # t2=list()
    # t=[t1,t2]
    t1 = ['系统', '行程', '黑名单', '日记', '功能', '指数', '体力', '省钱', '作用']
    len_t1 = len(t1)  # 关键词的个数

    # Q = raw_input('***please输入您的查询：')
    # print '***查询Q为：', Q

    # 数据库每个问题进行分词    D1_list = jieba.lcut(D1_read, cut_all=True)
    D_read = []
    D_list = []  # w问题分词后的列表 D_list[][]
    for i in range(len_row):
        D_read.append(data[i][1])  # 提取data的每个问题，再对问题进行分词 D_read[]
        D_list.append(jieba.lcut(D_read[i], cut_all=True))
        # print D_list[i]
    # print D_list

    # 查询中的分词
    Q_list = jieba.lcut(Q, cut_all=True)  # 查询Q的分词 Q_list
    # print "***查询Q的分词", Q_list
    Q_list_len = len(Q_list)  # 查询Q中的分词的个数 Q_list_len

    # for i in range(Q_list_len):   # 展示查询Q中的分词
    #     print Q_list[i]

    # for i in range(len_row):      #展示每个问题的分词的内容
    #     print '***第',i+1,'个问题分词***'
    #     for j in range(len_col):
    #         print D_list[i][j]

    ###计算文档分词为列表的长度
    len_list = []  # 存放每个问题的分词个数的一个列表 len_list[]
    for i in range(len_row):
        len_list.append(len(D_list[i]))
    len_count = len(len_list)  # 问题的个数 len_count

    # 统计词频
    def count(N, t1, D_list):
        match = []
        for i in range(N):  # N
            match.append(D_list.count(t1[i]))
        return match

    D_count = []  # 存放每个问题的词频 D_count[]
    for i in range(len_count):
        D_count.append(count(len_t1, t1, D_list[i]))
    # D1_count=count(len(t1), t1, D1_list)
    # D_count=[D1_count,D2_count,D3_count,D4_count]
    # print 'data中每个问题的词频：',D_count

    # 统计查询中的词频
    Q_count = []
    for i in range(len_t1):
        Q_count.append(Q_list.count(t1[i]))
    # print '***查询Q中的词频：', Q_count

    # cos余弦计算函数
    C = []

    def cosVector(x, y):
        if (len(x) != len(y)):
            print('error input,x and y is not in the same space')
            return
        result1 = 0.0
        result2 = 0.0
        result3 = 0.0
        for i in range(len(x)):
            result1 += x[i] * y[i]  # sum(X*Y)
            result2 += x[i] ** 2  # sum(X*X)
            result3 += y[i] ** 2  # sum(Y*Y)
        # print(result1)
        # print(result2)
        # print(result3)
        # print("result is "+str(result1/((result2*result3)**0.5))) #结果显示
        return str(result1 / ((result2 * result3) ** 0.5))

    # cos余弦方法计算相似度
    for i in range(len_row):
        # print '***第', i + 1, '个问题词频：', D_count[i], '相似度：', cosVector(D_count[i], Q_count)
        C.append(cosVector(D_count[i], Q_count))  # 余弦相似度计算的结果  C

    # print '相似度：', C

    list_sort = []
    for i in range(len_row):
        list_sort.append([i + 1, C[i]])
        # print list_sort[i]
    # print '原始顺序问题的相似度：', list_sort
    list_sort.sort(key=operator.itemgetter(1), reverse=True)

    # print '降序后的问题的相似度：', list_sort  # 降序后的问题的相似度表  list_sort[][0]--问题编号  list[][1]--问题相似度

    # print '问题推荐降序编号：'
    # for i in range(len_row):
    #     print list_sort[i][0]

    result=[]
    for i in range(3):
        result.append(list_sort[i][0])

    # print '文档顺序---相似度'
    # for i in range(len_row):
    #     print '问题编号：', list_sort[i][0], '---', '相似度：', list_sort[i][1]

    return result


#print '最后的结果：',aaa




