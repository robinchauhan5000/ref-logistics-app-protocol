from main.utils.cryptic_utils import verify_authorisation_header
from flask import g, request
from flask_expects_json import expects_json
from flask_restx import Namespace, Resource
from jsonschema import validate
from main.logger.custom_logging import log
import json

from main import constant
from main.models.ondc_request import OndcDomain
from main.repository.ack_response import get_ack_response
from main.service import send_message_to_queue_for_given_request
from main.service.common import dump_request_payload
from main.utils.schema_utils import get_json_schema_for_given_path, get_json_schema_for_response


issue_status_namespace = Namespace(
    'issue_status', description='Issue_status Namespace')


@issue_status_namespace.route("/v1/issue_status")
class issue_statusOrder(Resource):
    path_schema = get_json_schema_for_given_path('/issue_status', '1.0.0')

    # @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/issue_status')
        payload = request.get_json()
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            resp = get_ack_response(ack=False, error="Authorization header missing", context=payload[constant.CONTEXT])
        else:
            bool = verify_authorisation_header(auth_header, payload)
            if bool:
                resp = get_ack_response(ack=False, context=payload[constant.CONTEXT])
            else:
                resp = get_ack_response(ack=True, context=payload[constant.CONTEXT])
        log(json.dumps({f'{request.method} {request.path} req_body': json.dumps(payload)}))
        dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
        message = {
            "request_type": f"{OndcDomain.LOGISTICS.value}_issue_status",
            "message_ids": {
                "issue_status": payload[constant.CONTEXT]["message_id"]
            }
        }
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp


@issue_status_namespace.route("/v1/on_issue_status")
class OnSelectOrder(Resource):
    path_schema = get_json_schema_for_given_path('/on_issue_status')

    # @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/on_issue_status')
        payload = request.get_json()
        resp = get_ack_response(ack=True, context=payload[constant.CONTEXT])
        dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
        message = {
            "request_type": f"{OndcDomain.LOGISTICS.value}_on_issue_status",
            "message_ids": {
                "on_issue_status": payload[constant.CONTEXT]["message_id"]
            }
        }
        print("message----------", message)
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp
