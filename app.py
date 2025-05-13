from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/outbound", methods=["GET", "POST"])
def outbound():
    to_number = request.values.get("To", None)

    if not to_number:
        return Response(
            "<Response><Say>No destination number provided</Say></Response>",
            mimetype="text/xml"
        )

    twiml = twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Dial callerId="+18885974354">
            <Number>{to_number}</Number>
        </Dial>
    </Response>
    """
    return Response(twiml, mimetype="text/xml")

@app.route("/")
def index():
    return "Twilio TwiML Server is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

