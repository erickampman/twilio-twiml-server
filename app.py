from urllib.parse import urlparse

@app.route("/outbound", methods=["GET", "POST"])
def outbound():
    to_param = request.values.get("To", "")
    logging.info(f"Raw To param: {to_param}")
    logging.info(f"Incoming request values: {request.values}")

    # Try to extract the phone number if it's a SIP URI
    if to_param.startswith("sip:"):
        try:
            parsed = urlparse(to_param)
            to_number = parsed.path  # e.g. '+15102195558'
        except Exception as e:
            logging.error(f"Failed to parse SIP URI: {e}")
            to_number = ""
    else:
        to_number = to_param

    if not to_number:
        msg = "<Response><Say>No destination number provided</Say></Response>"
        logging.info(f"Responding with: {msg}")
        return Response(msg, content_type="application/xml; charset=utf-8")

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?><Response><Dial callerId="+18885974354"><Number>{to_number}</Number></Dial></Response>"""
    logging.info(f"Responding with: {twiml}")
    return Response(twiml.encode("utf-8"), content_type="application/xml; charset=utf-8")
