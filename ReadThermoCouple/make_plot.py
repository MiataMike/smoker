import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
from scipy import signal

filename = "pulled_pork_20190520"

# Load filename
data = genfromtxt(filename + '.csv', delimiter = ',')
time = np.arange(0,len(data))

ff = plt.figure(1)
plt.plot(time/3600.,data[:,1])
plt.plot(time/3600.,data[:,0])
plt.ylim([50, 400])
plt.xlim([0, np.cel(np.max(time/3600.))])
plt.xlabel('Time [hr]')
plt.ylabel('Temperature [F]')
plt.title("Smoker Temperature")
plt.grid()

plt.savefig(filename + '_smoker.png')

ff2 = plt.figure(2)
plt.plot(time/3600., data[:,3])
plt.plot(time/3600., data[:,4])
plt.xlim([0, 400])
plt.ylim([0, np.ceil(np.max(time/3600.))])
plt.xlabel('Time [hr]')
plt.ylabel('Temperature [F]')
plt.title('Probe Temperature')
plt.grid()

plt.savefig(filename + '_probe.png')

# Plot filtered probe slopes
b, a = signal.butter(3,0.005,btype='lowpass')
filtData = signalfiltfilt(b,a,data[:,4])
derive = 0.0 * len(filtData)
dt = time[1] - time[0]
for ii in range(0,len(filtData)-1):
    deriv[ii] = 3600.0 * filtDAta[ii+1] - filtData[ii]) / dt

# plot using least squares extrapolation
num = 500
y = [0.0] * (len(data[:,4])-num
for ii in range(0,len(y)):
    temp = np.polyfit(time[ii:ii+num],data[ii:ii+num,4],1)
    y[ii] = temp[0] * 3600.0
    
# Pot using average desamples

aveNum = 20
distNum = 25
y2 = [0.0] * (len(data[:,4]) -aveNum-distNum)
for ii in range(0,len(y2)):
    p1 = np.mean(data[ii:ii+aveNum,4])
    p2 = np.mean(data[ii+distNum:ii+distNum+aveNum,4])
    y2[ii] = 3600.0 * (p2 - p1) / distNum

# Plot
ff3 = plt.figure(3)
plt.plot(time[0:-2]/3600.0,deriv[0:-2])
plt.plot(time[num-1:-1]/3600.0,y)
plt.plot(time[aveNum+distNum01:-1]/3600.0,y2)
plt.xlabel('Time [hrs]')
plt.ylabel('Probe dF/dt [F/hr]')
plt.grid()
plt.ylim([-50, 100])
plt.show()

