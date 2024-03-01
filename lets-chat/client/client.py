from socket import socket, AF_INET, SOCK_STREAM
import time
import os
import atexit
import asyncio
import threading


class Message:

    def __init__(self, info, msgTime, msgText):
        self.m_info = info
        self.m_time = msgTime
        self.m_text = msgText

    def getMessage(self):
        name, ip = self.m_info
        return f"""
====================================================================
{self.m_time}
{name} | {ip} : {self.m_text} 
====================================================================
"""


class ChatClient:

    def __init__(self, ip, port, buffSize):
        self.m_ip = ip
        self.m_port = port
        self.m_buffSize = buffSize
        self.m_socket = socket(AF_INET, SOCK_STREAM)
        self.m_type = None
        self.m_isInit = False
        self.m_msgRecord = []

    def dealWithMessage(self):
        while True:
            res = self.m_socket.recv(self.m_buffSize).decode()
            msgTime, name, ip, text = res.split("|")
            message = Message([name, ip], msgTime, text)
            if len(self.m_msgRecord) >= 50:
                self.m_msgRecord.pop(0)
            self.m_msgRecord.append(message)

    def connect(self):
        # self.m_socket.setblocking(False)
        self.m_socket.connect((self.m_ip, self.m_port))
        atexit.register(self.exit)

    def exit(self):
        self.m_socket.send(f"exit".encode())

    def initNickName(self):
        print("++++++++++++++++++++++++++")
        nickName = input("please text your nickName: ")
        print("++++++++++++++++++++++++++")
        self.m_nickName = nickName
        self.m_isInit = True

    def displayTips(self):
        print("++++++++++++++++++++++++++")
        print(f"your ip address: {self.m_ip}")
        print(f"your nick name: {self.m_nickName}")
        print("++++++++++++++++++++++++++")
        print("please text something: ")

    async def getUserInput(self):
        userInput = await asyncio.get_event_loop().run_in_executor(None, input, "")
        msg = f"{self.m_nickName}|{userInput}"
        self.m_socket.send(msg.encode())
        os.system("cls")

    def display(self):
        while True:
            time.sleep(0.1)
            displayText = ""
            for message in self.m_msgRecord:
                text = message.getMessage()
                displayText += text
            print(displayText, end="\r", flush=True)

    def run(self):
        self.connect()
        if not self.m_isInit:
            self.initNickName()

        dealProcess = threading.Thread(target=self.dealWithMessage)
        dealProcess.start()
        displayerProcess = threading.Thread(target=self.display)
        displayerProcess.start()

        while True:
            loop2 = asyncio.get_event_loop()
            loop2.call_soon(self.displayTips)
            loop2.run_until_complete(self.getUserInput())
