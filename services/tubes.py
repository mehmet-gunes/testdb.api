import uuid

from flask import Blueprint, jsonify, request

from repository.db import db
from repository.models import Tube, User
from repository.schemas import TubeSchema

root = Blueprint('root', __name__)
# URL prefix with /tube
test_tube = Blueprint('test_tube', __name__)


# Get registered test tubes
@root.route('/', methods=['GET'])
def get_registered():
    """
    method is called with root URL .../
    :return: the tubes with 'registered' status
    """
    registered_tubes = Tube.query.filter_by(status='registered').all()
    tubes_schema = TubeSchema(many=True)
    result = tubes_schema.dump(registered_tubes)
    return jsonify(result)


# Get all test tube list
@test_tube.route('/', methods=['GET'])
def tubes():
    """
    method is called with .../tube/ URL
    :return: the list of all tubes
    """
    all_tubes = Tube.query.all()
    tubes_schema = TubeSchema(many=True)
    result = tubes_schema.dump(all_tubes)
    return jsonify(result)


# Create a new test tube record
@test_tube.route('/', methods=['POST'])
def post_tube():
    """
    creates a new tube for the given email.
    If barcode is given, it is ensured to be unique; otherwise a new one is generated.
    If user email does not exist, a new user is created.
    If status is not a valid option an error is returned.
    :return:
    """
    try:
        if 'barcode' in request.json:
            if Tube.query.filter_by(barcode=request.json['barcode']).first():
                raise ValueError()
            new_barcode = request.json['barcode']
        else:
            new_barcode = str(uuid.uuid4())
            while Tube.query.filter_by(barcode=new_barcode).first():
                new_barcode = str(uuid.uuid4())

        user = User.query.filter_by(email=request.json['email']).first()
        if not user:
            user = User(request.json['email'])
            db.session.add(user)
            db.session.commit()

        user_id = user.id

        if 'status' in request.json:
            if request.json['status'] not in ['registered', 'received', 'positive', 'negative', 'indeterminate']:
                raise ReferenceError()
            status = request.json['status']
        else:
            status = 'registered'

        new_tube = Tube(new_barcode, status, user_id)
        db.session.add(new_tube)
        db.session.commit()
        tube_schema = TubeSchema()
        return tube_schema.jsonify(new_tube)

    except AttributeError:
        return jsonify({"Error": f"User not found!"}), 400
    except ValueError:
        return jsonify({"Error": f"Barcode {request.json['barcode']} already in use!"}), 400
    except ReferenceError:
        return jsonify({"Error": f"Status {request.json['status']} is not valid!"}), 400


# Get a tube with barcode
@test_tube.route('/<barcode>', methods=['GET'])
def get_tube(barcode):
    """
    :param barcode:
    :return: tube details for the barcode given in the URL
    """
    try:
        tube_record = Tube.query.filter_by(barcode=barcode).first()
        if not tube_record:
            raise ValueError()
        tube_schema = TubeSchema()
        result = tube_schema.dump(tube_record)
        return jsonify(result)
    except ValueError:
        return jsonify({"Error": f"Tube with {barcode} not found!"}), 400


# Delete a tube record using barcode
@test_tube.route('/<barcode>', methods=['DELETE'])
def delete_tube(barcode):
    """
    Included for showing all CRUD operations but is not needed
    :param barcode:
    :return:
    """
    try:
        tube_record = Tube.query.filter_by(barcode=barcode).first()
        if not tube_record:
            raise ValueError()
        Tube.query.filter_by(barcode=barcode).delete()
        db.session.commit()
        return jsonify({"Success": f"Tube with {barcode} deleted!"}), 200
    except ValueError:
        return jsonify({"Error": f"Tube with {barcode} not found!"}), 200


# Update tube status
@test_tube.route('/', methods=['PATCH'])
def update_tubes():
    """
    Updates a list of barcodes with new status.
    If barcode is not registered or status is invalid, they are reported back within the "Skipped"
    :return:
    """
    updated = []
    skipped = []
    for code in request.json:
        tube_record = Tube.query.filter_by(barcode=code).first()
        if tube_record and request.json[code] in ['registered', 'received', 'positive', 'negative', 'indeterminate']:
            tube_record.status = request.json[code]
            db.session.commit()
            updated.append(code)
        else:
            skipped.append(code)

    return jsonify({"Updated": updated, "Skipped": skipped})
