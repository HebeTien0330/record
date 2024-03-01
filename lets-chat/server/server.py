from .defines import SERVER_CONNECT_LIMIT
from socket import socket, AF_INET, SOCK_STREAM
from multiprocessing import Process, Queue
import time
import asyncio
import copy

class ChatServer:

    def __init__(self, ip, port, buffSize):
        self.m_ip = ip
        self.m_port = port
        self.m_buffSize = buffSize
        self.m_socket = socket(AF_INET, SOCK_STREAM)
        self.init()
        self.m_ipList = []
        self.m_queueMap = {}

    def init(self):
        self.m_socket.bind((self.m_ip, self.m_port))
        self.m_socket.listen(SERVER_CONNECT_LIMIT)
        self.m_socket.setblocking(False)    # 使用非阻塞模式等待连接，避免主循环阻塞

    def createQueue(self, ip):
        if ip in self.m_queueMap:
            queue = self.m_queueMap[ip]
            return queue
        queue = Queue()
        self.m_queueMap[ip] = queue
        self.m_ipList.append(ip)
        return queue

    # 消息检查任务，循环检查全部队列是否有新消息，若有则push进所有队列
    async def checkProcess(self):
        queueMap = copy.copy(self.m_queueMap)
        for ip, queue in queueMap.items():
            if (queue.empty()):
                continue
            message = queue.get()
            if message == "exit":
                del self.m_queueMap[ip]
            self.systemMessage(message)

    # 广播系统消息
    def systemMessage(self, message):
        for ip, queue in self.m_queueMap.items():
            print(f"send message to {ip} {message}")
            queue.put(message) 

    def run(self):
        while True:
            time.sleep(0.1)
            try:
                client, addr = self.m_socket.accept()
                ip = addr[0]
                self.systemMessage(f"{ip} join in the chat")
                queue = self.createQueue(ip)
                chatProcess = ChatProcess(ip, client, self.m_buffSize, queue)
                chatProcess.create()
            except BlockingIOError:     # TODO: 捕获错误消耗太高，寻找更适合的实现方式
                continue
            finally:
                asyncio.run(self.checkProcess())


class ChatProcess:

    def __init__(self, ip, client, buffSize, queue):
        self.m_ip = ip
        self.m_client = client
        self.m_buffSize = buffSize
        self.m_queue = queue

    def create(self):
        process = Process(target=self.loop)
        self.m_process = process
        process.start()

    def createMessage(self, message):
        nickName, text = message.split("|")
        timestamp = int(round(time.time() * 1000))
        return f"{timestamp}|{self.m_ip}|{nickName}|{text}"

    def sendMessage(self):
        if self.m_queue.empty():
            return
        message = self.m_queue.get().encode()
        self.m_client.send(message)

    def loop(self):
        while True:
            message = self.m_client.recv(self.m_buffSize).decode()
            if message == "exit":
                self.m_queue.put("exit")
                print(f"{self.m_ip} has been exit")
                self.m_client.close()
                break
            message = self.createMessage(message)
            self.m_queue.put(message)
            self.sendMessage()
