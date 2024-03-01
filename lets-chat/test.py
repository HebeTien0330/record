from multiprocessing import Process, Queue
import time
import asyncio

def reader(q):
    while True:
        if not q.empty():
            value = q.get(True)
            print(f"get queue value {value}")

async def userInputAsync(q):
    userInput = await asyncio.get_event_loop().run_in_executor(None, input, "")
    q.put(userInput)

def tips():
    print("please text something: \n", end = "\r", flush=True)

def printer(q):
    while True:
        time.sleep(1)
        print("testing")

if __name__ =="__main__":
    q = Queue()
    p1 = Process(target=reader, args=(q,))
    p1.start()

    while True:
        # 创建一个事件循环
        loop = asyncio.get_event_loop()
        # 运行异步函数
        loop.call_soon(tips)
        loop.run_until_complete(userInputAsync(q))
