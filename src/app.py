"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/member/<int:id>', methods=['GET'])
def show_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify("Member not found"), 404



@app.route('/member', methods=['POST'])
def create_member():
    request_json = request.get_json()

    try:
        member = {
            "first_name": request_json.get("first_name"),
            "last_name": "Jackson",
            "id": request_json.get("id"), 
            "age": request_json.get("age"), 
            "lucky_numbers": request_json.get("lucky_numbers")
        }

        added_member = jackson_family.add_member(member)
        return jsonify("Member added successfully"), 201
    except:
        raise APIException('Something went wrong!', status_code=400)


@app.route('/members/<int:id>', methods=["DELETE"])
def delete_member(id):
    member = jackson_family.delete_member(id)
    
    if member:
        return jsonify({"done": True, "message": "Member with ID: " + str(id) + " was successfully deleted"}), 200
    
    return jsonify('bad request'), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
