import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin, login_user,logout_user,login_required,current_user
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, verify_jwt_in_request, get_jwt
from functools import wraps
from flask_caching import Cache
import redis
from celery import Celery
from celery.schedules import crontab

app = Flask(__name__) 
db_name = 'grocery.db'
app.config['SECRET_KEY'] = 'ugnqzabxzwrmkb'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
db=SQLAlchemy(app)
app.config['JWT_SECRET_KEY'] = 'ahsgfdkajsgdyfg'
CORS(app)
jwt = JWTManager(app)
#CACHING
# cache = Cache(app, config={'CACHE_TYPE': 'RedisCache','Cache_REDIS_HOST':'localhost','Cache_REDIS_PORT':5173,'Cache_REDIS_DB':0})
# cache.init_app(app)
# redis_client = redis.Redis(host='localhost', port=5173, db=0)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement =True)
    name=db.Column(db.String(50),nullable=False)
    def __init__(self,name):
        self.name=name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement =True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name= db.Column(db.String(150))
    approved=db.Column(db.Boolean,default=True)
    rid=db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    def __init__(self,email,password,name,rid=3,approved=True):
        self.email=email
        self.password=password
        self.name=name
        self.rid=rid
        self.approved=approved

class Interactions(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement =True)
    mg_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    interaction=db.Column(db.String(50))
    completed=db.Column(db.Boolean,default=False)
    def __init__(self,mg_id,inter):
        self.mg_id=mg_id
        self.interaction=inter

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(150))
    def __init__(self,name):
        self.name=name
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    cat_id=db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(150))
    dom = db.Column(db.String, nullable=False)
    price=db.Column(db.Integer,default=100)
    qty=db.Column(db.Integer)
    def __init__(self,cid,name,dom,price,qty):
        self.cat_id=cid
        self.name = name
        self.dom = dom
        self.price=price
        self.qty=qty

