from data_structures.package import Package


class DataHashingUtils:
    @staticmethod
    def load_package_data(file_path):
        # open the file in read mode
        with open(file_path, "r") as file:
            # read the lines from the file, skipping the first line (header)
            lines = file.readlines()[1:]
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
                status = "At Hub"  # initialize status to "At Hub"

                package = Package(
                    package_id,
                    address,
                    city,
                    state,
                    zip_code,
                    deadline,
                    weight,
                    status,
                    note,
                )
                # add the package to the list
                packages.append(package)
            # return the list of packages
            return packages
