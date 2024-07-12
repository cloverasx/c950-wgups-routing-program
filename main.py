# TODO: Update student ID# and remove this comment to ensure the line below
#       is the first line in this file.
# Name: A. Wayne Roberts, Student ID: C
# Course: C950 - Data Structures and Algorithms

# TODO: explain the process and the flow of the program

from datetime import datetime

# local imports
from algorithms.routing_algorithm import RoutingAlgorithm
from algorithms.routing_algorithm import Truck
from data_structures.package import Package
from data_structures.hash_table import HashTable
from ui.command_line_interface import CommandLineInterface
from utils.distance_calculator import DistanceCalculator
import utils.time_utils as tu
from utils.time_utils import TimeUtils
from utils.data_parsing_utils import DataParsingUtils


# TODO: Test function after parsing function works
def load_package_data(file_path):
    # open the file in read mode
    with open(file_path, "r") as file:
        # read the lines from the file
        lines = file.readlines()
        # create an empty list to store the packages
        packages = []
        # iterate through the lines
        for line in lines:
            # split the line by the comma
            data = line.strip().split(",")
            # extract the package data
            package_id = int(data[0])
            address = data[1]
            city = data[2]
            state = data[3]
            zip_code = data[4]
            deadline = data[5]
            weight = data[6]
            note = data[7]
            status = "At Hub"
            # create a package object
            package = Package(
                package_id,
                address,
                city,
                state,
                zip_code,
                deadline,
                weight,
                note,
                status,
            )
            # add the package to the list
            packages.append(package)
        # return the list of packages
        return packages


# TODO: Test function after parsing function works
def load_distance_table(file_path):
    # open the file in read mode
    with open(file_path, "r") as file:
        # read the lines from the file
        lines = file.readlines()
        # create an empty dictionary to store the distances
        distances = {}
        # iterate through the lines
        for line in lines:
            # split the line by the comma
            data = line.strip().split(",")
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


# Convert package file xlsx to csv
try:
    file_path = "data/WGUPS Package File.xlsx"  # TODO: Change to CONSTANT
    package_headers, package_data = DataParsingUtils.process_package_file(file_path)
    DataParsingUtils.save_package_file(package_headers, package_data)
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Convert distance table xlsx to csv
try:
    file_path = "data/WGUPS Distance Table.xlsx"  # TODO: Change to CONSTANT
    output_file = "data/distance_table.csv"
    locations, distances = DataParsingUtils.process_distance_table(file_path)
    DataParsingUtils.save_distance_file(locations, distances, output_file)
except Exception as e:
    print(f"An error occurred: {str(e)}")
