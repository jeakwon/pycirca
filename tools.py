import os

def get_desktop_file(filename):
    filepath = os.path.expanduser('~/Desktop')
    fullpath = os.path.join(filepath,filename)
    return fullpath