from flask import Blueprint, request, jsonify
from network_dashboard.db import db
import json

devices_api = Blueprint('devices_api', __name__, url_prefix='/api/v1/devices')

@devices_api.route('/', methods=['GET'])
def get_all_devices():
    devices = list(db.devices.find({}, {'_id': False, 'password': False}))
    return jsonify({'devices': devices}), 200

@devices_api.route('/<string:hostname>', methods=['GET'])
def get_single_device(hostname):
    device = db.devices.find_one({'hostname': hostname}, {'_id': False, 'password': False})
    if device:
        return jsonify({'device': device}), 200
    else:
        return jsonify({'message': 'Device not found'}), 404

@devices_api.route('/', methods=['POST'])
def create_device():
    data = request.get_json()
    new_device = {
        'ip_address': data['ip_address'],
        'hostname': data['hostname'],
        'username': data['username'],
        'password': data['password'],
        'ospf': json.loads(data['ospf']) if 'ospf' in data else None,
        'bgp': json.loads(data['bgp']) if 'bgp' in data else None,
        'interfaces': json.loads(data['interfaces']) if 'interfaces' in data else None
    }
    db.devices.insert_one(new_device)
    return jsonify({'message': 'Device added successfully'}), 201

@devices_api.route('/<string:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.get_json()
    update_fields = {
        'ip_address': data['ip_address'],
        'hostname': data['hostname'],
        'username': data['username'],
        'password': data['password'],
        'ospf': json.loads(data['ospf']) if 'ospf' in data else None,
        'bgp': json.loads(data['bgp']) if 'bgp' in data else None,
        'interfaces': json.loads(data['interfaces']) if 'interfaces' in data else None
    }
    result = db.devices.update_one({'_id': device_id}, {'$set': update_fields})
    if result.modified_count:
        return jsonify({'message': 'Device updated successfully'}), 200
    else:
        return jsonify({'message': 'No updates made or device not found'}), 404
