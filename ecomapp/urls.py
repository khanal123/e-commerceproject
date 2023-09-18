from django.urls import path
from .views import * 
# esari sabai views import garnu bhanda chine chine garnu is best practice 

app_name = 'ecomapp'
# aba yo app name lai main urls (project ko urls ) ma gayera include garnu parxa 

# no need to make separate urlpatterns for function based views and class based views ; eutai bhitra include garna milxa majale 

# yo yaa slug bhanera pathko xu ni tyo name chi uta models.py ma banako get_item_url() bhanne function ma pass gareko dictionary ko key ko name ho; aba slug nai huna parxa name bhanne chi xaina; but tyaa key ko j name xa tyo chi yaa lekhna paro 

urlpatterns = [ 
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>', ItemView.as_view(),name='product'),
    path('category/<slug>', CategoryView.as_view(),name='category'),
    path('subcategory/<slug>', SubcategoryView.as_view(),name='subcategory'),
    path('search',SearchView.as_view(),name='search'),
    path('signup',signup,name="signup"),
    path('login',login,name="login"),
    path('cart',cart,name="cart"),
    path('add_to_cart',add_to_cart,name="add_to_cart"),
    path('delete_cart/<slug>',delete_cart,name='delete_cart'),
    path('contact/',contact,name='contact')

] 




