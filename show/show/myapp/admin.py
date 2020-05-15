from django.contrib import admin

from myapp.models import Road,client,Choice , store_category,store_style,store

admin.site.register(Road)

admin.site.register(client)

admin.site.register(Choice)

admin.site.register(store_category)

admin.site.register(store_style)

admin.site.register(store)
