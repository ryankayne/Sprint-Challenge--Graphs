from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


def add_room_to_graph(room, exits):
    # setting key to room (int) and value to empty dict
    traversal_graph[room] = {}
    for exit in exits:
        # for every iteration of exit, set the key to the exit and value to ?
        # it would look like this {0: {'n': '?'}}
        traversal_graph[room][exit] = '?'

traversal_graph = {}
traversal_path = []
reverse = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

start_room = player.current_room.id
start_room_exits = player.current_room.get_exits()

# have to add prev_room to keep track later
prev_room = None
# have to establish travel_direction to keep track for traversal later
travel_direction = None

# start of search stack
s = Stack()
s.push(start_room)

# len room_graph is total rooms. so we need to keep running (while loop) until the graph I create is equal to the room_graph length
while len(traversal_graph) < len(room_graph):
    # normal stuff. while something is in the stack, run this code
    while s.size() > 0:
        # current room is the item popped off the stack
        current_room = s.pop()

        # if current_room (which is an integer) is not in the traversal graph, grab the room number and exits and put them through the graph method. 
        if current_room not in traversal_graph:
            exits = player.current_room.get_exits()
            add_room_to_graph(current_room, exits)

        # if first iteration, prev_room will be None, bc I had to set it like that default. but once it's not first iteration, it will set the current room to previous room's travel direction. (e.g. if room 0 traveled N to room 1, current_room would be 1 since prev_room was 0 and travel direction was N)
        if prev_room is not None:
            traversal_graph[prev_room][travel_direction] = current_room
            # I also have to keep track of the back track so for now I am running the travel direction through my reverse dictionary. I have to do this bc each move will change the prev room.
            traversal_graph[current_room][reverse[travel_direction]] = prev_room

        # if a ? is in the values slots of any of the dictionary keys, then do the following code
        if '?' in traversal_graph[current_room].values():
            exits = []
            # for the room direction and room id in the graph, 
            for room_direction, room_id in traversal_graph[current_room].items():
                # if room id is unknown, which is ?,
                if room_id == '?':
                    # then replace the ? with the room direction
                    exits.append(room_direction)
            # now out of the available exits, randomly choose a direction to travel
            travel_direction = random.choice(exits)
            # set the prev room to the current room
            prev_room = player.current_room.id
            # move to the next room
            player.travel(travel_direction)

            # add the traveled direction to the traversal path
            traversal_path.append(travel_direction)
            # push the current room number onto the stack to repeat the cycle
            s.push(player.current_room.id)
        else:
            s.pop()
            # this will cycle through until all rooms have been visited, creating the completed graph with all rooms and possible exits being documented. then when there's no more, it will pop off the last room which will terminate the While loop and onto the next section
    

    q = Queue()
    q.enqueue([player.current_room.id])
    # q.enqueue([world.starting_room.id])
    prev_room = None

    visited = set()
    
    while q.size() > 0:
        path = q.dequeue()
        current_room = path[-1]

        if current_room not in visited:
            visited.add(current_room)
            
            if '?' in traversal_graph[current_room].values():
                break
            else:
                # this for loop will cycle through an item in the traversal graph but only for the VALUES of the corresponding key for the passed in current room. e.g. 1: {'n': 2, 's': 0} would loop through 2 and 0. this loop is to set the prev room and next room based on current room.
                for next_room in traversal_graph[current_room].values():
                    # set prev room to the current room
                    prev_room = current_room
                    # set a new path to a list of the existing path (make a copy)
                    new_path = list(path)
                    # append the next room to the copied path
                    new_path.append(next_room)
                    # add the copied path to the Queue
                    q.enqueue(new_path)
    
    # take the path and reverse the order since we are going to back track in a second
    path = path[::-1]

    # while the path has more than 1 room in it, run the code
    while len(path) > 1:
        # we are setting the last item in the path to back track (already reversed)
        back_track = path.pop()

        # loop through the keys of the traversal graph
        for room_direction in traversal_graph[back_track]:
            # if graph[room number][direction] is the same as the last item in path, 
            if traversal_graph[back_track][room_direction] == path[-1]:
                # set travel direction to the room direction
                travel_direction = room_direction
                # set the prev room to the player's current room
                prev_room = player.current_room.id
                # move the player via the travel method with the room direction
                player.travel(room_direction)
                # also append that direction to the traversal path
                traversal_path.append(room_direction)
                # update the current room to the player's current room (after travel)
                current_room = player.current_room.id
    # once this is done, reset the prev room to None since while loop is done
    prev_room = None
    
    # push the current room to the Stack
    s.push(player.current_room.id)

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
