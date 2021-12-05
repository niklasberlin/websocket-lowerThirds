# Tornado WebSocket example

This is a websocket example for lower Thirds written in python.

## Installation

1. `pip install -r requirements.txt`

2. `python app.py`

3. http://localhost:8888/

4. Send a REST call:

## REST API examples

Set the first line ot the lower Third to "lineone" and the second line to "linetwo", the lower third will be displayed for 4000ms:
- `curl "http://localhost:8888/api?l1=lineone&l2=linetwo&d=4000"`


## License

MIT
