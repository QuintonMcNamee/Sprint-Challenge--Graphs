from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# utils
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

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

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
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

def traversal_function(world, traversal_path):

    # methods
    # choose an unexplored direction from the player's current room
    def get_unexplored_direction(visited, room):
        # declare variables
        room_id = room.id
        exits = visited[room_id]
        # loop through all directions in exits
        for direction in exits:
            # if direction is unexplored, return that direction
            if exits[direction] == '?' and room.get_room_in_direction(direction).id not in visited:
                return direction
        # else if all directions explored, return none
        return None

    # main
    # create a stack for dft
    s = Stack()
    # declare variables
    room_id = 0
    room = world.rooms[room_id]
    visited = {0: {}}
    # loop until all rooms have been explored
    while len(visited) < len(world.rooms):
        room = world.rooms[room_id]
        # if room hasnt been visited, set room in visited to none and directions to unexplored
        if room not in visited:
            visited[room.id] = {}
            for direction in room.get_exits():
                visited[room.id][direction] = '?'
        # choose next direction
        next_direction = get_unexplored_direction(visited, room)
        # if no unexplored directions
        if next_direction == None:
            # return the next room we will explore
            # get next traversal from the end of the stack
            next_traversal = s.pop()
            # add next traversal to traversal path
            traversal_path.append(next_traversal)
            next_room = room.get_room_in_direction(next_traversal)
            # if next room is unexplored, set the room id equal to the next room id
            if '?' in visited[next_room.id].values():
                room_id = next_room.id
        # else if there is an unexplored direction
        else:
            # add next direction to the traversal path
            traversal_path.append(next_direction)
            # declare the next room
            next_room = room.get_room_in_direction(next_direction)
            # add the next room id to the current room 
            visited[room_id][next_direction] = next_room.id
            # and set the next room id to unexplored
            visited[next_room.id] = {}
            # loop through all directions in exits
            for direction in next_room.get_exits():
                # set the direction in the next room to unexplored
                visited[next_room.id][direction] = '?'
            # flip the next direction
            if next_direction == 'n':
                flipped = 's'
            if next_direction == 'e':
                flipped = 'w'
            if next_direction == 's':
                flipped = 'n'
            if next_direction == 'w':
                flipped = 'e'
            visited[next_room.id][flipped] = room.id
            s.push(flipped)
            room_id = next_room.id

# run the traversal function
traversal_function(world, traversal_path)
# print out the traversal path
print('\n')
print('TRAVERSAL PATH: ', traversal_path)
print('\n')

# TRAVERSAL TEST
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
