from django.db import models
# Note: Database ma kei kura change garesi (i.e database ko structure chnage hune bittikai) jaile ni migrations chi compulsory garna parxa)

from django.urls import reverse # we have to import this cuz we have used reverse() below 

from django.conf import settings


# Variables :
# for active or default(inactive)
STATUS = (('active', 'active'), ('', 'default'))
# yesari duita separate tuple ma kina define gareko bhanda hamro databse ma jane value euta hunxa ani fromtend ma dekhine value arko hunxa jaile pani
# yo suru ko active part bhaneko form ko through database ma jane part ho ; ani paxadi ko active bhaneko webpage ma dekhine part ho ; yo bhayo active ko lagi
# ani tya default ko case ma suru ma Null xoddya xam(default nai lekhde ni pharak ta kei pardaina); cuz tala blank =True xa ; so yo bhaneko database ma submit hune actual value ho; ani paxadi ko default bhaneko webpage ma dekhine part
# yaa ta duita matra part xa tuple inside tuple ma cuz hamilai aile chiyeko duita condition matra xa ; ki ta active ki ta default ; tara edi hamilai ajhai aru field chiyeko xa bhane we can easily add more tuples inside tuples there
# hamile edi category display garauna chahadainau bhane default ma rakhdixau uta admin panel ma; jastai hamile tyo category chi ma add garxu hai future ma bhanne sochya xau re hai tara aile hamro tyo category related kunai paroduct xaina re display garauna bhane category tya main index page ma display garayera ta kaam bhayena; so category chi banai rakham ani paxi product add bhayesi teslai display garaula bhanne hisab le tya arko option default banako ho hamile

# for stock or out of stock:
STOCK = (('In Stock', 'In Stock'), ('Out of Stock', 'Out of Stock'))
# yo database ma jane part ra hamile dekhne part duitai ko eutai name lekhdida paxi gayera handle/filter garna sajilo hunxa bhanera ho; compulsory chi xaina eutai name huna parxa bhanera

# for labels:
# jastai kunai item new hola, kunai sale ma xa hola, kunai hot item hola; ho tro product mathi display garauna xa dyamically bhane yesko ni xuttai labels bhanne variable banauna parxa
Labels = (('Hot', 'Hot'), ('Sale', 'Sale'), ('New', 'New'))


# CREATE MODELS:
# Now lets create a model for dynamic contents in our webpage
# database ma jun jun table ma jj kura haru rakhne ho tyo sabko lagi yesari models create grna parxa
# kunai kunai kura chi static nai rakhna parne ni hunxa ; dynamic le sabai thau kaam garxa bhanne xaina ; so afule analyze garne kasto content lai dynamic banaune bhanera
# tei bhara kun kun kura ko lagi models banaune bhanera pailai identify garna parxa
# site ekdam attractive ra dynamic banauna paro bhane ta sakesamma maximum models banaunai parxa



# For Categories in an ecommerce site:
# kunai pani ecommerce ma suru mai maile sidai items / products halna midlaina ; first ma ta tyo item ko category or subcategory huna parxa
# ani balla matra hamile tesma item add garna milxa
# so let's create a model for Categories

class Category(models.Model):  #inheriting models.Model inside Item class
    title = models.CharField(max_length=200)  # for title
    slug = models.CharField(unique=True, max_length=100)
    # Aba ta sochlas harek category ko ta afnai id hunxa ni tei pani hamile slug kina use garyeu ta ???
    # cuz id bhanda better chi slug use garna maninxa ; id ma hami just integer rakhna payeu but slug ta afnai ichhya anusar j pani rakhna paauxau jasle garda paxi kosaile kei product khojyo google ma bhane sidai hamro product display hos on the basis of slug....google le crawl garne bela hamro slug herxa ra user le search gareko keyword yedi hamro slug sanga matching xa bhane tyo result dekhauxa; so slug plays a better role in SEO than Id...

    # aba kun kun category lai display garne kun kun lai nagarne bhanne yo status le determine garxa
    status = models.CharField(choices=STATUS, max_length=100, blank=True)

    def __str__(self):
        return self.title  # yo bhaneko chi admin panel ma tyo database ko content k ko aadhar ma display garaune bhaneko
        # aba title ko basis ma tya content display hunxa admin panel ma

    # Category antargat ko items display garauna ko lagi ni yesto muni bana jastai function banauna parxa(url dynamic banauna yesto gareko hai..afnai marji anusar ko url banara ani slug pass garna sakiyo ni ta)
    def get_category_url(self):
        return reverse("ecomapp:category", kwargs={'slug': self.slug})


