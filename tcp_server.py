import socket
import sys
import argparse
import json
import time
import RPi.GPIO as gpio

host = ''
data_payload = 4096
backlog = 1

#
DS = 16     # Serial Data
STCP = 20  # Latch
SHCP = 21  # Clock
#
DS2 = 26
STCP2 = 19
SHCP2 = 13

#
IC_7447_A = 2
IC_7447_B = 3
IC_7447_C = 4
IC_7447_D = 17


#
MachineInfo={}

#
LED_STATE = [0,128,192,224,240,248,252,254,255] #0 1 2 3 4 5 6 7 8

def shiftout(byte,outPipe):
    if(outPipe == 1):
        ds =  DS     # Serial Data
        stcp = STCP # Latch
        shcp = SHCP  # Clock
    else:
        ds =  DS2     # Serial Data
        stcp = STCP2 # Latch
        shcp = SHCP2  # Clock

    gpio.output(stcp, 0)
    b = ''
    for x in range(8):
        bit = ((byte >> x) & 1)
        b = b + str(bit)
        gpio.output(ds, bit)
        gpio.output(shcp, 1)
        gpio.output(shcp, 0)

    # print(b[::-1])
    gpio.output(stcp, 1)

def showServerIP():
    return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

def showMonitorState():
    cpuModel = MachineInfo.get('CPU_Model','unkonw')
    cpuCount = MachineInfo.get('CPU_Count','unkonw')
    cpuCountLogical = MachineInfo.get('CPU_Count_Logical','unkonw')
    ramTotalSize = MachineInfo.get('RAM_Total_Size','unkonw')
    print("Machine Info:",cpuModel,cpuCount,cpuCountLogical,ramTotalSize)

def mapStateToLed(usedPrecent,pipNumber):
        if(usedPrecent==0):
            shiftout(LED_STATE[0],pipNumber)
        elif(usedPrecent<=12.5):
            shiftout(LED_STATE[1],pipNumber)
        elif(usedPrecent<=25.0):
            shiftout(LED_STATE[2],pipNumber)
        elif(usedPrecent<=37.5):
            shiftout(LED_STATE[3],pipNumber)
        elif(usedPrecent<=50.0):
            shiftout(LED_STATE[4],pipNumber)
        elif(usedPrecent<=62.5):
            shiftout(LED_STATE[5],pipNumber)
        elif(usedPrecent<=75.0):
            shiftout(LED_STATE[6],pipNumber)
        elif(usedPrecent<=87.5):
            shiftout(LED_STATE[7],pipNumber)
        elif(usedPrecent<=100):
            shiftout(LED_STATE[8],pipNumber)
        else:
            shiftout(0,pipNumber)


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
        cpuUsed = float(data.get('CPU_PERCENT',0.0))
        memUsed = float(data.get('MEM_USED',0.0))
        mapStateToLed(cpuUsed,1)
        mapStateToLed(memUsed,2)
        print(cpuUsed,memUsed)
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
    #init
    gpio.setmode(gpio.BCM)
    gpio.setup(DS, gpio.OUT)
    gpio.setup(SHCP, gpio.OUT)
    gpio.setup(STCP, gpio.OUT)

    gpio.setup(DS2, gpio.OUT)
    gpio.setup(SHCP2, gpio.OUT)
    gpio.setup(STCP2, gpio.OUT)

    gpio.setup(IC_7447_A,gpio.OUT)
    gpio.setup(IC_7447_B,gpio.OUT)
    gpio.setup(IC_7447_C,gpio.OUT)
    gpio.setup(IC_7447_D,gpio.OUT)

    #test
    gpio.output(IC_7447_A,1)
    gpio.output(IC_7447_B,0)
    gpio.output(IC_7447_C,0)
    gpio.output(IC_7447_D,0)

    #
    for x in range(9):
        shiftout(LED_STATE[x],1)
        shiftout(LED_STATE[x],2)
        time.sleep(0.05)
    #
    for x in range(9):
        shiftout(LED_STATE[8-x],1)
        shiftout(LED_STATE[8-x],2)
        time.sleep(0.05)

    #
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, default=8080)
    given_args = parser.parse_args()
    port = given_args.port
    print(showServerIP())
    runSocketServer(port)