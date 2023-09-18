from django.shortcuts import render , redirect
# for class based views we have to import View
from django.views.generic.base import View
from .models import *
from django.contrib.auth.models import User 
from django.contrib import messages , auth
from django.contrib.auth.decorators import login_required
# for api
from django.core.mail import EmailMessage
from rest_framework import viewsets , generics 
from .serializers import * 
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.filters import OrderingFilter, SearchFilter 

# # Function based view 
# def contact(request):
#     inform = {}  # empty dictionary
#     inform['information'] = Information.objects.all()

#     if request.method == 'POST':
#         name = request.POST['name']
#         subject = request.POST['subject']
#         email = request.POST['email']
#         message = request.POST['message']

#         info = Contact.objects.create(
#             name=name,
#             subject=subject,
#             email=email,
#             message=message 
#         )
#         info.save()
#     return render(request, 'contact.html', inform) # mathiko dictionary pass gardina paro 


# Till now we created function based views
# now let's create class based views to render the templates
# sano sano app ko lagi chi function based use hunxa(yesma inherit garna mildaina yesko main disadvantage) tara thulo thulo app jasma query haru dherai use hunxa tesma class based view better hunxa (cuz class based view ma OOP use garna painxa)
# there are three types of generic views:  view, detail view(dictionary ko aadhar ma data aayera basxa), list view(list ko aadhar ma data aayera basxa)
# teen ota generic view madhya euta lai chi inherit garnai parxa main class based view ma


# Yo muniko class based view chi value matra declare garna ho
class BaseView(View):  # inheriting generic view
    template_views = {}  # creating empty dictionary
# euta arko kura edi maile yo dictionary aru xuttai different class based view ma use garna chahe bhane majale use garna sakinxa simply by inheriting like as below ( aba tala nai her na dictionary ta BaseView class ko ho ni but use bhako xa HomeView maa)
# yo dictionary each and every time multiple thau ma majale use garna sakixna

# VVI note: edi yo BaseView class lai aru class haru le inherit garxan bhane ta pratyak class ma jj query haru define bhako xa; tyo queries haru chi sabai page le use garna paune bho


# yo categories ra subcategories sabai page ma inherit garne ho bhane yei BaseView class ma rakhdine
# BaseView class ma rakheko query haru bhaneko sab page ma inherit hunxa by default
# Tara yo tala tira ko class haru ma chi j query lekhya xa tei respective page ko lagi matra apply hunxa 
 
    template_views['categories'] = Category.objects.all()
    template_views['subcategories'] = Subcategory.objects.all()


# Yo muniko class based view chi html page(in this case index.html) ma gayera value lai view garauna ho
# tesko lagi BaseView class lai yaa inherit garna parxa:
# inherit garna ko main reason chi tyo template_views bhanne dictionary lai aba yaa ma use garxu k
# yesari duita class based view banara garyo bhane code chi nikai xoto hunxa k

