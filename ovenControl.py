import requests
import time
import csv
import numpy as np
import datetime
import sys
import os

def getTemperature(ip):
    url = 'http://' + ip + '/atmocontrol?Temp1Read='
    r = requests.get(url)
    response = r._content.decode('utf-8')
    st = response.find(' ') + 1
    en = response.find(',')
    return float(response[st:en])
    
def setTemperature(ip, temperature):
    url = 'http://' + ip + '/atmocontrol?TempSet=' + str(temperature)
    r = requests.get(url)
    response = r._content.decode('utf-8')
    return response
    
def getProgram(filename):
    rawdat = []
    try:
        with open(filename) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                rawdat.append(row)
        temperatures = [float(x[0]) for x in rawdat]
        waitInMinutes = [float(x[1]) for x in rawdat]
        return temperatures, waitInMinutes
    except:
        print('Problem reading in file. Make sure there are only numbers')

def appendToCSVFile(filename, data):
	try:
		with open(filename, 'a', newline = '') as outfile:
			writer = csv.writer(outfile)
			writer.writerow(data)
	except:
		print("Couldn't write to csv file for some reason")

# Set up IP for communication, and read in the scheduled program
ip = '192.168.100.100'
programFilename = 'program.csv'
logFilename = time.strftime('%Y%m%d_%H%M') + '.csv'
(temperatures, waitInMinutes)  = getProgram( programFilename )
nsteps = len(temperatures)

# Print the planned schedule, and check whether it's all right
os.system('cls')
print("\r\nI've read in the programmed schedule, and I'm going to do:\r\n")
for i in range(nsteps):
    print('%.1f °C for %.0f minutes' % (temperatures[i], waitInMinutes[i]))
print("\r\nAll in all this will take %.0f minutes (= %.1f hours)" % (sum(waitInMinutes), sum(waitInMinutes)/60.0))
print("\r\nIs that what you wanted? [y/n]")
inp = input()
if inp == 'y':
    print("Great, starting...")
else:
    print("Check your schedule again. Shutting down...")
    sys.exit()

# Preallocate some variables for storing log data
loggedTemperatures = np.array([])
setpointTemperatures = np.array([])
loggedTimes = np.array([])

# Store the time at which the step starts, so that we know when to switch to the next one
timeStepStart = datetime.datetime.now()

curStep = 0
timeNextStep = timeStepStart + datetime.timedelta(minutes = waitInMinutes[curStep])
setTemperature(ip, temperatures[curStep])

# Enter loop where we log data, and step if the time is right
try:
    while True:
        curTime = time.time()
        measTemp = getTemperature(ip)
        setTemp = temperatures[curStep]
        loggedTimes = np.append(loggedTimes, curTime)
        loggedTemperatures = np.append(loggedTemperatures, measTemp)
        setpointTemperatures = np.append(setpointTemperatures, setTemp)
        
        print([curTime, setTemp, measTemp])
        appendToCSVFile(logFilename, [curTime, setTemp, measTemp])
    
        # Is it time for the next step yet?
        if datetime.datetime.now() > timeNextStep:
            if curStep <= (nsteps - 2):
                curStep += 1
                setTemperature(ip, temperatures[curStep])
                timeNextStep = datetime.datetime.now() + datetime.timedelta(minutes = waitInMinutes[curStep])
            else:
                # This was the final step, reset the temperature to 20°C
                setTemperature(ip, 20)
                temperatures[curStep] = 20
                
        # Repeat every 10 seconds
        time.sleep(10)
                
except KeyboardInterrupt:
    # When aborted, reset the temperature to 20°C
    setTemperature(ip, 20)