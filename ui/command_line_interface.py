import os
import time


class CommandLineInterface:
    def __init__(self, simulation):
        self.simulation = simulation

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def display_menu(self):
        self.clear_screen()
        print("1. Run live simulation")
        print("2. Look up package")
        print("3. Look up truck")
        print("4. Exit")
        return input("Select an option: ")

    def run_live_simulation(self):
        self.clear_screen()
        print("Running live simulation... Ctrl+C to stop.")
        try:
            while True:
                self.simulation.run_step()
                self.clear_screen()
                print(self.simulation.get_status())
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nSimulation stopped.")

    def lookup_package(self):
        package_id = input("Enter package ID: ")
        package = next(
            (p for p in self.simulation.package_table if p.id == int(package_id)), None
        )
        if package:
            print(package)
        else:
            print("Package not found.")
        input("Press Enter to continue...")

    def lookup_truck(self):
        truck_id = input("Enter truck ID: ")
        truck = next((t for t in self.simulation.trucks if t.id == int(truck_id)), None)
        if truck:
            print(truck)
        else:
            print("Truck not found.")
        input("Press Enter to continue...")

    def run(self):
        while True:
            choice = self.display_menu()
            if choice == "1":
                self.run_live_simulation()
            elif choice == "2":
                self.lookup_package()
            elif choice == "3":
                self.lookup_truck()
            elif choice == "4":
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")
                time.sleep(1)
