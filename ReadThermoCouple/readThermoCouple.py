import serial
import sys
import time
import datetime
import numpy as np
from thermister import *
import matplotlib.pyplot as plt
import os

# Set port name
ser = serial.Serial('COM6',9600)

# Initialize variables for speeeeeed
sessionName = 'test_001'
index = 0
temperature1 = [0.0]*80000
temperature2 = [0.0]*80000
temperature3 = [0.0]*80000
temperature4 = [0.0]*80000
toggle = [0]*80000
fcsv = open(sessionName + '.csv','w+')
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
    bytesToRead = bytesToRead + ser.inWaiting()
    if bytesToRead > 20:
        data = str(ser.read(bytesToRead))
        data_split = data[2:-1].split(',')
        if len(data_split) < 6:
            # Parse thermocouple data
            temperature1[index] = ((float(data_split[0]) - 1.25)/.005 * 9.0 / 5.0) + 32.0
            temperature2[index] = ((float(data_split[1]) - 1.25)/.005 * 9.0 / 5.0) + 32.0
            
            # Parse thermister data
            volt3 = float(data_split[3])
            volt4 = float(data_split[4])
            resistor3 = voltDivR1( 5.0, volt3, R2)
            resistor4 = voltDivR1( 5.0, volt4, R2)
            temperature3[index] = K2F(steinhartHartTemp(coe[0], coe[1], coe[2], resistor3))
            temperature4[index] = K2F(steinhartHartTemp(coe[0], coe[1], coe[2], resistor4))
            
            # Grab toggle value
            toggle[index] = data_split[2]
            outputStr = '{:.2f}, {:.2f}, '.format(temperature1[index],temperature2[index])
            outputStr = outputStr + '{}, {:.2f}, {:.2f}'.format(toggle[index],temperature3[index],temperature4[index])
            sys.stdout.write(str(index) + ': ' + outputStr + '\n')
            index = index + 1
            fcsv.write(outputStr + '\n')
        bytesToRead = 0
    if bytesToRead < 21:
        bytesToRead = 0
    
    # Decide how often to make plots and save data to update webpage
    if np.mod(index,10) == 0:
        ct = datetime.datetime.now()
        # Add all values to dict for export to webpage
        data_dict['SET_MEAT_TYPE'] = 'Pork (Default)'
        data_dict['SET_DESIREDTEMP'] = '{:.1f}'.format(200.0)
        data_dict['SET_CURRENTDURATION'] = '{:.2f}'.format(index / 3600.0)
        data_dict['SET_TIME_REMAINING'] = 'TODO'
        data_dict['SET_PROB_1'] = '{:.2f}'.format(temperature3[index-1])
        data_dict['SET_PROBE_SLOPE_1'] = 'TODO'
        data_dict['SET_PROBE_2'] = '{:.2f}'.format(temperature4[index-1])
        data_dict['SET_PROBE_SLOPE_2'] = 'TODO'
        data_dict['SET_SMOKER_1'] = '{:.2f}'.format(temperature1[index-1])
        data_dict['SET_SMOKER_2'] = '{:.2f}'.format(temperature2[index-1])
        data_dict['SET_AVERAGESMOKER'] = '{:.2f}'.format(np.mean(temperature1[1:index-1]))
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
    elif np.mod(index+4,10) == 0:
        if os.path.exists('../MOVEMOTOR.txt'):
            with open('../MOVEMOTOR.txt','r') as mm:
                motor_cmd = float(mm.read())
            os.remove('../MOVEMOTOR.txt')
            if motor_cmd > 0:
                ser.write(b'1')
            elif motor_cmd < 0:
                ser.write(b'2')
        time.sleep(0.1)
    else:
        time.sleep(0.1)


ff.close()



