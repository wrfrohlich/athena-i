#---------------------------------------------------------------------------------------
#
#            Name: Eng. William da Rosa Frohlich
#
#            Project: ATHENA I - API
#
#            Date: 2021.04.19
#
#---------------------------------------------------------------------------------------

import json
import socket
from bottle import Bottle, request

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = ''
port = 18000
address = (server, port)

print ('socket: created')

class API(Bottle):
    def __init__(self):
        super().__init__()
        print("api: initiated")
        self.route('/',method='POST', callback=self.send_request)

    def send_request(self):
        print("api: message received")
        name = request.forms.get('name')
        surname = request.forms.get('surname')
        msg = ("START;" + str(name) + ";" + str(surname))

        sock.sendto(msg.encode('utf-8'), address)
        print("api: package sent")

        if (str(name) == "" and str(surname) == ""):
            return 'Shutting down'
        else:
            return 'Name: {} {}'.format(name, surname)

        sock.close()

if __name__ == '__main__':
    api = API()
    api.run(host='0.0.0.0', port=8080, debug=False)
