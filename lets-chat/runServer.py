from server.server import ChatServer
from utils import getLocalIp
from defines import SERVER_PORT, BUFFERSIZE

def main():
    ip = getLocalIp()
    server = ChatServer(ip, SERVER_PORT, BUFFERSIZE)
    server.run()


if __name__ == "__main__":
    main()