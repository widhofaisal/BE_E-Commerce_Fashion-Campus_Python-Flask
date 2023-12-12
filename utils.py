from datetime import datetime
from flask import Flask
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, DateTime, select, insert
# from flask_cors import CORS

# from sqlalchemy.ext.declarative import declarative_base

# from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE

# Base = declarative_base()


def get_engine():
    return create_engine("sqlite:///FinalProject.db", future=True)
    # return create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/fashioncampus_db")
    
def create_app():
    app = Flask(__name__)
    
    
    engine = get_engine()
    meta = MetaData()
    
    # SKEMA TABEL TULIS DISINI
    Table(
        "images",
        meta, 
        Column("id", String, nullable=False), # PAKE UUID
        Column("image_url", String, nullable=False, unique=True),
        Column("title", String, nullable=True)
    )
    
    Table(
        "users",
        meta,
        Column("user_id", String, primary_key=True, nullable=False, unique=True), # PAKE UUID
        Column("name", String, nullable=False),
        Column("email", String, nullable=False, unique=True),
        Column("phone_number", String, nullable=False),
        Column("password", String, nullable=False),
        Column("type", String, nullable=False), # DEFAULT BUYER
        Column("buyer_balance", Integer, default=0),
        Column("seller_revenue", Integer, default=0),
        Column("token", String),
        Column("address_name", String, nullable=False),
        Column("address_phone", String, nullable=False),
        Column("address", String, nullable=False),
        Column("city", String, nullable=False),
    )
    
    Table(
        "products",
        meta,
        Column("product_id", String, primary_key=True, nullable=False, unique=True), # PAKE UUID
        Column("product_owner", String, nullable=False),
        Column("owner_id", String, nullable=False),
        Column("product_name", String, nullable=False), # APAKAH PERLU UNIQUE ??
        Column("description", String, nullable=False), 
        Column("images", String, nullable=False),
        Column("condition", String, nullable=False),
        Column("category", String, nullable=False),
        Column("ai_category", String, nullable=True),
        Column("price", Integer, nullable=False),
        Column("deleted", Integer, nullable=False),
    )
    
    Table(
        "categories",
        meta,
        Column("id", String, primary_key=True, nullable=False, unique=True), # PAKE UUID
        Column("title", String, unique=True, nullable=False),
        Column("deleted", Integer, nullable=False),
        Column("ai_category", String, nullable=True),
    )
    
    Table(
        "cart",
        meta,
        Column("cart_id", String, primary_key=True, nullable=False, unique=True),
        Column("cart_owner", String, nullable=False),
        Column("owner_id", String, nullable=False),
        Column("product_id", String, nullable=False),
        Column("quantity", Integer, nullable=False),
        Column("size", String, nullable=False),
    )
    
    Table(
        "order",
        meta,
        Column("order_id", String, primary_key=True, nullable=False, unique=True),
        Column("created_at", String, default=str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))),
        Column("shipping_method", String, nullable=False),
        Column("owner_id", String, nullable=False),
        Column("buyer_name", String, nullable=False),
        Column("sold_id", String, nullable=False),
        Column("order_price", Integer, nullable=False)
        
    )
    
    Table(
        "sold",
        meta,
        Column("sold_id", String, primary_key=True, nullable=False, unique=True),
        Column("product_id", String, nullable=False),
        Column("quantity", Integer, nullable=False),
        Column("size", String, nullable=False),
        Column("product_name", String, nullable=False),
        Column("price", Integer, nullable=False),
        Column("images", String, nullable=False),
    )
    
    meta.create_all(engine)
    return app, meta


app, meta = create_app()

t_categories = meta.tables.get('categories')
t_images = meta.tables.get('images')
t_users = meta.tables.get('users')
t_products = meta.tables.get('products')
t_cart = meta.tables.get('cart')
t_order = meta.tables.get('order')
t_sold = meta.tables.get('sold')


def run_query(query, commit: bool = False):
    """Runs a query against the given SQLite database.

    Args:
        commit: if True, commit any data-modification query (INSERT, UPDATE, DELETE)
    """
    engine = get_engine()
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if commit:
            conn.execute(query)
            conn.commit()
        else:
            return [dict(row) for row in conn.execute(query)]

