import os
from time import sleep

##### Config #####
minTemp = 8
maxTemp = 90
ipmiAddress = "192.168.1.33"
ipmiUser = "admin"
ipmiPassword = "password"
fanCurve = lambda x: 0.1 if x < 0.5 else 0.2 if x < 0.7 else x
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

lastSpeed = -1
while True:
    currentTemp = getMaxTemp()
    percentage = round((currentTemp-minTemp) / (maxTemp-minTemp), 2)
    newSpeed = fanCurve(percentage)
    if not lastSpeed == newSpeed:
        setFanSpeed(newSpeed)
        print(f"Fan speed set to {round(newSpeed*100)}% (temp: {currentTemp}°C, {round(percentage*100)}%)")
        lastSpeed = newSpeed

    sleep(1)