from flask import Blueprint, request, render_template
from sqlalchemy import insert, select, delete, update
from utils import run_query, t_images, t_categories, t_users, t_products, t_cart, t_order, t_sold
import uuid
import base64
import os
import jwt

admin_bp = Blueprint("admin_bp",__name__, url_prefix="/")


# [Endpoint 21 : Get Orders]
@admin_bp.route("/orders", methods=["GET"])
def get_orders():
    
    headers = request.headers.get('Authentication')
    sort_by=request.args.get('sort_by')
    page=request.args.get('page')
    page_size=request.args.get('page_size')
    
    # if headers and sort_by and page and page_size:
    if headers:
    
        # check if user with level admin and the token is exist
        headers_valid = run_query(select(t_users).where(t_users.c.type=="seller", t_users.c.token==headers))
        
        if headers_valid:
            
            result= run_query(select(t_order, t_users).join(t_users, t_order.c.owner_id==t_users.c.user_id))
            
            json_result=[]
            for row in result:
                
                # get total price
                total_price=0
                sold_id=row['sold_id'].split()
                for id in sold_id:
                    sold_detail = run_query(select(t_sold).where(t_sold.c.sold_id==id))
                    sold_detail=sold_detail[0]
                    
                    price=float(sold_detail['quantity'])*float(sold_detail['price'])
                    total_price+=price
                    
                temp_json={
                    "id":row['order_id'],
                    "user_name":row['buyer_name'],
                    "created_at":row['created_at'],
                    "user_id":row['owner_id'],
                    "user_email":row['email'],
                    "total":row['order_price']
                }
                
                json_result.append(temp_json)
            
            return {
                "data": json_result
            }

        else :    
            
            return {"message" : "ERROR!!! : Can't add, headers not valid"}
        
    else :
            
            return {"message" : "ERROR!!! : Can't add,  headers or request body not exist"}
        

# [Endpoint 22 : Create Product] - dengan asumsi FE ngasih BE image dalam bentuk base64
@admin_bp.route("/products", methods=["POST"])
def create_product():
    
    headers = request.headers.get('Authentication')
    
    # check if user with level admin and the token is exist
    headers_valid = run_query(select(t_users).where(t_users.c.type=="seller", t_users.c.token==headers))
    
    if headers_valid:
        
        product_owner = headers_valid[0]['name']
        owner_id = headers_valid[0]['user_id']

        product_name = request.json.get('product_name')
        condition = request.json.get('condition')
        category = request.json.get('category')
        description = request.json.get('description')
        images = request.json.get('images')
        price =  request.json.get('price')
        
        # generate jwt token
        product_id = jwt.encode({product_name:condition}, category, algorithm='HS256')
        
        # check if product is exist : unique by name, condition, category, deleted
        result = run_query(select(t_products).where(t_products.c.product_name==product_name, t_products.c.condition==condition, t_products.c.category==category, t_products.c.deleted=="0"))
        
        if result:
            
            return {"message": "ERROR!!! : Can't add, product already exist"}
        
        elif product_name and condition and category and description and images and price :
            
            stripped_product_name = product_name.replace(" ","_")
            image_url = ""
            i = 1
            image_id = str(uuid.uuid4())
            
                
            for data_images in images :
                
                # # SKENARIO 1 : bila ada gambar default + base64
                if data_images[:11] == "data:image/":
                    print("@@@@@@@@ masuk sini")
                    print("@@@@@@@@",data_images[:12])
                    
                    data_images=data_images.split("base64,")[1]
                    
                # # SKENARIO 2 : bila hanya ada gambar default
                # # SKENARIO 2 : bila hanya ada base64

                i=uuid.uuid1()
                    
                decoded_data=base64.b64decode((data_images))
                img_file = open(f'assets/images/{stripped_product_name}_{i}.png', 'wb')
                img_file.write(decoded_data)
                img_file.close()
                image_url += f'/assets/images/{stripped_product_name}_{i}.png '
                    
                # add images to table 'images'
                run_query(insert(t_images).values({"id":image_id ,"image_url": f'/assets/images/{stripped_product_name}_{i}.png', "title": product_name}), True)
                print("$$$$$$$ atas sini insert to t_images")   
                
                
            # add products data to database
            try:
                run_query(insert(t_products).values({"product_id":product_id, "product_owner": product_owner, "owner_id":owner_id ,"product_name":product_name, "description":description, "images":image_url, "condition":condition, "category":category, "ai_category":category, "price":price, "deleted":0}), True)
                
            except:
                run_query(delete(t_images).where(t_images.c.id==image_id), True)
                
            return {"message": "Product added"}
        
    
        else :
            
            return {"message" : "ERROR!!! : Can't add,  request body not valid"}
            
    
    else :    
        
        return {"message" : "ERROR!!! : Can't add, headers not valid"}
    



