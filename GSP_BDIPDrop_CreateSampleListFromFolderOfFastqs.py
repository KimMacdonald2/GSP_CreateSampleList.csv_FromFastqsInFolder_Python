# -*- coding: utf-8 -*-
"""
Created on Fri May  2 15:18:45 2025

@author: KIMMACDO
"""
  
#import packages
import glob
import os
import subprocess
import fnmatch
import pandas as pd
import numpy as np

import pathlib
from pathlib import Path
import sys


import time
import json
sys.path.append(".")

import shutil


#-------Find all fastq.gz or .fq.gz files in folder with your files------

# #convert all MS backslashes to forward slashes (for directories/filepaths)
# line = r"this\is\a\line\with\backslashes"
# new_line = line.replace("\\", "/")
# print(new_line)
# # Output: this/is/a/line/with/backslashes

#folder with NCBI/ENA downloaded files
directoryPath = "C:/path/to/FolderWithFastqFiles"

# Set output CSV file path
outputCsvPath = directoryPath + "/SampleList.csv"
#print(outputCsvPath)

# #test: print contents of directory with fastqs
# items = os.listdir(directoryPath)
# for item in items:
#     print(item) #worked

#create function to list files in a directory with matching pattern (call later)
def list_files_with_pattern(directoryPath, pattern):
  """
  Lists files in a folder that match a given pattern.

  Args:
    folder_path: The path to the folder to search.
    pattern: The pattern to match (e.g., "*.txt", "image*").

  Returns:
    A list of file paths that match the pattern.
  """
  return glob.glob(os.path.join(directoryPath, pattern))

# Example usage:
#directoryPath = "/path/to/your/folder"  # Replace with the actual folder path
pattern = "*.gz"  # Replace with your desired pattern
#fastq_files = list_files_with_pattern(directoryPath, pattern)

fastq_filePath = list_files_with_pattern(directoryPath, pattern)

#print(fastq_filePath)
#print(fastq_files)


#Create SampleList.csv table (empty) (will append results into it in loop)
df_SampleList1 = pd.DataFrame(columns=['Sample_Name', 'Project_ID', 'File_Forward', 'File_Reverse'])
print(df_SampleList1)



#if the given directory path has .gz files, then count and list them, then create SampleList.csv file for them:
if fastq_filePath:
    matching_files = len(list(fastq_filePath))
    #print(matching_files)
    print(matching_files, "Files matching the .gz pattern in path", directoryPath, ":")
    for file_path in fastq_filePath:
      file = file_path.split('\\')[-1] #To split a string in Python using the backslash character `\` as a delimiter, it's crucial to handle the backslash as a literal character. Since `\` is an escape character, it needs to be escaped itself in the split() method using \\.
      print(file)
      
      #store fastq filename for forward read in variable
      F_substring = "_1"
      if F_substring in file:
        F_read = file  
        #print("F read is ", F_read)
      
      
      #since are iterating through 1 filename at a time, there will be a _1 or _2 but not both, so can't properly populate df
      #df would look like
      #SRR12345     SRR12345_1.fastq.gz
      #SRR12345                             SRR12345_2.fastq.gz
        
        #This way will also remove duplicates b/c only 1 of the pair will match
        R_read = F_read.replace("_1", "_2")
      
        #store SampleID in variable
        sampleID = file.split('_')[0]
        #print("SampleID is ", sampleID)
      
      #create table to turn into SampleList file
      
# [Data]			
# Sample_Name	Project_ID	File_Forward	File_Reverse
# SRR2567187	empty	SRR2567187_1.fq.gz	SRR2567187_2.fq.gz
# SRR2567176	empty	SRR2567176_1.fq.gz	SRR2567176_2.fq.gz
# SRR2567175	empty	SRR2567175_1.fq.gz	SRR2567175_2.fq.gz

        
      
      #df_Fastqs = ['Sample_Name', 'Project_ID', 'File_Forward', 'File_Reverse']
      #df_Fastqs = []
      
        #populate SampleList columns with the results
        new_row = pd.DataFrame({'Sample_Name': [sampleID], 'Project_ID': [""], 'File_Forward': [F_read], 'File_Reverse': [R_read]})
        #pd.DataFrame(new_row)
        df_SampleList1 = pd.concat([df_SampleList1, new_row], ignore_index=True)
        #print(df_SampleList1)
      
      
else:
  print("No files found matching the .gz pattern.")

print("")
print ("SampleList.csv contents will be:")
print("")
print(df_SampleList1)

#Insert row at top with "[Data]"
df_SampleList1.columns = pd.MultiIndex.from_tuples(
    zip(['[Data]', '', '', ''], 
        df_SampleList1.columns))
print(df_SampleList1)


#Save output to file
df_SampleList1.to_csv(outputCsvPath, encoding='cp1252', index=False)
