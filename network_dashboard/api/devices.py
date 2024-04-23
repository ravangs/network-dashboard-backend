import logging
from flask import Blueprint, request, jsonify
from network_dashboard.db import db
from flask_cors import CORS
from network_dashboard.configuration.configure import configure_router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

devices_api = Blueprint('devices_api', __name__, url_prefix='/api/v1/devices')
CORS(devices_api)

@devices_api.route('/', methods=['GET'])
def get_all_devices():
    devices = list(db.devices.find({}, {'_id': False, 'password': False}))
    logging.info("Fetched all devices")
    return jsonify({'devices': devices}), 200

@devices_api.route('/<string:hostname>', methods=['GET'])
def get_single_device(hostname):
    device = db.devices.find_one({'hostname': hostname}, {'_id': False, 'password': False})
    if device:
        logging.info(f"Device found: {hostname}")
        return jsonify({'device': device}), 200
    else:
        logging.warning(f"Device not found: {hostname}")
        return jsonify({'message': 'Device not found'}), 404

@devices_api.route('/', methods=['POST'])
def create_device():
    data = request.get_json()
    logging.info(f"Attempting to create device with hostname: {data['hostname']}")
    try:
        new_device = {
            'management_ip': data['management_ip'],
            'hostname': data['hostname'],
            'username': data['username'],
            'password': data['password'],
            'ospf': data.get('ospf'),
            'bgp': data.get('bgp'),
            'interfaces': data.get('interfaces'),
            'ipv6': data.get('ipv6'),
        }
        db.devices.insert_one(new_device)
        configure_router(new_device)
        logging.info(f"Device created and configured successfully: {data['hostname']}")
        return jsonify({'message': 'Device added successfully'}), 201
    except Exception as e:
        logging.error(f"Failed to create device: {data['hostname']}, Error: {str(e)}")
        return jsonify({'message': 'Failed to create device'}), 500

@devices_api.route('/<string:hostname>', methods=['PUT'])
def update_device(hostname):
    data = request.get_json()
    logging.info(f"Attempting to update device: {hostname}")
    try:
        update_fields = {
            'management_ip': data['management_ip'],
            'hostname': data['hostname'],
            'username': data['username'],
            'password': data['password'],
            'ospf': data.get('ospf'),
            'bgp': data.get('bgp'),
            'interfaces': data.get('interfaces'),
            'ipv6': data.get('ipv6'),
        }
        result = db.devices.update_one({'hostname': hostname}, {'$set': update_fields})
        if result.modified_count:
            configure_router(update_fields)
            logging.info(f"Device updated successfully: {hostname}")
            return jsonify({'message': 'Device updated successfully'}), 200
        else:
            logging.warning(f"No updates made or device not found: {hostname}")
            return jsonify({'message': 'No updates made or device not found'}), 404
    except Exception as e:
        logging.error(f"Failed to update device: {hostname}, Error: {str(e)}")
        return jsonify({'message': 'Failed to update device'}), 500
