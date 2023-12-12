# 2. Get Banner 
# Bobot nilai: 0.5 poin 
# Metode: GET 
# URL: /home/banner 
# Response: 
# Key Example 
# data { 
#  "data": [ 
#  { 
#  "id": "uuid", 
#  "image": "/something/image.png", 
#  "title": "lorem ipsum blablabla" 
#  } 
#  ] 
# } 

# 3. Get Category 
# Bobot nilai: 0.5 poin 
# Metode: GET 
# URL: /home/category 
# Response: 
# Key Example 
# data { 
#  "data": [ 
#  { 
#  "id": "uuid", 
#  "image": "/something/image.png", 
#  "title": "Category A" 
#  } 
#  ] 
# } 




# HALAMAN INI UNTUK ROUTE HOME

from flask import Blueprint, request
from sqlalchemy import select, insert
from utils import run_query, t_categories, t_images, t_products, t_users
import uuid

home_bp = Blueprint("home", __name__, url_prefix="/home")

# [ENDPOINT 2 : Get Banner]
@home_bp.route("/banner", methods=["GET"])
def get_banner() :
    
    # STARTING PACK
    # DON'T DELETE :TARUH DI /home/banner 
    # CHEAT : input image for banner
    image_id=str(uuid.uuid1())
    user_id=str(uuid.uuid4())
    
    # check if banner.jpg not exist:
    banner_exists=run_query(select(t_images).where(t_images.c.image_url=="/assets/images/banner1.png"))
    if not banner_exists:
        run_query(insert(t_images).values({"id":image_id ,"image_url": "/assets/images/banner1.png", "title": "Thrifting Murah Berkualitas Hanya di FASHION CAMPUS"}), True)
        run_query(insert(t_images).values({"id":image_id ,"image_url": "/assets/images/banner2.png", "title": "Thrifting Murah Berkualitas Hanya di FASHION CAMPUS"}), True)
        run_query(insert(t_images).values({"id":image_id ,"image_url": "/assets/images/banner3.png", "title": "Thrifting Murah Berkualitas Hanya di FASHION CAMPUS"}), True)
        run_query(insert(t_images).values({"id":image_id ,"image_url": "/assets/images/ayu_tenan.png", "title": "Sorry Product Not Found"}), True)
    
    # sign up the seller/admin
    seller_exist=run_query(select(t_users).where(t_users.c.type=="seller"))
    if not seller_exist:
        run_query(insert(t_users).values({
            "user_id":user_id, 
            "name":"widho faisal", 
            "email":"widhofaisal26@gmail.com", 
            "phone_number":"088232571983", 
            "password":"@admin123", 
            "type":"seller", 
            "buyer_balance":0, 
            "seller_revenue":0, 
            "token":"Not Login",
            "address_name":"--seller--",
            "address_phone":"--seller--",
            "address":"--seller--",
            "city":"--seller--"
            }), True)
    
    
    # 
    # DON'T DELETE UNTIL THIS LINE !!!!
    # 
    result = run_query(select(t_images.c.id, t_images.c.image_url.label("image"), t_images.c.title).where(t_images.c.title=="Thrifting Murah Berkualitas Hanya di FASHION CAMPUS"))
    
    
    
    if result :
            
        return {"data":result}
        # return { "data": [{"id":result['id'], "image":result["image_url"], "title":result["title"]}]}

    else :
        return {"message" : "ERROR!!! : image for banner doesn't exist"}

# [ENDPOINT 3 : Get Category] ---> di table 'categories' hanya ada id dan title, jadi image di ambil dengan inner join dari table 'products'
@home_bp.route("/category", methods=["GET"])
def get_category() :
    
    categories = run_query(select(t_categories).where(t_categories.c.deleted==0))
    
    temp_result=[]
    for category in categories:
        result = run_query(select(t_products.c.images.label('image'), t_categories.c.id, t_categories.c.title).join(t_categories, t_categories.c.id==t_products.c.category).where(t_products.c.category==category['id']))
        if result:
            result=result[0]
        
            temp_result.append({
                "id":result['id'],
                "image":result['image'].split(" ")[0],
                "title":result['title'].upper(),
            })
    
    return {"data":temp_result}