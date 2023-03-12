from project.app import app
import socket


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

ip_address = get_ip_address()



if __name__ == '__main__':
    app.run(debug=True, host = ip_address, port=5000)

