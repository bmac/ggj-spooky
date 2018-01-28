label world_map:
    call screen map_screen


image world_map = im.Scale("images/map.png", 1920, 1080)

define map_tile_x = 480
define map_tile_y = 270

screen map_screen(interactable=True):
    timer 0.5 action [Function(poll), Jump("world_map")]
    add "world_map"
    if interactable:
        imagemap:
            idle "world_map"

            hotspot (map_tile_x*0, map_tile_y*0, map_tile_x, map_tile_y) action Jump("map_0_0")
            hotspot (map_tile_x*1, map_tile_y*0, map_tile_x, map_tile_y) action Jump("map_1_0")
            hotspot (map_tile_x*2, map_tile_y*0, map_tile_x, map_tile_y) action Jump("map_2_0")
            hotspot (map_tile_x*3, map_tile_y*0, map_tile_x, map_tile_y) action Jump("map_3_0")

            hotspot (map_tile_x*0, map_tile_y*1, map_tile_x, map_tile_y) action Jump("map_0_1")
            hotspot (map_tile_x*1, map_tile_y*1, map_tile_x, map_tile_y) action Jump("map_1_1")
            hotspot (map_tile_x*2, map_tile_y*1, map_tile_x, map_tile_y) action Jump("map_2_1")
            hotspot (map_tile_x*3, map_tile_y*1, map_tile_x, map_tile_y) action Jump("map_3_1")

            hotspot (map_tile_x*0, map_tile_y*2, map_tile_x, map_tile_y) action Jump("map_0_2")
            hotspot (map_tile_x*1, map_tile_y*2, map_tile_x, map_tile_y) action Jump("map_1_2")
            hotspot (map_tile_x*2, map_tile_y*2, map_tile_x, map_tile_y) action Jump("map_2_2")
            hotspot (map_tile_x*3, map_tile_y*2, map_tile_x, map_tile_y) action Jump("map_3_2")

            hotspot (map_tile_x*0, map_tile_y*3, map_tile_x, map_tile_y) action Jump("map_0_3")
            hotspot (map_tile_x*1, map_tile_y*3, map_tile_x, map_tile_y) action Jump("map_1_3")
            hotspot (map_tile_x*2, map_tile_y*3, map_tile_x, map_tile_y) action Jump("map_2_3")
            hotspot (map_tile_x*3, map_tile_y*3, map_tile_x, map_tile_y) action Jump("map_3_3")

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
    show screen map_screen(interactable=False)
    "This part of the map isn't implemented yet."
    jump world_map

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
