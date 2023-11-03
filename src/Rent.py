from src.Data import default_cars


class Rent:
    def __init__(self, c):
        self.connection = c
        for car in default_cars:
            self.add_car(car["car_id"], car["make"], car["model"])

    def car_exists(self, car_key):
        if self.connection.exists(car_key):
            return True
        else:
            print("Car by that ID doesn't exits!")
            return False

    def add_car(self, car_id, make, model):
        """Add a car to the redisdb database."""
        # Using hashes to store car details
        car_key = f"car:{car_id}"
        self.connection.hset(car_key, mapping={
            "make": make,
            "model": model
        })

    def get_all_cars(self):
        # Fetch all car keys
        car_keys = self.connection.keys("car:*")
        cars = []
        for key in car_keys:
            car_details = self.connection.hgetall(key)
            car_id = key.decode('utf-8').split(":")[1]
            make = car_details[b'make'].decode('utf-8')
            model = car_details[b'model'].decode('utf-8')
            cars.append({
                "car_id": car_id,
                "make": make,
                "model": model
            })
        return cars

    def rent_car(self, car_id, customer_name):
        car_key = f"car:{car_id}"
        pipeline = self.connection.pipeline()
        pipeline.watch(car_key)
        if not self.car_exists(car_key):
            return
        # Check if car is already rented
        if pipeline.hget(car_key, "rented_by"):
            print(f"Car {car_id} is already rented!")
            return
        try:
            pipeline.multi()
            pipeline.hset(car_key, "rented_by", customer_name)
            pipeline.execute()
            owner = self.get_car_owner(car_id)
            print(f"Car {car_id} rented to {owner}!")
        except self.connection.exceptions.WatchError:
            print(f"Car {car_id} was just rented by someone else!")

    def return_car(self, car_id):
        car_key = f"car:{car_id}"
        if not self.car_exists(car_key):
            return
        # Check if car is already rented
        if not self.connection.hget(car_key, "rented_by"):
            print(f"Car {car_id} is not currently rented!")
            return
        # If rented, remove rented_by field for the car
        self.connection.hdel(car_key, "rented_by")
        print(f"Car {car_id} returned successfully!")

    def get_car_status(self, car_id):
        car_key = f"car:{car_id}"
        if not self.car_exists(car_key):
            return
        rented_by = self.connection.hget(car_key, "rented_by")
        if rented_by:
            print(f"Car {car_id} is rented by {rented_by.decode('utf-8')}")
        else:
            print(f"Car {car_id} is available for rent")

    def get_car_owner(self, car_id):
        car_key = f"car:{car_id}"
        return self.connection.hget(car_key, "rented_by").decode('utf-8')
