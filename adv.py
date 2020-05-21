from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# class Queue():
#     def __init__(self):
#         self.queue = []
#     def enqueue(self, value):
#         self.queue.append(value)
#     def dequeue(self):
#         if self.size() > 0:
#             return self.queue.pop(0)
#         else:
#             return None
#     def size(self):
#         return len(self.queue)
            
visited = set()
d = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
# path = []

# while len(path) > 0:
#     move = path.pop()
#     player.travel(move)

#     if player.current_room not in visited_rooms:
#         traversal_path.append(d[move])
#         path.append(d[move])
#         visited_rooms.add(player.current_room)

def dft(start_node):
# while len(visited) < len(room_graph):
    s = Stack()
    s.push([player.current_room])

    while s.size() > 0:
        current_path = s.pop()
        # print(current_path)
        # move = path.pop()
        # player.travel(move)
        current_room = current_path[-1]
        player.current_room = current_room
        visited.add(current_room)
        exits = current_room.get_exits()
        # if path > 0:
            # print('direction', player.direction)
            # traversal_path.append(player.direction)
        neighbors = []
        for exit in exits:
            neighbor = current_room.get_room_in_direction(exit)
            if neighbor not in visited:
                neighbors.append(exit)
                
        if len(neighbors) > 0:
            copy = list(current_path)
            copy.append(current_room.get_room_in_direction(neighbors[0]))
            traversal_path.append(neighbors[0])
            s.push(copy)



while len(visited) < len(room_graph):
    current_room = player.current_room
    dft(player.current_room)
    # print(player.current_room.id)
    # break
    unvisited_neighbors = []
    temp = []
    count = 1
    while len(unvisited_neighbors) == 0:
        exits = player.current_room.get_exits()
        for exit in exits:
            neighbor = player.current_room.get_room_in_direction(exit)
            if neighbor not in visited:
                unvisited_neighbors.append(neighbor)
                player.travel(exit)
                break
        if len(unvisited_neighbors) == 0:
            next_direction = d[traversal_path[-count]]
            player.travel(next_direction)
            temp.append(next_direction)
            count += 1
    traversal_path += temp

print(traversal_path)            

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#################################################

# for movement in traversal_path:
#     player.travel(movement)
#     visited_rooms.add(player.current_room)
            # else:
            #     if len(exits) < 2:
            #         continue
                        
# path = ['n']

# while len(path) > 0:
#     move = path.pop()
#     player.travel(move)

    # if player.current_room not in visited:
    #     traversal_path.append(d[move])
    #     path.append(d[move])
                
    # direct = current_room.get_exits()


# while len(visited) < len(room_graph):
#     print(dft(player.current_room))

# print("visited", len(visited))


    # 
    # 
    # 
    #  len(room_graph):
    #     if player.current_room not in visited:
    #         s.push(player.current_room)
    #     else:





#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