class Cart(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id=db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    no=db.Column(db.Integer)
    price=db.Column(db.Integer)
    def __init__(self,usid,itid,no,price):
        self.user_id=usid
        self.item_id=itid
        self.no=no
        self.price=price

# # Role-based decorator
# def role_required(required_role):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorator(*args, **kwargs):
#             verify_jwt_in_request()
#             claims = get_jwt()
#             user_role = claims.get('role')
#             if user_role == required_role:
#                 return fn(*args, **kwargs)
#             else:
#                 return jsonify(msg=f"{required_role.capitalize()}s only!"), 401
#         return decorator
#     return wrapper

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"]=="admin":
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper

def user_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"]=="user":
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Users only!"), 403

        return decorator

    return wrapper


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    users=User.query.filter_by(name=username).all()
    for u in users:
        if u.name == username and check_password_hash(u.password,password):
            if u.rid==1:
                access_token = create_access_token(identity=username, additional_claims={"role": "admin"})
                return jsonify({'message': 'Admin login successful', 'access_token': access_token}), 200
            elif u.rid == 2:
                if u.approved:
                    access_token = create_access_token(identity=username, additional_claims={"role": "manager"})
                    return jsonify({'message': 'Store Manager login successful', 'access_token': access_token,"id":u.id}), 200
                else:
                    return jsonify({'message': 'Please Wait for Admin Approval'}),200
            elif u.rid==3:
               access_token = create_access_token(identity=username, additional_claims={"role": "user"})
               return jsonify({'message': 'User login successful', 'access_token': access_token,"id":u.id}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

def isnotem(a):
    if "@" not in a:
        return True
    if ".com" not in a:
        return True
    if len(a)<7:
        return True
    return False

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    em = data.get('email')
    r=data.get('role')
    users=User.query.filter_by(rid=Role.query.filter_by(name=r).first().id)
    # if isnotem(em):
    #     return jsonify({'error': 'Invalid Email'}), 400
    if any(u.name == username for u in users):
        return jsonify({'error': 'Username already exists'}), 400
    if any(u.email == em for u in users):
        return jsonify({'error': 'Email already exists'}), 400
    if r=="User":
        u=User(email=em,password=generate_password_hash(password),name=username)
        db.session.add(u)
        db.session.commit()
    if r=="Store Manager":
        u=User(email=em,password=generate_password_hash(password),name=username,rid=2,approved=False)
        db.session.add(u)
        u=User.query.filter_by(name=username).first()
        it=Interactions(mg_id=u.id,inter="Approval for new manager")
        db.session.add(it)
        db.session.commit()
        return jsonify({'message': 'Registration successful Wait for Admin Approval'}), 200
    return jsonify({'message': 'Registration successful'}), 200

@app.route('/cl', methods=['GET'])
@jwt_required()
def cl():
    print("works fine here")
    token = request.headers.get('Authorization')
    token = token.split(" ")[1]
    u=User.query.filter_by(name=get_jwt_identity()).all()
    
    for i in u:
        if i.rid in [3,2,1]:
            return {"message":"success"}
    return {"message" : "Fail"}

@app.route('/ca',methods=['GET'])
@jwt_required()
def ca():
    token = request.headers.get('Authorization')
    token = token.split(" ")[1]
    u=User.query.filter_by(name=get_jwt_identity()).all()
    for i in u:
        if i.rid == 1:
                return {"message":"success"}
    return {"message":"fail"}


@app.route('/cm',methods=['GET'])
@jwt_required()
def cm():
    token = request.headers.get('Authorization')
    token = token.split(" ")[1]
    u=User.query.filter_by(name=get_jwt_identity()).all()
    for i in u:
        if i.rid ==2:
            if i.approved==True:
                return {"message":"success"}
            # return {"message":"not approved"}
    return {"message":"fail"}

@app.route("/getcat",methods=['GET'])
# @cache.memoize(timeout=10)
def getcat():
    c=Category.query.all()
    l=[]
    for i in c:
        l.append({"id":i.id,"name":i.name})
    return l

@app.route("/getitem",methods=['GET'])
# @cache.memoize(timeout=10)
def getitem():
    c=Item.query.all()
    l=[]
    for i in c:
        l.append({"id":i.id,"cid":i.cat_id,"name":i.name})
    return l


@app.route("/getreq",methods=['GET'])
@admin_required()
# @cache.memoize(timeout=10)
def getreq():
    q=Interactions.query.all()
    l=[]
    for i in q:
        l.append({"id":i.mg_id,"interaction":i.interaction})

    return l

@app.route("/addc",methods=['GET','POST'])
@admin_required()
def addc():
    data = request.get_json()
    c=Category.query.filter_by(name=data.get("name")).all()
    if c:
        return {"message":"category exists"}
    c1=Category(name=data.get("name"))
    db.session.add(c1)
    db.session.commit()
    return {"message":"success"}

@app.route("/accept",methods=['GET','POST'])
@admin_required()
def accept():
    data = request.get_json()
    i=Interactions.query.filter_by(mg_id=data.get("id")).first()
    u=User.query.filter_by(id=i.mg_id).first()
    db.session.delete(i)
    u.approved=True
    db.session.commit()
    return {"message":"success"}

@app.route("/deletecat",methods=['GET','POST'])
@admin_required()
def deletecat():
    data = request.get_json()
    c=Category.query.filter_by(id=data.get("id")).first()
    i=Item.query.filter_by(cat_id=c.id).all()
    for j in i:
        c1=Cart.query.filter_by(item_id=j.id).all()
        for k in c1:
            db.session.delete(k)
    db.session.delete(c)
    db.session.commit()
    return {"message":"success"}

@app.route("/updatecat",methods=['GET','POST'])
@admin_required()
def updatecat():
    data = request.get_json()
    u=Category.query.filter_by(id=data.get("id")).first()
    u.name=data.get("name")
    db.session.commit()
    return {"message":"success"}

@app.route("/additem",methods=['GET','POST'])
# @cache.memoize(timeout=10)
def additem():
    data=request.get_json()
    it=Item(cid=data.get("catid"),name=data.get("name"),price=data.get("price"),qty=data.get("qty"),dom=data.get("dom"))
    db.session.add(it)
    db.session.commit()
    return {"message":"success"}

@app.route("/updateit",methods=['GET','POST'])
def  updateitem():
    data=request.get_json()
    it=Item.query.filter_by(id=data.get("id")).first()
    it.name=data.get("name")
    it.price=data.get("price")
    it.qty=data.get("qty")
    it.dom=data.get("dom")
    db.session.commit()
    return {"message":"success"}

@app.route("/deleteit",methods=['GET','POST'])
def deleteit():
    data = request.get_json()
    u=Item.query.filter_by(id=data.get("id")).first()
    c=Cart.query.filter_by(item_id=u.id).all()
    for i in c:
        db.session.delete(i)
    db.session.delete(u)
    db.session.commit()
    return {"message":"success"}

@app.route("/search",methods=['GET',"POST"])
# @cache.memoize(timeout=10)
def search():
    v=request.get_json()
    c=[]
    it=[]
    if v=={} or v['key']=="":
        c=Category.query.all()
        it=Item.query.all()
    else:
        c=Category.query.filter_by(name=v['key']).all()
        if c==[]:
            it=Item.query.filter_by(name=v['key']).all()
            for j in it:
                c.append(Category.query.filter_by(id=j.cat_id).first())
        else:
            for i in c:
                it.extend(Item.query.filter_by(cat_id=i.id).all())
    cl=[]
    il=[]
    for i in c:
        cl.append({"id":i.id,"name":i.name})
    for i in it:
        il.append({"id":i.id,"cid":i.cat_id,"name":i.name,"qty":i.qty,"price":i.price,"dom":i.dom[:10]})
    return {"cat":cl,"it":il}

@app.route("/addtocart",methods=['GET','POST'])
# @cache.memoize(timeout=10)
def addtocart():
    data=request.get_json()
    i=Item.query.filter_by(id=data.get("id")).first()
    if i.qty<data.get("qty"):
        return {"message":"out of stock"}
    if data.get("qty")==0:
        return {"message":"success"} 
    i.qty-=data.get("qty")
    c=Cart(usid=data.get("idu"),itid=i.id,no=data.get("qty"),price=(data.get("qty")*i.price))
    db.session.add(c)
    db.session.commit()
    return {"message":"success"}

@app.route("/getitems/<int:user_id>", methods=['GET'])
# @cache.memoize(timeout=10)
@user_required()
def getitems(user_id):
    c = Cart.query.filter_by(user_id=user_id).all()
    cl=[]
    for i in c:
        cl.append({"id":i.id,"name":Item.query.filter_by(id=i.item_id).first().name,"qty":i.no,"price":i.price,"iid":i.item_id})
    return cl

@app.route("/deletecart",methods=['GET','POST'])
def deletecart():
    data = request.get_json()
    print(data.get("id"))
    c=Cart.query.filter_by(id=data.get("id")).first()
    print(c)
    i=Item.query.filter_by(id=c.item_id).first()
    i.qty+=c.no
    db.session.delete(c)
    db.session.commit()
    return {"message":"success"}

@app.route("/interact",methods=["POST"])
# @cache.memoize(timeout=10)
def interact():
    data=request.get_json()
    i=Interactions(mg_id=data.get("id"),inter=(data.get("task")+data.get("cname")))
    db.session.add(i)
    db.session.commit()
    return {}


def create_db():
    with app.app_context():
        db.create_all()
        q=Role.query.all()
        if not q:
            r=Role(name="Admin")
            db.session.add(r)
            db.session.add(Role(name="Store Manager"))
            db.session.add(Role(name="User"))
            db.session.add(User(name="admin",password=generate_password_hash("pass"),email="admin@email.com",rid=1))
            db.session.commit()
            
if __name__=="__main__":
    create_db()
    app.run(debug=True)