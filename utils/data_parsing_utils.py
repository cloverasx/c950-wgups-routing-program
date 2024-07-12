import openpyxl
import csv
from utils.string_utils import StringUtils as su


class DataParsingUtils:
    @staticmethod
    def clean_string(s):
        # Note: I was having problems finding the data in the xlsx file and found
        # that this could clean up the data.
        s = str(s)
        s = su.remove_commas(s)
        s = su.clean_whitespace(s)
        s = su.convert_to_lowercase(s)
        return s

    # TODO: the following works well with the package file currently. Will need updated for
    # the distance table file and any logic checking and error handling.
    @staticmethod
    def process_package_file(file_path):
        workbook = openpyxl.load_workbook(file_path)
        worksheet = workbook.active
        header_row = None
        for row_index, row in enumerate(
            worksheet.iter_rows(min_row=1, max_row=worksheet.max_row), start=1
        ):
            cell_values = [DataParsingUtils.clean_string(cell.value) for cell in row]
            # print(f"Row {row_index}: {cell_values}")  # Debugging output
            if "address" in cell_values and "city" in cell_values:
                header_row = row_index
                # print(f"Header row found at row {header_row}")  # Debugging output
                break
        if header_row is None:
            raise ValueError(
                "Could not find a header row containing both 'address' and 'city'."
            )
        headers = [
            DataParsingUtils.clean_string(cell.value)
            for cell in worksheet[header_row]
            if cell.value
        ]
        # print(f"Headers: {headers}")  # Debugging output
        data = []
        for row in worksheet.iter_rows(
            min_row=header_row + 1, max_row=worksheet.max_row, values_only=True
        ):
            if any(cell for cell in row):
                data.append(
                    [
                        DataParsingUtils.clean_string(cell) if cell else ""
                        for cell in row[: len(headers)]
                    ]
                )
        return headers, data

    @staticmethod
    def save_package_file(package_headers, package_data):
        with open("data/package_file.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(package_headers)
            for row in package_data:
                writer.writerow(row)

    @staticmethod
    def process_distance_table(file_path):
        workbook = openpyxl.load_workbook(file_path)
        worksheet = workbook.active

        # Find the last row with data in all columns
        last_full_row = None
        for row in reversed(list(worksheet.rows)):
            if all(cell.value is not None for cell in row):
                last_full_row = row
                break

        if last_full_row is None:
            raise ValueError(
                "Could not find a fully populated row in the distance table."
            )

        # Determine the number of columns in the matrix
        matrix_size = sum(1 for cell in last_full_row if cell.value is not None)

        # Calculate the start row
        start_row = last_full_row[0].row - (matrix_size - 3)

        # Extract location names and distances
        locations = []
        distances = []
        for row in worksheet.iter_rows(
            min_row=start_row, max_row=last_full_row[0].row, values_only=True
        ):
            location_name = DataParsingUtils.clean_string(row[0])
            locations.append(location_name)
            # Start from index 1 to skip the first column (location name)
            row_distances = [
                float(cell) if isinstance(cell, (int, float)) else 0
                for cell in row[1:matrix_size]
            ]
            distances.append(row_distances)

        return locations, distances

    @staticmethod
    def save_distance_file(locations, distances, output_file):
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(
                ["Location"] + [f"Distance_{i+1}" for i in range(len(locations))]
            )
            for i, distances_row in enumerate(distances):
                writer.writerow([locations[i]] + distances_row)
