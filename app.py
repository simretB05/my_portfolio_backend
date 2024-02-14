from flask import Flask, request, make_response, jsonify from flask_cors 
import CORS
import uuid
import dbcreds
import apiHelper
import dbhelper

app = Flask(__name__)

CORS(app)

@app.post('/api/client')
def post_new_client():
    error = apiHelper.check_endpoint_info(
        request.json, [username, email, password, bio, image_url])
    if (error != None):
        return make_response(jsonify(error), 400)
    results = dbhelper.run_procedure('CAll insert_new_client(?,?,?,?,?)', [request.json.get(username), request.json.get(
        email), request.json.get(password), request.json.get(bio), request.json.get(image_url)])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response(jsonify(results), 500)

@app.post('/api/login')
def post_new_token():
    uuid_value = uuid.uuid4()
    error = apiHelper.check_endpoint_info(
        request.json, [username, password])
    if (error == None):
        token = str(uuid_value)
    elif(error != None):
        return make_response(jsonify(error), 'somthing wrong')
    results = dbhelper.run_procedure('CAll insert_new_token(?,?,?)', [
                                     
    request.json.get(username), request.json.get(password), token])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response(jsonify(results), 500)


@app.delete('/api/login')
def delete_token():
    error = apiHelper.check_endpoint_info(request.json, [token])
    if (error != None):
        return make_response(jsonify(error), 400)
    results = dbhelper.run_procedure('CAll delete_token(?)', [
                                     request.json.get(token)])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response(jsonify(results), 500)


@app.get('/api/client')
def get_client_data():
    error = apiHelper.check_endpoint_info(request.args, [token])
    if (error != None):
        return make_response(jsonify(error), 400)
    results = dbhelper.run_procedure('CAll get_client_data(?)', [
                                     request.args.get(token)])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response(jsonify(results), 500)


if(dbcreds.production_mode == True):
    print(Running in Production Mode)
    import bjoern # type: ignore
    bjoern.run(app, 0.0.0.0, 5000)
else:
    from flask_cors import CORS
    CORS(app)
    print(Running in Development Mode)
    app.run(debug=True)

