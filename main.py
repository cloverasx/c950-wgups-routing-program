# TODO: Update student ID# and remove this comment to ensure the line below
#       is the first line in this file.
# Name: A. Wayne Roberts, Student ID: C
# Course: C950 - Data Structures and Algorithms

# TODO: explain the process and the flow of the program

from datetime import datetime
# local imports
from algorithms.routing_algorithm import Truck
from algorithms.routing_algorithm import RoutingAlgorithm
from data_structures.package import Package
from data_structures.hash_table import HashTable
from ui.command_line_interface import CommandLineInterface
from utils.distance_calculator import DistanceCalculator
from utils.time_utils import TimeUtils

# TODO: Test function after parsing function works
def load_package_data(file_path):
    # open the file in read mode
    with open(file_path, 'r') as file:
        # read the lines from the file
        lines = file.readlines()
        # create an empty list to store the packages
        packages = []
        # iterate through the lines
        for line in lines:
            # split the line by the comma
            data = line.strip().split(',')
            # extract the package data
            package_id = int(data[0])
            address = data[1]
            city = data[2]
            state = data[3]
            zip_code = data[4]
            deadline = data[5]
            weight = data[6]
            status = "At Hub"
            # create a package object
            package = Package(package_id, address, city, state, zip_code, deadline, weight, status)
            # add the package to the list
            packages.append(package)
        # return the list of packages
        return packages

# TODO: Test function after parsing function works
def load_distance_table(file_path):
    # open the file in read mode
    with open(file_path, 'r') as file:
        # read the lines from the file
        lines = file.readlines()
        # create an empty dictionary to store the distances
        distances = {}
        # iterate through the lines
        for line in lines:
            # split the line by the comma
            data = line.strip().split(',')
            # extract the addresses and distances
            address1 = data[0]
            address2 = data[1]
            distance = float(data[2])
            # check if the address is already in the dictionary
            if address1 in distances:
                # add the distance to the existing address
                distances[address1][address2] = distance
            else:
                # create a new entry for the address
                distances[address1] = {address2: distance}
        # return the dictionary of distances
        return distances

# TODO: This doesn't provide the output I want yet; iterate and determine what 
#       will fit the model best.
# parse xlsx into properly formatted csv
import pandas as pd
def parse_xlsx(file_path, first_header):
    """
    Parses an XLSX file and converts it into a properly formatted CSV file.
    
    Args:
        file_path (str): The path to the XLSX file to be parsed.
        first_header (str): The first header to identify the start of relevant data.
    
    Returns:
        str: Path to the generated CSV file.
    """
    # Read the XLSX file using pandas, without headers
    xlsx_data = pd.read_excel(file_path, sheet_name=0, header=None)
    
    # Find the index of the first header
    header_index = None
    for idx, row in xlsx_data.iterrows():
        if first_header in row.values:
            header_index = idx
            break
    
    if header_index is None:
        raise ValueError(f"Header '{first_header}' not found in the XLSX file.")
    
    # Read the Excel file again, now with the correct header row
    relevant_data = pd.read_excel(file_path, sheet_name=0, header=header_index)
    
    # Create a CSV file path
    csv_file_path = file_path.replace('.xlsx', '.csv')
    
    # Save the relevant data to a CSV file
    relevant_data.to_csv(csv_file_path, index=False)
    
    return csv_file_path

# parse the distance table xlxs into csv
parse_xlsx('data/WGUPS Package File.xlsx', 'Package\nID') # with above^^^
