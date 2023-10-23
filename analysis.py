#!/usr/bin/env python
# coding: utf-8

# In[]:
print("Hello world!")

# In[]:

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

# Put datalog data into a "CSV" file (spreadsheet)
headers = ['Time', 'Tension', 'Temperature', 'Pressure', 'Altitude']
read_file = pd.read_csv('DATALOGNS110RAW.TXT', names=headers, index_col=False)

# In[130]:
np_time = read_file['Time']
new_times = []

for time in np_time:
    new_times.append(time[(time.find("|") + 1):])


# In[183]:
# Get time in terms of seconds since launch.

raw_seconds = []

# Convert all hours/minutes to seconds
for time in new_times:
    hours = int(time[:(time.find(":"))])
    sliced = time[(time.find(":") + 1):]
    minutes = int(sliced[:(sliced.find(":"))])
    sliced = sliced[(sliced.find(":") + 1):]
    SECONDS = int(sliced)
    
    # Subtract the first seconds value from all seconds readings.
    if ('offset' not in locals()):
        offset = (3600 * hours) + (60 * minutes) + SECONDS
    raw_sec = ((3600 * hours) + (60 * minutes) + SECONDS) - offset
        
    
    raw_seconds.append(raw_sec)
    


# In[188]:
# Differentiate seconds of the same value. Assume every reading is equally
# spaced apart and adjust seconds values accordingly.

last_second = 0
sub_array = []
i = 1
j = 0
count = 1

for sec in range(len(raw_seconds) - 1):
    if raw_seconds[i] == raw_seconds[i - 1]:
        count = count + 1
    else:        
        if count > 0:
            decimal = 1/count
        else:
            decimal = 0
        while j < count:
            #print(count)
            raw_seconds[(i - count) + j] = raw_seconds[(i - count) + j] + (decimal * j)
            j = j + 1
            
        #Resets counters  
        count = 1  
        j = 0
        

    i = i + 1

# Set time to the ones we just calculated
read_file['Time'] = raw_seconds

# In[265]:
# Get rid of junk values from before and after launch

#new_df = read_file
new_df = read_file[15500:80000]  # TUFF 110

# In[274]:
# Tension, Altitude, and Temperature

z = np.linspace(0, 10, 1000)
new_df.plot(x ='Time', y='Tension', kind = 'line', title = 'Time vs. Tension', 
            xlabel = 'Time (seconds)', ylabel = 'Tension (lbs)')