# Import necessary libraries and modules
import grpc
import soldier_pb2
import soldier_pb2_grpc
import logging

# Configure the logging settings
logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Define a function to run the client application
def run():
    # Create a gRPC channel to connect to the server
    channel = grpc.insecure_channel('localhost:50051')
    stub = soldier_pb2_grpc.SoldierMatrixServiceStub(channel)

    # Prompt the user to enter simulation parameters and log the inputs
    field_size = int(input("Enter the desired size of the matrix (field size): "))
    logging.info("Entered field size: %d", field_size)

    num_soldier = int(input("Enter the number of soldiers you want (Num_soldier): "))
    logging.info("Entered number of soldiers: %d", num_soldier)

    t = int(input("Enter the time interval (t) between missile launches in seconds: "))
    logging.info("Entered time interval (t): %d", t)

    T = int(input("Enter the total simulation time (T) in seconds: "))
    logging.info("Entered total simulation time (T): %d", T)

    # Create a gRPC request with the user-entered parameters
    request = soldier_pb2.SoldierMatrixRequest(field_size=field_size, Num_soldier=num_soldier,t=t,T=T)

    try:
        # Call the gRPC service method to generate the soldier matrix
        response = stub.GenerateMatrix(request)

        # Check if the response contains a matrix row (indicating a missile hit)
        if response.matrix_row:
            print(f"\033[91m{response.matrix_row[0]}\033[0m") 
        else:
            commander_id = None
            count=0
            
            # Print information about soldiers and commander after the simulation
            print("\nInformation about soldiers and commander after the War.")
            logging.info("Information about soldiers and commander after the War.")
            print()
            for soldier in response.soldiers:
                print(f"ID: {soldier.id}, Position: ({soldier.x}, {soldier.y}), Speed: {soldier.speed}, Commander: {soldier.is_commander}, Alive: {soldier.alive}")
                logging.info(f"ID: {soldier.id}, Position: ({soldier.x}, {soldier.y}), Speed: {soldier.speed}, Commander: {soldier.is_commander}, Alive: {soldier.alive}")
                count = count + 1
                if soldier.is_commander:
                    commander_id = soldier.id

            if count == 0:
                print("\033[91mAll Soldiers and commander died.\033[0m")
                logging.info("All Soldiers and commander died.")
            print()

            if commander_id is not None:
                print(f"Soldier ID {commander_id} is elected as the commander.")
                logging.info(f"Soldier ID {commander_id} is elected as the commander.")
            print()

            rem_soldier = len(response.soldiers)

            # Determine the outcome of the war based on the remaining soldiers
            if num_soldier % 2 == 0:
                if rem_soldier > (num_soldier/2):
                    print("\033[92mSoldiers won war.\033[0m")
                    logging.info("Soldiers won war.")
                else:
                    print("\033[91mSoldiers lost War.\033[0m")
                    logging.info("Soldiers lost war.")
            else:
                if rem_soldier < ((num_soldier+1)/2):
                    print("\033[91mSoldiers lost war.\033[0m")
                    logging.info("Soldiers lost war.")
                else:
                    print("\033[92mSoldiers won war.\033[0m") 
                    logging.info("Soldiers won war.")

    except grpc.RpcError as e:
        # Handle gRPC communication errors here
        print(f"An error occurred: {e.details()}")
    
if __name__ == '__main__':
    # Run the client application
    run()
