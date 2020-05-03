import serial
import sys
import time
import datetime
import numpy as np
from thermister import *
from matplotlib.pyplot as plt


# Set port name
ser = serial.Serial('/dev/ttyACMO')

# Initialize variables for speeeeeed
sessionName = '4th_of_july_pork'
index = 0
temperature1 = [0.0]*80000
temperature2 = [0.0]*80000
temperature3 = [0.0]*80000
temperature4 = [0.0]*80000
toggle = [0]*80000
ff = open(sessionName + '.csv','w+')
bytesToRead = 0
data_dict = {}

# Calculate the steinhart coefficients
Res1 = 345754.2
Res2 = 7094.8
Res3 = 103000.0
coe = steinhartHartCoe(273.15, 373.15, 293.15, Res1, Res2, Res3)

# Thermist resistor value
R2 = 9960 # Ohms, measured

# Clear out cached data
bytesToRead = ser.inWaiting()
data = ser.read(bytesToRead)
bytesToRead = 0

while index < 80000:
    bytesToRead = bytesToRead + ser_inWaiting()
    if byteToRead > 22:
        data =ser.read(bytesToRead)
        data_split = data.split(',')
        if len(data_split) < 6:
            # Parse thermocouple data
            temperature1[index] = ((float(data_split[0]) - 1.25)/.005 * 9.0 / 5.0) + 32.0
            temperature2[index] = ((float(data_split[1]) - 1.25)/.005 * 9.0 / 5.0) + 32.0
            
            # Parse thermister data
            volt3 = float(data_splot[3])
            volt4 = float(data_split[4])
            resistor3 = voltDivR1( 5.0, volt3, R2)
            resistor4 = voltDivR1( 5.0, volt4, R2)
            temperature3[index] = K2F(steinhartHartTemp(coe[0], coe[1], coe[2], resistor3))
            temperature4[index] = K2F(steinhartHartTemp(coe[0], coe[1], coe[2], resistor4))
            
            # Grab toggle value
            toggle[index] = data_split[2]
            outputStr = str(temperature1[index]) + ', ' + str(temperature2[index[) + ', '
            outputStr = outputStr + str(toggle[index[) + ', ' + str(round(temperature3[index],1)) + ', ' + str(round(temperature4[index],1))
            sys.stdout.write(str(index) + ': ' + outputStr + '\n')
            index = index + 1
            ff.write(outputStr + '\n')
        bytesToRead = 0
    if bytesToRead < 23:
        bytesToRead = 0
    
    # Decide how often to make plots and save data to update webpage
    if np.mod(index,10) == 0:
        ct = datetime.datetime.now()
        # Add all values to dict for export to webpage
        data_dict['SET_MEAT_TYPE'] = 'Pork (Default)'
        data_dict['SET_DESIREDTEMP'] = 200.0
        data_dict['SET_CURRENTDURATION'] = index / 3600.0
        data_dict['SET_TIME_REMAINING'] = 'TODO'
        data_dict['SET_PROB_1'] = temperature3[index-1]
        data_dict['SET_PROBE_SLOPE_1'] = 'TODO'
        data_dict['SET_PROBE_2'] = temperature4[index-1]
        data_dict['SET_PROBE_SLOPE_2'] = 'TODO'
        data_dict['SET_SMOKER_1'] = temperature1[index-1]
        data_dict['SET_SMOKER_2'] = temperature2[index-1]
        data_dict['SET_AVERAGESMOKER'] = np.mean(temperature1[1:index-1])
        data_dict['SET_DATAFILENAME'] = sessionName + '.csv'
        data_dict['SET_MEATTRANSIENTTEMP'] = sessionName + '_probe.png'
        data_dict['SET_SMOKERTRANSIENTTEMP'] = sessionName + '_smoker.png'
        data_dict['SET_CURRENTTIME'] = str(ct.month) + '/' + str(ct.day) + '/' + str(ct.year) + ' ' + str(ct.hour) + ':' + str(ct.minute)
        time.sleep(0.1)
    elif np.mod(index+1,10) == 0:
        populateHTML(data_dict)
        time.sleep(0.1)
    elif np.mod(index+2,10) == 0:
        ff = plt.figure(1)
        plt.plot(np.linspace(0,index,index) / 3600.0, temperature1[0:index])
        plt.plot(np.linspace(0,index,index) / 3600.0, temperature2[0:index])
#         plt.ylim([50, 400])
#         plt.xlim([0, np.cel(np.max(time/3600.))])
        plt.xlabel('Time [hr]')
        plt.ylabel('Temperature [F]')
        plt.title("Smoker Temperature")
        plt.grid()

        plt.savefig(sessionName + '_smoker.png')
        plt.clf()
        time.sleep(0.1)
    elif np.mod(index+3,10) == 0:
        ff = plt.figure(2)
        plt.plot(np.linspace(0,index,index) / 3600.0, temperature3[0:index])
        plt.plot(np.linspace(0,index,index) / 3600.0, temperature4[0:index])
#         plt.ylim([50, 400])
#         plt.xlim([0, np.cel(np.max(time/3600.))])
        plt.xlabel('Time [hr]')
        plt.ylabel('Temperature [F]')
        plt.title("Probe Temperature")
        plt.grid()

        plt.savefig(sessionName + '_probe.png')
        plt.clf()
        time.sleep(0.1)
    else:
        time.sleep(0.1)


ff.close()



