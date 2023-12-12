from flask import Blueprint, request
from sqlalchemy import select, insert, update, join, delete
from utils import run_query, t_products, t_categories, t_users, t_cart, t_order, t_sold
import uuid

cart_bp = Blueprint("cart_bp", __name__, url_prefix="/")

# [Endpoint 11 : Get Users Cart]
@cart_bp.route("/cart", methods=["GET"])
def get_users_carts():
    
    # get request body
    headers = request.headers.get('Authentication')
    
    # check if headers exist
    if headers:
        
        # check if header valid
        headers_valid = run_query(select(t_users).where(t_users.c.token==headers))
        if headers_valid:
            owner_id = headers_valid[0]['user_id']
            temp_json=[]
            
            # retrieve data from table t_cart
            result = run_query(select(t_cart, t_products).join(t_products, t_cart.c.product_id==t_products.c.product_id).where(t_cart.c.owner_id==owner_id))
            for item in result:
                print("=====",item)
                temp_json.append({
                    "id" : item['cart_id'],
                    "details": {"quantity":item['quantity'], "size":item['size']},
                    "price" : item['price'],
                    "image" : item['images'].split()[0],
                    "name" : item['product_name']
                })
            
            return {
                "data" : temp_json
            }
            # retrieve data from table t_products
            
        else:
            return {"message":"ERROR!!! can't get users cart, haeders not valid"}    
        
    else :
        return {"message":"ERROR!!! can't get users cart, headers not exist"}
        
      
      

# [Endpoint 12 : Get User's Shipping Address]
@cart_bp.route("/user/shipping_address", methods=["GET"])
def get_users_shipping_address():
    
    # get request body
    headers = request.headers.get('Authentication')
    
    # check if headers exist
    if headers:
        
        # check if header valid
        headers_valid = run_query(select(t_users).where(t_users.c.token==headers))
        if headers_valid:
            owner_id = headers_valid[0]['user_id']
            
            result = run_query(select(t_users).where(t_users.c.user_id==owner_id))
            
            temp_json=[]
            for row in result:
                temp_json.append({
                    "id":row['user_id'],
                    "name":row['address_name'],
                    "phone_number":row['address_phone'],
                    "address":row['address'],
                    "city":row['city']
                })
            
            return {
                "data" : temp_json[0]
            }
        
        else:
            return {"message":"ERROR!!! can't get users cart, headers not valid"}   
        
    else :
        return {"message":"ERROR!!! can't get users cart, headers not exist"}        
  
        

# [Endpoint 13 : Get Shipping Price]
@cart_bp.route("/shipping_price", methods=["GET"])
def get_shipping_price():
    
    # get request body
    headers = request.headers.get('Authentication')
    
    # check if headers exist
    if headers:
        
        # check if header valid
        headers_valid = run_query(select(t_users).where(t_users.c.token==headers))
        if headers_valid:
            
            owner_id = headers_valid[0]['user_id']
            # temp_json=[]
            
            # retrieve data from table t_cart
            result = run_query(select(t_cart, t_products).join(t_products, t_cart.c.product_id==t_products.c.product_id).where(t_cart.c.owner_id==owner_id))
            
            total_harga=0
            for row in result:
                total_harga+=int(row['price'])*int(row['quantity'])
                
            # get regular price
            regular_price=0
            if total_harga<200000:
                regular_price=0.15*total_harga
            else:
                regular_price=0.2*total_harga 
                
            # get next day price
            nextday_price=0
            if total_harga<300000:
                nextday_price=0.2*total_harga
            else:
                nextday_price=0.25*total_harga
            
            return {
                "data" : [
                    {
                        "name":"regular",
                        "price":regular_price
                    },
                    {
                        "name":"next day",
                        "price":nextday_price
                    }
                ]
            }
                
        
        else:
                return {"message":"ERROR!!! can't get users cart, headers not valid"}    
        
    else :
        return {"message":"ERROR!!! can't get users cart, headers not exist"}    
        
        
        
        
