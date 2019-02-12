import pyabf
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib import gridspec, dates
from tools import gui

def merge(filenames=None,save=False):
    if filenames is None: filenames=gui.askfiles(title='Select converted csv',filetypes=[('csv','*.csv'),])
    dfs = [pd.read_csv(filename,index_col=0) for filename in filenames]
    merged = pd.concat(dfs, axis=0)
    merged.index=pd.to_datetime(merged.index)
    merged = merged.groupby(merged.index).sum()
    if save is True: merged.to_csv(gui.asksave())
    return merged
        

class Actogram:
    def __init__(self, get_merged=False,save_merged=False):
        if get_merged:
            self.Raw = pd.read_csv(gui.askfile(filetypes=[('csv','*.csv'),]),index_col=0,)
        else:
            self.Raw = merge(save = save_merged)
        self.Raw.index = pd.to_datetime(self.Raw.index)
        self.RawStart = self.Raw.index[0]
        self.RawEnd = self.Raw.index[-1]
        self.Duration = self.RawEnd-self.RawStart
        self.Channels = self.Raw.columns.values
        self.ActoStart = None
        self.ActoEnd = None
        
 
    def shape(self, Start=None, RowNum=None, Type=1, DeltaHours=24, zt_start=8):

        # Inval
        DF = self.Raw
        if not (isinstance(Type , int) and Type > 0): raise ValueError('Type should be natural number')
        if DeltaHours>0: TimeDelta = datetime.timedelta(hours=DeltaHours)
        if not Start: Start = self.RawStart
        Start = Start.replace(hour=zt_start,minute=0,second=0)
        if (Start-self.RawStart)<datetime.timedelta(0):Start+datetime.timedelta(days=1)
        if not RowNum: RowNum = int(np.ceil((self.RawEnd-Start)/TimeDelta))
            
        
        # Trace Separation    
        Frame = []
        Range = []
        for n in range(RowNum):
            RowStart = Start + n*TimeDelta
            RowEnd   = RowStart + Type*TimeDelta

            Range.append([n,RowStart, RowEnd])
            Frame.append(DF[(RowStart<=DF.index) & (DF.index<RowEnd)])
            
        self.Frame = pd.concat(Frame,keys=range(RowNum))
        self.Range = pd.DataFrame(np.array(Range),columns=['RowNum','RowStart','RowEnd']).set_index('RowNum')
        self.DeltaHours = DeltaHours
        self.TimeDelta = TimeDelta
        self.RowNum = RowNum
        self.Type = Type
        self.ActoStart = self.Range.values[0][0]
        self.ActoEnd = self.Range.values[-1][-1]
        return self.Frame, [self.ActoStart,self.ActoEnd]
    
    
    
    def plot(self, Channels=None, RowWidth=8, RowHeigt=0.3,RowYlim=360,
             Color='k', Alpha=0.6, Linewidth=0, RowNumPlotGap=5, 
             show_xAxis= True, show_yAxis= True, show_channel= True):
        
        df = self.Frame
        xr = self.Range
        Type = self.Type
        TimeDelta = self.TimeDelta
        End = self.ActoEnd
        RowGapHours=self.DeltaHours
        rows = self.Frame.index.levels[0]
        gs = gridspec.GridSpec(len(rows), 1, wspace=0.0, hspace=0.0)
        figsize = (RowWidth, RowHeigt*len(rows))        
        
        
        if Channels is None: Channels = self.Channels
        
        self.figs = {}
        for chn in Channels:            
            self.figs[chn] = plt.figure(num=chn,figsize=figsize)
            for row in rows:
                x = df[chn][row].index
                y = df[chn][row].values
                ax = plt.subplot(gs[row])
                ax.set_facecolor(((0,0,0,0)))
                try:
                    plt.fill_between(x, y, step="pre", alpha=Alpha, color=Color,linewidth=Linewidth,linestyle='None')
