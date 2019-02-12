import os
import pyabf
from tools import gui, signal

def abf_process(abfFilename):
    abf = pyabf.ABF(abfFilename)
    abf.dataHPF = signal.HPF(abf)
    abf.dataABS = signal.ABS(abf)
    abf.dataDSP = signal.DSP(abf)
    abf.dataTIM = signal.TIM(abf)
    abf.dataTHR = signal.THR(abf)
    abf.dataBNR = signal.BNR(abf)
    abf.dataFIN = signal.FIN(abf)
    abf.dataACT = signal.ACT(abf)
    return abf


        
def convert(filenames=None,directory=None):
    if filenames is None: filenames = gui.askfiles(filetypes=[('.abf','*.abf'),('all','*.*')])
    if directory is None: directory = gui.askdir(title='Select folder to save')
    for filename in filenames:
        try:
            ID = pyabf.ABF(filename).abfID
            Converted = abf_process(filename)
            fullpath = os.path.join(directory,ID+'.csv')
            Converted.dataACT.to_csv(fullpath)
            print(fullpath + ' saved')
        except:
            print(filename + 'Convert failed xxxxxxxx')
    gui.alert(title="Alert",message="Convert finished")
