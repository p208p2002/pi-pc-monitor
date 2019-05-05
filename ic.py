import RPi.GPIO as gpio

class IC74595():
    def __init__(self,DS,STCP,SHCP):
        self.DS = DS
        self.STCP = STCP
        self.SHCP = SHCP
        gpio.setup(self.DS, gpio.OUT)
        gpio.setup(self.SHCP, gpio.OUT)
        gpio.setup(self.STCP, gpio.OUT)

    def shiftout(self,byte):
        gpio.output(self.STCP, 0)
        b = ''
        for x in range(8):
            bit = ((byte >> x) & 1)
            b = b + str(bit)
            gpio.output(self.DS, bit)
            gpio.output(self.SHCP, 1)
            gpio.output(self.SHCP, 0)

        gpio.output(self.STCP, 1)

class IC7447():
    def __init__(self,A,B,C,D):
        self.A = A # mapping to 7447 input A - D
        self.B = B
        self.C = C
        self.D = D
        gpio.setup(self.A,gpio.OUT)
        gpio.setup(self.B,gpio.OUT)
        gpio.setup(self.C,gpio.OUT)
        gpio.setup(self.D,gpio.OUT)

    def off(self):
        gpio.output(self.A,1)
        gpio.output(self.B,1)
        gpio.output(self.C,1)
        gpio.output(self.D,1)

    def show(self,num):
        if(num == 0):
            gpio.output(self.A,0)
            gpio.output(self.B,0)
            gpio.output(self.C,0)
            gpio.output(self.D,0)
        elif(num == 1):
            gpio.output(self.A,1)
            gpio.output(self.B,0)
            gpio.output(self.C,0)
            gpio.output(self.D,0)
        elif(num == 2):
            gpio.output(self.A,0)
            gpio.output(self.B,1)
            gpio.output(self.C,0)
            gpio.output(self.D,0)
        elif(num == 3):
            gpio.output(self.A,1)
            gpio.output(self.B,1)
            gpio.output(self.C,0)
            gpio.output(self.D,0)
        elif(num == 4):
            gpio.output(self.A,0)
            gpio.output(self.B,0)
            gpio.output(self.C,1)
            gpio.output(self.D,0)
        elif(num == 5):
            gpio.output(self.A,1)
            gpio.output(self.B,0)
            gpio.output(self.C,1)
            gpio.output(self.D,0)
        elif(num == 6):
            gpio.output(self.A,0)
            gpio.output(self.B,1)
            gpio.output(self.C,1)
            gpio.output(self.D,0)
        elif(num == 7):
            gpio.output(self.A,1)
            gpio.output(self.B,1)
            gpio.output(self.C,1)
            gpio.output(self.D,0)
        elif(num == 8):
            gpio.output(self.A,0)
            gpio.output(self.B,0)
            gpio.output(self.C,0)
            gpio.output(self.D,1)
        elif(num == 9):
            gpio.output(self.A,1)
            gpio.output(self.B,0)
            gpio.output(self.C,0)
            gpio.output(self.D,1)