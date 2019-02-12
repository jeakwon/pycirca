from tools import gui
import os

class Master:
    def __init__(self,filenames=None,get_new_csv=False):
        if filenames is None: filenames = gui.askfiles(filetypes=[('.abf','*.abf'),('all','*.*')])
        self.filenames = filenames
        self.check_csv_exist()
        
    def check_csv_exist(self):
        for filename in self.filenames:

            ID = os.path.splitext(os.path.basename(filename))[0]
            csv = os.path.splitext(filename)[0]+'.csv'
            csv_exist = os.path.exists(csv)
            if not csv_exist: print('{}.csv not exist'.format(ID))
