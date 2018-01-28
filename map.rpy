label world_map:
    call screen map_screen


image world_map = im.Scale("images/map.png", 1920, 1080)

define map_tile_x = 480
define map_tile_y = 270

default map_0_3_room = Room("map_0_3", [RoomObject("river"),
                                          RoomObject("road")])

screen map_screen(interactable=True):
    if interactable:
        timer 0.5 action [Function(poll), Jump("world_map")]
    add "world_map"
    if interactable:
        imagemap:
            idle "world_map"

            hotspot (map_tile_x*0, map_tile_y*0, map_tile_x, map_tile_y) action Call("go_to_map", x=0, y=0)
            hotspot (map_tile_x*1, map_tile_y*0, map_tile_x, map_tile_y) action Call("go_to_map", x=1, y=0)
            hotspot (map_tile_x*2, map_tile_y*0, map_tile_x, map_tile_y) action Call("go_to_map", x=2, y=0)
            hotspot (map_tile_x*3, map_tile_y*0, map_tile_x, map_tile_y) action Call("go_to_map", x=3, y=0)

            hotspot (map_tile_x*0, map_tile_y*1, map_tile_x, map_tile_y) action Call("go_to_map", x=0, y=1)
            hotspot (map_tile_x*1, map_tile_y*1, map_tile_x, map_tile_y) action Call("go_to_map", x=1, y=1)
            hotspot (map_tile_x*2, map_tile_y*1, map_tile_x, map_tile_y) action Call("go_to_map", x=2, y=1)
            hotspot (map_tile_x*3, map_tile_y*1, map_tile_x, map_tile_y) action Call("go_to_map", x=3, y=1)

            hotspot (map_tile_x*0, map_tile_y*2, map_tile_x, map_tile_y) action Call("go_to_map", x=0, y=2)
            hotspot (map_tile_x*1, map_tile_y*2, map_tile_x, map_tile_y) action Call("go_to_map", x=1, y=2)
            hotspot (map_tile_x*2, map_tile_y*2, map_tile_x, map_tile_y) action Call("go_to_map", x=2, y=2)
            hotspot (map_tile_x*3, map_tile_y*2, map_tile_x, map_tile_y) action Call("go_to_map", x=3, y=2)

            hotspot (map_tile_x*0, map_tile_y*3, map_tile_x, map_tile_y) action Call("go_to_map", x=0, y=3)
            hotspot (map_tile_x*1, map_tile_y*3, map_tile_x, map_tile_y) action Call("go_to_map", x=1, y=3)
            hotspot (map_tile_x*2, map_tile_y*3, map_tile_x, map_tile_y) action Call("go_to_map", x=2, y=3)
            hotspot (map_tile_x*3, map_tile_y*3, map_tile_x, map_tile_y) action Call("go_to_map", x=3, y=3)

    $ ghost_position = latest_poll.get('ghost_position', '')
    if character == 'human' and ghost_position.startswith("map_"):
        $ (m, x, y) = ghost_position.split("_")
        $ x = int(x)*map_tile_x + int(map_tile_x/2)
        $ y = int(y)*map_tile_y + int(map_tile_y/2)
        add "images/map_ghost.png":
            pos (x, y)
            anchor (0.5, 0.5)


label go_to_map(x, y):
    show screen map_screen(interactable=False)
    $ next = "_".join(["map", str(x), str(y)])
    if character == "ghost":
        $ update_game(ghost_position = next)
    else:
        $ update_game(human_position = next)
    jump expression next

label map_0_0:
    show screen map_screen(interactable=False)
    "This part of the map is inaccessible."
    jump world_map

label map_1_0:
    show screen map_screen(interactable=False)
    "This part of the map is inaccessible."
    jump world_map

label map_2_0:
    show screen map_screen(interactable=False)
    "This part of the map is inaccessible."
    jump world_map

label map_3_0:
    show screen map_screen(interactable=False)
    "This part of the map is inaccessible."
    jump world_map



label map_0_1:
    show screen map_screen(interactable=False)
    "This part of the map isn't implemented yet."
    jump world_map

label map_1_1:
    show screen map_screen(interactable=False)
    "This part of the map isn't implemented yet."
    jump world_map

label map_2_1:
    show screen map_screen(interactable=False)
    "This part of the map isn't implemented yet."
    jump world_map

label map_3_1:
    show screen map_screen(interactable=False)
    "This part of the map isn't implemented yet."
    jump world_map



label map_0_2:
    show screen map_screen(interactable=False)
    "This part of the map isn't implemented yet."
    jump world_map

label map_1_2:
    show screen map_screen(interactable=False)
    "This part of the map isn't implemented yet."
    jump world_map

label map_2_2:
    show screen map_screen(interactable=False)
    "This part of the map isn't implemented yet."
    jump world_map

label map_3_2:
    show screen map_screen(interactable=False)
    "This part of the map isn't implemented yet."
    jump world_map


label map_0_3:
    $ room = map_0_3_room
    jump room_loop

label map_1_3:
    show screen map_screen(interactable=False)
    "This part of the map isn't implemented yet."
    jump world_map

label map_2_3:
    show screen map_screen(interactable=False)
    "This part of the map isn't implemented yet."
    jump world_map

label map_3_3:
    show screen map_screen(interactable=False)
    "This part of the map isn't implemented yet."
    jump world_map
