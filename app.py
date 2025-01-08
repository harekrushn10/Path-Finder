from flask import Flask, jsonify, request
from collections import deque
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class RoadNetwork:
    def __init__(self):
        self.graph = {}

    def add_intersection(self, intersection_id):
        if intersection_id not in self.graph:
            self.graph[intersection_id] = []

    def add_road(self, from_intersection, to_intersection, length, speed_limit):
        if from_intersection in self.graph and to_intersection in self.graph:
            self.graph[from_intersection].append({
                'to': to_intersection,
                'length': length,
                'speed_limit': speed_limit
            })
            # Add reverse road for bidirectional path
            self.graph[to_intersection].append({
                'to': from_intersection,
                'length': length,
                'speed_limit': speed_limit
            })
        else:
            print(f"One or both intersections {from_intersection}, {to_intersection} do not exist.")

    def find_path(self, source, destination):
        if source == destination:
            return [source], 0, 0  # No need for average speed if same

        visited = set()
        queue = deque([(source, [source], 0, 0)])  # (current_node, path, total_distance, total_speed)
        
        while queue:
            current, path, total_distance, total_speed = queue.popleft()
            
            if current == destination:
                avg_speed = total_speed / len(path) if len(path) > 1 else total_speed
                return path, total_distance, avg_speed

            for road in self.graph.get(current, []):
                next_intersection = road['to']
                if next_intersection not in visited:
                    visited.add(next_intersection)
                    queue.append((
                        next_intersection,
                        path + [next_intersection],
                        total_distance + road['length'],
                        total_speed + road['speed_limit']
                    ))

        # If no direct path found, try finding a path via another node
        for via in self.graph.keys():
            if via != source and via != destination:
                path1, dist1, speed1 = self.find_path(source, via)
                path2, dist2, speed2 = self.find_path(via, destination)
                if path1 and path2:
                    total_dist = dist1 + dist2
                    total_speed = speed1 + speed2
                    avg_speed = total_speed / (len(path1) + len(path2) - 1)  # avg speed for combined path
                    return path1 + path2[1:], total_dist, avg_speed

        return None, 0, 0  # No path found

# Initialize road network and add intersections and roads
network = RoadNetwork()

# Add intersections
intersections = ['Alkapuri Circle', 'Kala Ghoda Circle', 'Akota Bridge Junction',
                 'Jetalpur Bridge Junction', 'Nyay Mandir Intersection', 'Waghodia Chowkdi',
                 'Parul University', 'National Highway 8', 'Vadodara-Halol Highway', 'Vadodara-Mumbai Expressway']

for intersection in intersections:
    network.add_intersection(intersection)

# Add roads with distances and speed limits
network.add_road('Alkapuri Circle', 'Kala Ghoda Circle', 2.5, 50)
network.add_road('Kala Ghoda Circle', 'Akota Bridge Junction', 3.0, 50)
network.add_road('Akota Bridge Junction', 'Jetalpur Bridge Junction', 2.0, 50)
network.add_road('Jetalpur Bridge Junction', 'Nyay Mandir Intersection', 1.5, 40)
network.add_road('Nyay Mandir Intersection', 'Alkapuri Circle', 2.8, 40)
network.add_road('Waghodia Chowkdi', 'Parul University', 10.0, 60)
network.add_road('Waghodia Chowkdi', 'National Highway 8', 5.0, 80)
network.add_road('Parul University', 'Vadodara-Halol Highway', 12.0, 60)
network.add_road('National Highway 8', 'Vadodara-Mumbai Expressway', 15.0, 100)
network.add_road('Vadodara-Halol Highway', 'Alkapuri Circle', 18.0, 70)

@app.route('/find_path', methods=['GET'])
def find_path_route():
    source = request.args.get('source')
    destination = request.args.get('destination')
    
    path, total_distance, avg_speed = network.find_path(source, destination)
    
    if path:
        return jsonify({"path": path, "total_distance": total_distance, "avg_speed": avg_speed})
    else:
        return jsonify({"path": None, "total_distance": 0, "avg_speed": 0})

if __name__ == '__main__':
    app.run(debug=True)