class HomeView(BaseView):
    # aba request argument handle garna ko lagi euta get() function banauna parxa
    # request hami user le patahune ho certain content malai access garna paryo hai ; malai tyo content de bhanera; ani tyo request ko  badla ma server le response pathauxa ani tespaxi we are able to see the content of the webpage

    # junsukai view hos request chi jaile ni chinxa
    def get(self,request):  # self parameter is a instance of  class; it represents objects of that class

        # aba hami (query or context variable) haru banam  (bhannale le paila python ma instance varibales banautheu ni ho tei bhanna khojya khas ma)
        # class based view ko lagi chi khali agadi self add garde pugyo aru sab same as function based views
        # here query is written in the form of key : value pair
        # for eg: 'items' is a key jasma Item.objects.all() bhanne value (bhayebhar ko sab item bhanna khojya) gayera basxa
        # yaa naya naya key haru add gardai janu bhaneko mathi ko dictionary bhitra add hudai janu ho ;
        # jaile in templates ma loop lauda use hune bhaneko dictionary ko key or context variable ho ;  


        # self.template_views['items'] = Item.objects.all()
        # all() function le ta bhayebharko item sab dekhauxa 
        # but hamilai tya teen ota aafu le chaheko item matra dekhauna xa bhane we should use filter() function
        # ani tyo models.py ma product_front_page bhanne field banaka xa hola; ra by default tyo false ma rakhya xau bhane aba yaa True garera rakdine 
        # Aba tya click garesi True hunxa natra etikai xoddyo bhane false hunxa by default 
        # Bhayebhar ko sab item lai front page ma display garayera ta kaam xaina ;tya space pani thorai hunxa ra site nai dhilo load hunxa tyo bhayesi ta ; so front= true garera filter gardesi harek category ko hamle chaheko teen ota item matra front ma display hunxa 

        self.template_views['items'] = Item.objects.filter(product_front_page= True)
        self.template_views['slider'] = Slider.objects.all()
        self.template_views['ads'] = Ad.objects.all()
        self.template_views['special_offers'] = Item.objects.filter(special_offer = True)
        # yo filter bhanne function through hami le chaheko anusar ko filtration garna milxa 
        # aba maile models.py ma ta special_offers by default False banako xu tara yaa k garxu bhane tyo special_offers lai True banaidinxu jasle garda special_offers True bhako product matra filter bhayera tya template ma dekhinxa out of all items added 
        # Actual kaam kasari garxa bhane Item bhanne database ma bhako table ma gayera herxa k; ani jun jun item ko special_offers = True xa tyo table ma tyo tyo item lai matra tyo template ma dekhaune kaam garxa 
        

        # aba yo bhaye bhar ko query haru kaa render garne ta bhanda index.html ma render garne ; for that we have to pass that dictionary as an argument
        return render(request, 'index.html', self.template_views)


# Create a new class based view for quick view items: 
# Dictionary xuttai banairana pardaina ; sidai BaseView class lai inherit gardine ; this is the advantage of creating class based views  
class ItemView(BaseView):
    def get(self,request,slug):
        self.template_views['view_items'] = Item.objects.filter(slug=slug)
        # aba jun slug ko value urls ma gako xa tesko item view garna parne xa hamilai ; so we can use filter function for that
        # yo filter function  ma use bhako pailo slug chi mathi url maa as an id aayeko slug ho bhane paxadi ko slug chi item ko database/models ma bhako slug ho
        # ra yedi yo slug value match bhayesi matra tyo product ko info view garau bhaneko 
        return render(request,'single.html',self.template_views)
        
 # New class based view for Category:
class CategoryView(BaseView):
    def get(self,request,slug):
# Aba yaa ali different concept xa...mathi ko items display garne ra view garne jasto xaina; tya mathi ta euta item view garna ko lagi euta slug use hunthyo ra tyo slug le jun item lai represent gareko xa tyo display hunthyo ; tara yaa ta category ma click garesi tyo category related sab item haru display huna paryo ni ta ; euta matra item ta aune haina ; so tesko lagi hamile yo category ko slug kun chi ho tyo chinna paryo ani teskai addhar ma tyo category ko sab items display garna paryo ..so esto garam
# aba yaa get() launa parne hunxa jasle value haru lai tanxa ...filter() le chi query banaune ho tara get() le chi value haru tanne ho database bata 
        category_id = Category.objects.get(slug=slug).id
# Note yo agadi ko actegory_id chi variable ho so j name banaye ni huxa tei lina parxa bhanne xaina

# Aba yaa ekdam important cha hai...yesko meaning bujham paila...
# Yelle k bhanxa bhane tapaiko Category bhanne model/database ma jau ani tana(get gara) value ; kun chi value tanne ta bhanda id bhanne value tana; jasma tya models ma bhako slug bhanne field ra yaa mathi bata pass bhako slug ko value same hunxa...yo mathi pass bhako slug chi urls.py ma as an id ko rup ma pass bhako slug ho ;  
# Aba chi k hunxa bhanda category_id ko value chi number ma auxa; tyo Category ko slug lai represent garne tesko category_id jun integer form ma xa tyo tanaxa aba yaa get() function le  
# aba hamile po 'electronics' bhanne slug dekhiraxau ta tyo category ko lagi ; tara database le ta dekhya hunna tyo cuz database ma primary key bhaneko ta id xa  
# aba aile ta hamile id taneu haina ra yedi paxi gayera hamilai aru kei chiz tanna man lago bhane ni yesari nai get() method user garera garne jaile pani 
# slug lai nai primary key banaideko bhaye yo sab garna pardaina thyo tara hamro case ma ta primary key bhaneko id ho; tei bhara tyo slug sanga milne id taneko hamile
# slug lai suru mai primary key banauna ni sakthe maile...but tyo garnu better practice haina ; garna namilne bhanne chi haina  
 
