from flask import Flask, request, make_response, jsonify ,send_file
import os
from reportlab.pdfgen import canvas
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
    from flask import Flask, send_file
import os

app = Flask(__name__)

@app.get('/api/download_resume')
def download_resume():
    # Specify the folder and filename
    folder_name = 'resume_pdf'
    pdf_filename = 'SimretPaulosResume.pdf'

    # Construct the full path to the PDF file
    pdf_path = os.path.join(os.getcwd(), folder_name, pdf_filename)

    # Check if the file exists
    if os.path.exists(pdf_path):
        # Send the file as a response
        return send_file(pdf_path, as_attachment=True)
    else:
        return "File not found"

if __name__ == '__main__':
    app.run(debug=True)




if dbcreds.production_mode:
    print("Running in Production Mode")
    import bjoern
    bjoern.run(app, '0.0.0.0', 5000)
else:
    from flask_cors import CORS 
    CORS(app)
    print("Running in Development Mode")  
    app.run(debug=True)
