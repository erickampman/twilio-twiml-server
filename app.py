from flask import Flask, request, Response
from urllib.parse import urlparse
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logging.info(f"Starting app.py execution")

@app.route("/outbound", methods=["GET", "POST"])
def outbound():
    to_param = request.values.get("To", "")
    logging.info(f"Raw To param: {to_param}")

    # Extract phone number from SIP URI if needed
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

@app.route("/")
def index():
    return "Twilio TwiML Server is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
