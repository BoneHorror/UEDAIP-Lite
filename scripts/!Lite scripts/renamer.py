import os

temp_beyond_dir = 'F:/animosity/extracted sprites/beyond - photon cannon, taar mine, taar controller/temp'
def replace_filename(directory):
    os.chdir(directory)
    filenames = os.listdir()
    for file in filenames:
        #replace(a, b) -> replace a in names of all files in dir with b
        os.rename(file, file.replace('000', '001'))

def replace_incontent(directory):
    pass

replace_filename(temp_beyond_dir)

