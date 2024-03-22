from socket import socket, AF_INET, SOCK_STREAM
import time
import pickle
import sys

class rpcClient:

    def __init__(self, ip, port, buffSize):
        self.m_ip = ip
        self.m_port = port
        self.m_buffSize = buffSize
        self.m_socket = socket(AF_INET, SOCK_STREAM)
        self.m_messageId = 1
        self.m_messageSet = {}
    
    def connect(self):
        self.m_socket.connect((self.m_ip, self.m_port))

    def callRemoteFunc(self, func, args, cb):
        message = Message(self.m_messageId, func, args, cb)
        self.m_messageSet[self.m_messageId] = message
        self.m_messageId += 1
        byteMsg = pickle.dumps(message)
        size = sys.getsizeof(byteMsg)
        size = bytes(size).zfill(self.m_buffSize)
        message = size + byteMsg
        self.m_socket.send(message)

    def getResponse(self):
        messageSize = self.m_socket.recv(self.m_buffSize).decode()
        message = self.m_socket.recv(messageSize)
        message = pickle.loads(message)
        cb = message.getCallBack()
        try:
            cb()
        except:
            pass
        finally:
            del self.m_messageSet[message.m_id]


"""
rpc message
用于封装rpc消息, 包含序号、远程函数路径、执行参数、回调函数
通过定时器检查回调是否超时, 如果超时则进行超时处理
"""
class Message:

    def __init__(self, id, func, args, cb):
        self.m_id = id
        self.m_func = func
        self.m_args = args
        self.m_cb = cb
        self.m_createTime = time.time()

    def getFunc(self):
        return self.m_func
    
    def getArgs(self):
        return self.m_args
    
    def getCallBack(self):
        return self.m_cb

    def checkTimeOut(self, curTime):
        pass


