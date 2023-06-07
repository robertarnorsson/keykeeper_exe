import platform
import socket

def getSystemInfo():
    try:
        info={}
        info['hostname']=socket.gethostname()
        info['processor']=platform.processor()
        return info
    except Exception as e:
        print(e)
