import pyabf
import os
import matplotlib.pyplot as plt
filepath = os.path.expanduser('~/Desktop')
filename = 'f1.abf'
fullpath = os.path.join(filepath,'f1.abf')
abf = pyabf.ABF(fullpath)
abf.setSweep(3)
print(abf.sweepY) # sweep data (ADC)
print(abf.sweepC) # sweep command (DAC)
print(abf.sweepX) # sweep times (seconds)
plt.plot(abf.sweepX,abf.sweepY)
plt.show()