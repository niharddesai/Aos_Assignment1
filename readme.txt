Problem Statement: In an NxN battlefield, M soldiers with varying speeds and positions face missile attacks categorized by impact and radius. The Commander, randomly chosen from the soldiers, relays threat information. Soldiers can move within their speed limit to avoid the missile's impact zone. If the Commander dies, a new one is randomly selected. If over 50% of soldiers survive after T time, victory is achieved.

--------------------------------------------------------
	GROUP DETAILS 
--------------------------------------------------------

**Group Members:**

1. DESAI NIHAR DHIRENDRAKUMAR     (2023H1030093P)
2. DOSHI DISHANTKUMAR NIKESHKUMAR (2023H1030095P)

**Description:**

This assignment implements a soldier matrix simulation using gRPC, where soldiers and a commander move on a grid while avoiding missile attacks. The simulation tracks soldier positions, missile strikes, and commander elections.


--------------------------------------------------------
           INSTRUCTIONS TO RUN THE CODE
--------------------------------------------------------

**Prerequisites:**

1. Python 3.x installed on your system.

**Step 1: Install gRPC**

Before running the code, you need to install the gRPC Python library and gRPC tools.

$ sudo python -m pip install grpcio

For gRPC tools,

$ python -m pip install grpcio-tools

This step is necessary to install additional tools required for gRPC code generation and protocol compilation.


**Step 2: Generate gRPC Code**

To ensure that the gRPC code is up-to-date, you need to regenerate the code using the service definition file soldier.proto. Run the following command:

$ python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. soldier.proto

This regenerates soldier_pb2.py which contains our generated request and response classes and soldier_pb2_grpc.py which contains our generated client and server classes.


**Step 3: Run the Soldier Matrix Simulation**

Now that you have installed gRPC and generated the code, follow these steps to run the soldier matrix simulation:

1. Run the server:

$ python soldier_server.py

The server will start and listen for incoming requests.

2. Open another terminal window and run the client:

$ python soldier_client.py

The client will prompt you to enter simulation parameters, including matrix size, the number of soldiers, time intervals, and simulation time. Follow the prompts to configure the simulation.

Observe the simulation results in the client terminal. You will see the matrix, soldier movements, missile alerts, and the status of soldiers and the commander.


***Additional Information:***


- Soldiers in the simulation are assigned unique IDs, positions, and speeds, allowing for dynamic movement and decision-making during the simulation.

- The commander, represented by a distinct soldier, plays a pivotal role in the simulation. The code handles commander elections when the current commander is eliminated due to a missile strike.

- The simulation provides valuable insights into real-time decision-making, as soldiers dynamically assess the battlefield, avoid missile strikes, and strive to survive.

- The code is designed to handle various scenarios, such as different grid sizes, soldier counts, and time intervals, making it a versatile tool for studying different battlefield conditions.

- Customization is encouraged: Modify the simulation parameters, such as field size, the number of soldiers, and time intervals, to observe diverse simulation outcomes.

- This project serves as an educational resource for learning about gRPC, distributed systems, and real-time simulation in Python.

- Explore the codebase to gain a deeper understanding of how gRPC services, client-server interactions, and real-time updates are implemented in the context of a soldier matrix simulation.

Git Repo Link: https://github.com/niharddesai/Aos_Assignment1.git














 
