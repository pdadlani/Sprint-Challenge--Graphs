from room import Room
from player import Player
from world import World

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
traversal_path = []

# dict to keep track of unvisited exits
unvisited_exits = {}
# list to keep track of previous moves
previous = []
# opposites dict
opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}


# main method
def main():
    # starting at the player's current room, which is room 0

    # while lenght of unvisted exits is less than length of room graph
    while len(unvisited_exits) < len(room_graph)-1:
        # add the player's current room to the 'unvisited exits' dict
        add_to_graph(player.current_room)

        # while there are no more exits to visit for player's current room
        while len(unvisited_exits[player.current_room.id]) == 0:
            # walk in reverse direction, using previous' last value
            rev_dir = previous.pop()
            travel(rev_dir)

        # otherwise, choose one of the random directions from player's current room
        for_dir = unvisited_exits[player.current_room.id].pop()
        # add the direction to previous, to keep track
        previous.append(opposites[for_dir])
        travel(for_dir)

# method to add room to graph
def add_to_graph(room):
    # if the room is not in unvisited exits dict
    if room.id not in unvisited_exits:
        # add the room and its exits
        # excluding the direction that player just came from
        possible_exits = room.get_exits()
        if len(previous) > 0: #allows to simplify main() code by not manually adding starting room
            possible_exits.remove(previous[-1])
        unvisited_exits[room.id] = possible_exits

# method to travel in given direction
def travel(direction):
    # append the direction to the traversal path
    traversal_path.append(direction)
    # have player move in this direction
    player.travel(direction)

main()


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



# #######
# # UNCOMMENT TO WALK AROUND
# #######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
