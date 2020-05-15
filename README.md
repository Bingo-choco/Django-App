# Django-App
use django to implement an online application  
:whale:This is the first time that I used django to implement the idea of our team :  
:bulb:Plan user's leisure time due to their habits  
( When they sign up, they need to answer an online query in order to render our app design a more personal schedule.)

  
:gift_heart:File show is this django app, you could straightforward clone it :gift_heart:   
:sunny: This app is my curriculumn design, so my team has also written a concluding report in chinese.  
I also commit it on hub.(In Word) You could see the detailed design and functions of my app.:v:  
:ghost:Below I'll show each key pages and tell you fuctions and features of it in chinese.      
I'll supplement the English version later :wink:  
ps:本算法涉及到的娱乐地点地理坐标，以及各个属性值偏好，纯属虚构 :foggy:  

:flags:(1)主界面：  
![image](https://github.com/Bingo-choco/Django-App/blob/master/img/Main.jpg)  
  
  
:flags:(2)登录，注册页面:  
![image](https://github.com/Bingo-choco/Django-App/blob/master/img/Register.jpg)  
  

:flags:(3)个人中心  
登记个人爱好，之后会根据你的偏好生成地点推荐   
![image](https://github.com/Bingo-choco/Django-App/blob/master/img/Personal_center.jpg)  
  

:flags:(4)路线规划界面  
遗传算法解决TSP问题，得出用户偏好路线  
![image](https://github.com/Bingo-choco/Django-App/blob/master/img/Show_plan.jpg)    
![image](https://github.com/Bingo-choco/Django-App/blob/master/img/TSP_question.jpg)    
  
  
:flags:(5)评论界面  
对今日所去地点进行评论，评论结果会对存储在数据库中的该用户偏好产生影响  
![image](https://github.com/Bingo-choco/Django-App/blob/master/img/Evaluate.jpg)  
  
  
:flags:(6)日志生成  
利用评论页面结果自动生成日志，日志背景可以点击后随机更新  
![image](https://github.com/Bingo-choco/Django-App/blob/master/img/generate_Log.jpg)  
  
    
    
:flags:(7)问答系统
针对用户提出的针对系统功能的问题进行解答，采用了Idf+余弦方式实现问答匹配
![image](https://github.com/Bingo-choco/Django-App/blob/master/img/Q_and_A.jpg)  
  