# [Endpoint 23 : Update Product] - dengan asumsi FE ngasih BE image dalam bentuk base64
@admin_bp.route("/products", methods=["PUT"])
def update_product():
    
    headers = request.headers.get('Authentication')
    
    # check if user with level admin and the token is exist
    headers_valid = run_query(select(t_users).where(t_users.c.type=="seller", t_users.c.token==headers))
    
    import json
    temp_request = json.loads(request.get_data())
    
    if headers_valid:
    
        product_name = temp_request['product_name']
        description = temp_request['description']
        condition = temp_request['condition']
        category = temp_request['category']
        product_id = temp_request['product_id']
        images = temp_request['images']
        price =  temp_request['price']
        # print("===========",product_id)
        # check if product is exist : unique by name, condition, category
        result = run_query(select(t_products).where(t_products.c.product_id==product_id))
        
        if not result :
            
            return {"message": "ERROR!!! : Can't update, product doesn't exist"}
            
        elif product_name and condition and category and description and product_id and images and price:
            
            # print("------",result[0]['images'])
            # delete_existing_images(result[0]['images'])
            
            
            stripped_product_name = product_name.replace(" ","_")
            
            print("--------- images= ",images)
            print("--------- result[0]['images']= ",result[0]['images'])
            
            image_url = ""
            image_id = str(uuid.uuid4())
            i = 1
            
            each_url_in_db = result[0]['images'].split()
            for each in each_url_in_db:
                print(f"------- each({each}) not in images({images})")
                if each not in images:
                    delete_existing_images(each)
                else:
                    image_url += each + " "
                    
            for data_images in images :
                
                # # SKENARIO 1 : bila ada gambar default + base64
                if data_images[:1] != "/":
                    
                    data_images=data_images.split("base64,")[1]
                    
                # # SKENARIO 2 : bila hanya ada gambar default
                # # SKENARIO 2 : bila hanya ada base64

                    i=uuid.uuid1()
                    
                 
                    decoded_data=base64.b64decode((data_images))
                    img_file = open(f'assets/images/{stripped_product_name}_{i}.png', 'wb')
                    img_file.write(decoded_data)
                    img_file.close()
                    image_url += f'/assets/images/{stripped_product_name}_{i}.png '
                    
                    # add images to table 'images'
                    run_query(insert(t_images).values({"id":image_id ,"image_url": f'/assets/images/{stripped_product_name}_{i}.png', "title": product_name}), True)
                    print("$$$$$$$ atas sini insert to t_images")
                    
            run_query(update(t_products).where(t_products.c.product_id==product_id).values({"images":image_url}),True)
            
            
            # add products data to database
            run_query(update(t_products).where(t_products.c.product_id==product_id).values({"product_name":product_name, "description":description, "condition":condition, "category":category, "price":price}), True)
            
            return {"message": "Product updated"}
            
        else :
            
            return {"message": "ERROR!!! : Can't update, request body not valid"}
        
        
    return {"message" : "ERROR!!! : Can't add, headers not valid"}
    
            

# [Endpoint 24 : Delete Product]
@admin_bp.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id) :
    
    headers = request.headers.get('Authentication')
    
    # check if user with level admin and the token is exist
    headers_valid = run_query(select(t_users).where(t_users.c.type=="seller", t_users.c.token==headers))
    
    if headers_valid:
    
        result = run_query(select(t_products.c.images).where(t_products.c.product_id==product_id))
        if not result :
            
            return {"message" : "ERROR!!! : product_id doesn't exist"}
        
        elif product_id :
            
            # execute delete images from assets/images
            # delete_existing_images(result[0]['images'])
            
            # execute delete product
            run_query(update(t_products).where(t_products.c.product_id==product_id).values({"deleted":1}), True)
        
            return {"message" : "Product Deleted"}
        
        else :
            
            return {"message" : "ERROR!!! : Request body not valid"}
        
    return {"message" : "ERROR!!! : Can't add, headers not valid"}
        

