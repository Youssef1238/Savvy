import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from database import User,Transaction,Savings,Category
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token,get_jwt
)


app = Flask(__name__)

load_dotenv()

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 300 
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400 
jwt = JWTManager(app)
blacklist = set()
# USERS ROUTING ---------------------------------------------------------------------
# -----------------------------------------------------------------------------------

@app.route('/user' , methods = ["GET"])
@jwt_required()
def handelUser():
    user = User()
    return jsonify(user.getAll()) 


@app.route('/register' , methods = ["POST"])
def handelRegister():
    user = User()
    data = request.get_json()
    res = user.add(**data)
    if(res == None) : return "username already used !" , 409
    elif (type(res) == str) : return res , 400
    else : 
        access_token = create_access_token(identity=data["username"])
        refresh_token = create_refresh_token(identity=data["username"])
        res["access_token"] = access_token
        res["refresh_token"] = refresh_token
        return jsonify(res) , 200    

@app.route('/login' , methods = ["POST"])
def handelUserVerification():
    user = User()
    data = request.get_json()
    res = user.Verify(**data)
    if(res == 0) : return "username incorrect !" , 404
    elif(res == 1) : return "password incorrect !" , 404
    else : 
        
        access_token = create_access_token(identity=data["username"])
        refresh_token = create_refresh_token(identity=data["username"])
        res["access_token"] = access_token
        res["refresh_token"] = refresh_token
        return jsonify(res) , 200

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()  
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist

@app.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def logout():
    jti = get_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Logged out successfully"}), 200


@app.route('/user/<id>' , methods = ["GET","PUT","DELETE"])
@jwt_required()
def handelOneUser(id):
    user = User()
    if request.method == "GET" :
        res = user.getOne(id)
        user.close()
        if(res == None) : return "doesn't exist ", 404
        return jsonify(res)
    elif request.method == "PUT":
        data = request.get_json()
        res = user.update(id,**data)
        user.close()
        if(res == 0) : return "Account updated", 200
        elif(res == None) : return "doesn't exist" , 404
        return res , 400
    else :
        res = user.delete(id)
        user.close()
        if(res == 0) : return "Account deleted", 200
        elif(res == None) : return "doesn't exist" , 404
        return res , 400
    


# TRANSACTIONS ROUTING ---------------------------------------------------------------------
# ------------------------------------------------------------------------------------------


@app.route('/transaction' , methods = ["GET","POST"])
@jwt_required()
def handelTransaction():
    transaction = Transaction()
    if request.method == "GET" :
        return jsonify(transaction.getAll()) 
    else:
        data = request.get_json()
        res = transaction.add(**data)
        if res == 0 : return "Transaction added" , 200
        return res , 400


@app.route('/transaction/<id>' , methods = ["GET","PUT","DELETE"])
@jwt_required()
def handelOneTransaction(id):
    transaction = Transaction()
    if request.method == "GET" :
        res = transaction.getOne(id)
        transaction.close()
        if(res == None) : return "doesn't exist", 404
        return jsonify(res)
    elif request.method == "PUT":
        data = request.get_json()
        res = transaction.update(id,**data)
        transaction.close()
        if(res == 0) : return "Transaction updated", 200
        elif(res == None) : return "doesn't exist" , 404
        return res , 400
    else :
        res = transaction.delete(id)
        transaction.close()
        if(res == 0) : return "Transaction deleted", 200
        elif(res == None) : return "doesn't exist" , 404
        return res , 400


@app.route('/transaction/user/<id>' , methods = ["GET"])
@jwt_required()
def handelTransactionByUser(id):
    transaction = Transaction()

    res = transaction.getByUser(id)
    transaction.close()
    return jsonify(res)
    

# SAVINGS ROUTING --------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------


@app.route('/saving' , methods = ["GET","POST"])
@jwt_required()
def handelSaving():
    saving = Savings()
    if request.method == "GET" :
        return jsonify(saving.getAll()) 
    else:
        data = request.get_json()
        return saving.add(**data)

@app.route('/saving/user/<id>' , methods = ["GET"])
@jwt_required()
def handelSavingsByUser(id):
    saving = Savings()

    res = saving.getByUser(id)
    saving.close()
    return jsonify(res)

@app.route('/saving/<id>' , methods = ["GET","PUT","DELETE"])
@jwt_required()
def handelOneSaving(id):
    saving = Savings()
    if request.method == "GET" :
        res = saving.getOne(id)
        saving.close()
        if(res == None) : return "doesn't exist", 404
        return jsonify(res)
    elif request.method == "PUT":
        data = request.get_json()
        res = saving.update(id,**data)
        saving.close()
        if(res == None) : return "doesn't exist ", 404
        return res
    else :
        res = saving.delete(id)
        saving.close()
        if(res == None) : return "doesn't exist ", 404
        return res

@app.route('/saving/generate' , methods = ["POST"])
@jwt_required()
def handelGenerate():
    saving = Savings()
    data = request.get_json()
    res = saving.generate(**data)
    if res == 0 : return "Solution generated", 200
    else : return res, 400


# CATEGORIES ROUTING --------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------


@app.route('/category' , methods = ["GET","POST"])
@jwt_required()
def handelCategory():
    category = Category()
    if request.method == "GET" :
        return jsonify(category.getAll()) 
    else:
        data = request.get_json()
        res = category.add(**data)
        if(res == 0) : return "category added", 200
        elif(res == None) : return "name already used" , 409
        return res , 400


@app.route('/category/<id>' , methods = ["GET","PUT","DELETE"])
@jwt_required()
def handelOneCategory(id):
    category = Category()
    if request.method == "GET" :
        res = category.getOne(id)
        category.close()
        if(res == None) : return "doesn't exist", 404
        return jsonify(res)
    elif request.method == "PUT":
        data = request.get_json()
        res = category.update(id,**data)
        category.close()
        if(res == 0) : return "category updated", 200
        elif(res == None) : return "doesn't exist" , 404
        return res , 400
    else :
        res = category.delete(id)
        category.close()
        if(res == 0) : return "category deleted", 200
        elif(res == None) : return "doesn't exist" , 404
        return res , 400

@app.route('/category/user/<id>' , methods = ["GET"])
@jwt_required()
def handelCategoryByUser(id):
    category = Category()

    res = category.getByUser(id)
    category.close()
    return jsonify(res)
    


if(__name__ == "__main__"):
    app.run(debug=True,port=5544)