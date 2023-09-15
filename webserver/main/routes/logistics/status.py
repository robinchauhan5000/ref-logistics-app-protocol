from flask import g, request
from flask_expects_json import expects_json
from flask_restx import Namespace, Resource, reqparse
from jsonschema import validate
from main.logger.custom_logging import log
import json

from main import constant
from main.models.ondc_request import OndcDomain
from main.repository.ack_response import get_ack_response
from main.service import send_message_to_queue_for_given_request
from main.service.common import dump_request_payload
from main.utils.schema_utils import get_json_schema_for_given_path, get_json_schema_for_response

status_namespace = Namespace('status', description='Status Namespace')


@status_namespace.route("/v1/status")
class StatusOrder(Resource):
    path_schema = get_json_schema_for_given_path('/status')

    @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/status')
        resp = get_ack_response(ack=True)
        payload = request.get_json()
        log(json.dumps({f'{request.method} {request.path} req_body': json.dumps(payload)}))
        dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
        message = {
            "request_type": f"{OndcDomain.LOGISTICS.value}_status",
            "message_ids": {
                "status": payload[constant.CONTEXT]["message_id"]
            }
        }
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp


@status_namespace.route("/v1/on_status")
class OnSelectOrder(Resource):
    path_schema = get_json_schema_for_given_path('/on_status')

    @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/on_status')
        resp = get_ack_response(ack=True)
        payload = request.get_json()
        dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
        message = {
            "request_type": f"{OndcDomain.LOGISTICS.value}_on_status",
            "message_ids": {
                "on_status": payload[constant.CONTEXT]["message_id"]
            }
        }
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp
