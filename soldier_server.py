# Import necessary libraries and modules
import grpc
import soldier_pb2
import soldier_pb2_grpc
import random
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import re
import logging

# Configure the logging settings
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize commander position as (-1, -1)
commander_position = (-1, -1)
soldiers = []  # Store the soldiers list globally
server = None  # Store the server object

def print_matrix(matrix):
     # Function to print the matrix with formatting
    for row in matrix:
        for val in row:
            is_red = bool(re.search(r'\033\[[0-9;]*m', val))
            clean_val = re.sub(r'\033\[[0-9;]*m', '', val)
            padding = max(0, 7 - len(clean_val))
            # If it's not red, set the text color to green
            formatted_val = val if is_red else "\033[92m{}\033[0m".format(clean_val.ljust(7))
            print(formatted_val, end=' ')
        print()
        print()

def printLayout(matrix):
     # Function to print the matrix with formatting
    for row in matrix:
        for val in row:
            
            clean_val = re.sub(r'\033\[[0-9;]*m', '', val)
            formatted_val = "\033[92m{:<7}\033[0m".format(clean_val)  # Ensure a width of 7 characters
            print(val.replace(clean_val, formatted_val), end=' ')
            
        print()
        print()

def soldiers_info(soldiers):
     # Function to print initial soldiers' information
    print("\nIntial soldiers information:")
    print()
    for soldier in soldiers:
        print(f"ID: {soldier.id}, Position: ({soldier.x}, {soldier.y}), Speed: {soldier.speed}, Commander: {soldier.is_commander}, Alive: {soldier.alive}")
        logging.info(f"ID: {soldier.id}, Position: ({soldier.x}, {soldier.y}), Speed: {soldier.speed}, Commander: {soldier.is_commander}, Alive: {soldier.alive}")

        if soldier.is_commander:
            commander_id = soldier.id

    if commander_id is not None:
        print()
        print(f"Soldier ID {commander_id} is elected as the commander.")
        logging.info(f"Soldier ID {commander_id} is elected as the commander.")

    print()

