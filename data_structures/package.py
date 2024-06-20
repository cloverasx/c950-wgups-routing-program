import csv
from data_structures.Hash_Table import HashTable  # remove this after testing

class Package:
    def __init__(self, package_id, address, city, state, zip, deadline, mass, notes, status=None, loc_name=None,):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes
        self.status = status
        self.loc_name = loc_name
        
        
    

# non-class function
def import_package_from_csv(file_path, hash_table):
    """
    Imports package data from a CSV file
    
    Args:
        file (str): file path to CSV file
    """
    pass

    # Open the CSV file
    with open(file_path, newline='') as csvfile:
        # Create a CSV reader object, specifying the quote character as '|'
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')

        # Iterate over the rows in the CSV file
        for row in csvreader:
            # create a new package object
            p_id, p_add_, p_city, p_state, p_zip, p_deadline, p_mass, p_notes = row[:8]
            package = Package(int(p_id), p_add_, p_city, p_state, p_zip, p_deadline, p_mass, p_notes)
            # insert into hash table
            hash_table.insert(package)
                

## USAGE:
# hash_table = HashTable()
# import_package_from_csv('CSV/Package_File.csv', hash_table)
