from client.client import ChatClient
from utils import getLocalIp
from defines import SERVER_PORT, BUFFERSIZE

def main():
    ip = getLocalIp()
    client = ChatClient(ip, SERVER_PORT, BUFFERSIZE)
    client.run()


if __name__ == "__main__":
    main()