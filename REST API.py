from flask import Flask, request
from datetime import datetime
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

# Store all received messages in a dictionary.
# The room ID is used as a key and the messages stored in a list as the value
# THIS IS NOT HOW IT WOULD BE DONE IN PRODUCTION, A DATABASE WOULD BE USED.
MESSAGE_STORE = {}

app = Flask(__name__)

@app.route("/send", methods=["POST"])
def send():
    """API Endpoint to send message (add it to MESSAGE_STORE)"""
    try:
        new_message = request.json
    except BadRequest and UnsupportedMediaType:  # Catch if non-json content is sent
        return {"error": "Invalid JSON"}, 400
    
    # Check API Request is in specified format
    if len(request.json.keys()) != 3:
        return {"error": "Invalid request format"}, 400  # Status code 400 = Bad request

    if not new_message.get("room_id"):
        return {"error": "Room ID Not Provided"}, 400  # Status code 400 = Bad request
    
    if not new_message.get("from"):
        return {"error": "No from username"}, 400  # Status code 400 = Bad request

    if not new_message.get("message"):
        return {"error": "No message text provided"}, 400  # Status code 400 = Bad request

    # Add timestamp to message (as unix timestamp)    
    new_message["sent_at"] = datetime.now().timestamp()
    
    # Store message alongside any existing messages
    MESSAGE_STORE[new_message.get("room_id")] = MESSAGE_STORE.get(new_message.get("room_id"), []) + [new_message]

    return new_message, 200  # Status code 200 = OK
    

@app.route("/receive", methods=["POST"])
def receive():
    """Request a list of messages sent to specified room."""

    try:
        room_id = request.json.get("room_id")
    except BadRequest and UnsupportedMediaType:  # Catch if non-json content sent
        return {"error": "Invalid JSON"}, 400

    # Check API Request valid
    if not room_id:
        return {"error": "Room ID Not Provided"}, 400  # Status code 400 = Bad Request
    
    if len(request.json.keys()) > 1:
        return {"error": "Invalid request format"}, 400  # Status code 400 = Bad Request

    # Send list of messages back from MESSAGE_STORE
    return {
        "room": room_id,
        "messages": MESSAGE_STORE.get(room_id, [])
    }

@app.route("/rooms", methods=["GET"])
def rooms():
    """Retrieve a list of all currently active rooms."""
    return {"rooms": list(MESSAGE_STORE.keys())}

@app.route("/<path:requested_endpoint>", methods=["GET", "POST"])
def not_found(requested_endpoint):
    """Return a 404 Error if no such endpoint exists"""
    return {"error": "Endpoint not found"}, 404

if __name__ == "__main__":
    app.run(debug=True)