# [Endpoint 24.5 : Get Category] - This is additional endpoint
# @admin_bp.route("/categories", methods=["GET"])
# def get_category() :
    
#     headers = request.headers.get('Authentication')
    
#     # check if user with level admin and the token is exist
#     headers_valid = run_query(select(t_users).where(t_users.c.type=="seller", t_users.c.token==headers))
    
#     if headers_valid:
    
#         result = run_query(select(t_categories))
        
#         return {"data" : result}  
    
#     return {"message" : "ERROR!!! : Can't get category, headers not valid"}  






# HELPER METHOD for endpoint 23, 24
def delete_existing_images(images):
    images = images.split()
    for image in images:
        
        image_del=image
        if image[:1] != "/":
            image_del='/'+image
        run_query(delete(t_images).where(t_images.c.image_url==image_del), True)
        
        if image[:1] == "/":
            image = image[1:]
            
        os.remove(f"{image}")


# [Endpoint 25 : Create Category]
@admin_bp.route("/categories", methods=["POST"])
def create_category():
    
    headers = request.headers.get('Authentication')
    
    import json
    temp_request = json.loads(request.get_data())
    category_name = temp_request['category_name']
    
    # check if user with level admin and the token is exist
    headers_valid = run_query(select(t_users).where(t_users.c.type=="seller", t_users.c.token==headers))
    
    if headers_valid:
        
        # generate jwt token
        import jwt
        category_id = jwt.encode({"category_name":category_name}, headers, algorithm='HS256')
        
        result = run_query(select(t_categories).where(t_categories.c.title==category_name))
        
        if result :
            
            return {"message" : "ERROR!!! : Can't create category, category already exist"}
            
        else :
        
            run_query(insert(t_categories).values({"id": category_id, "title":category_name, "deleted":0, "ai_category":category_name}), True)
            return {"message" : "Category added"}
        
    return {"message" : "ERROR!!! : Can't get category, headers not valid"} 



# [Endpoint 26 : Update Category]
@admin_bp.route("/categories/<category_id>", methods=["PUT"])
def update_category(category_id):
    
    headers = request.headers.get('Authentication')
    
    import json
    temp_request=json.loads(request.get_data())
    category_name = temp_request['category_name']
    
    # check if user with level admin and the token is exist
    headers_valid = run_query(select(t_users).where(t_users.c.type=="seller", t_users.c.token==headers))
    
    if headers_valid:
        
        result = run_query(select(t_categories).where(t_categories.c.id==category_id))
        
        if not result:
            
            return {"message" : "ERROR!!! : category_id doesn't exist"}
            
        elif category_id and category_name:
            
            # update in table 'categories'
            run_query(update(t_categories).where(t_categories.c.id==category_id).values({"title":category_name}), True)
            
            return {"message" : "Category Updated"}
        
        else :
            
            return {"message" : "ERROR!!! : Can't update category, request body not valid"}

    return {"message" : "ERROR!!! : Can't update category, headers not valid"} 


# [Endpoint 27 : Delete Category]
@admin_bp.route("/categories/<category_id>", methods=["DELETE"])
def delete_category(category_id):
    
    headers = request.headers.get('Authentication')
    
    # check if user with level admin and the token is exist
    headers_valid = run_query(select(t_users).where(t_users.c.type=="seller", t_users.c.token==headers))
    
    if headers_valid:
        
        result = run_query(select(t_categories).where(t_categories.c.id==category_id))
        
        if result:
            
            run_query(update(t_categories).where(t_categories.c.id==category_id).values({"deleted":1}), True)
            
            return {"message" : "Category Deleted"}
        
        else :
            
            return {"message" : "ERROR!!! : Can't delete category, 'category_id' doesn't exist"}
        
    return {"message" : "ERROR!!! : Can't update category, headers not valid"} 


# [Endpoint 28 : Get Total Sales]
@admin_bp.route("/sales", methods=["GET"])
def get_total_sales():
    
    headers = request.headers.get('Authentication')
    
    # check if user with level admin and the token is exist
    headers_valid = run_query(select(t_users).where(t_users.c.type=="seller", t_users.c.token==headers))
    
    if headers_valid:
    
        result = run_query(select(t_users).where(t_users.c.token==headers))
        result = result[0]['seller_revenue']
        
        return {
            "data" : {
                "total" : result
            }
        }

    return {"message" : "ERROR!!! : Can't get sales, headers not valid"} 

