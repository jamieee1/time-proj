from flask import Flask, jsonify, render_template
import datetime as dt
import socket
import struct

app = Flask(__name__)

def RequestTimefromNtp(addr):
    REF_TIME_1970 = 2208988800  # Reference time
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    client.sendto(data, (addr, 123))
    data, address = client.recvfrom(1024)
    if data:
        t = struct.unpack('!12I', data)[10]
        t -= REF_TIME_1970
    return t

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/get-time', methods = ['POST', 'GET'])
def get_time():
    time_now = RequestTimefromNtp('europe.pool.ntp.org')
    return jsonify(time_now)


if __name__ == '__main__':
    app.run(debug=True)
