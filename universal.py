# [Get Image ]
# Bobot nilai: 1 poin 
# Metode: GET 
# URL: /image/{image_name.extension} 
# Response: image file 
# For any error messages, you should return with this response. Response: 
# Key Example 
# message success, user already exists

from flask import Blueprint, request, render_template, send_file
from utils import run_query, t_images
from sqlalchemy import select

universal_bp = Blueprint("universal_bp", __name__, url_prefix="/assets/images")


# [ENDPOINT 1 : Get Image]
@universal_bp.route("/<url_image>", methods=["GET"])
def get_image(url_image) :
    
    # check if url_image is exist in database
    result = run_query(select(t_images).where(t_images.c.image_url == f"/assets/images/{url_image}"))
    if result :
        
        return send_file(f"assets/images/{url_image}", mimetype='image')
    
    return {"Message" : f"ERROR!!! : 'assets/images{url_image}' doesn't exist"}


    
    