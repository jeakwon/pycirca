import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

def datetime_to_epoch(x):
    return x.astype(np.int64)//10**9

def epoch_to_datetime(x):
    return x.astype("datetime64[s]")

def get_pgram(x,y,t_start=1,t_end=50):
    """
    x: time series, seconds
    y: values
    t_start, t_end: plot range for lomb-scargle-periodogram. (unit: hour)
    """
    x = x/3600
    n = len(x)*10
    T = np.linspace(t_start,t_end,n)
    pgram = signal.lombscargle(x, y, 2*np.pi/T, normalize=True)
    return T, pgram

def get_tau(T,pgram):
    maxidx = np.argmax(pgram)
    tau = T[maxidx]
    return tau

def get_tau_from_df(df,t_start=1,t_end=50):
    x=datetime_to_epoch(df.index.levels[1])
    cols = df.columns
    taus={}
    for col in cols:
        y=df[col].values
        T,pgram = get_pgram(x,y,t_start,t_end)
        tau = get_tau(T,pgram)
        taus[col]=tau
        print(col,tau)
    return taus

def plot_pgram_from_df(df,t_start=1,t_end=50):
    x=datetime_to_epoch(df.index.levels[1])
    cols = df.columns
    fig = plt.figure(figsize=(20,10))
#    fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
#                wspace=0.0, hspace=0.0)
    i = 0
    for col in cols:
        i+=1
        y=df[col].values
        T,pgram = get_pgram(x,y,t_start,t_end)
        tau = get_tau(T,pgram)
        ax = fig.add_subplot(2,8,i)
        ax.plot(T,pgram,'k')
#        ax.legend('Tau : {:2f}'.format(tau))
        ax.set_xlabel('Time(hour)')
        ax.set_title('Ch: {}, Tau: {:2f}'.format(col,tau))