# [Endpoint 14 : Create Order]
@cart_bp.route("/order", methods=["POST"])
def create_order():
    
    # get request body
    headers = request.headers.get('Authentication')
    shipping_method = request.json.get('shipping_method')
    shipping_address = request.json.get('shipping_address')
    
    # check if headers exist
    if headers and shipping_method and shipping_address:
        
        # check if header valid
        headers_valid = run_query(select(t_users).where(t_users.c.token==headers))
        if headers_valid:
            
            owner_id = headers_valid[0]['user_id']
            
            # retrieve data from table t_cart
            result = run_query(select(t_cart, t_products).join(t_products, t_cart.c.product_id==t_products.c.product_id).where(t_cart.c.owner_id==owner_id))
            
            # get shipping price data using endpoint 13
            import requests
            response = requests.get("http://127.0.0.1:5000/shipping_price", headers={"Authentication":headers})
            response=response.json()
            
            # get lower shipping method string
            shipping_method = shipping_method.lower()
            
            # get shipping price according to shipping method
            shipping_price=0
            for row in response['data']:
                if row['name']==shipping_method :
                    shipping_price=row['price']
            
            # error handler
            if shipping_price==0:
                return {"message" : "ERROR!!! request body not valid or cart is empty"}
            
            # get total harga
            total_harga=0
            for row in result:
                total_harga+=int(row['price'])*int(row['quantity'])
                
            # total harga + shipping price
            checkout_harga = shipping_price+total_harga
            
            current_balance = float(headers_valid[0]['buyer_balance'])
            # check apakah buyer_balance cukup
            if current_balance < checkout_harga:
                return {
                    "message" : "ERROR!!! you not have enough balance, need more",
                    "details" : {
                        "current_balance" : current_balance,
                        "checkout_harga" : checkout_harga,
                        "needs more" : (current_balance-checkout_harga)*(-1)
                    }
                }
            
            else :
                temp_sold_id=[]
                
                # mengisi tabel sold
                res=result
                for row in res:
                    sold_id=str(uuid.uuid1())
                    
                    run_query(insert(t_sold).values({
                        "sold_id":sold_id, 
                        "product_id":row['product_id'], 
                        "quantity":row['quantity'],
                        "size":row['size'],
                        "product_name":row['product_name'],
                        "price":row['price'],
                        "images":row['images']
                    }), True)
                    
                    temp_sold_id.append(sold_id)
                print("-------- sukses isi tabel sold")
                
                # mengisi tabel order
                res=result
                sold_id_for_t_order=" "
                sold_id_for_t_order=sold_id_for_t_order.join(temp_sold_id)
                
                order_id=str(uuid.uuid4())
                    
                run_query(insert(t_order).values({
                    "order_id":order_id,
                    "shipping_method":shipping_method,
                    "owner_id":res[0]['owner_id'],
                    "buyer_name":res[0]['cart_owner'],
                    "sold_id":sold_id_for_t_order,
                    "order_price":checkout_harga
                }), True)
                print("-------- sukses isi tabel order")
                
                new_balance = current_balance-checkout_harga
                
                # mengurangi balance user/buyer
                run_query(update(t_users).where(t_users.c.token==headers).values({"buyer_balance":new_balance}), True)
                
                
                # mengupdate seller_revenue
                current_reveneu = run_query(select(t_users).where(t_users.c.type=="seller"))
                new_revenue = float(current_reveneu[0]['seller_revenue'])+total_harga
                
                run_query(update(t_users).where(t_users.c.type=="seller").values({"seller_revenue":new_revenue}), True)
                
                # menghapus cart user/buyer
                run_query(delete(t_cart).where(t_cart.c.owner_id==owner_id), True)
            
                return {"message" : "Order Success"}
            
        else :
            return {"message":"ERROR!!! can't get users cart, headers not valid"}    
        
    else :
        return {"message":"ERROR!!! can't get users cart, headers and parameters doesn't exist"} 




# [Endpoint 15 : Delete Cart Item]
@cart_bp.route("/cart/<cart_id>", methods=["DELETE"])
def delete_cart_item(cart_id):
    
    # get headers
    headers = request.headers.get('Authentication')
    
    # check if request exist
    if cart_id and headers:
        headers_valid = run_query(select(t_users).where(t_users.c.token==headers))
        cart_valid=run_query(select(t_cart).join(t_users, t_cart.c.owner_id==t_users.c.user_id).where(t_cart.c.cart_id==cart_id, t_users.c.token==headers))
        print(cart_valid)
        # check if cart id valid
        if headers_valid and cart_valid:
            
            # delete cart item by cart_id
            run_query(delete(t_cart).where(t_cart.c.cart_id==cart_id), True)
            
            return {"message" : "Cart deleted"}
        
        elif not headers_valid:
            return {"message" : "ERROR!!! can't delete cart, headers not valid"}
        
        elif not cart_valid:
            return {"message" : "ERROR!!! can't delete cart, cart_id not valid"}
            
        
    else:
        return {"message" : "ERROR!!! can't delete cart, headers and parameters doesn't exist"}
    
    
    
    
# [Endpoint 17 : Change Shipping Address]
@cart_bp.route("/user/shipping_address", methods=["PUT"])
def change_shipping_address():
    
    # get request body
    headers = request.headers.get('Authentication')
    shipping_address = request.json.get('shipping_address')
    
    # check if headers exist
    if headers and shipping_address:
        
        # check if header valid
        headers_valid = run_query(select(t_users).where(t_users.c.token==headers))
        if headers_valid:
            owner_id = headers_valid[0]['user_id']
            
            run_query(update(t_order).where(t_order.c.owner_id==owner_id).values({
                "name":shipping_address['name'],
                "phone_number":shipping_address['phone_number'],
                "address":shipping_address['address'],
                "city":shipping_address['city'],
            }), True)
            
            return {"message" : "Change Shipping Address Success"}
            
        else:
            return {"message" : "ERROR!!! can't change shipping address, headers not valid"}
    
    else:
        return {"message" : "ERROR!!! can't change shipping address, headers and parameters doesn't exist"}