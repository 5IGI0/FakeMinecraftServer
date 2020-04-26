from protocol import TCPSocketConnection, Connection
import json
import base64
from time import time
from random import randint
import os

def get_player_amount(_max, _min, random):
  day_second = time()%86400
  tmp = day_second-43200
  if tmp < 1:
    tmp = tmp*-1
  return int((_max-_min)*(tmp/43200))+randint(random*-1, random)+_min

def handler(client, address, config, connection_id):
    connection_id = hex(connection_id)[2:]
    connection_id = "0"*(10-len(connection_id)) + connection_id
    try:
        print(f"[{connection_id}][info]: new connection from {address[0]}:{address[1]}")
        conn = TCPSocketConnection(client)

        result = conn.read_buffer()

        if result.read_varint() != 0:  # if it isn't minecraft protocol
            print(f"[{connection_id}][warning]: this connection does not use the miencraft protocol !")
            client.close()
            return

        proto_version = result.read_varint()
        host = result.read_utf()
        print(f"[{connection_id}][info]: protocol version :{proto_version}")
        print(f"[{connection_id}][info]: host             :{host}")
        print(f"[{connection_id}][info]: port             :{result.read_ushort()}")

        connection_type = result.read_varint()

        if connection_type == 2:  # login
            buf = conn.read_buffer()
            buf.read_varint()
            print(f"[{connection_id}][info]: login tried with {buf.read_utf()}'s account")
            data = Connection()
            data.write_varint(0)
            with open("kick_payload.json") as fp:
                data.write_utf(json.dumps(json.loads(fp.read())))
            conn.write_buffer(data)
            client.close()
            return
        elif connection_type != 1: # if unkown connection type
            print(f"[{connection_id}][waring]: this client requested an unknown connection type !")
            client.close()
            return

        # status query
        while True:
            result = conn.read_buffer()
            action = result.read_varint()

            if action == 0:
                print(f"[{connection_id}][info]: status requested")
                data = Connection()
                data.write_varint(0)
                with open("status_payload.json") as fp:
                    status = json.load(fp)
                status["version"]["protocol"] = proto_version
                status["players"]["online"] = get_player_amount(config["rush_hour"], config["min_player"], config["random"])
                status["players"]["max"] = config["player_slot"]
                if os.path.isfile("favicon.png"):
                    with open("favicon.png", "rb") as fp:
                        status["favicon"] = "data:image/png;base64,"+base64.b64encode(fp.read()).decode()
                data.write_utf(json.dumps(status))
                conn.write_buffer(data)
            elif action == 1:
                data = Connection()
                data.write_varint(1)
                data.write_long(result.read_long())
                conn.write_buffer(data)
                print(f"[{connection_id}][info]: pong !")
            else:
                print(f"[{connection_id}][warning]: not implemented requests ! {action}")
                break

        client.close()
    except OSError as e: # connection closed
        client.close()
    except Exception as e:
        print(f"[{connection_id}][error]: {e}")
        client.close()