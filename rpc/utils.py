import socket

# 打包函数
class Functor():

    def __init__(self, func, *args, **kwargs):
        self.m_func = func
        self.m_args = args
        self.m_kwargs = kwargs

    def __call__(self, *args, **kwargs):
        newArgs = tuple(list(self.m_args) + list(args))
        newKwargs = dict(list(self.m_kwargs.items()) + list(kwargs.items()))
        return self.m_func(*newArgs, **newKwargs)


def getLocalIp():
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    return ip