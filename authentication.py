from flask import Blueprint, request
from utils import run_query, t_users
from sqlalchemy import insert, select, update
import uuid

signup_bp = Blueprint("sign-up", __name__, url_prefix="/sign-up")
signin_bp = Blueprint("sign-in", __name__, url_prefix="/sign-in")

# [Endpoint 4 : Sign-up]
@signup_bp.route("", methods=["POST"])
def sign_up():
    
    name = request.json["name"]
    email = request.json["email"]
    phone_number = request.json["phone_number"]
    password = request.json["password"]
    address_name="address_name DEFAULT"
    address_phone="address_phone DEFAULT"
    address="address DEFAULT"
    city="city DEFAULT"
    
            
    result = run_query(select(t_users).where(t_users.c.email==email, t_users.c.type=="buyer"))
    
    if result :
        
        return {"message" : "ERROR!!! : Can't sign up, user (buyer or seller) already exist"}
    
    else :
    
        user_id = str(uuid.uuid1())
        
        run_query(insert(t_users).values({
            "user_id":user_id, 
            "name":name, "email":email, 
            "phone_number":phone_number, "password":password, 
            "type":"buyer", 
            "buyer_balance":0, 
            "seller_revenue":0, 
            "token":"Not Login",
            "address_name":address_name,
            "address_phone":address_phone,
            "address":address,
            "city":city
            }), True)
        
        return {"message" : "success, user created"}


# [Endpoint 5 : Sign-in]
@signin_bp.route("", methods=["POST"])
def sign_in():
    
    email=request.json["email"]
    password=request.json["password"]
    
    print(email,password)
    
    result = run_query(select(t_users).where(t_users.c.email==email, t_users.c.password==password))
    
    # check if user already sign-up
    if result :
            
        result=result[0]
            
        # generate jwt token
        import jwt
        token = jwt.encode({"email":email}, password, algorithm='HS256')
            
        # update token column in table users
        run_query(update(t_users).where(t_users.c.email==email, t_users.c.password==password).values({"token":token}), True)
            
        # statement to return
        user_information = {"name":result["name"], "email":result["email"], "type":result["type"]}
            
        return {"user_information":user_information, "token":token, "message":"Login success"}

            
    else :
        return {"message" : "ERROR!!! : Can't sign in, email or password incorrect"}