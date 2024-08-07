from main.utils.cryptic_utils import verify_authorisation_header
from flask import request
from main.models.ondc_request import OndcAction
from main.utils.checkstale_utils import checkstale
from flask_expects_json import expects_json
from flask_restx import Namespace, Resource, reqparse
from jsonschema import validate
from main.logger.custom_logging import log
import json

from main import constant
from main.models.error import BaseError
from main.models.ondc_request import OndcDomain
from main.repository.ack_response import get_ack_response
from main.service import send_message_to_queue_for_given_request
from main.service.common import dump_request_payload
from main.utils.schema_utils import get_json_schema_for_given_path, get_json_schema_for_response

search_namespace = Namespace('search', description='Search Namespace')


@search_namespace.route("/v1/search")
class SearchCatalogues(Resource):
    def post(self):
        payload = request.get_json()
        path_schema = get_json_schema_for_given_path('/search', payload[constant.CONTEXT]["core_version"])
        @expects_json(path_schema)

        def innerFunction():
            response_schema = get_json_schema_for_response('/search', payload[constant.CONTEXT]["core_version"])
            if checkstale(domain=OndcDomain.LOGISTICS, action=OndcAction.SEARCH, timestamp=payload[constant.CONTEXT]["timestamp"], message_id=payload[constant.CONTEXT]["message_id"]):
                auth_header = request.headers.get("Authorization")
                if auth_header is None:
                    resp = get_ack_response(ack=False, error="Authorization header missing", context=payload[constant.CONTEXT])
                else:
                    bool = verify_authorisation_header(auth_header, payload)
                    if bool:
                        resp = get_ack_response(ack=False, error="Authorization failed", context=payload[constant.CONTEXT])
                    else:
                        resp = get_ack_response(ack=True, context=payload[constant.CONTEXT])
                log(json.dumps({f'{request.method} {request.path} req_body': json.dumps(payload)}))
                dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
                message = {
                    "request_type": f"{OndcDomain.LOGISTICS.value}_search",
                    "message_ids": {
                        "search": payload[constant.CONTEXT]["message_id"]
                    }
                }
                send_message_to_queue_for_given_request(message)
                validate(resp, response_schema)
                return resp
            else:
                resp = get_ack_response(ack=False)
                log(json.dumps({f'{request.method} {request.path} req_body': json.dumps(payload)}))
                dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
                return resp

        return innerFunction()    


@search_namespace.route("/v1/on_search")
class OnSearch(Resource):
    def post(self):
        payload = request.get_json()
        path_schema = get_json_schema_for_given_path('/on_search', payload[constant.CONTEXT]["core_version"])

        @expects_json(path_schema)
        def innerFunction():
            response_schema = get_json_schema_for_response('/on_search', payload[constant.CONTEXT]["core_version"])
            resp = get_ack_response(ack=True, context=payload[constant.CONTEXT])
            dump_request_payload(payload, domain=OndcDomain.LOGISTICS.value)
            message = {
                "request_type": f"{OndcDomain.LOGISTICS.value}_on_search",
                "message_ids": {
                    "on_search": payload[constant.CONTEXT]["message_id"]
                }
            }
            send_message_to_queue_for_given_request(message)
            validate(resp, response_schema)
            return resp

        return innerFunction()    

