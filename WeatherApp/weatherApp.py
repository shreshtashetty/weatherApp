import flask
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
import test

# Configure the Flask application to connect with the MongoDB server
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/weather"
# app.config['MONGO_DBNAME'] = 'weather'
# app.config['SECRET_KEY'] = 'secret_key'

# # Connect to MongoDB using Flask's PyMongo wrapper
mongo = PyMongo(app)
db = mongo.db
col = mongo.db["current"]
print ("MongoDB Database:", mongo.db)

# Declare an app function that will return some HTML
@app.route("/curr", methods = ['GET'])
def get_all_current_updates():
    current = mongo.db.current_data
    output = []
    for q in current.find():
        # import ipdb;ipdb.set_trace()
        output.append({'City':q['name'], 'Weather':q['main']})
    # aa = current.find()
    # output.append(aa.json())
    # return {"result":output}
    return jsonify({"result":output})

if __name__ == '__main__':
    app.run(debug=True)