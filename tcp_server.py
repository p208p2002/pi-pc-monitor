import socket
import sys
import argparse
import json
import time

host = ''
data_payload = 4096
backlog = 1

#
MachineInfo={}

def showServerIP():
    return print([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])

def showMonitorState():
    cpuModel = MachineInfo.get('CPU_Model','unkonw')
    cpuCount = MachineInfo.get('CPU_Count','unkonw')
    cpuCountLogical = MachineInfo.get('CPU_Count_Logical','unkonw')
    ramTotalSize = MachineInfo.get('RAM_Total_Size','unkonw')
    print("Machine Info:",cpuModel,cpuCount,cpuCountLogical,ramTotalSize)


def updateMonitorState(jsonStr):
    global MachineInfo
    jsonData={}
    try:
        jsonData = json.loads(jsonStr)
    except:
        print("Parse json data fail")

    eventType = jsonData.get("Type")
    print("Event Type:",eventType)

    #case event type
    if(eventType == 'BASIC_MSG'):
        data = jsonData.get('Data',{})
        MachineInfo = data
    elif(eventType == 'USAGE_MSG'):
        data = jsonData.get('Data',{})
        print(data)
        pass
    else:
        print('unknow event type')

    # final
    showMonitorState()


def runSocketServer(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (host, port)
    print ("Starting up echo server  on %s port %s" % server_address)
    sock.bind(server_address)
    sock.listen(backlog)

    #
    print ("Waiting new client")
    client, address = sock.accept()
    print("Address:",address)

    #time out count
    timeOut = 10.0
    lastRecvTime = time.time()
    nowtime = time.time()
    while True:
        #over 10s no recv new data
        if(nowtime - lastRecvTime >= timeOut):
            print("client lost connect")
            client.close()
            print ("Waiting new client")
            client, address = sock.accept()
            lastRecvTime = time.time()
            nowtime = time.time()

        nowtime = time.time()#refresh time out count
        data = client.recv(data_payload)#recv data
        if data:
            lastRecvTime = time.time()
            updateMonitorState(data.decode())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, default=8080)
    given_args = parser.parse_args()
    port = given_args.port
    showServerIP()
    runSocketServer(port)