from utils import app
import os

# MENDAFTARKAN BLUEPRINT SETIAP KALI MEMBUAT FILE BARU / HEAD ROUTE BARU
from home import home_bp
from universal import universal_bp
from authentication import signup_bp, signin_bp
from admin import admin_bp
from product_list import product_list_bp
from product_detail import product_detail_bp
from profil import profil_bp
from cart import cart_bp
from sudo import sudo_bp

# SWAGGER
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

# app.register_blueprint(swaggerui_blueprint)


blueprints = [home_bp, universal_bp, signup_bp, signin_bp, admin_bp, product_list_bp, product_detail_bp, profil_bp, cart_bp, sudo_bp, swaggerui_blueprint]
for blueprint in blueprints :
    app.register_blueprint(blueprint)

# @app.after_request
# def apply_caching(request):

#     request.headers["Access-Control-Allow-Origin"] = "*"
#     return request

@app.after_request
def apply_caching(request):

    request.headers["Access-Control-Allow-Origin"] = "*"
    request.headers["Access-Control-Allow-Headers"] = "Authentication, Content-Type, Content-Length, Content-Encoding, Content-Language, Content-Location"
    # request.headers["Access-Control-Allow-Headers"] = "Content-Type, Content-Length, Content-Encoding, Content-Language, Content-Location, Content-Range, Content-Security-Policy, Content-Security-Policy-Report-Only"
    request.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, UPDATE, DELETE"
    request.headers["Access-Control-Max-Age"] = "86400"
    return request

# TESTING KONEKSI 
@app.route("/")
def home() :
    
    return "<h1>BACKEND_URL of Fashion Campus by BlankOn</h1><br><h3><a href='http://34.126.123.217:5000/api/docs/'>API Documentation</a></h3>"


if __name__ == "__main__" :
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    
# semua kode dibawah ini tidak akan dijalankan




