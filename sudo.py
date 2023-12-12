from flask import Blueprint, request, render_template
from sqlalchemy import insert, select, delete, update
from utils import (
    run_query,
    t_images,
    t_categories,
    t_users,
    t_products,
    t_cart,
    t_order,
    t_sold,
)
import uuid
import requests
import base64
import json

sudo_bp = Blueprint("sudo_bp", __name__, url_prefix="/")


@sudo_bp.route("/starter-pack", methods=["GET"])
def starter_pack_list():

    # AUTO INPUT CATEGORIES
    categories_title = [
        "tshirt top",
        "trouser",
        "pullover",
        "dress",
        "coat",
        "sandals",
        "shirt",
        "sneaker",
        "bag",
        "ankle boot",
        "hat",
    ]
    
    # ini headers seller/admin
    headers = run_query(select(t_users).where(t_users.c.type=="seller"))
    if headers:
        headers = headers[0]['token']
        headers={"Authentication":headers}

    print("=====1")
    print(headers)
    response1 = []
    for title in categories_title:
        response=requests.post("http://127.0.0.1:5000/categories",json={"category_name": title},headers=headers)
        response1.append(response.text)
    print("=====CATEGORY CLEAR")



    # AUTO INPUT PRODUCTS

    
    # ini daftar nama produk
    temp_productName = [
        ["T-Shirt Red Velvet", "T-Shirt White Brave", "T-Shirt Black Tatto"],
        ["Trousser White Cobra", "Trousser Gray Amaze", "Trousser Pure Black"],
        ["Pullover White Snow", "Pullover Black Wolf", "Pullover Grey Brave"],
        ["Dress Long Brave", "Dress Red Blood", "Dress Batik Indo"],
        ["Coat Snow Warm", "Coat Mantel Gajah", "Coat Bulu Wolf"],
        ["Sandal Brown Lazy", "Sandal Black Macho", "Sandal Tiger Hood"],
        ["Shirt Bapak Kampung", "Shirt Koko Muslim", "Shirt Muscle Superman"],
        ["Sneaker Grey Running", "Sneaker White Mall", "Sneaker ABC Combine"],
        ["Bag White Campus", "Bag Main Perform", "Bag Solid Metalica"],
        ["Ankle Boat Arcimedes", "Ankle Boat Primadona", "Ankle Boat Mamaia"],
        ["Hat of Heart", "Hat Hati Hati", "Hat Avocado Guava"],
    ]

    # ini daftar harga
    temp_price = [
        "75000",
        "90000",
        "80000",
        "110000",
        "150000",
        "60000",
        "45000",
        "145000",
        "200000",
        "200000",
        "25000",
    ]
    
    # get base64 data
    f=open('assets/hasil.json')
    data_images=json.load(f)
    
    # looping untuk insert data lewat request "http://127.0.0.1:5000/products"
    response2=[]
    for i in range(len(categories_title)): #range ini berdasarkan jumlah category
        
        for ii in range(3): #range ini berdasarkan jumlah produk per category nya
            
            # random condition
            condition = "used"
            if ii % 2 == 0: condition = "new"
            
            # get category id
            category_id=run_query(select(t_categories).where(t_categories.c.title==categories_title[i]))
            if category_id:
                category_id=category_id[0]['id']
            
            # menampung json untuk request
            json_final = {
                "product_name":temp_productName[i][ii],
                "condition":condition,
                "category":category_id,
                "description":f"This is the {temp_productName[i][ii]}. Quality materials and competitive prices.",
                "images":data_images[i][ii],
                "price":temp_price[i]
            }
            
            # print(json_final)


            response=requests.post("http://127.0.0.1:5000/products", json=json_final, headers=headers)
            response2.append(response.text)
    print("=========PRODUCTS CLEAR")  
            
    return{"message":"Success auto input","categories":response1,"products":response2}


