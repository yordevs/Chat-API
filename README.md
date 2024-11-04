# Chat API Reference
The chat API is designed to be an incredibly simple REST API to be used as an educational tool when learning about APIs.

No authentication is required however ensure you have `"Content-Type: application/json"` in your request header.

## Endpoints:
### POST /send
Sends a message into a specified room. Request is stored in MESSAGE_STORE until server restarted.

*Example Request:*
```json
{
    "room_id": "Will Test Room",
    "from": "Will Hall",
    "message": "Hello, what are you doing at 17:00 on Wednesday?"
}
```

*Example Response:*
```json
{
    "room_id": "Will Test Room",
    "from": "Will Hall",
    "message": "Hello, what are you doing at 17:00 on Wednesday?",
    "sent_at": 1730758663.598467
}
```
Note: The `sent_at` field returns a timestamp in the relation to the [unix epoch](https://www.epochconverter.com/).

### POST /receive
Receives all messages that have previously been sent to the specified room.

*Example Request:*
```json
{
    "room_id": "Will Test Room"
}
```

*Example Response:*
```json
{
    "room_id": "Will Test Room",
    "messages": [
        {
            "room_id": "Will Test Room",
            "from": "Will Hall",
            "message": "Hello, what are you doing at 17:00 on Wednesday?",
            "sent_at": 1730758663.598467
        },
        {
            "room_id": "Will Test Room",
            "from": "Will Hall",
            "message": "Because there is an excellent session being run in PZA/113",
            "sent_at": 1730758663.53237
        }
    ]
    
}
```

*Example Response (No Messages):*
```json
{
    "room_id": "Will Test Room",
    "messages": []
    
}
```

Note: The `sent_at` field returns a timestamp in the relation to the [unix epoch](https://www.epochconverter.com/).

### GET /rooms
Returns a list of all rooms that currently contain messages.

*Example Response:*
```json
{
    "rooms": [
        "Will Test Room"
    ]
}
```

## Error Responses
Error responses may be returned if the request is an invalid format or if an invalid endpoint is requested. An invalid format will result in a status code `400` and an unknown endpoint will return `404`.

A JSON formatted response may provide an additional error message.

*Example error response:*
```json
{
    "error": "room_id not provided"
}
```