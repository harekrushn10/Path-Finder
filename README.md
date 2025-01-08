# Path-Finder
### Road Network Path Finder - Documentation (For README file)

#### Overview
The **Road Network Path Finder** is an application that allows users to find the shortest paths between various intersections in a road network. The network is represented as a graph where intersections are nodes and roads between them are edges. The pathfinding algorithm helps users determine the most efficient route based on available roads and their properties (e.g., length and speed limits). The application supports bidirectional paths and can suggest intermediate routes if a direct path is not available.

#### Features
- **Bidirectional Paths**: The application supports bidirectional paths, meaning if there is a road from `A` to `B`, there is also a road from `B` to `A`.
- **Shortest Path Finder**: The algorithm computes the shortest path based on the distance between intersections.
- **Via Routes**: If no direct path exists between the source and destination, the system will compute the path via intermediate intersections, ensuring maximum flexibility in route selection.
- **Dynamic Interaction**: Users can select different source and destination intersections through a simple web interface and get the route information in real-time.
- **Real-time Data Fetch**: Data is fetched from a backend server to compute and display the path dynamically on the frontend.
- **Distance Calculation**: The total distance of the path is displayed, so users can compare various routes.

---

### Data Structures Used

The following data structures are utilized in the application:

1. **Graph** (Adjacency List)
   - **Representation**: The road network is represented as a graph using an **adjacency list**.
   - **Nodes**: The intersections (e.g., `Alkapuri Circle`, `Kala Ghoda Circle`, etc.) are the nodes in the graph.
   - **Edges**: The roads between intersections are edges, and each edge contains information about:
     - **Destination Intersection** (where the road leads)
     - **Distance** (the length of the road in kilometers)
     - **Speed Limit** (the maximum speed allowed on the road)
   - **Bidirectionality**: For each road, we add the reverse road (making the graph bidirectional), so we ensure that traffic can flow in both directions between intersections.
   
2. **Queue** (Breadth-First Search)
   - **Representation**: A **queue** (implemented using Python's `deque` from the `collections` module) is used to implement the pathfinding algorithm.
   - **Why BFS?**: Breadth-First Search (BFS) is used to explore the graph starting from the source node. It explores neighbors level by level, ensuring that the shortest path is found when nodes are visited.
   - **Queue Operations**:
     - **Push**: For each intersection, push the current intersection and path along with the accumulated distance onto the queue.
     - **Pop**: Pop the first element from the queue, check if it is the destination, and explore its neighbors.
   - **Visit Tracking**: A **visited set** is used to keep track of intersections that have already been explored to prevent reprocessing and infinite loops.
   - **Path Reconstruction**: If the destination is found, the path and total distance are returned.

3. **Sets** (Visited Intersections)
   - **Representation**: A **set** is used to store the intersections that have already been visited during the BFS traversal.
   - **Why Sets?**: Sets provide fast O(1) average-time complexity for membership checks, ensuring that previously visited intersections are not revisited, preventing cycles and redundant calculations.

---

### How It Works

1. **Backend Logic**:
   - The backend (written in Python using **Flask**) handles the graph creation, pathfinding, and response generation.
   - The `RoadNetwork` class is responsible for:
     - Adding intersections to the graph.
     - Adding roads with distances and speed limits between intersections (including bidirectional roads).
     - The `find_path` method uses a **Breadth-First Search (BFS)** algorithm to explore the graph and find the shortest path.
     - If no direct path exists, the function attempts to find a path via intermediate intersections, ensuring a path is found even when there are no direct roads.

2. **Frontend Logic**:
   - The frontend (HTML + JavaScript) provides a user-friendly interface where users can select a source and destination intersection from dropdown lists.
   - When the user selects a route and clicks the "Find Path" button, the frontend sends an HTTP GET request to the backend with the selected source and destination.
   - The backend responds with a JSON object containing the path and the total distance.
   - The frontend then dynamically updates the page to display the path (if found) along with the total distance.

3. **Path Calculation**:
   - The BFS algorithm explores the road network to find the shortest path from the source to the destination.
   - If the destination is unreachable from the source (no direct or via paths exist), the system will notify the user accordingly.

---

### Example Use Case

1. **Finding a Direct Path**:
   - **Source**: `Alkapuri Circle`
   - **Destination**: `Kala Ghoda Circle`
   - **Result**: The shortest direct path (if exists) is returned along with its total distance.

2. **Finding a Path via Another Intersection**:
   - **Source**: `Parul University`
   - **Destination**: `Waghodia Chowkdi`
   - **Result**: The system checks if there is a direct path. If not, it searches for an alternative route via intermediate intersections.

3. **Bidirectional Pathfinding**:
   - The system supports finding paths in both directions. For example, a request to find the path from `Parul University` to `Waghodia Chowkdi` is equivalent to finding the path from `Waghodia Chowkdi` to `Parul University`.

---

### Project Structure

```
/Road-Network-Path-Finder
│
├── app.py               # Flask backend with pathfinding logic
├── templates/
│   ├── index.html       # Frontend HTML file with user interface
│
└── requirements.txt     # Python dependencies
```

---

### How to Run the Project

1. **Set Up Python Environment**:
   - Ensure you have **Python 3.x** installed.
   - Install the required dependencies using `pip`:
     ```
     pip install -r requirements.txt
     ```

2. **Run the Backend**:
   - In your terminal, navigate to the project directory and run:
     ```
     python app.py
     ```
   - This will start the Flask server on `http://127.0.0.1:5000`.

3. **Access the Frontend**:
   - Open the `index.html` file in a browser (ensure it's served via a web server or opened as a local file).

4. **Using the Application**:
   - Select a source and destination intersection, click "Find Path," and the path and distance will be displayed.

---

### Future Improvements
- **Path Optimization**: Extend the system to optimize paths based on travel time (incorporating speed limits) rather than just distance.
- **User Authentication**: Add user authentication for personalized features (e.g., saving favorite routes).
- **Real-Time Traffic**: Integrate real-time traffic data to dynamically adjust the route based on current conditions.
