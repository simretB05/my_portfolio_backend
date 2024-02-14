from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import dbcreds
import apiHelper
import dbhelper 

app = Flask(__name__) 
CORS(app)

@app.post('/api/user_contact')
def post_new_user_contact():
    error=apiHelper.check_endpoint_info(request.form,["user_name","user_email_address","user_message"]) 
    if (error != None ):
      return make_response(jsonify(error), 400)
    if(request.files):
        filename =apiHelper.save_file(request.files['file'])
    else:
        filename=None
    results = dbhelper.run_procedure('CAll  my_user_contact_inform(?,?,?)',[request.form.get('user_name'),request.form.get('user_email_address'),request.form.get('user_message')])
    if(type(results)==list):
        return make_response(jsonify(results), 200)
    else:
      return make_response(jsonify(results), 500) 

if dbcreds.production_mode:
    print("Running in Production Mode")
    import bjoern
    bjoern.run(app, '0.0.0.0', 5000)
else:
    from flask_cors import CORS 
    CORS(app)
    print("Running in Development Mode")  
    app.run(debug=True)
