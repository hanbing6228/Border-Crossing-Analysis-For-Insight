# -*- coding: utf-8 -*-
# import the os module
import os


# Module for reading CSV files
import csv
import sys

#Define a dictionary to receive monthly 
result = {}

#Define a dictionary to receive monthly sum of value
measure_sum_by_month = {}

# Define the function to group by month and have it accept the 'data_str' as its sole parameter
def get_month(date_str):
    
    # Split the data on space by date and time
    mmddyyyy = date_str.split(" ")
    
    # Split the data on / by month and year
    mmddyyyy1 = mmddyyyy[0].split("/")
    
    #return a splited date for groupby
    return mmddyyyy1[0] + "/" + "01" + "/" + mmddyyyy1[2] + " " + mmddyyyy[1] + " " + mmddyyyy[2]

# Define the function to caculate monthly data
def data_by_month():    
   
   # CSV reader specifies delimiter and variable that holds contents
    with open('input.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',') 
        
        # Read the header row first (skip this step if there is no header)
        #csv_header = next(csvreader)
        
        # Read each row of data after the header
        for row in csvreader:
            
            #setup grouped months as the key of result
            key = get_month(row[4])            
            
            # Loop through the result data, append Measure and Value as the value of monthly result
            if key in result:
                values = []
                values = (result.get(key))
                
                #If the month's name in a row, append new row in the list
                values.append([row[5], row[6]])
                result[key] = values
            
            #If the month's name not in a row, write a new key for result
            else:
                result[key] = [[row[5], row[6]]]            
    return

# Define the function to caculate the sum of the value by measure column
def sum_by_measure(value_lists):
    sum_measure = {}
    
    # Loop through the value data of the result dictionary, append sum of the value as the value in sum_measure dictionary
    for value_list in value_lists:
        
        #set the key with the type of the measure column
        key = value_list[0]
        
        #if the tpye is not in the sun_measure dictionary, write a new type for the list
        if key not in sum_measure:
            sum_measure[key] = int(value_list[1])
        
        #If the thpe is in the list, plus the new data
        else:
            sum = sum_measure[key] + int(value_list[1])
            sum_measure[key] = sum 
    
    #return grouped sum data dictionary
    return sum_measure

#Call function
data_by_month()

#Loop monthly data, calculate sum of value
for key, value in result.items():
    
    #sum_by_measure(value)
    measure_sum_by_month[key] = sum_by_measure(value)

#Loop monthly sum data, calculate moving average of sum
total_upto_month = {}
average_upto_month = {}

count = 0
for month, measure_sum in measure_sum_by_month.items():
    temp_dic = {}
    temp_average = {}
    if count == 0:
        total_upto_month[month] = measure_sum
        average_upto_month[month] = measure_sum
        temp_dic = measure_sum
    else:
        for measure, sub_sum_by_measure in measure_sum.items():
            if measure not in temp_dic:
                temp_dic[measure] = 0
            temp_dic[measure] = measure_sum[measure] + temp_dic[measure]
            temp_average[measure] = temp_dic[measure] / (count + 1)
            total_upto_month[month] = temp_dic
            average_upto_month[month] = temp_average
    count += 1

# print out the dictionary for sum
print(total_upto_month)

# Print out the dictionary for moving average
print(average_upto_month)

# I calculate the data very well but I still can not get it into csv.
# Here is  the code testing, but I think I don't have enough time.
"""
border = []
date = []
measure = []
avg_type_lists = []
avg_type_lists = []
value = []
average = []
with open('input.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',') 
    for row in csvreader:
        border.append(row[3])


for key, value in average_upto_month.items(): 
    avg_type_lists.append(value)
for avg_type_list in avg_type_lists:
    for key, value in avg_type_list.items():
        date.append()
        measure.append(key)
        average.append(value)
print(average)
print(date)
print(measure)
print(value)

cleaned_csv = zip(border, date, measure, average)


# Set variable for output file
output_file = os.path.join("..", "output", "report4.csv")

#  Open the output file
#with open(output_file, "w", newline="") as csvfile:
with open(output_file, 'ab') as csvfile:
    
    # Initialize csv.writer
    writer = csv.writer(csvfile, newline='')

    # Write the header row
    writer.writerow(["Border", "Date", "Measure", "Value", "Average"])
    writer.writerow(cleaned_csv)

"""