class SoldierMatrixService(soldier_pb2_grpc.SoldierMatrixServiceServicer):
    def __init__(self):
        # Initialize the service
        self.T = None
        self.t = None
        self.missile_thread = None
        self.field_size = None  # Initialize field size as None
        self.matrix = None  # Initialize the matrix as None
        self.missile_coordinates= []
        self.commander = None
        self.soldier = None
        super().__init__()

    def GenerateMatrix(self, request, context):
         # gRPC service method to generate the soldier matrix
        global commander_position, soldiers, server  # Access the global variables

        field_size = request.field_size
        Num_soldier = request.Num_soldier
        self.t = request.t  # Get t from the client request
        self.T = request.T  # Get T from the client request


        # Initialize the field size and matrix if not already set
        if self.field_size is None:
            self.field_size = field_size
            self.matrix = [['.' for _ in range(field_size)] for _ in range(field_size)]

        if Num_soldier > self.field_size * self.field_size:
            # Stop the server if there are more soldiers than available positions
            self.stop_server1()
            return soldier_pb2.SoldierMatrixResponse(matrix_row=["Error: More soldiers than available positions."])

        # Generate random positions for Num_soldier soldiers and place 'S' at those positions
        soldiers = []

        occupied_positions = set()

        for soldier_id in range(1, Num_soldier + 1):  # Soldier IDs from 1 to n
        # Generate a random position and check if it's already occupied
            while True:
                x, y = random.randint(0, self.field_size - 1), random.randint(0, self.field_size - 1)
                if (x, y) not in occupied_positions:
                    break

            # Mark the position as occupied
            occupied_positions.add((x, y))    

            self.matrix[x][y] = f"S{soldier_id}"        #Use soldier ID to mark the position
            
            # Generate a random speed
            speed = random.randint(0, 4)

            # Add the soldier to the list
            soldiers.append(soldier_pb2.Soldier(id=soldier_id, x=x, y=y, speed=speed,alive=True))

        if soldiers:
            commander = random.choice(soldiers)
            commander.is_commander = True
            commander_position = (commander.x, commander.y)
            self.matrix[commander_position[0]][commander_position[1]] = f"C{commander.id}"
        
        soldiers_info(soldiers)

        print("Initial battlefield view:")
        print()
        printLayout(self.matrix)

        self.simulate_missiles(self.matrix)

        def stop_server():
        # Stop the server gracefully
            server.stop(0)

        threading.Thread(target=stop_server).start()

        return soldier_pb2.SoldierMatrixResponse(soldiers=soldiers)
    

    def simulate_missiles(self, matrix):
         # Simulate missile launches and update the matrix
        global soldiers
        self.T = int(self.T)
        self.t = int(self.t)

        count = 1
        # Simulate missile launches every t seconds until T duration
        while self.T > 0:
            
            x, y = random.randint(0, self.field_size - 1), random.randint(0, self.field_size - 1)
            impact_radius = random.randint(1, 4)

            print()
            print()
            print("Battlefield view after launching missile -", count,":")
            logging.info(f"Battlefield view after launching missile - {count}:")

            alive=len(soldiers)
            print("Number of soldiers currently alive:",alive)
            logging.info(f"Number of soldiers currently alive: {alive}")
            # Update the matrix to mark the impact of the missile
            missile_coordinates, matrix_copy =self.Missile_Approaching(x, y, impact_radius)

            self.T -= self.t

            print_matrix(matrix_copy)
           
            self.broadcast_commander(missile_coordinates)
            
            count=count+1
            # Sleep for t seconds
            time.sleep(self.t)
        print()    
        print("View of battlefield after the war.") 
        logging.info("View of battlefield after the war.") 
        alive=len(soldiers)
        print("Total number of soldiers alive after the war:",alive) 
        logging.info(f"Total number of soldiers alive after the war: {alive}") 
        printLayout(matrix)

    def Missile_Approaching(self, x, y, impact_radius):
        # Simulate missile impact on the matrix
        
        radius=2*impact_radius-1
        new_x1=x-(impact_radius-1)
        new_y1=y-(impact_radius-1)

        missile_coordinates=[]

        new_x2=new_x1+radius-1
        new_y2=new_y1+radius-1

        matrix_copy = [row[:] for row in self.matrix]
     
        for i in range(new_x1, new_x2 + 1):
           for j in range(new_y1, new_y2 + 1):
               if 0 <= i < self.field_size and 0 <= j < self.field_size:  # Check if the coordinates are within valid bounds
                    existing_value = self.matrix[i][j]
                    matrix_copy[i][j] = f'\033[91m{existing_value:7}\033[0m'
                    missile_coordinates.append((i,j))
 
        print(f"Missile launched at coordinates (x={x}, y={y}) with impact radius {impact_radius}")
        logging.info(f"Missile launched at coordinates (x={x}, y={y}) with impact radius {impact_radius}")
        print()

        return missile_coordinates, matrix_copy

    def broadcast_commander(self,missile_coordinates):
        # Broadcast missile alert to soldiers and commander
        print()
        print("\033[91mMissile Alert.\033[0m")
        logging.info("Missile Alert.")
        print()
    
        self.red_zone(missile_coordinates)
        self.take_shelter(missile_coordinates)

    def red_zone(self,missile_coordinates):
         # Identify soldiers and commander in the red zone
        count=0
        for soldier in soldiers:
            obj_coordinate = (soldier.x, soldier.y)
            if soldier.is_commander:

                if obj_coordinate in missile_coordinates:
                    print("\033[91mCommander {} is in the red zone.\033[0m".format(soldier.id))
                    logging.info("Commander {} is in the red zone.".format(soldier.id))
                    count=count+1
            else:
                if obj_coordinate in missile_coordinates:
                    print("\033[91mSoldier {} is in the red zone.\033[0m".format(soldier.id))
                    logging.info("Soldier {} is in the red zone.".format(soldier.id))
                    count=count+1
        
        if count == 0:
            print("No soldiers and Commander are in the red zone.")
            logging.info("No soldiers and Commander are in the red zone.")
        print()


    def take_shelter(self, missile_coordinates):
        # Determine safe moves for soldiers and commander

        # Create a copy of the soldiers list to avoid modifying it during iteration
        soldiers_copy = soldiers[:]
        
        commander = None  # Initialize the commander variable
        reelect_commander = False  # Initialize the reelect_commander flag

        # Create a set to keep track of occupied positions
        occupied_positions = {(soldier.x, soldier.y) for soldier in soldiers_copy}
        
        random.shuffle(soldiers_copy)
        for soldier in soldiers_copy:
            if soldier.is_commander:
                commander = soldier  # Assign the commander object
                continue  # Skip the commander

            obj_coordinate = (soldier.x, soldier.y)

            if obj_coordinate not in missile_coordinates:
                pass

            else:
                safe_moves = []  # List to store safe move options

                for dx in range(-soldier.speed, soldier.speed + 1):
                    for dy in range(-soldier.speed, soldier.speed + 1):
                        new_x, new_y = soldier.x + dx, soldier.y + dy

                        # Check if the new coordinates are within bounds and not in the missile zone
                        if (
                            0 <= new_x < self.field_size
                            and 0 <= new_y < self.field_size
                            and (new_x, new_y) not in missile_coordinates 
                        ):
                            safe_moves.append((new_x, new_y))
                
                # Check if the current position is still a safe move (updated position after the first missile)
                if obj_coordinate not in missile_coordinates:
                    safe_moves.append(obj_coordinate)

                if safe_moves:
                    # Filter out safe moves that are not already occupied
                    safe_moves = [move for move in safe_moves if move not in occupied_positions]

                if not safe_moves:
                    # If no safe moves are available after filtering, mark the soldier as dead
                    soldier.alive = False
                    soldiers.remove(soldier)
                    self.matrix[soldier.x][soldier.y] = '.'
                    occupied_positions.remove((soldier.x, soldier.y))
                else:
                    # Choose a safe move deterministically 
                    new_x, new_y = random.choice(safe_moves)
                    
                    # Remove the previous position from occupied_positions if it exists
                    occupied_positions.remove((soldier.x, soldier.y))

                    # Add the new position to occupied_positions
                    occupied_positions.add((new_x, new_y))
                    self.matrix[soldier.x][soldier.y] = '.'
                    soldier.x, soldier.y = new_x, new_y
                    self.matrix[new_x][new_y] = f"S{soldier.id}" 
                    print("\033[92mSoldier {} finally moved to safe zone at {}\033[0m".format(soldier.id, (soldier.x, soldier.y)))
                    logging.info("Soldier {} finally moved to safe zone at {}".format(soldier.id, (soldier.x, soldier.y)))

        if commander:
            safe_moves = []  # List to store safe move options for the commander

            obj_coordinate = (commander.x, commander.y)
            if obj_coordinate not in missile_coordinates:
                pass

            else:

                for dx in range(-commander.speed, commander.speed + 1):
                    for dy in range(-commander.speed, commander.speed + 1):
                        new_x, new_y = commander.x + dx, commander.y + dy

                        # Check if the new coordinates are within bounds and not in the missile zone
                        if (
                            0 <= new_x < self.field_size
                            and 0 <= new_y < self.field_size
                            and (new_x, new_y) not in missile_coordinates 
                        ):
                            safe_moves.append((new_x, new_y))
                
                # Check if the current position is still a safe move (updated position after the first missile)
                if (commander.x, commander.y) not in missile_coordinates:
                    safe_moves.append((commander.x, commander.y))

                if safe_moves:
                    # Filter out safe moves that are not already occupied
                    safe_moves = [move for move in safe_moves if move not in occupied_positions]

                if not safe_moves:
                    # If no safe moves are available after filtering, mark the soldier as dead
                    commander.alive = False
                    soldiers.remove(commander)
                    self.matrix[commander.x][commander.y] = '.'
                    occupied_positions.remove((commander.x, commander.y))
                else:
                    # Choose a safe move deterministically (e.g., prioritize movement in a specific order)
                    new_x, new_y = random.choice(safe_moves)
                    
                    # Remove the previous position from occupied_positions if it exists
                    occupied_positions.remove((commander.x, commander.y))

                    # Add the new position to occupied_positions
                    occupied_positions.add((new_x, new_y))
                    self.matrix[commander.x][commander.y] = '.'
                    commander.x, commander.y = new_x, new_y
                    self.matrix[new_x][new_y] = f"C{commander.id}"
                    print("\033[92mCommander {} finally moved to safe zone at {}\033[0m".format(commander.id, (commander.x, commander.y)))
                    logging.info("Commander {} finally moved to safe zone at {}".format(commander.id, (commander.x, commander.y)))
                    
        num_soldiers = len(soldiers)
        if num_soldiers != 0:
            if not commander.alive:
                reelect_commander = True  # Set the flag to re-elect a commander
        
        if reelect_commander:
            new_commander = None
            
            # Find a new commander from the remaining alive soldiers (if any)
            for soldier in soldiers_copy:
                if soldier.alive and not soldier.is_commander:
                    new_commander = soldier
                    break
            
            if new_commander:
                # Set the is_commander flag for the new commander
                new_commander.is_commander = True
                commander = new_commander
                print()
                print("Commander", commander.id, "has been re-elected.")
                logging.info("Commander {} has been re-elected.".format(commander.id))
                self.matrix[new_commander.x][new_commander.y] = f"C{commander.id}"
            else:
                print("There are no eligible soldiers to become the new commander.")
                logging.info("There are no eligible soldiers to become the new commander.")

        total_dead_soldiers = [soldier for soldier in soldiers_copy if not soldier.alive]

        self.was_hit(total_dead_soldiers)
            
    def was_hit(self,total_dead_soldiers):
    # Report on soldiers and commander hit by missiles
        count=0
        if total_dead_soldiers:
            print()
            print("\033[91mInformation About soldiers who died after the missile launch:\033[0m")
            logging.info("Information About soldiers who died after the missile launch:")
            for dead_soldier in total_dead_soldiers:
                if dead_soldier.is_commander:

                    print("\033[91mCommander {} is dead\033[0m".format(dead_soldier.id))
                    logging.info("Commander {} is dead".format(dead_soldier.id))
                    count=count+1
                else:
                    print("\033[91mSoldier {} is dead\033[0m".format(dead_soldier.id))
                    logging.info("Soldier {} is dead".format(dead_soldier.id))
                    count=count+1

        if count==0:
            print()
            print("No soldiers and Commander died during this missile attack.")
            logging.info("No soldiers and Commander died during this missile attack.")

    def stop_server1(self):
        global server
        if server:
            # Stop the server gracefully
            server.stop(0)

def serve():
    # Function to start the gRPC server
    global server
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    soldier_pb2_grpc.add_SoldierMatrixServiceServicer_to_server(SoldierMatrixService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    # Start the gRPC server
    serve()


