#! /usr/bin/env python3

import os
import requests
import argparse

# Indicates accepted command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory")
parser.add_argument("-uri", "--uri")
parser.add_argument("-f", "--fields")

args = parser.parse_args()
directory = args.directory
uri = args.uri
# Converts string of fields into a list and strips each entry of blank characters if present
fields = args.fields.split(",")
for index, item in enumerate(fields):
    fields[index] = item.strip()
    
# Function parses the contents of a passed data file into a list of elements and builds a dictionary for a POST request with provided fields
def dataparse(datafile):
    datafile = os.path.join(directory, datafile)
    with open(datafile, "r") as data:
        parsedData = data.readlines()
    if len(parsedData) != len(fields):
        raise Exception("Error parsing file {}: Field-value error.".format(datafile))
    requestData = {}
    for index, field in enumerate(fields):
        requestData[field] = parsedData[index].strip()
    return requestData


def postrequest(requestData):
    response = requests.post(uri, json=requestData)
    if response.ok:
        print(f"Request completed successfully for {len(requestData)} files.")
    else:
        print(f"Request failed with status code {response.status_code}")
        
filelist = os.listdir(directory)
requestBody = []
for file in filelist:
    fileData = dataparse(file)
    requestBody.append(fileData)
postrequest(requestBody)
