from flask import Blueprint, request
from sqlalchemy import select, insert, update
from utils import run_query, t_products, t_categories, t_users, t_cart
import uuid

product_detail_bp = Blueprint("product_detail_bp", __name__, url_prefix="/")

# [Endpoint 9 : Get Product Details]
@product_detail_bp.route("products/<id>", methods=["GET"])
def get_product_details(id):
    
    result = run_query(select(t_products).where(t_products.c.product_id==id))
    
    if result:
        result = result[0]
        
        category_name = run_query(select(t_categories).where(t_categories.c.id==result['category']))
        category_name = category_name[0]['title']
        
        return {
            "data" : {
                "id" : result['product_id'], 
                "title" : result['product_name'],
                "size" : ["S", "M", "L"],
                "product_detail" : result['description'],
                "price" : result['price'],
                "images_url" : result['images'].split(),
                "category_id" : result['category'],
                "category_name" : category_name
            }
        }
    
    else :
        return {"message" : "ERROR!!! : Can't get product detail, id doesn't exist"}
    
    
# [Endpoint 10 : Add to cart]
@product_detail_bp.route("/cart", methods=["POST"])
def add_to_cart():
    
    # is all request body exist
    headers = request.headers.get('Authentication')
    product_id = request.json.get('id')
    quantity = request.json.get('quantity')
    size = request.json.get('size')
    
    if headers and id and quantity and size:
        # is headers valid
        headers_valid = run_query(select(t_users).where(t_users.c.type=="buyer", t_users.c.token==headers))
        
        if headers_valid:
            # get user name
            cart_owner = headers_valid[0]['name']
            owner_id = headers_valid[0]['user_id']
            
            # if item exist in cart --> increase quantity . unique by item_id and size
            item_in_cart = run_query(select(t_cart).where(t_cart.c.product_id==product_id, t_cart.c.size==size))
            
            # check if product_id exist in t_products
            product_id_exist=run_query(select(t_products).where(t_products.c.product_id==product_id))
            if product_id_exist:
                
                if item_in_cart :
                    current_quantity=item_in_cart[0]['quantity']
                    new_quantity=float(current_quantity)+float(quantity)
                    
                    # increase quantity to existing item in cart
                    run_query(update(t_cart).where(t_cart.c.product_id==product_id, t_cart.c.size==size).values({
                        "quantity":new_quantity
                    }), True)
                    
                    return {"message" : "Increase item quantity in cart success"}
                
                else:
                    cart_id = str(uuid.uuid1())
                    
                    # add new item to cart
                    run_query(insert(t_cart).values({
                        "cart_id":cart_id, 
                        "cart_owner":cart_owner,
                        "owner_id":owner_id,
                        "product_id":product_id, 
                        "quantity":quantity,
                        "size":size
                        }), True)
                    
                    return {"message" : "Item added to cart success"}
                
            else:
                return {"message" : "ERROR!!! : Can't add to cart, product_id not valid (not exist in t_products)"}
            
        else :
            return {"message" : "ERROR!!! : Can't add to cart, headers not valid"}
        
    else :
        return {"message" : "ERROR!!! : Can't add to cart, request body is missing"}
    
    
    
    # else add item to cart
    