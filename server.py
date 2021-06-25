from flask import Flask, render_template, request, Response
import os, json, sys
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.document import Document
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

databaseName = os.environ["databaseName"]
account_user_name = os.environ["account_user_name"]
apikey = os.environ["apikey"]


#Connect to the database
client = Cloudant.iam(account_name=account_user_name, api_key=apikey, connect=True)
myDatabase = client.create_database(databaseName)

app = Flask("Web Hook")
CORS(app)

def getAllPets(kind):
    if(kind == "dog"):
        selector = {'kind': {'$eq': 'Dog'}}
        docs = myDatabase.get_query_result(selector)
        pets = []
        for doc in docs:
            pet_instance ={}
            pet_instance["id"] = doc["_id"]
            pet_instance["name"] = doc["name"]
            pet_instance["age"] = doc["age"]
            pet_instance["breed"] = doc["breed"]
            pets.append(pet_instance)
        return {"pets": pets}
    elif(kind == "cat"):
        selector = {'kind': {'$eq': 'Cat'}}
        docs = myDatabase.get_query_result(selector)
        for doc in docs:
            pet_instance ={}
            pet_instance["id"] = doc["id"]
            pet_instance["name"] = doc["name"]
            pet_instance["age"] = doc["age"]
            pet_instance["breed"] = doc["breed"]
            pets.append(pet_instance)
        return {"pets": pets}
    else:
        return {"pets":[]}

def getPetDetails(id):
    selector = {'_id': {'$eq': id}}
    docs = myDatabase.get_query_result(selector)
    for doc in docs:
        print("come here")
        pet_instance ={}
        pet_instance["name"] = doc["name"]
        pet_instance["age"] = doc["age"]
        pet_instance["breed"] = doc["breed"]
        pet_instance["comments"] = doc["comments"]
        return pet_instance

@app.route("/pets/<id>")
def getPetPic(id):
    selector = {'_id': {'$eq': id}}
    docs = myDatabase.get_query_result(selector)
    print(docs)
    for doc in docs:
        document = Document(myDatabase, document_id=id)
        attachment = document.get_attachment(attachment=doc['filename'],headers={"Content-Type":"jpeg/png"})
        return Response(attachment, mimetype='image/jpg')

@app.route("/pets",methods=["POST"])
def pets():
    pets = []
    req = request.form['req']
    if(req == "getAllPets"):
        kind = request.form['kind']
        return getAllPets(kind)
    elif(req == "getPetDetails"):
        id = request.form['id']
        return getPetDetails(id)
    elif(request.args['req'] == "getPetImage"):
        id = request.form['id']
        return getPetPic(id)
    return {}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
