from main.repository.db import get_first_ondc_request
from datetime import datetime

def checkstale(domain, action, message_id, timestamp):
    OndcRequest = get_first_ondc_request(domain=domain, action=action, message_id=message_id)
    if OndcRequest:
        return compare_timestamp(timestamp_db=OndcRequest['context']['timestamp'], timestamp=timestamp)
    else:
        return True

def compare_timestamp(timestamp_db, timestamp):

    db_timestamp = datetime.strptime(timestamp_db, "%Y-%m-%dT%H:%M:%S.%fZ")
    req_timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    return db_timestamp < req_timestamp
 