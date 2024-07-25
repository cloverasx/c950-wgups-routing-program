# TODO: Update student ID# and remove this comment to ensure the line below
#       is the first line in this file.
# Name: A. Wayne Roberts, Student ID: C
# Course: C950 - Data Structures and Algorithms

# TODO: explain the process and the flow of the program

from datetime import datetime


# local imports
from data_structures.truck import Truck
from data_structures.package import Package
from data_structures.hash_table import HashTable
from data_structures.graph import Graph
from ui.command_line_interface import CommandLineInterface
from utils.data_parsing_utils import DataParsingUtils
from data_structures.route import NearestNeighbor
from delivery_simulation import DeliverySimulation
import config


def main():
    # Convert Excel files to CSV if needed
    DataParsingUtils.process_package_file(config.PACKAGE_FILE)
    DataParsingUtils.process_distance_table(config.DISTANCE_FILE)
    DataParsingUtils.convert_package_file_to_csv(
        config.PACKAGE_FILE, config.PACKAGE_FILE_CSV
    )
    DataParsingUtils.convert_distance_file_to_csv(
        config.DISTANCE_FILE, config.DISTANCE_FILE_CSV
    )

    # Initialize and run the simulation
    simulation = DeliverySimulation(config.PACKAGE_FILE_CSV, config.DISTANCE_FILE_CSV)
    simulation.run_simulation()

    # Display results
    # print(f"Total mileage: {simulation.get_total_mileage()}")

    # # Implement user interface for checking package status
    # while True:
    #     user_input = input(
    #         "Enter a time to check package status (HH:MM) or 'q' to quit: "
    #     )
    #     if user_input.lower() == "q":
    #         break
    #     try:
    #         check_time = datetime.datetime.strptime(user_input, "%H:%M").time()
    #         package_id = int(input("Enter package ID: "))
    #         status = simulation.get_package_status(package_id, check_time)
    #         print(f"Package {package_id} status at {user_input}: {status}")
    #     except ValueError:
    #         print(
    #             "Invalid input. Please use HH:MM format for time and a valid package ID."
    #         )


if __name__ == "__main__":
    main()
