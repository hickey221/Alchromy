#Takes in excel output from the U.V.-vis machine and converts it to a .dat file
#for Spectral Deconvultion using Rich Hickey's program

#Input: Raw data from U.V.-vis
#Output: .dat file of spectra with 'nm' and 'A' headings
###Warning: Will overwrite current files if they are in the output folder###

####### ####### #######
#import libraries to navigate directories and make folders
from os import listdir, makedirs
from os.path import isfile, join, basename, exists
#import libraries to edit excel files
#import xlwt
import xlrd
import numpy as np #Numpy for data handling

#Folder to work in, change this for different data locations
mypath = r"C:\Users\martindale.40\Box Sync\Palmer Lab Research\ApoHeme\TestForProgram"
xlsfiles = [ join(mypath,f) for f in listdir(mypath) if isfile(join(mypath,f)) and '.xls' in  f]

#Set to suppress scientific notation when printing
np.set_printoptions(suppress=True)

#Go through each excel file in the folder and convert to a text file
for xlsfile in xlsfiles:
    book = xlrd.open_workbook(xlsfile)
    sheet = book.sheet_by_index(0)

    #Call values once and store them
    rows = sheet.nrows
    cols = sheet.ncols

    #Initialize an array of zeros
    array = np.zeros([rows, cols])
    temp_array = np.zeros([rows, cols])

    #Go through each cell and collect data
    for row in range(0,rows):
        for col in range(0,cols):
            array[row,col] = sheet.cell_value(row,col)

    #Close the workbook since it is not needed
    book.release_resources()

    #Create the header for the file
    header = ["A" for col in range(0, cols+1)]
    header[0] = "nm"
    header[1]=  "\t"

    #Create a filename and open the file
    f_name = xlsfile.replace('.xls','.dat')
    file = basename(f_name)
    rp = "Convert/" + file
    dirpath = f_name.replace(file, "Convert")
    f_name = f_name.replace(file, rp)

    #Check to see if the directory exists yet and make the file and directory
    if not exists(dirpath):
        makedirs(dirpath)
        print("New directory has been made")
    file = open(f_name, 'w')

    #Print the header and then go through the array and print elements as
    #individual strings
    for str in header:
        file.write(str)
    file.write("\n")
    width = array.shape[1]
    print(width)
    for num in array:
        #[ file.write(np.array(num[n]+"\t")) for n in range(0,width)]
        file.write(np.array_str(num[0])+"\t"+np.array_str(num[1]))
        file.write("\n")

    #Don't forget to close the file when done
    file.close()
    #Et C'est Fin
