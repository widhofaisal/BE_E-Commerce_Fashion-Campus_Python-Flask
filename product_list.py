from flask import Blueprint, request
from sqlalchemy import select
from utils import run_query, t_products, t_categories

product_list_bp = Blueprint("product_list_bp", __name__, url_prefix="/")

# [Endpoint 6 : Get Product List]
@product_list_bp.route("products", methods=["GET"])
def get_product_list():
    
    page = request.args.get('page')
    page_size = request.args.get('page_size')
    sort_by = request.args.get('sort_by')
    category = request.args.get('category')
    price = request.args.get('price')
    condition = request.args.get('condition')
    product_name = request.args.get('product_name')
    
    print("/////",condition)
    result=[]
    
    if category and product_name:
        print("==========",product_name)
        
        for each in category.split(","):
            # print("----------",each)
            
            temp = run_query(
                select(
                    t_products.c.product_id.label('id'), 
                    t_products.c.images.label('image'), 
                    t_products.c.product_name.label('title'), 
                    t_products.c.price,
                    t_products.c.condition
                )
                .where(t_products.c.category==each, t_products.c.deleted==0)
                .filter(t_products.c.product_name.like(f"%{product_name}%"))
            )
            for row in temp:
                result.append(row)
    
    
    elif category:
        
        for each in category.split(","):
            # print("----------",each)
            
            temp = run_query(
                select(
                    t_products.c.product_id.label('id'), 
                    t_products.c.images.label('image'), 
                    t_products.c.product_name.label('title'), 
                    t_products.c.price,
                    t_products.c.condition
                )
                .where(t_products.c.category==each, t_products.c.deleted==0)
            )
            for row in temp:
                result.append(row)
                
    elif product_name:
        print("=====2=====",product_name)
        temp = run_query(
            select(
                t_products.c.product_id.label('id'), 
                t_products.c.images.label('image'), 
                t_products.c.product_name.label('title'), 
                t_products.c.price,
                t_products.c.condition
            )
            .join(t_categories, t_categories.c.id==t_products.c.category)
            .where(t_products.c.deleted==0, t_categories.c.deleted==0)
            .filter(t_products.c.product_name.like(f"%{product_name}%"))
        )
        for row in temp:
            result.append(row)
          
    else:
        temp = run_query(
            select(
                t_products.c.product_id.label('id'), 
                t_products.c.images.label('image'), 
                t_products.c.product_name.label('title'), 
                t_products.c.price,
                t_products.c.condition
            )
            .where(t_products.c.deleted==0)
        )
        for row in temp:
            result.append(row)
    
    # PRICE EXIST
    after_price=[]
    if price:
        price=price.split(",")
        
        for row in result:
            if float(row['price']) >= float(price[0]) and float(row['price']) <= float(price[1]):
                after_price.append(row)
        result=after_price      
    
    
    temp_result=[]
    if condition:
        
        for each in condition.split(","):
            for row in result:
                print(row['condition'])
                if row['condition']==each:
                    print("add")
                    temp_result.append(row)
        result=temp_result        
                           
    # return {"result":result}
            
    if sort_by:
        lines=[]
        if sort_by.split(" ")[1]=="a_z":
            print("--------masuk sort 1")    
            lines = sorted(result, key=lambda k: k.get("price", 0), reverse=False)
            
        elif sort_by.split(" ")[1]=="z_a":
            print("--------masuk sort 2")    
            lines = sorted(result, key=lambda k: k.get("price", 0), reverse=True)
        result=lines
        
    json_result=[]
    
    for row in result:
        temp_json={}
            
        first_image = row['image'].split()
        print("===---===",row)
        print("===---===",first_image)
        first_image = first_image[0]
            
        temp_json={
            "id":row['id'],
            "image":first_image,
            "title":row['title'],
            "price":row['price']
        }
            
        json_result.append(temp_json)
        
    temp_json_result=len(json_result)
    
    # using param page and page_size
            
    # # ALGORITMA 1
    # temp_pagesize=[]
    # temp=[]
    # for each_row in range(len(json_result)):
    #     print(f"{each_row}%{page_size}= ",each_row%page_size==0)
    #     if each_row%page_size==0 and each_row!=0:
    #         temp_pagesize.append(temp)
    #         temp=[]    
    #     temp.append(json_result[each_row])
        
    # json_result=temp_pagesize   
    
    
    # ALGORITMA 2
    
    if page and page_size:
        page=int(page)
        page_size=int(page_size)
    
        total=page*page_size
        if temp_json_result>total:
            # if total>temp_json_result:
            #     total=temp_json_result
        
            temp_pagesize=[]
            for i in range(total-page_size,total):
                print("====",i)
                temp_pagesize.append(json_result[i])
            
            json_result=temp_pagesize
    
    # if temp_json_result<total:
    #     total=temp_json_result
        
    #     temp_pagesize=[]
    #     for i in range(total-page_size,total):
    #         print("====",i)
    #         temp_pagesize.append(json_result[i])
        
    #     json_result=temp_pagesize
    
    # return{"a":json_result}
    
    # DI LOOP, DI SPLIT YANG IMAGES URL
    if len(json_result)==0:
        json_result.append({
            "id": "none",
            "image": "/assets/images/ayu_tenan.png",
            "price": 0,
            "title": "Not Found"
        })
    
    return {"data": json_result , "total_rows":temp_json_result, "total_row_inpage":len(json_result)}




# [Endpoint 7 : Get Category]
@product_list_bp.route("categories", methods=["GET"])
def get_category():
    
    result = run_query(select(t_categories.c.id, t_categories.c.title))
        
    return {
        "data":  result
    }
    # route ini gak akan di jalananin karena duplikasi route dengan endpoint 24.5 di admin.py




# [Endpoint 8 : Search Product by Image]
@product_list_bp.route("products/search_image", methods=["POST"])
def search_product_by_image():
    
    img_base64=request.json.get('image')
    
    import base64
    decoded_data=base64.b64decode((img_base64))
    img_file = open(f'AI/target.png', 'wb')
    img_file.write(decoded_data)
    img_file.close()
    
    from AI.main import Main
    # img_url=request.json.get('img_url')
    img_url="AI/target.png"
    
    result= Main.run_search_by_image(img_url)
    print("RESULT BEFORE = ",result)
    result=result.lower()
    result=result.replace("-","")
    result=result.replace("/","")
    print("RESULT AFTER = ",result)
    
    category_result = run_query(select(t_categories).where(t_categories.c.ai_category==result))
    
    if category_result:
        print("---------------",category_result)
        return {"category":category_result[0]['id'], "title":category_result[0]['title']}
        
    return {"message":f"failed, image category not found {result}"}
    
    
    
    # img_base64=request.json.get('image')
    # return {"message":img_base64}
    
    # image_base64 = request.args.get('image')
    
    # category_name = alogiritma_anak_AI(image_base64)
    
    # result = run_query(select(t_categories).where(t_categories.c.title==category_name))
    
    # return {"category_id" : result[0]['id']}




