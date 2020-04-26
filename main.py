import socket
import json
from connection_handler import handler
from protocol import TCPSocketConnection, Connection

try:
    import thread
except:
    import _thread as thread

with open("config.json") as fp:
    config = json.load(fp)

soc = socket.socket(socket.AF_INET)
soc.bind(('0.0.0.0', config["port"]))
soc.listen(5)

connection_id = 0

try:
    while True:
        client, addr = soc.accept()
        connection_id += 1
        thread.start_new_thread(handler, (client, addr, config, connection_id))
except Exception:
    soc.close()