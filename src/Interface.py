class Interface:
    def __init__(self, r, u):
        self.username = None
        self.rent = r
        self.user = u

    @staticmethod
    def display_menu():
        print("---------- Car Rent Menu ----------")
        print("1. Rent a car")
        print("2. Return a car")
        print("3. View status of a car")
        print("4. View all cars")
        print("5. Back")
        return input("Please select an option (1-5): ")

    def login(self):
        print("---------- Login ----------")
        self.username = input("Username: ")
        password = input("Password: ")
        if self.user.login_user(self.username, password):
            self.user_interface()
        self.authentication()

    def register(self):
        print("---------- Register ----------")
        self.username = input("Username: ")
        password = input("Password: ")
        if self.user.register_user(self.username, password):
            self.user_interface()
        self.authentication()

    def authentication(self):
        print("---------- Connection ----------")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Please select an option (1-3): ")
        if choice == '1':
            self.login()
        elif choice == '2':
            self.register()
        elif choice == '3':
            exit(0)

    def print_cars(self):
        cars = self.rent.get_all_cars()
        for car in cars:
            print(car)

    def user_interface(self):
        while True:
            choice = self.display_menu()
            if choice == '1':
                self.print_cars()
                car_id = input("Enter car ID to rent: ")
                self.rent.rent_car(car_id, self.username)

            elif choice == '2':
                car_id = input("Enter car ID to return: ")
                self.rent.return_car(car_id)

            elif choice == '3':
                self.print_cars()
                car_id = input("Enter car ID to view status: ")
                self.rent.get_car_status(car_id)

            elif choice == '4':
                self.print_cars()

            elif choice == '5':
                self.authentication()

            else:
                print("Invalid option! Please select a number between 1 and 5.")
