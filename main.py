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
from data_structures.graph import Graph
from ui.command_line_interface import CommandLineInterface
from utils.distance_calculator import DistanceCalculator
import utils.time_utils as tu
from utils.time_utils import TimeUtils
from utils.data_parsing_utils import DataParsingUtils
from utils.data_hashing_utils import DataHashingUtils
from utils.graph_utils import GraphUtils


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

# load the package data from the file
packages = DataHashingUtils.load_package_data("data/package_file.csv")

# load the packages into a hash table
package_table = HashTable()
for package in packages:
    package_table.insert(package.id, package)

# load the distance graph from the file
distance_graph = GraphUtils.load_distance_graph("data/distance_table.csv")
