from flask import Flask, jsonify,request
from flask_pymongo import PyMongo,ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/pythonreacatdb'
mongo = PyMongo(app)

CORS(app)

db=mongo.db.animals

@app.route('/animals', methods=['POST'])
def createAnimal():
    id = db.insert_one({
        'Nombre_animal': request.json['Nombre_animal'],
        'Raza': request.json['Raza'],
        'Genero': request.json['Genero']

    })
    return jsonify(str(id))

@app.route('/animals', methods=['GET'])
def getAnimals():
    animal= []
    for doc in db.find():
        animal.append({
            '_id': str(doc['_id']),
            'Nombre_animal': doc['Nombre_animal'],
            'Raza': doc['Raza'],
            'Genero': doc['Genero']
        })
    return jsonify(animal)

@app.route('/animal/<id>', methods=['GET'])
def getAnimal(id):
    animal= db.find_one({
        '_id': ObjectId(id)
    })
    return jsonify({
        '_id': str(animal['_id']),
        'Nombre_animal': animal['Nombre_animal'],
        'Raza': animal['Raza'],
        'Genero': animal['Genero']
    })

@app.route('/animals/<id>', methods=['DELETE'])
def deletanimals(id):
    db.delete_one({
        '_id': ObjectId(id)
    })
    return jsonify({"message":"Deleting"})

@app.route('/animals/<id>', methods=['PUT'])
def updateanimals(id):
    db.update_one({
        '_id': ObjectId(id)
    },
    {
        '$set': {
            'Nombre_animal': request.json['Nombre_animal'],
            'Raza': request.json['Raza'],
            'Genero': request.json['Genero']
            }})
    return jsonify({"message":"animals updated"})

if __name__ == '__main__':
    app.run(debug=True)