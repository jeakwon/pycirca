import pyabf
import os
filepath = os.path.expanduser('~/Desktop')
filename = "f1.abf"
fullpath = os.path.join(filepath,filename)
abf = pyabf.ABF(fullpath)
abf.setSweep(3)
print(abf.sweepY) # sweep data (ADC)
print(abf.sweepC) # sweep command (DAC)
print(abf.sweepX) # sweep times (seconds)
