import socket
import sys
import argparse
import json
import time
import RPi.GPIO as gpio
import signal
import sys
from ic import IC74595,IC7447

host = ''
data_payload = 4096
backlog = 1

#
gpio.setmode(gpio.BCM)

#
DS = 16     # Serial Data
STCP = 20  # Latch
SHCP = 21  # Clock

DS2 = 26
STCP2 = 19
SHCP2 = 13

IC_7447_A = 2
IC_7447_B = 3
IC_7447_C = 4
IC_7447_D = 17

#
MachineInfo={}
LED_STATE = [0,128,192,224,240,248,252,254,255] #0 1 2 3 4 5 6 7 8

#
BTN_PIN = 27
DOT_PIN = 22
SERVER_IP = 0

#parts
digNumDisplay = IC7447(IC_7447_A,IC_7447_B,IC_7447_C,IC_7447_D)
cpuLED = IC74595(DS,STCP,SHCP)
ramLED = IC74595(DS2,STCP2,SHCP2)

def signal_handler(sig, frame):
    gpio.cleanup()
    sys.exit(0)

def showIP(channel):
    if (SERVER_IP == 0):
        digNumDisplay.off()
    else:
        for i in range(len(SERVER_IP)):
            if(SERVER_IP[i] != '.'):
                digNumDisplay.show(int(SERVER_IP[i]))
                gpio.output(DOT_PIN, 1)
            else:
                digNumDisplay.off()
                gpio.output(DOT_PIN, 0)
            time.sleep(0.5)
        digNumDisplay.off()
        gpio.output(DOT_PIN, 1)

def showServerIP():
    return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

def showMonitorState():
    cpuModel = MachineInfo.get('CPU_Model','unkonw')
    cpuCount = MachineInfo.get('CPU_Count','unkonw')
    cpuCountLogical = MachineInfo.get('CPU_Count_Logical','unkonw')
    ramTotalSize = MachineInfo.get('RAM_Total_Size','unkonw')
    print("Machine Info:",cpuModel,cpuCount,cpuCountLogical,ramTotalSize)

def mapStateToLed(usedPrecent,pipNumber):
        led = 0
        if pipNumber == 1:
            led = cpuLED
        elif pipNumber == 2:
            led = ramLED

        if(usedPrecent==0):
            led.shiftout(LED_STATE[0])
        elif(usedPrecent<=12.5):
            led.shiftout(LED_STATE[1])
        elif(usedPrecent<=25.0):
            led.shiftout(LED_STATE[2])
        elif(usedPrecent<=37.5):
            led.shiftout(LED_STATE[3])
        elif(usedPrecent<=50.0):
            led.shiftout(LED_STATE[4])
        elif(usedPrecent<=62.5):
            led.shiftout(LED_STATE[5])
        elif(usedPrecent<=75.0):
            led.shiftout(LED_STATE[6])
        elif(usedPrecent<=87.5):
            led.shiftout(LED_STATE[7])
        elif(usedPrecent<=100):
            led.shiftout(LED_STATE[8])
        else:
            led.shiftout(0)


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
    print ("Starting up server  on %s port %s" % server_address)
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
            gpio.output(DOT_PIN, 0)
            lastRecvTime = time.time()
            updateMonitorState(data.decode())
        gpio.output(DOT_PIN, 1)

if __name__ == '__main__':
    #init
    gpio.setup(DOT_PIN, gpio.OUT)
    gpio.setup(BTN_PIN, gpio.IN, pull_up_down=gpio.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    gpio.add_event_detect(BTN_PIN,gpio.RISING,callback=showIP,bouncetime=1000) # Setup event on pin 10 rising edge
    signal.signal(signal.SIGINT, signal_handler)

    #self test
    for x in range(9):
        cpuLED.shiftout(LED_STATE[x])
        ramLED.shiftout(LED_STATE[x])
        digNumDisplay.show(x+1)
        time.sleep(0.05)

    for x in range(9):
        cpuLED.shiftout(LED_STATE[8-x])
        ramLED.shiftout(LED_STATE[8-x])
        digNumDisplay.show(9-x)
        time.sleep(0.05)

    digNumDisplay.off()

    #
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, default=8080)
    given_args = parser.parse_args()
    port = given_args.port
    SERVER_IP=showServerIP()
    print(SERVER_IP)
    runSocketServer(port)