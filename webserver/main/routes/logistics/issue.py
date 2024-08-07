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


issue_namespace = Namespace('issue', description='Issue Namespace')


@issue_namespace.route("/v1/issue")
class IssueOrder(Resource):
    path_schema = get_json_schema_for_given_path('/issue')

    # @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/issue')
        resp = get_ack_response(ack=True, context=payload[constant.CONTEXT])
        payload = request.get_json()
        log(json.dumps({f'{request.method} {request.path} req_body': json.dumps(payload)}))
        dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
        message = {
            "request_type": f"{OndcDomain.LOGISTICS.value}_issue",
            "message_ids": {
                "issue": payload[constant.CONTEXT]["message_id"]
            }
        }
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp


@issue_namespace.route("/v1/on_issue")
class OnSelectOrder(Resource):
    path_schema = get_json_schema_for_given_path('/on_issue')

    # @expects_json(path_schema)
    def post(self):
        response_schema = get_json_schema_for_response('/on_issue')
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
        dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
        message = {
            "request_type": f"{OndcDomain.LOGISTICS.value}_on_issue",
            "message_ids": {
                "on_issue": payload[constant.CONTEXT]["message_id"]
            }
        }
        send_message_to_queue_for_given_request(message)
        validate(resp, response_schema)
        return resp
