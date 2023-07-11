from flask import Flask, render_template, request, flash, url_for, redirect
import pandas as pd 
import os
from datetime import date
import random
from werkzeug.utils import secure_filename
from PIL import Image
# from dotenv import load_dotenv
import os

# from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
# from clarifai_grpc.grpc.api import service_pb2_grpc
# stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

# from clarifai_grpc.grpc.api import service_pb2, resources_pb2
# from clarifai_grpc.grpc.api.status import status_code_pb2
# metadata = (('authorization', 'Key 02aad03316c148aab10375c462ae4f68'),)

app = Flask(__name__)

# def get_tags_from_path(image_path):
#     print("image path => ",image_path)
#     with open(image_path,"rb") as f:
#         file_bytes = f.read()
#     tags = []
#     request = service_pb2.PostModelOutputsRequest(
#     model_id='aaa03c23b3724a16a56b629203edc62c',
#     inputs=[
#       resources_pb2.Input(data=resources_pb2.Data(image=resources_pb2.Image(base64=file_bytes)))
#     ])
#     response = stub.PostModelOutputs(request, metadata=metadata)

#     if response.status.code != status_code_pb2.SUCCESS:
#         raise Exception("Request failed, status code: " + str(response.status.code))

#     for concept in response.outputs[0].data.concepts:
#         tags.append(concept.name)
#     return tags

# img_path = "static/image.jpg"
# path = "static/image.jpg"

# def classification(image_path):
#     ## Code for image classification

#     tags = get_tags_from_path(image_path)
#     print(tags)
#     plumber_set = ['faucet','pipes','pipe','shower','wash','basin','water','washcloset','bathroom','water closet','flush','bathtub','steel','plumber','plumbing','wet']
#     electrical_set = ['electrical','electronics','power','appliance','computer','conditioner','technology','wire','connection','switch','electricity','lamp','ceiling','fan','heater']
#     carpenter_set = ['wood', 'wooden', 'furniture', 'table', 'chair', 'stool','carpentry','antique','comfort','armchair','old', 'inside', 'empty', 'family', 'no person', 'seat', 'antique', 'vintage', 'house', 'desk', 'design', 'desktop', 'room', 'decoration', 'luxury',  'wardrobe', 'cabinet', 'interior design', 'drawer', 'cupboard', 'indoor']

#     score_plumber = 0
#     score_electrical = 0
#     score_carpenter = 0

#     #### has n^2 complexity
#     for tag in tags:
#         if(tag in plumber_set):
#             score_plumber+=1
#         if(tag in electrical_set):
#             score_electrical+=1
#         if(tag in carpenter_set):
#             score_carpenter += 1


#     if(max(score_electrical,score_plumber, score_carpenter)==0):
#         return "something went wrong, could not predict the department"
#     else:
#         if(score_plumber == max(score_electrical,score_plumber, score_carpenter)):
#             return "plumber"
#         if(score_electrical == max(score_electrical,score_plumber, score_carpenter)):
#             return "electrical"
#         else:
#             return "carpenter"
    

 user_database = pd.read_excel(r"users.xlsx")
service_provider_database = pd.read_excel(r"service_providers.xlsx")
current = pd.read_excel(r"current_user.xlsx")
current_service = pd.read_excel(r"current_service_provider.xlsx")
req_database = pd.read_excel(r"requests.xlsx")

def email_found(email):
        for i in user_database['Email']:
            if(email == i):
                return True
        
        return False

def phone_found(phone):
        for i in user_database['Phone Number']:
            if(phone == i):
                return True
        
        return False

def match(email, password):
    p = 0
    q = 0
    for i in user_database['Email']:
        p += 1
        if(email == i):
            for j in user_database['Password']:
                q += 1 
                if j == password and p == q:
                    return True
    return False

def email_found2(email):
        for i in service_provider_database['Email']:
            if(email == i):
                return True
        
        return False

def phone_found2(phone):
        for i in service_provider_database['Phone Number']:
            if(phone == i):
                return True
        
        return False

def match2(email, password):
    p = 0
    q = 0
    for i in service_provider_database['Email']:
        p += 1
        if(email == i):
            for j in service_provider_database['Password']:
                q += 1 
                if j == password and p == q:
                    return True
    return False

def find_name(email):
    p = 0
    q = 0
    for i in user_database['Email']:
        p += 1
        if(email == i):
            for j in user_database['Name']:
                q += 1 
                if p == q:
                    return j
    return False

@app.route('/')
def ini():
        return render_template('user_service_provider.html')

@app.route('/user_login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            current_user_name = find_name(email)
            current.loc[len(current.index)] = [current_user_name]
            return render_template("home.html", current_user_name = current_user_name)

            #email and password found and match, then authenticate

            if email_found(email):
                if(match(email, password)):
                    flash('Logged in successfully!', category='success')
                    current_user_name = find_name(email)
                    return render_template("home.html", current_user_name = current_user_name)
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist, Please Sign Up', category='error')
    return render_template("login.html")


@app.route('/service_login', methods = ['GET', 'POST'])
def login2():
    if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            return render_template("service_provider_home.html")
            #email and password found and match, then authenticate

            if email_found2(email):
                if(match2(email, password)):
                    flash('Logged in successfully!', category='success')
                    return render_template("service_provider_home.html")
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist, Please Sign Up', category='error')
    return render_template("service_login.html")

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    email = request.form.get('email')
    password = request.form.get('password1')
    confirmpass = request.form.get('password2')
    name = request.form.get('Name')
    address = request.form.get('address')
    phone = request.form.get('Phone Number')
    user_database.loc[len(user_database.index)] = [email, password, name, address, phone] 
    user_database.to_excel('users.xlsx', index=False)
    if(email_found(email) or phone_found(phone)):
        flash('Error! Try again.', category='error')
    else:
        flash('Logged in successfully!', category='success')
    return render_template("sign_up.html")

@app.route('/service_sign_up', methods = ['GET', 'POST'])
def service_sign_up():
    email = request.form.get('email')
    password = request.form.get('password1')
    confirmpass = request.form.get('password2')
    name = request.form.get('Name')
    address = request.form.get('address')
    phone = request.form.get('Phone Number')
    type = request.form.get('type')
    service_provider_database.loc[len(service_provider_database.index)] = [email, password, name, address, phone, type] 
    service_provider_database.to_excel('service_providers.xlsx', index=False)
    if(email_found2(email) or phone_found2(phone)):
        flash('Error! Try again.', category='error')
    else:
        flash('Logged in successfully!', category='success')
    return render_template('service_sign_up.html')

@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    ls = []
    q = 0
    # ml code
    type = 'plumber'
    for i in service_provider_database['Email']:
        if(service_provider_database['Service Type'][q] == type):
            ls.append([service_provider_database['Email'][q], service_provider_database['Name'][q], service_provider_database['Phone'][q], service_provider_database['Address'][q]])
        q += 1
    
    return render_template("add_service.html", current_user_name = current['Current'][0], list_of_services = ls)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    current.drop(current.tail(1).index,inplace=True)
    current.to_excel('current_user.xlsx', index = False)
    return redirect(url_for('login'))


@app.route('/logout_service_provider', methods=['GET', 'POST'])
def service_logout():
    # current.drop(current.tail(1).index,inplace=True)
    # current.to_excel('current_user.xlsx', index = False)
    return redirect(url_for('login2'))

@app.route('/pending_requests')
def pending_requests():
    return render_template('service_provider_home.html')

@app.route('/accepted_requests', methods=['GET', 'POST'])
def accepted_requests():
    return render_template('accepted_requests.html')

@app.route('/completed_requests', methods=['GET', 'POST'])
def completed_requests():
    return render_template('completed_requests.html')

@app.route('/deleted_services', methods=['GET', 'POST'])
def deleted_services():
    return render_template("deleted_services.html", current_user_name = current['Current'][0])

if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'reet'
    app.run(debug=True)