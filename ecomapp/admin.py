from django.contrib import admin

from .models import *  

# * nadiyera each and every models ko name lekhera garda ni hunxa ; but that is tedious work 

# . le chi k bujhauxa bhane yei directory(appecom) ko models bhitra bata bhaneko  ; yedi xuttai directory bata bhako bhaye teskoname.models garnu parthyo ; so same directory ho bhane .lekhe pugxa 


# Register your models here 
# after making models never forget to register that model in admin.py 

admin.site.register(Category) 

admin.site.register(Subcategory) 

admin.site.register(Item) 

admin.site.register(Slider) 

admin.site.register(Ad)

admin.site.register(Contact) 

admin.site.register(Information)

admin.site.register(Cart) 