# For Sub Categories: 
class Subcategory(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(unique=True, max_length=100)
    status = models.CharField(choices=STATUS, max_length=100, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # aba Category ko sabai data yo Subcategory class ko category bhanne field le access garna pauxa because of ForeignKey
    # to know more about foreignkey see below im Item class

    def __str__(self):
        return self.title

    # Subcategory ko basis ma item display garauna ko lagi yesari mathi jastai euta function() banaune 
    def get_subcategory_url(self):
        return reverse("ecomapp:subcategory", kwargs={'slug': self.slug})



# Models For products and items:
class Item(models.Model):
    title = models.CharField(max_length=300)  # product ko name
    price = models.IntegerField()  # FloatField rakhe pani hunxa
    discounted_price = models.IntegerField(default=0)
    # default means kei narakhe si 0 set hunxa afai
    # cuz sabai product ma discount hunxa bhanne xaina ni ta; teso bela so edi tyo field empty xodna khojyo bhane error dinxa k ; so if we donot wish to give discount on certain product leave it as default= 0 or we can also do blank= True (tyo field required xaina hai bhaneko )

    # image = models.TextField()  # suru ma image lai TextField() nai rakdine k .... paxi yekai choti image file upload garne bela yo model bhari jaa jaa chinxa sab ma ImageField() set gardai jane ho
    image = models.ImageField(upload_to='media')
    
    # sakesamma image chi yesto choose garne jasko background white xax; ecommerce ma ta image le nai ho sabse thulo role khelne ; tei bhar image chi dami huna paro; for that halka photo editing skills bhako ramro

    # product ko description hunxa bhanne ni xaina ni ; so blank= True gardeko so that hamile tyo field lai empty xodda ni kei error nadyos
    description = models.TextField(blank=True)

    slug = models.CharField(max_length=300, unique=True)
    # slug means unique id of any product/item
    # j name rakhe ni hunxa but sakesamma choto mitho plaine english text raakhne for better SEO (tyo url link bhanda paxadi aune bhaneko slug ho)(tyo pura underscore; yo tyo nagarne)
    # link paxadi id matra rakhne garxa koi koi le but using slug is a good practice for better SEO

    # url dynamic banauda important role khelne slug le ho; so sakesamma yeslai dynamic banauna parxa
    # hamile kunai pani product ma click garim bhane ; browser ma certain euta link pathaunu parne hunxa so that yo id ko saman chi maile herna khojeko xu bhaninxa ; so tyo id sanga match hune saman chi database ma herera tya bata filter garera hamilai view garauna parne hunxa
    # so tesko lagi hami slug use garxau
    # unique = True means harek item ko lagi xuttai xuttai slug hunxa hai bhaneko ; euta item ma use gareko slug arko ma edi mistakely use garim bhane ta database ma usle khojda tei id ko duita item hunxa; so error dinxa

    # aba jastai kunai pani item stock ma xa ki xaina ; out of stock bhaisako ki; ho tesko bare ma ni xuttai fields banauna sakxau
    stock = models.CharField(max_length=100, choices=STOCK) 
    # choices is used to make dropdown
    # STOCK bhanne euta variable banaidiyeu ra mathi teslai define gardiyeu

    # aba hamile khali tyo grocery ko product matra ta rakdainau hola;
    # theme po tyo choose gareu ta ; tara further aru saman pani update garna paro re ( suppose laptop; mobile) bhane we should create another model
    brand = models.CharField(max_length=300)
    # labels bhaneko item hot, new or sale ma xa tesko lagi banako field
    labels = models.CharField(choices=Labels, max_length=100, blank=True)
    # blank = True bhanera rakhnai paro or default=1 rakhe ni hunxa; kinaki sadhai tyo item ma sale lageko hunxa or new item ho or hot item ho bhanne ni ta xaina ni; hamle kei narakhda pani django le error nadiyos bhannali blank =True gareko jasle garda tyo field compulsory xa bhanne xaina

    # for special_offer section(template ko last tira xa):
    # Item special offer ma parxa ki pardaina bhanna lai hami BooleanField linxau...BooleanField tick garne option dinxa k; special offer ma xa bhane tick garne which means True natra etikai xodesi it means False...
    special_offer = models.BooleanField(default=False)
    # by default chi untick nai hunu paryo so default  = False lageko

    # Kun kun product lai front page ma dekhaue tesko lagi ni euta field banam
    product_front_page = models.BooleanField(default=False)

    # Aba yo item kun category or subcategory ma parxa bhanera tya hamile dekhauna parne hola; tesko lagi mathi ko jun field xa teslai inherit garnu parxa
    # inherit garne bhannale hamile tya ForeignKey launa parne huna sakxa

    # ForeignKey provide a many-to-one relationship by adding a column to the local model to hold the remote value
    # Aba ForeignKey ko help le hami Category ra Subcategory ko bhaye bhar ko sabai data yesari Items bhitra access garna sakxau ra main kura chi kunai pani certain id ko through bata maile tyo data access garna pauxu
    # aba tala her na Category bhanne class ho; ra tesko bhaye bhar ko data Item class bhitra ko category bhanne field le handle gariraxa ; ra aba Category bhanne class ko sab data tyo category bhanne field ma auxa
    # Yo kina garinxa bhanda hamro pratyek thau ma jaa field hunxa tyo field haruko sankhya ghatos bhanera
    # So jaa pani kunai pani field lai dynamic banauna paryo bhane ; tesko sabai bhanda pailai euta tabele banaune ; ani kunai pani euta certain field lai chi tyo table ma bhako data lai tana or use gara bhanna ko lagi we use foreignkey

    # Requires two positional arguments ; the class to which the model is related and the on_delete attribute
    # on_delete = models.CASCADE bhanna le chi edi maile kunai pani items/products haru hataye bhanesi tyo sanga related category/subcategory pani hatera jaaos bhaneko  ; on_delete = True ni garna milxa

    # django ma afno default primary key bhaneko id bhanne hunxa ; foreign key le herne bhaneko main primary key nai ho ; primary key ko data lai chi foreignkey le lagera afno field ma lagera rakhxa

    # yesari foreign key bata tano bhane automatic dropdown menu milera aidinxa
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    # default= 1 narakhe ni hunxa
    # defualt = 1 rakhnu ko meaning chi hamile suru ma jun category banauxau (jastai yo case ma hamile Electonics bhanne category bana xam) ani tya kunai pani item add garda kheri tesko default category chi electronics hunxa tara teslai hamle majale change ni garna sakxau
    # tei bhayera suru ma jun category banauxau tyo chi item ko default cayegory hos bhannalai hamile default = 1  gareko

    # JASTAI hamile category bhanera yaa field ko name raakhe pani actual databse ma jane bhaenko chi euta category ko id hunxa (db browser ma gayera herna sakxas tya category_id bhanera baseko hunxa) ani tyo id ko aadhar ma chi hamile yaa further kaam haru garnu parne hunxa

    # Actual jun category bhanne model ma harek category ko jun unique id hunxa ni haina; ani aba hamile yaa item bhanne model ma edi foreign key lagayera mathi ko category lai tanya xau bhanesi yo item bhanne model ma jun category_id (ra subcategory_id lai ni same nai ho) bhanne baneko hunxa tesle line value bhanekai main category ko id ho; jastai maile main category ma electonics bhanne category banako the bhane ani manau ki tesko id 1 thyo re then aba ma jati electonics related product haru add garxu item bhanne model ma ; tesle by default sab ko id 1 linxa ....jasale garda hami lai paxi filtering garne bela ekdamai kaam lagxa...aba koi manxe le chahanxa ki electronics ko matra product display hos tyo page ma bhanesi elle k garxa bhane tyo main category ma electronics ko id kati xa herxa ani yaa item bhanne models ma tyo product ko category_id match garxa ani tei anusar tyo category bhako sab item tyo page ma display hunxa filtered bhayera....

    # Hamile kunai lai pani aile yaa primary key bhanera banaki xaina(i.e Primary key = True rakhekai xaina ra aile lai tyo jaruri ni xaina; id lai nai hami primary key bhanera mandinxau k dherai jasto case ma ) ; edi testo condition xa bhane jun field lai hamile foreign key anusar tanya xau tesko name ayera basne haina k(Electonics bhanera basne haina); rather tyo category ko id kati xa tyo ayera basne ho tyo item bhanne database ma ...ra field ko name yaa lekhda category bhaye ni tya item bhanne database model ma chi category_id bhanera baseko hunxa

    # note: id bhanne kura jaile ni 1 bata suru huxna ; cuz yo auto increment field ho ani jati hamile add gardai gayeu teti baddai janxa

    # Ra subcategory ko case ma ni same nai ho

    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

# paxi yo function call garnu parxa tya index.html ma so aile yaa banako jasle save price return garxa by subtracting real price with discounted price
    def specials_offers(self):
        return self.price - self.discounted_price
# yaa % form ma ni return garna sakinxa jastai eti% save garyo hai bhanne hunxa ki kunai kunai site ma ho testai functionality chiyo bhane just formula launa janna paryo

# note: models.py bhitra banako function haru praye jasto templates ma call garinxa

# for quick viewing of product:
    def get_item_url(self):
        return reverse("ecomapp:product", kwargs={'slug': self.slug})
# aba lets make a function ; jastai kunai pani item ma click garesi tesko url dine function banam...
# aba yaa return chi ali differently garinxa ; reverse ko through return garinxa ; elle hamro kwargs lai pass garxa
# pailo argument chi homeview bata product bhanne page ma reverse/redirect garne bhanera banako ; ra arko chi ma kwargs pass garxu as a dictionary ; jasko key or id  chi 'slug' xa ani value 'self.slug' pass garxu
# Yo agadi ko slug bhaneko chi maile urls.py ma banako thee ni tyo slug or id ho bhane paxadi ko slug chi database ma bhako items ko slug ho
# agadi ko slug le chi tyo hamro database ma bhayeko harek items ko slug lai k name diyera mathi url bar ma display garne bhanne bujhauxa ;
# slug matra lekhna painxa bhanne xaina...edi eta patti slug ko name id xa bhane uta ni id nai lina parxa urls.py ma
# edi yo get_item_urls bhanne function kunai template ma  call bhayo bhane chi yo appecom bhanne app ko product bhanne url ma chi database ma bhayeko tyo item ko slug lai pathauxa
# Url lai dynamic banauna yii steps garnai parxa ; nabhaye tya quick view ma click garo bhane vhayebhar ko item dekhinxa ; but hamlai ta tyo respective item matra dekhaunu xa ; so tesko lagi hamilai slug chinxa
# khas yaa gareko etti ho id pass garera arko page render hune functionality banako ho

# kwargs le k garne ho bhanne man maa laa xa hola?
# Yeta sun kunai pani class bhitra bata certain method lai (in this case get_item_url()) kuani na kunai thau (jastai yo case ma chi template ma) bata call garne banako xu re...ani tya chi kunai certain loop bhitra kunai pani link create gareko xu bhane tyo link bhitra bata maile yo function lai call garna pauxu...ani tesko lagi maile euta dictionary pass garnu parne hunxa jasma slug bhanne key ko value yesko original mathi bhako slug janxa as self.slug....ho tei bhara na ta ...click garda mathi url paxadi slug dekhinxa


# for cart:
    def add_to_cart(self):
        return reverse("ecomapp:add_to_cart",kwargs={'slug':self.slug})


# For Slider/ Carousel/Banner:
class Slider(models.Model):
    # tya slider ko image mathi aba majale afule j title lekhna ni payo
    title = models.CharField(max_length=300)
    image = models.TextField()

    rank = models.IntegerField()  # tyo tala ko golo golo ko lagi... slider ko tala patti ko golo golo jasma click garda xutta xuttai image show garxa... number le garda nai tyo effect layko ho k ....edi rank lai unique banaune ho bhane tesma unique attribute add garna ni milxa

    # suru ma webpage load bhayo re ; slider ko kun image lai first ma dekhaune bhanne status le determin garxa
    # slider ma dui status matra possible xan: one is Active and other is Default or Null
    # Edi kunai pani slider first ma visible garna paryo bhane chi tya tyo slider lai Active garauna parxa k
    # Ek choti ma euta matra slider active huna sakxa ra aru sabai baki slider bhaneko null or default hunxa

    status = models.CharField(choices=STATUS, max_length=100, blank=True)
    # choices ko kaam bhaneko dropdown generate garne ho
    # STATUS is a variable jasko value maile mathi tira define garya xu; nabhaye sidai yei bhitra ni tyo value (tuple inside tuple or list inside list) define garda hunxa
    # blank = True tetibela garne jaba kunai field unrequired hunxa ; not every fields are compulsory every time

    # tyo slider ko mathi patti (Big Save bhanera lekhya xa ni ho tesko lagi)
    upper_part = models.CharField(max_length=400, blank=True)
    # tyo slider ko tala patti (Get flat 10% cashback lekhya xa ni ho tesko lagi)
    lower_part = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return self.title


# For displaying Ad (display below products in template)
class Ad(models.Model):
    title = models.CharField(max_length=300)
    image = models.TextField()
    status = models.CharField(choices=STATUS, max_length=100, blank=True)
    upper_part = models.CharField(max_length=400, blank=True)
    lower_part = models.CharField(max_length=400, blank=True)
    middle_part = models.CharField(max_length=400, blank=True)
    # category ko aadhar ma filter garnu parne huna sakxa add lai ni tei bhayera ForeignKey layera taneko eslai ni
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title


# lets make contact form dynamic by creating a model:
# For contact :
class Contact(models.Model):
    name = models.CharField(max_length=400)

    subject = models.TextField()  # subject alikati thulo hunxa so use Textfield()

    email = models.CharField(max_length=400)
    # EmailField lage ni hunxa for better validation but aile lai Charfield nai lagam
    # Suruma euta field rakhya xa paxi arko change garna man lagyo bhane we can do it ; tara migration chi garna parxa compulsarily

    message = models.TextField()

    def __str__(self):
        return self.email


# # For owner's information in contact page:
class Information(models.Model):
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=300)
    fax = models.CharField(max_length=300)
    email = models.CharField(max_length=300)

    def __str__(self):
        return self.address

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    # cart ma jane item ko slug 
    slug = models.TextField()
    title = models.CharField(max_length=200,blank=True)
    image = models.TextField(blank=True)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0) 
    quantity = models.IntegerField(default=1)   
    checkout = models.BooleanField (default=False)                     

    def __str__(self):
        return self.user.username

    def delete_cart(self):
        return reverse("ecomapp:delete_cart",kwargs={'slug':self.slug})
