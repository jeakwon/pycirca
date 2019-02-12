__all__ =["butter_highpass","butter_highpass_filter","HPF",
          "ABS","DownSampling","DSP","TIM","Rosin_Threshold",
          "THR","BNR","FIN","ACT"]

import numpy as np
import pandas as pd
import datetime
from scipy.signal import butter, filtfilt


# 1. High Pass Filter
def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff=cutoff/nyq
    b, a = butter(order, normal_cutoff, btype='high',analog=False)
    
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    
    return y

def HPF(abf):
    cutoff = 1
    order = 5
    fs = abf.dataRate

    FiltArr = np.array([butter_highpass_filter(signal, cutoff, fs, order) for signal in abf.data])
    
    return FiltArr


# 2. Absolute Value
def ABS(abf):
    AbsArr = np.array([abs(signal) for signal in abf.dataHPF])
    
    return AbsArr


# 3. Down Sampling
def DownSampling(signal, factor):
    M = factor
    N = int(np.ceil(len(signal)/factor))
    
    X = np.copy(signal)
    X.resize(N,M)
    Y = np.mean(X,1)
    
    return Y

def DSP(abf):
    DownSampleArr = np.array([DownSampling(signal, abf.dataRate) for signal in abf.dataABS])
    
    return DownSampleArr


# 4. Get Time Stamps
def TIM(abf):
    RecStart = abf.abfDateTime
    Duration = int(np.ceil(abf.sweepLengthSec))
    TimeArr = np.array([RecStart + datetime.timedelta(seconds=i) for i in range(Duration)])
    
    return TimeArr


# 5. Rosin Thresholding
def Rosin_Threshold(signal):
    x = signal
    bins = int(len(x)/10) # 1/10 size of data 
    hists, bin_edges = np.histogram(x,bins=bins)

    # Histogram peak coordinate Xp, Yp
    Xp = hists.argmax()
    Yp = hists.max()

    # Histogram non-zero end coordinate Xe, Ye
    Xe = np.where(hists>0)[0][-1]
    Ye = hists[Xe]

    # Assign start values for best threshold finding
    best_idx = -1
    max_dist = -1

    # Find best index on histogram
    for X in range(Xp, Xe):
        Y = hists[X]
        a = [Xp-Xe, Yp-Ye]
        b = [X -Xe, Y -Ye]
        cross_ab = a[0]*b[1]-b[0]*a[1]
        dist = np.linalg.norm(cross_ab)/np.linalg.norm(a)
        if dist>max_dist:
            best_idx = X
            max_dist = dist

    # Calculate threshold with bin_edge values
    Threshold = 0.5*(bin_edges[best_idx]+bin_edges[best_idx+1])
    
    return Threshold

def THR(abf):
    Thresh_List = [Rosin_Threshold(signal) for signal in abf.dataDSP]
    
    return Thresh_List


# 6. Binary Data
def BNR(abf):
    BinaryArr = np.array([abf.dataDSP[i]>abf.dataTHR[i] for i in range(abf.channelCount)]).astype(int)
    return BinaryArr


# 7. Time + Data
def FIN(abf):
    Time = abf.dataTIM # (Time Stamp * 1)
    Data = abf.dataBNR.T # (Datas * channel num)
    DF = pd.DataFrame(data=Data,index=Time)
    
    return DF


# 8. Activity Conts (6min bin size)
def ACT(abf,bins='6min'):
    OneSecDF = abf.dataFIN
    ActCountDF = OneSecDF.resample(bins).sum()
    
    return ActCountDF


