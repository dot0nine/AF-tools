#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Andrey Romanyuk
#
# Created:     17/03/2022
# Copyright:   (c) Andrey Romanyuk 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os, glob



def open_files(full_path=os.getcwd(), _filter="*.txt"):
    # print('Looking for the directory:\t', full_path)
    if not os.path.exists(full_path):
        print(f'no dir {dir}')
    else:
        filelist = []  # list of raw files to process
        os.chdir(full_path)
        # print('Scanning for data files in:\t', full_path)
        for file in glob.glob(_filter):
            filelist.append(file)  # add txt files to the list
        # print('The following files will be processed:')
        # for file in filelist:
        #     print(file)
        return filelist


#def read_data(files, mode='multiple'):

    #if mode == 'multiple':









def main():
    pass

if __name__ == '__main__':
    main()