@sudo_bp.route("/starter-pack/input-data", methods=["GET"])
def input_data():

    user_login = run_query(
        select(t_users).where(
            t_users.c.type == "seller", t_users.c.token != "Not Login"
        )
    )
    if not user_login:
        return {"message": "can't use this features, login as admin first"}

    empty_category = run_query(select(t_categories))
    empty_product = run_query(select(t_products))
    if empty_category and empty_product:
        return {"message": "there is still exist categories and products"}

    else:

        headers = {
            "Authentication": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndpZGhvZmFpc2FsMjZAZ21haWwuY29tIn0.CQsY36m6sFdq7iyPULQ38TwDA6oU2u_yCBku2Rcd83w"
        }

        # input 10 category to t_categories
        temp_categories_json = [
            "tshirt",
            "trouser",
            "pullover",
            "dress",
            "coat",
            "sandal",
            "shirt",
            "sneaker",
            "bag",
            "ankle boot",
            "hat",
        ]

        # # generate jwt token
        import jwt

        temp_category_jwt = []
        for item in temp_categories_json:
            category_id = jwt.encode(
                {"category_name": item}, headers["Authentication"], algorithm="HS256"
            )
            temp_category_jwt.append(category_id)

        temp_response_input_category = []
        for row in temp_categories_json:

            category_exist = run_query(
                select(t_categories).where(t_categories.c.title == row)
            )
            if not category_exist:
                response = requests.post(
                    "http://127.0.0.1:5000/categories",
                    json={"category_name": row},
                    headers=headers,
                )
                temp_response_input_category.append(response.json())

        # input product to t_products
        temp_product_name = [
            ["T-Shirt Red Velvet", "T-Shirt White Brave", "T-Shirt Black Tatto"],
            ["Trousser White Cobra", "Trousser Gray Amaze", "Trousser Pure Black"],
            ["Pullover White Snow", "Pullover Black Wolf", "Pullover Grey Brave"],
            ["Dress Long Brave", "Dress Red Blood", "Dress Batik Indo"],
            ["Coat Snow Warm", "Coat Mantel Gajah", "Coat Bulu Wolf"],
            ["Sandal Brown Lazy", "Sandal Black Macho", "Sandal Tiger Hood"],
            ["Shirt Bapak Kampung", "Shirt Koko Muslim", "Shirt Muscle Superman"],
            ["Sneaker Grey Running", "Sneaker White Mall", "Sneaker ABC Combine"],
            ["Bag White Campus", "Bag Main Perform", "Bag Solid Metalica"],
            ["Ankle Boat Arcimedes", "Ankle Boat Primadona", "Ankle Boat Mamaia"],
            ["Hat of Heart", "Hat Hati Hati", "Hat Avocado Guava"],
        ]

        temp_category = [
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYXRlZ29yeV9uYW1lIjoidHNoaXJ0dG9wIn0.0r2WZjyB-nSuQTileaOOAjgSz6J-QjWHmOdGtSF4QrY",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYXRlZ29yeV9uYW1lIjoidHJvdXNzZXIifQ.RHs24i4v8SfGZiyjgwtyv92GCmva1gAWHXWY-kyJ3Vg",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYXRlZ29yeV9uYW1lIjoicHVsbG92ZXIifQ.d9FcFotlYlOI8SOXdU5upJVRKkHiiYJ2dnUXAMDG8KI",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYXRlZ29yeV9uYW1lIjoiZHJlc3MifQ.GZ8W_3P1HMEfvOFgBtCFKIbeEMxWUdcAypfLjN7qR4I",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYXRlZ29yeV9uYW1lIjoiY29hdCJ9.jFVFvYxvhyWdSWp9y4fucIeSXhZCXyE_OgKRh3cTeMc",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYXRlZ29yeV9uYW1lIjoic2FuZGFsIn0.eEiR8KpMXyWa9X0aHvkUNpJvdbJnzofMw-_T97IKuco",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYXRlZ29yeV9uYW1lIjoic2hpcnQifQ.9-9S8QdezOHZChitF17weftwzWj3AD3ykBYGy884Aek",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYXRlZ29yeV9uYW1lIjoic25lYWtlciJ9.DQ-9DVPrGERSohfYSb4Xaad8Mv-aQYTxGZiIk5Amzig",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYXRlZ29yeV9uYW1lIjoiYmFnIn0.EXWCSe2X_5clEgXzWiFaV8zfgSerjnJo1pbV8TSzj54",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYXRlZ29yeV9uYW1lIjoiYW5rbGUgYm9hdCJ9.okat-NkmkOA5P1UXeTrxD9xygCGlQIZgyoQEer2kG-c",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjYXRlZ29yeV9uYW1lIjoiaGF0In0.8UIAxvUCZHNyT3Z9E0MAl74IqPINEIStMuzzIyJvGFk",
        ]

        temp_price = [
            "75000",
            "90000",
            "80000",
            "110000",
            "150000",
            "60000",
            "45000",
            "145000",
            "200000",
            "200000",
            "25000",
        ]

        temp_base64 = []

        for folder in range(11):

            # generate description by each product's name
            temp_description = []
            for first in range(11):
                each_category = []
                for second in range(3):
                    description = f"This is the {temp_product_name[first][second]}. Quality materials and competitive prices."
                    each_category.append(description)
                temp_description.append(each_category)

            each_category2 = []
            for first in range(1, 7):

                each_product = []
                for second in range(1, 3):

                    url = f"assets/sudo_products/{folder}/{first}-{second}.jpg"
                    with open(url, "rb") as img_file:
                        my_string = base64.b64encode(img_file.read())
                        each_product.append(str(my_string.decode()))
                each_category2.append(each_product)
            temp_base64.append(each_category2)

        # return {"a":temp_description}

        json_result = []
        for i in range(11):
            for ii in range(6):

                condition = "new"
                if ii % 2 == 0:
                    condition = "used"

                temp_result = {}
                temp_result = {
                    "product_name": temp_product_name[i][ii],
                    "condition": condition,
                    "category": temp_category_jwt[i],
                    "description": temp_description[i][ii],
                    "images": temp_base64[i][ii],
                    "price": temp_price[i],
                }
                json_result.append(temp_result)

        # temp_response_input_product=[]
        for each in json_result:

            stripped_product_name = each["product_name"].replace(" ", "_")

            image_url = ""
            for data_images in each["images"]:

                i = uuid.uuid1()
                image_id = str(uuid.uuid4())

                decoded_data = base64.b64decode((data_images))
                img_file = open(f"assets/images/{stripped_product_name}_{i}.png", "wb")
                img_file.write(decoded_data)
                img_file.close()
                image_url += f"/assets/images/{stripped_product_name}_{i}.png "

                # add images to table 'images'
                run_query(
                    insert(t_images).values(
                        {
                            "id": image_id,
                            "image_url": f"/assets/images/{stripped_product_name}_{i}.png",
                            "title": each["product_name"],
                        }
                    ),
                    True,
                )

            # generate jwt token
            product_id = jwt.encode(
                {each["product_name"]: each["condition"]},
                each["category"],
                algorithm="HS256",
            )

            run_query(
                insert(t_products).values(
                    {
                        "product_id": product_id,
                        "product_owner": "widho faisal",
                        "owner_id": "f010189f-5f0f-4b9d-8ad3-40b9d760da65",
                        "category": each["category"],
                        "condition": each["condition"],
                        "description": each["description"],
                        "images": image_url,
                        "price": int(each["price"]),
                        "product_name": each["product_name"],
                        "deleted": 0,
                    }
                ),
                True,
            )

        #     import json
        #     response2 = requests.post("http://127.0.0.1:5000/products", json=each_final, headers={'Authentication':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndpZGhvZmFpc2FsMjZAZ21haWwuY29tIn0.CQsY36m6sFdq7iyPULQ38TwDA6oU2u_yCBku2Rcd83w'})
        #     temp_response_input_product.append(response2.text)
        #     # print("------------------",response)

        # response_final = requests.post("http://127.0.0.1:5000/products", json=json_result[0], headers={"Authentication":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndpZGhvZmFpc2FsMjZAZ21haWwuY29tIn0.CQsY36m6sFdq7iyPULQ38TwDA6oU2u_yCBku2Rcd83w"})
        # response = requests.get("http://127.0.0.1:5000/home/banner")
        # return
        return {"message": "success auto input categories and products"}

        # return {"product_name":temp_product_name, "category":temp_category ,"base64":temp_base64, "description":temp_description}
        # return temp_response_input_category, temp_response_input_product


