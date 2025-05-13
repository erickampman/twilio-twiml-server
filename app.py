from flask import Flask, request, Response
import logging

def clean_twiml(xml_str):
    return xml_str.encode("utf-8").lstrip()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/outbound", methods=["GET", "POST"])
def outbound():
    to_number = request.values.get("To", None)
    logging.info(f"Received request with To={to_number}")

    if not to_number:
        msg = "<Response><Say>No destination number provided</Say></Response>"
        logging.info(f"Responding with: {msg}")
        return Response(msg.strip(), mimetype="text/xml")

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?><Response><Dial callerId="+18885974354"><Number>{to_number}</Number></Dial></Response>"""

    logging.info(f"Responding with: {twiml}\n")
    return Response(
        twiml.encode("utf-8"),
        headers={"Content-Type": "application/xml; charset=utf-8"}
    )


@app.route("/")
def index():
    return "Twilio TwiML Server is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
