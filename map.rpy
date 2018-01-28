image lamp_god = "images/lamp_god.png"
image lamp_god = "images/lamp_god_sad.png"
image lamp_dark = "lamp_dark.png"
image lamp_light = "lamp_light.png"

define p = Character("Oracle")
define g = Character("Vesper")
define c = Character("Velvet")
define h = Character("Margot")
define r = Character("River spirit")
define l = Character("Mortimer")
define b = Character("Crow")
define s = Character("Snake")

label world_map:
    call screen map_screen

image world_map = im.Scale("images/map.png", 1980, 1020)
image map_1_1 = "images/map_1_1/bg.png"
image bad_ghost = "images/bad_ghost.png"
define map_tile_x = 480
define map_tile_y = 270
default lamp_cave = False

default map_0_3_room = Room("map_0_3", [RoomObject("river"),
                                          RoomObject("road")])


default map_3_3_room = Room("map_3_3", [RoomObject("cave")])

# power station
default map_0_2_room = Room("map_0_2", [RoomObject("battery"),
                                          RoomObject("wires")])

# river
default map_1_3_room = Room("map_1_3", [RoomObject("river"), RoomObject("bush"), RoomObject("tires")])

# cat
default map_2_3_room = Room("map_2_3", [RoomObject("river"), RoomObject("grass")])

screen map_screen(interactable=True):
    if interactable:
        timer 0.5 action [Function(poll), Function(renpy.restart_interaction)]
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
    if interactable:
        frame:
            align (1.0, 0.0)
            textbutton "end day":
                action Jump("end_day")


label go_to_map(x, y):
    show screen map_screen(interactable=False)
    $ next = "_".join(["map", str(x), str(y), "scene"])
    if character == "ghost":
        $ update_game(ghost_position = next)
    else:
        $ update_game(human_position = next)
    jump expression next

label map_0_0_scene:
    "This part of the map is inaccessible."
    jump world_map

label map_1_0_scene:
    "This part of the map is inaccessible."
    jump world_map

label map_2_0_scene:
    "This part of the map is inaccessible."
    jump world_map

label map_3_0_scene:
    "This part of the map is inaccessible."
    jump world_map



label map_0_1_scene:
    "This part of the map isn't implemented yet."
    jump world_map

label map_1_1_scene:
    scene onlayer screens
    show map_1_1
    show bad_ghost:
        align (0.5, 0.5)
        zoom 0.5
    "You got spooked!"
    if character == 'human' and not latest_poll.get('seen_bad_ghost', False):
        $ update_game(seen_bad_ghost=True, energy=latest_poll.get('energy', 6) - 1)
    jump world_map

label map_2_1_scene:
    "This part of the map isn't implemented yet."
    jump world_map

label map_3_1_scene:
    "This part of the map isn't implemented yet."
    jump world_map



label map_0_2_scene:
    $ room = map_0_2_room
    jump room_loop

label map_0_2_battery_interact:
    if character == 'human':
        "This looks like an outpost for carrying out maintenance on the power lines."
        "There's usually good stuff in places like these."
        play sound "music/drawers.mp3"
        "In the drawer there's an empty flare gun, an old matchbox, some bandages and rubbing alcohol..."
        # if gum:
        #     "...and the dust shadow from the gum I took. I wonder what it tastes like."
        # if lamp_cave:
        "...aha! And an old portable generator, with a battery still inside. I think it might still have some juice."
        $ s = inventory.add(Item('battery', "images/battery.png", look="A battery. Maybe for a lamp or something."))

        # else:
        #     "...and a pack of what I think used to be chewing gum."
        #     "I pocket the gum. Maybe I'll try it later."
        #     $ gum = True
    else:
        g "My electrical senses are tingling. I forgot I had those."
        g "A working battery? In that power station?"
        g "We could probably find a use for it..."
    return

label map_1_2_scene:
    "This part of the map isn't implemented yet."
    jump world_map

label map_2_2_scene:
    "This part of the map isn't implemented yet."
    jump world_map

label map_3_2_scene:
    "This part of the map isn't implemented yet."
    jump world_map


label map_0_3_scene:
    $ room = map_0_3_room
    jump room_loop

label map_1_3_scene:
    $ room = map_1_3_room
    play sound "music/river_indicator.mp3"
    jump room_loop

label map_1_3_river_interact:
    if character == 'ghost':
        play sound "music/unpurified_stream.mp3"
        show river_ghost

        "This is a river spirit. It speaks with the water, not with words."
        "It used to be teeming with fish, but I sense no life in it now."
        "I think it's sick. There's something stuck in it..."
    else:
        "I listen closely to the river."
        play sound "music/unpurified_stream.mp3"
        "It's making a sickly gargling noise... and everything alive around here is avoiding it."
        "I wonder if I can help."
        $ river_sick = True
    jump room_loop

label river_plastic:
"Two thick black garbage bags are stuck on a rock in the river. They smell thick and foul."
if river_sick:
   "This must be what's making the river sick."
   "I yank at the bags until they come loose, then put them down safely away from the water."
   $ plastic = True
else:
   "They must have come from the city. I wonder how old they are."


label river_resolve:
    "The river sounds clean and happy. I close my eyes for a moment to listen to it..."
    show river_ghost
    "...And when I open them, there's a fish floating in the air above me."
    "It doesn't say anything - perhaps it can't - but it watches me intently. Perhaps it means to thank me with its presence."
    "We sit for a while together on the riverbank, listening to the rushing of the water."
    pause(1.0)
    "I must have drifted off for a moment. When I come to, the river spirit is gone."
    "But there's a smaller fish lying in its place, and more, I think, in the water."
    "Is this a gift for me?"
    ## (Player gets fish)

label map_2_3_scene:
    $ room = map_2_3_room
    play sound "music/river_indicator.mp3"

    jump room_loop

label map_3_3_scene:
    $ room = map_3_3_room
    jump room_loop

label map_3_3_cave_interact:
    if character == 'human':
        "Nothing there."
    else:
        show lamp_ghost
        l "...Hmph."
        g "Um... hello?"
        l "Nothing."
        g "What is it? We're here to help."
        l "I don't need help. I'm a strong, independent ghost."
        g "Well, alright. I'll be going then."
        l "...fine. Don't help me then."
        g "But you just said..."
        l "Fine. Just leave me in the dark like all the other wandering spirit mediums."
        l "It's not like I'm afraid of the dark or anything."
        l "I've only been cleaning my lamp, waiting for someone like you to come light it for me, for about three hundred years."
        l "I'll be fine. It's fine."
        l "I'm fine."
        g "Alright, alright. Light the lamp. I get it."