#                    EventMarker()
                except:
                    print('Error occured while plotting Channel:{}, Row:{}'.format(chn,row))

                plt.ylim([0,RowYlim])
                plt.xlim(xr.loc[row])

                for spine in ax.spines:
                    ax.spines[spine].set_visible(False)
                plt.xticks([])
                plt.yticks([])
                plt.tick_params(which='both',right=False,top=False,)

                hfmt = dates.DateFormatter('%m/%d %H:%M')
                ax.xaxis.set_major_formatter(hfmt)
                
                if show_yAxis is True:    
                    if row%RowNumPlotGap is 0:
                        plt.ylabel('{}'.format(row)).set_rotation(0)

            if show_xAxis is True:
                xTicks_ = [End - x*TimeDelta for x in range(Type+1)][::-1]
                xTicksLabel_ =[x*RowGapHours for x in range(Type+1)]
                plt.xticks(xTicks_,xTicksLabel_)



            if show_channel is True:            
                plt.xlabel('Channel #'+chn)
            
    
    def plotall(self, Channels=None, RowWidth=3, RowHeigt=0.1,RowYlim=360,
             Color='k', Alpha=1, Linewidth=0, RowNumPlotGap=5, 
             show_xAxis= True, show_yAxis= True, show_channel= True):
        
        df = self.Frame
        xr = self.Range
        Type = self.Type
        TimeDelta = self.TimeDelta
        End = self.ActoEnd
        RowGapHours=self.DeltaHours
        rows = self.Frame.index.levels[0]
        gsparent = gridspec.GridSpec(2,8)
        gschildren = {}

        figsize = (RowWidth*8, RowHeigt*len(rows)*2.5)        
        self.allfig = plt.figure(figsize=figsize)
        
        if Channels is None: Channels = self.Channels
        
        for chn in Channels:  
            gschildren[chn] = gridspec.GridSpecFromSubplotSpec(
                    len(rows), 1, wspace=0.0, hspace=0.0, subplot_spec=gsparent[int(chn)])

            for row in rows:
                x = df[chn][row].index
                y = df[chn][row].values
                ax = plt.subplot(gschildren[chn][row])
                ax.set_facecolor(((0,0,0,0)))
                try:
                    ax.fill_between(x, y, step="pre", alpha=Alpha, color=Color, linewidth=Linewidth,)
#                    EventMarker()
                except:
                    print('Error occured while plotting Channel:{}, Row:{}'.format(chn,row))

                ax.set_ylim([0,RowYlim])
                ax.set_xlim(xr.loc[row].values)

                for spine in ax.spines:
                    ax.spines[spine].set_visible(False)
                plt.xticks([])
                plt.yticks([])
                plt.tick_params(which='both',right=False,top=False,)

                hfmt = dates.DateFormatter('%m/%d %H:%M')
                ax.xaxis.set_major_formatter(hfmt)
                
                if show_yAxis is True:    
                    if row%RowNumPlotGap is 0:
                        plt.ylabel('{}'.format(row)).set_rotation(0)

            if show_xAxis is True:
                xTicks_ = [End - x*TimeDelta for x in range(Type+1)][::-1]
                xTicksLabel_ =[x*RowGapHours for x in range(Type+1)]
                plt.xticks(xTicks_,xTicksLabel_)



            if show_channel is True:            
                plt.xlabel('Channel #'+chn)
    
    
    
    def info(self):
        print('\n###### Useful class variables and methods ######')
        
        # Variable Info
        print('\n1. Variable List (Large Capital)\n')
        print('{:>10}: {}'.format('.Raw','>> Returns raw dataframe'))
        print('{:>10}: {}'.format('.RawStart',self.RawStart))
        print('{:>10}: {}'.format('.RawEnd',self.RawEnd))
        print('{:>10}: {}'.format('.ActoStart',self.ActoStart))
        print('{:>10}: {}'.format('.ActoEnd',self.ActoEnd))
        print('{:>10}: {}'.format('.Duration',self.Duration))
        print('{:>10}: {}'.format('.Channels',self.Channels))
        print('{:>10}: {}'.format('.RowNum',self.RowNum))
        print('{:>10}: {}'.format('.Frame','>> Returns shaped dataframe'))
        print('{:>10}: {}'.format('.Range','>> Returns shaped time Stamps'))
        
        # Method Info
        print('\n2. Method List (Small Capital)\n')
        print('{:>10}: {}'.format('.info()','>> Returns actogram information'))
        print('{:>10}: {}'.format('.shape()','>> Returns shaped DataFrame and TimeRange'))

    def set_ylim(self,ylim=[0,360]):
        import matplotlib.axes as axes
        if self.allfig: 
            axs=self.allfig.findobj(axes.Axes)
            for ax in axs:
                ax.set_ylim(ylim)
        if self.figs: 
            for fig in self.figs:
                axs=self.fig.findobj(axes.Axes)
                for ax in axs:
                    ax.set_ylim(ylim)
#FileName =  gui.askfile(filetypes=[('.csv','*.csv'),('all','*.*')])
#acto = Actogram(FileName)
#acto.shape(Start = datetime.datetime(2018,4,15,8,0,0),Type=1,RowNum=19)
#acto.plot(Channels=i,Alpha=1,RowWidth=6, RowHeigt=0.2,)