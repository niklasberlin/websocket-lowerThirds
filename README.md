# Tornado WebSocket example for Lower Thirds

# do not consider this stable!

This is a websocket example for lower Thirds written in python. It is intended to be used by the xHain Hack and Makespace in Berlin during the second edition of the remote chaos experience (rc3 rev2) from the CCC in 2021.

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
