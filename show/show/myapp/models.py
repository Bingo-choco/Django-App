from django.db import models


class Road(models.Model):
    location = models.TextField(max_length=200)

    money = models.IntegerField(default=0)

    score = models.IntegerField(default=0)


class client(models.Model):

    name = models.CharField(max_length=20)

    password = models.CharField(max_length=20)

    email = models.EmailField()

    mobile = models.CharField(max_length=20)

    strength = models.FloatField(default=0)

    money = models.FloatField(default=0)

    start_place = models.CharField(max_length=40)




class store_category(models.Model):

   name =models.CharField(max_length=20)


class store_style(models.Model):

    name = models.CharField(max_length=20)

    category = models.ForeignKey(store_category, on_delete=models.CASCADE)


class Choice(models.Model):

    user = models.ForeignKey(client, on_delete=models.CASCADE)

    choice_kind = models.ForeignKey(store_style, on_delete=models.CASCADE)

    choice_about = models.CharField(max_length=20)

    choice_no = models.IntegerField(default=3)


class store(models.Model):

    name = models.CharField(max_length=40)

    category = models.ForeignKey(store_category, on_delete=models.CASCADE)

    style = models.ForeignKey(store_style, on_delete=models.CASCADE)

    cost = models.IntegerField(default=3)

    x = models.IntegerField(default=0)

    y = models.IntegerField(default=0)


class route(models.Model):

    user = models.ForeignKey(client, on_delete=models.CASCADE)

    date = models.DateField()

    store_route = models.CharField(max_length= 200)

    hours = models.IntegerField(default = 4)

    people_num = models.IntegerField(default = 2)


class QandA (models.Model):

    Q_content = models.CharField(max_length = 50)

    Q_answer = models.CharField(max_length = 200)


class review(models.Model):

    route = models.ForeignKey(route, on_delete=models.CASCADE )

    store = models.ForeignKey(store, on_delete=models.CASCADE )

    date = models.DateField()

    satisfaction = models.IntegerField(default= 3)

    content = models.CharField(max_length=200)

    is_reviewed = models.IntegerField(default=0)




















