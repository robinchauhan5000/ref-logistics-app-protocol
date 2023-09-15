import json
from jsonschema.exceptions import ValidationError

from main.utils.path_utils import get_project_root

f = open(f"{get_project_root()}/schemas/schema.json")
logistics_json_schema = json.load(f)
f = open(f"{get_project_root()}/schemas/schema-v1.json")
logistics_json_schema_v1 = json.load(f)


def transform_json_schema_error(e: ValidationError):
    absolute_path = list(e.absolute_path)
    path_in_str = ""
    for x in absolute_path:
        path_in_str += f"['{x}']" if type(x) == str else f"[{x}]"
    message = e.message
    final_message = f"Validation error: {message} for path: {path_in_str}"
    return final_message


def get_json_schema_for_given_path(path, core_version='1.2.0', request_type='post', domain="logistics"):
    # domain_schema = logistics_json_schema if domain == "logistics" else logistics_json_schema
    domain_schema = logistics_json_schema_v1 if core_version == '1.1.0' else logistics_json_schema
    path_schema = domain_schema['paths'][path][request_type]['requestBody']['content']['application/json']['schema']
    path_schema.update(domain_schema)
    return path_schema


def get_json_schema_for_response(path, core_version='1.2.0', request_type='post', status_code=200, domain="logistics"):
    # domain_schema = logistics_json_schema if domain == "logistics" else logistics_json_schema
    domain_schema = logistics_json_schema_v1 if core_version == '1.1.0' else logistics_json_schema
    path_schema = domain_schema['paths'][path][request_type]['responses'][str(
        status_code)]['content']['application/json']['schema']
    path_schema['title'] = 'Something'
    path_schema.update(domain_schema)
    return path_schema


def get_json_schema_for_component(component):
    path_schema = logistics_json_schema['components']['schemas'][component]
    path_schema['title'] = component
    path_schema.update(logistics_json_schema)
    return path_schema
