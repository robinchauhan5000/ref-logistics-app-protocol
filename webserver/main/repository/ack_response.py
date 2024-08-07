def get_ack_response(ack=True, error=None, context=None):
    resp = {
        "context": context,
        "message":
            {
                "ack":
                    {
                        "status": "ACK" if ack else "NACK"
                    }
            }
    }
    resp.update({"error": error}) if error else None
    return resp