# [ ROUTE HELPER ]


@sudo_bp.route("/alldb", methods=["GET"])
def get_all_table():

    # DONT DELETE
    #
    # input banner and sign-up admin
    response = requests.get("http://127.0.0.1:5000/home/banner")
    response = response.json()
    #
    # DONT DELETE

    # remove DB if already exists
    # db_name = "FinalProject.db"
    # if os.path.isfile(db_name):
    #     # os.remove(db_name)
    #     print("db ada================")

    # CHEAT : input image for helper images
    # run_query(insert(t_images).values({"id":image_id, "image_url":"/assets/images/T-shirt.png", "title":"The Helper Image"}), True)

    # run_query(delete(t_products).where(t_products.c.product_id=="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJLYW9zIFNvYmVrIjoibmV3In0.Akd7SACyNI0M8Ua3wxLMgExvxk8tzL3F7LyHHdbmv6Y"), True)
    # run_query(delete(t_images).where(t_images.c.title=="Aerostreet Bolong"), True)
    # run_query(delete(t_users), True)
    # run_query(delete(t_sold), True)
    # run_query(delete(t_order), True)
    # run_query(update(t_images).where(t_images.c.image_url==""))
    # run_query(delete(t_images), True)

    # run_query(delete(t_products), True)
    # run_query(delete(t_images), True)

    data_images = run_query(select(t_images))
    data_categories = run_query(select(t_categories))
    data_users = run_query(select(t_users))
    data_products = run_query(select(t_products))
    data_cart = run_query(select(t_cart))
    data_order = run_query(select(t_order))
    data_sold = run_query(select(t_sold))

    # print(data_products)

    return render_template(
        "for_admin_alldb.html",
        data_images=data_images,
        data_categories=data_categories,
        data_users=data_users,
        data_products=data_products,
        data_cart=data_cart,
        data_order=data_order,
        data_sold=data_sold,
    )


@sudo_bp.route("/jajal", methods=["GET"])
def get_jajal():

    nama=request.json.get('nama')

    return {"result": nama, "method":request.method}
