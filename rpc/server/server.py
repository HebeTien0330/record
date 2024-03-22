from importlib import import_module
from socket import socket, AF_INET, SOCK_STREAM
from ..defines import SERVER_CONNECT_LIMIT
from ..utils import getLocalIp, Functor
import json
import pickle

 

class rpcServer:

    def __init__(self, ip, port, buffSize):
        self.m_ip = ip
        self.m_port = port
        self.m_buffSize = buffSize
        self.m_socket = socket(AF_INET, SOCK_STREAM)
        self.m_route = {}
        
    def afterInit(self):
        self.m_socket.bind((self.m_ip, self.m_port))
        self.m_socket.listen(SERVER_CONNECT_LIMIT)

    def accept(self):
        client, addr = self.m_socket.accept()
        ip = addr[0]
        localIp = getLocalIp()
        for serverId in g_Route:
            serverInfo = g_Route[serverId]
            if serverInfo["ip"] == "localhost":
                serverIp = localIp
            else:
                serverIp = serverInfo["ip"]
            if serverIp != ip:
                continue
            self.m_route[serverId] = client

    def recv(self):
        for client in self.m_route.values():
            messageSize = client.recv(self.m_buffSize).decode()
            if not messageSize:
                continue
            message = client.recv(messageSize)
            message = pickle.loads(message)
            self.execRemoteRequest(message)
            
    def execRemoteRequest(self, message):
        funcPath = message.getFunc()
        args = message.getArgs()
        cb = message.getCallBack()
        func = import_module(funcPath)
        ret = func(*args)
        cb = Functor(cb, ret)
        message.m_cb = cb



def initRouteTable():
    with open("../route.json") as routeTable:
        route = json.loads(routeTable.read())
        route = dict(route)
        return route


if "g_RouteTable" not in globals():
    global g_Route
    g_Route = initRouteTable()
