import os
from time import sleep

##### Config #####
minTemp = 8
maxTemp = 90
ipmiAddress = "192.168.1.33"
ipmiUser = "admin"
ipmiPassword = "password"
fanCurve = lambda x: max(0.05, pow(x, 5))
##################

def getMaxTemp():
    output = os.popen('sensors').read()
    cpuCount = output.count("Package id")
    temps = [99] * cpuCount

    i = 0
    while True:
        start = output.find("Package id")
        if start < 0: break
        start = start+len("Package id X: +")+1
        end = start + 2

        temps[i] = int(output[start:end].replace('.', ''))
        output = output[end:]
        i += 1

    return max(temps)

def setFanSpeed(percentage):
    percentage = round(percentage*100)

    if percentage < 0: percentage = 0
    if percentage > 100: percentage = 100

    os.system(f"ipmitool -I lanplus -H {ipmiAddress} -U {ipmiUser} -P {ipmiPassword} raw 0x30 0x30 0x02 0xff {hex(percentage)} > /dev/null")

# Enabling manual fan control
os.system(f"ipmitool -I lanplus -H {ipmiAddress} -U {ipmiUser} -P {ipmiPassword} raw 0x30 0x30 0x01 0x00 > /dev/null")

lastSpeed = -1
lastTemp = -1
while True:
    currentTemp = getMaxTemp()
    percentage = round((currentTemp-minTemp) / (maxTemp-minTemp), 2)
    newSpeed = round(fanCurve(percentage), 2)
    if (not lastSpeed == newSpeed) and abs(lastTemp-currentTemp) >= 3:
        setFanSpeed(newSpeed)
        print(f"Fan speed set to {round(newSpeed*100)}% (temp: {currentTemp}°C, {round(percentage*100)}%)")
        lastSpeed = newSpeed
        lastTemp = currentTemp

    sleep(1)