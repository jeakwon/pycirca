# import libs
import tkinter
from tkinter import filedialog, simpledialog, messagebox

def tk_on():
    root = tkinter.Tk()
    root.wm_attributes("-topmost", 1) #use to make window topmost
    root.withdraw() #use to hide tkinter window
    
def askdir(title='Please select a directory'):
    tk_on()
    
    get = filedialog.askdirectory(title=title)
    if len(get) is 0: raise ValueError('No folder selected')
    return get
        
        
def askfile(title='Please select a file',filetypes=[('All files','*.*'),]):
    tk_on()
    
    get = filedialog.askopenfilename(title=title, filetypes=filetypes)
    if len(get) is 0: raise ValueError('No file selected')
    return get


def askfiles(title='Please select a file',filetypes=[('All files','*.*'),]):
    tk_on()
    
    get = filedialog.askopenfilenames(title=title, filetypes=filetypes)
    if len(get) is 0: raise ValueError('No file selected')
    return get

def asksave(title='Save your file',defaultextension=".csv"):
    tk_on()
    
    get = filedialog.asksaveasfile(title='Save your file' ,mode='w', defaultextension=defaultextension)
    if get is None: return
    return get

        
def askstr(title='Enter String',prompt='Please enter strings'):
    tk_on()
    
    get = simpledialog.askstring(title=title,prompt=prompt)
    if get is not None and get.strip():
        return get # .strip is used to ensure the user doesn't enter only spaces ' '
    else:
        raise ValueError('Invalid String', 'You must enter something')
        
def askint(title='Enter Integer', prompt='Please enter an integer'):
    tk_on()
    
    get = simpledialog.askinteger(title=title,prompt=prompt)
    if get is not None: 
        return get
    else:
        raise ValueError('You must enter something')
        
def alert(title="title", message="message"):
    tk_on()
    
    messagebox.showinfo(title=title, message=message)