# Aba yeti garesi mathi jastai query banaune to filter those items among all items present there if ecomapp_item bhanne table ma bhayeko category_id matches with ecomapp_category bhanne table bata fetch gareko id:  
# Match garauna chine id ho but actual ma url ma jane chi tesko slug ho hai 
        self.template_views['category_items'] = Item.objects.filter(category_id=category_id)
        return render(request,'category.html',self.template_views)

# Aba yo kura majale bujh hai : (VVI topic)
# yeti bujhe dherai kura bujhinxa jun hami aru projects ma ni implement garna sakxau 
# Jasatai maile mathi ko logic bujhna lai DB browser khole
# ani ecomapp_category table ma gaye 
# tya hamro Category ko lagi id ra slug present xa 
# hamile yaa bata pathune bhaneko chi slug ho 
# TARA 
# Item bhanne field lai ta tha xaina ni hamro Category haru ko slug k ho bhanera
# Item lai ta khali yo respective category ko id matra tha xa...Ta ecomapp_item bhanne table ma gayera herna sakxas...Tya jati pani item xa tii sab ko euta id xa...last tira hola category_id bhanera euta column xa ....ho tyo bhaneko nai yo ecomapp_category bhanne table ma bhanko id bhanne column ho ....Aba yeso samjhi ta hamile foreignkey layera Category lai Item bhanne field bhitra taneko theu ni...ho tesle garda tyo item bhanne table ma aba harek item ko lagi tyo Category ko slug jadaina k rather tyo category ko id chi gayera basxa (same in case subcategory ni item field ma tanya xau foreignkey layera bhane)...kina testo bhayo slug kina tya gayena...cuz hamile primary key ta id lai nai banako xau ni ta...jollai primary key banako xau tei gayera basne ho tya item ko category_id bhanne column ma .... aba tya different item holan jasko category_id ( 1 1 1...2 2 2 etc ) testai hola manau...aba tyo 1 or 2 or bla bla bla lai represent garne category kun ho bhanera herna ta hamile ecomapp_category ko table mai gayera hernu paro ani id match garnu paro ani balla tha hunxa yee yo category ko item po ho tyo bhanera

# Aba tei bhara hamile mathi bhanna paro k; la hai tapai le click garne bela ta yo ecomapp_category ma bhako slug janxa ; ani tespaxi yo slug bhako category ko id kun chi ho bhanne kura tya patta launa paro ...jastai electronics bhanne slug ko id 1 raixa re...bhanesi aba yedi yesko id 1 ho bhane yo sanga related item haru kun kun ho ta bhanne kura tya items ma gayera tha hunxa cuz tya category id anusar item milera baseka hunxan ; thus aba hamile template ma certain Category ma click gareu bhane tyo item ma bhako sabai product visible nabhai ecomapp_category bhanne table bata aako id = ecomapp_item bhanne table ma bhako category_id match hune product haru display garna sakinxa...tesaiko lagi mathi hamle query haru banako.....Aba mathi product ko case ma chi euta ma click garda tesko bare ma dekhinthyo jaslai one to one relationship bhaninxa bhane yaa ta euta category ma click garda tyo related many products dekhine bho which signifies one to many relationship(euta Category ko dherai item) or many to one relationship(Dherai item ko euta category)...THIS IS THE MAIN LOGIC BEHIND IT (VVI) 


# # Class based view for Subcategory:
class SubcategoryView(BaseView):
    def get(self,request,slug):

        subcategory_id = Subcategory.objects.get(slug=slug).id
        self.template_views['subcategory_items'] = Item.objects.filter(subcategory_id=subcategory_id)
        return render(request,'subcategory.html',self.template_views)
# Same concept for subcategory as discussed above 


# class based view for searching items/products 
# search ko lagi slug pathauna pardaina 
class SearchView(BaseView):
    def get(self,request):
        # query bhanne euta variable banauxu jasle template(base.html) bata aako data lai handle garxa 
        # Uta template bata pathako Search lai yaa catch garera render garna parxa ;
        # name ="Search " bhanne xa ni input tag bhitra ho tei ho
        # __icontains is for search 
        query = request.GET.get('Search','None')
        if not None:
            self.template_views['search_result'] =Item.objects.filter(title__icontains=query)
        self.template_views['search_for'] = query
        return render(request,'search.html',self.template_views)


