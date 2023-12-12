from flask import Blueprint, request
from sqlalchemy import select, insert, update
from utils import run_query, t_products, t_categories, t_users, t_order, t_sold

profil_bp = Blueprint("profil_bp", __name__, url_prefix="/")




# [Endpoint 16 : User Details]
@profil_bp.route("/user", methods=["GET"])
def user_details():
    
    headers = request.headers.get('Authentication')
    result = run_query(select(t_users.c.name, t_users.c.email, t_users.c.phone_number).where(t_users.c.token==headers))
    
    
    return {
        "data" : result[0]
    }
    

# [Endpoint 17 : Change Shipping Address]
@profil_bp.route("/user/shipping_address", methods=["POST"])
def change_shipping_address():
    
    # get request body
    headers = request.headers.get('Authentication')
    shipping_address = request.get_json()
    print("=========", headers, request.get_json())
    # check if headers exist
    if headers and shipping_address:
        
        # check if header valid
        headers_valid = run_query(select(t_users).where(t_users.c.token==headers, t_users.c.type=="buyer"))
        if headers_valid:
            owner_id = headers_valid[0]['user_id']
            
            run_query(update(t_users).where(t_users.c.user_id==owner_id).values({
                "address_name":shipping_address['name'],
                "address_phone":shipping_address['phone_number'],
                "address":shipping_address['address'],
                "city":shipping_address['city'],
            }), True)
            
            return {"message" : "Change Shipping Address success"}
            
        else:
            return {"message" : "ERROR!!! can't change shipping address, headers not valid"}
    
    else:
        return {"message" : "ERROR!!! can't change shipping address, headers and parameters doesn't exist"}
    


# [Endpoint 18 : Top-up Balance]
@profil_bp.route("/user/balance", methods=["POST"])
def top_up_balance():
    
    amount = request.json.get('amount')
    headers = request.headers.get('Authentication')
    
    if amount and headers :
    
        # get curret buyer_balance
        result = run_query(select(t_users.c.buyer_balance).where(t_users.c.token==headers))
        new_buyer_balance = int(result[0]['buyer_balance']) + int(amount)
        
        # update buyer_balance
        run_query(update(t_users).where(t_users.c.token==headers).values({"buyer_balance":new_buyer_balance}), True)
        
        return {
            "message" : "Top Up balance success"
        }
    
    else:
        return {
            "message" : "ERROR!!! : can't top-up balance, amount or headers not valid",
            "details" : f"headers, amount = {headers}, {amount}"
        }
    
    
    
# [Endpoint 19 : Get User Balance]
@profil_bp.route("/user/balance", methods=["GET"])
def get_user_balance():
    
    headers = request.headers.get('Authentication')
    
    if headers:
        result = run_query(select(t_users.c.buyer_balance).where(t_users.c.token==headers))
        
        return {
            "data" : {
                "balance" : result[0]['buyer_balance']
            }
        }
        
    else :
        return {
            "message" : "ERROR!!! : can't get user balance, headers not valid"
        }
        
    
    
    
# [Endpoint 20 : User Orders]
@profil_bp.route("/user/order", methods=["GET"])
def user_orders():
    
    headers = request.headers.get('Authentication')
    
    if headers:
        
        # check if header valid
        headers_valid = run_query(select(t_users).where(t_users.c.token==headers, t_users.c.type=="buyer"))
        if headers_valid:
            
            result_master = run_query(select(t_order, t_users).join(t_users, t_order.c.owner_id==t_users.c.user_id).where(t_users.c.token==headers))
            # print("========",result_master)
            
            json_result=[]
            for result in result_master:
                # print("========",result)
                # temp_products : tampung all sold product
                temp_products=[]
                sold_id=result['sold_id'].split()
                for id in sold_id:
                    sold_detail = run_query(select(t_sold).where(t_sold.c.sold_id==id))
                    sold_detail=sold_detail[0]
                    
                    total_price=float(sold_detail['quantity'])*float(sold_detail['price'])
                    
                    temp_products.append(
                        {
                            "id":sold_detail['product_id'],
                            "details":{
                                "quantity":sold_detail['quantity'],
                                "size":sold_detail['size']
                            },
                            "price":total_price,
                            "image":sold_detail['images'].split()[0],
                            "name":sold_detail['product_name']
                        }
                    )
                
                temp_json={}
                temp_json={
                        "id":result['order_id'],
                        "created_at":result['created_at'],
                        "products":temp_products,
                        "shipping_method":result['shipping_method'],
                        "shipping_address":{
                            "name":result['address_name'],
                            "phone_number":result['address_phone'],
                            "address":result['address'],
                            "city":result['city']
                        }
                    }
                
                json_result.append(temp_json)   
            
            
            return {
                "data":json_result
            }
        
        return {
            "message" : "ERROR!!! : can't get user balance, headers not valid"
        }
        
    else :
        
        return {"message" : "ERROR!!! can't get user orders, headers doesn't exist"}
    