# For Sign Up / Register 
# we create a function based view 
# NEVER DO sihn up and login in class based view 
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            # aba maile tyo username/email exists garxa ki nai database tyo herna parne hunxa k; if exits garxa bhane further proceed garna nadine 
            if User.objects.filter(username=username).exists():
                messages.error(request,"The username is already taken")
                return redirect('ecomapp:signup')

            elif User.objects.filter(email=email).exists():
                messages.error(request,"The email is already registered")
                return redirect('ecomapp:signup')

            else:
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password 
                ) 
                user.save()
                user = auth.authenticate(username=username,password=password)
                auth.login(request,user)
                return redirect('/')
                messages.success(request,"You are registered successfully!!! Go to login")
                # sign up bhayesi directly home page ma redirect garne 
                return redirect('ecomapp:signup')
        else:
            messages.error(request,"Passwords do not not match")
                
            return redirect('ecomapp:signup')  

    return render(request,'signup.html') 

# for custom login:

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request,"Username or Password do not match ")
            return redirect('ecomapp:login')
    return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


# for cart 
# main UI ma visible garaune cart yo ho 
def cart(request):
    views = {}
    views['carts'] = Cart.objects.filter(checkout=False,user=request.user) # checkout nabhako item haru matra cart ma display hunu paryo tesko lagi checkout lai True gardine ; ani request.user means tyo session maa bhako user lai matra garna dee bhaneko 
    return render(request,'cart.html',views)


# yo talako add to cart chi database ma value halna matra ho 
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        title = request.POST['title']
        slug = request.POST['slug']
        image = request.POST['image']
        price = request.POST['price']
        description = request.POST['description']
        # if there is already an item in cart ; just update that value 
        if Cart.objects.filter(slug=slug).exists():
            quantity= Cart.objects.get(slug=slug).quantity 
            # filter le no of values return garxa but get le euta matra value return garxa 
            Cart.objects.filter(slug=slug).update(quantity=quantity+1)
            return redirect('ecomapp:cart') 
        # else if cart is empty; create the new cart 
        else:
            my_cart = Cart.objects.create(
                    user = request.user,
                    slug = slug,
                    title = title,
                    image = image, 
                    price = price,
                    description = description,
                    ) 
            my_cart.save() 
            return redirect('ecomapp:cart') 
    else:
        return redirect('/')

# to delete items in cart 
def delete_cart(request,slug):
    if Cart.objects.filter(slug=slug).exists():
            Cart.objects.filter(slug=slug).delete()
            messages.success(request,"Item is deleted.")
            return redirect('ecomapp:cart')
    else:
            return redirect('ecomapp:cart')
            messages.error(request,"Item is not in your database ")

# for contact
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        subject = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']
            
        contact = Contact.objects.create(
                name = name,
                email = email,
                subject = subject,
                message = message,
            )
        contact.save() 
        email = EmailMessage(
                'New message',
                f'<html><body><b>{name}</b> with email {email} has sent you message:  <i>{message}</i> </body> </html>',
                email,
                ['uknownothingjonsnow23@gmail.com'] 
            )            
        email.content_subtype="html"
        email.send()
        messages.success(request,"Thank You !! The message is sent")
        return redirect('ecomapp:contact')
    return render(request,'contact.html')
         

# for rest api:
# We must now create a view set of that serializer:

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all() # kasto kisimko value api ma dekhaune ..
    serializer_class = ItemSerializers  # Pass that database queryset into the serializer we just created, so that it gets converted into JSON and rendered

# note:
# serializers create garyo, viewset create garyo and then register garne in urls section 

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all() 
    serializer_class = AdSerializers   

# for filter (istall dajngo-filter first)
# ecommerce ma filtering dherai hune items/products lai nai ho 
class ItemFilterListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializers

    filter_backends = (DjangoFilterBackend,OrderingFilter,SearchFilter)

    filter_fields = ['id','title','price','discounted_price','stock','brand','labels','special_offer','category','subcategory'] #filter garanalai 

    ordering_fields = ['id','title','price','labels'] # order anausar milauna lai 

    search_fields = ['title','description'] # search garnalai 



