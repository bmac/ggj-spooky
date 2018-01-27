define p = Character(None, what_color="#FFF")
# define dog = Character("dog", what_color="#a46579")

### Styles
style say_dialogue:
    outlines [ (absolute(2), "#000", absolute(0), absolute(0)) ]
    color "#FFF"
    xmaximum 500
    xalign 0.5
    yalign 0.75

style choice_button:
    yoffset 350
    ymaximum 40
    background Frame("images/frame.png", 5, 5)

style choice_vbox:
    spacing 4

style choice_button_text:
    outlines [ (absolute(2), "#000", absolute(0), absolute(0)) ]
    hover_outlines [ (absolute(2), "#C15200", absolute(0), absolute(0)) ]
    color "#FFF"
    ###

init python:
    import requests

init:
    $ config.mouse = { 'default' : [ ('images/cursor.png', 20, 20)] }
    $ config.keymap['game_menu'] = [ 'K_ESCAPE', 'K_MENU']
    default preferences.text_cps = 80

    default forest_room = Room("forest", [RoomObject("axe"),
                                          RoomObject("letter")])

label forest_scene:
    $ room = forest_room
    jump room_loop

label start:
    $ dialogue_box["dog"] = {'x':0.35, 'y':180}
    $ inventory = Inventory()
    $ hud = HUD()
    jump forest_scene
    jump lobby

label intro:
    scene bg yard
    show dog at truecenter
    p "You arrive home after a long day, ready to plop into bed."
    p "Except before you can even get inside your house, you notice a sad dog sitting in your yard."

    $ dog_mood = "happy"
    show dog at bark
    dog "Arf! Arf!"
    $ dog_mood = "sad"

    "You recognize the dog as your neighbors. Normally you'd give them a call, but the dog looks especially sad today."
    dog "*wimper*"
    "Maybe you can cheer him up a bit before bringing him back. The neighbors usually are not home this early anyways."

    $ dog_mood = "happy"
    show dog at bark
    dog "Arf! Arf!"
    $ dog_mood = "sad"

    "INSTRUCTIONS: This is a point and click game. Left click to 'look' at an object, right click to 'interact'. To use an inventory object on an object in the room, right click the inventory object to hold it in your hand, then click on the room object."

    jump yard_scene

label yard_house_look:
    "It's small, but it's home."
    return
label yard_house_interact:
    "You run your hands along the vinyl siding."
    return

label yard_door_look:
    "The front door of your house"
    return
label yard_door_interact:
    if not dog_played:
        "You reach for the front door but Fido immediately jumps up around your legs, almost tripping you."
        "He clearly wants someone to play with. Perhaps you can humor him for a bit before you go inside."
    elif not dog_fed:
        "You're just about to turn the doorknob when you hear a soft whine behind you."
        "You turn around to see Fido sadly pushing his food bowl towards you."
        "Perhaps you can find him something to snack on. You already know there is nothing in your kitchen for him, but maybe you can find something in your shed."
    else:
        "You finally make it inside."
        "Home sweet home!"
        $ renpy.pop_call()
        jump bed_room_scene
    return

label yard_food_bowl_look:
    if not dog_fed and not dog_played:
        "Huh, Fido carried his food bowl with him the whole way here."
    else:
        "Oh no, Fido left his bowl here...I'll return it tomorrow."
    return
label yard_food_bowl_interact:
    if not inventory.contains("dog_food") and not dog_fed:
        "You don't have anything to fill it with."
    elif inventory.contains("dog_food"):
        "Maybe Fido would like some food."
    elif dog_fed and not dog_played:
        "You already gave him some food."
    elif dog_fed and dog_played:
        "You'll return the bowl in the morning. It's getting late and you'd rather get to bed right now."
    return
label yard_food_bowl_use:
    if held.name == "bone":
        $ dog_mood = "angry"
        "Fido looks a bit peeved as you put the bone in his food bowl."
        "Clearly he doesn't think that belongs there so you take it back."
        $ dog_mood = "sad"
    elif held.name == "dog_food":
        $ dog_mood = "happy"
        "Fido's ears perk up immediately when he hears the rattle of the box of dog food."
        "You pour what little is left into his bowl. It should tide him over until his owner comes home."
        $ dog_fed = True
        $ inventory.drop("dog_food")
        if not dog_played:
            $ dog_mood = "sad"
        else:
            call neighbor_comes_home from _call_neighbor_comes_home
    return


label yard_dog_look:
    "Fido, your neighbor's mischievous but friendly dog."
    return
label yard_dog_interact:
    if not dog_greeted:
        "You pet Fido"
        $ dog_mood = "happy"
        "He cheers up for a second and happily licks your hands."
        $ dog_mood = "sad"
        $ dog_greeted = True
    elif not dog_played:
        "You roll around a bit trying to entice Fido to play with you."
        "He doesn't quite seem to get it...maybe if you had a toy for him to play with."
    elif not dog_fed:
        "You pet Fido while he lays calmly on your lawn."
        $ dog_mood = "happy"
        "He looks up at you with a big grin, but then looks down at his food bowl expectantly."
        $ dog_mood = "sad"
        "Clearly he's looking for something specific from you."
    return
label yard_dog_use:
    if held.name == "bone":
        $ dog_mood = "happy"
        "Fido's tail starts wagging as you pull out the plastic bone."
        "You toss it for him a number of times before he finally settles down quietly and knaws on the bone."
        $ dog_played = True
        $ inventory.drop("bone")
        if not dog_fed:
            $ dog_mood = "sad"
        else:
            call neighbor_comes_home from _call_neighbor_comes_home_1
    elif held.name == "dog_food":
        "I'd rather not fed him directly. Better to put it in the food bowl he so thoughtfully brought with him."
    else:
        "Fido looks up at you curiously."
    return

label yard_backyard_look:
    "Your back yard. All that's really back there is a shed you use for storage."
    return
label yard_backyard_interact:
    if not dog_played or not dog_fed:
        "Maybe you can find something for Fido back here."
        $ renpy.pop_call()
        jump shed_scene
    else:
        "No, you don't need to go back there right now."
        return

label shed_shelves_look:
    "A bunch of knick-knacks from here and there."
    return
label shed_shelves_interact:
    if not dog_food_taken:
        "You peruse your shelves."
        "Buried behind some spare tarps, you find a box of dog food left over when you pet sat for your neighbors a few weeks ago."
        "Fido might like this."
        $ s = inventory.add(Item('dog_food', "images/dog_food.png", look="Doggo-O's. For the discerning pupper in your life."))
        $ dog_food_taken = True
    else:
        "It's a mess and you don't really care to dig through it now."
    return

label shed_leave_look:
    return
label shed_leave_interact:
    $ renpy.pop_call()
    jump yard_scene
    return

label shed_skeleton_look:
    "An old plastic skeleton left over from Halloween."
    "Spooky!"
    return
label shed_skeleton_interact:
    if not bone_taken:
        "Hmm..."
        "You gingerly tug at the skeletons femur."
        scene bg shed
        show sad_skeleton
        $ shed_room.get("skeleton")["image"] = "sad_skeleton"
        "..."
        "Oops. Oh well, no sense in letting this plastic bone go to waste now."
        $ s = inventory.add(Item('bone', "images/bone.png", look="A plastic bone I stole off a poor skeleton in my shed."))
        $ bone_taken = True
    else:
        "The poor skeleton has been through enough. Best to leave it be for now."
    return

label neighbor_comes_home:
    "Just then your neighbors car pulls in."
    "They apologize for letting Fido get out again and thank you for looking after him."
    "After exchanging some pleasantries, they take Fido back to their home and you're left standing in your own yard."
    $ yard_room.remove("dog")
    return

label bed_room_mirror_look:
    "A big antique mirror you got from the flea market."
    return
label bed_room_mirror_interact:
    "Mirror mirror on the wall, who is the best dog sitter of them all?"
    return

label bed_room_window_look:
    "It's pretty bright out considering how late it is."
    return
label bed_room_window_interact:
    "Did you hear about the glass blower who accidentally inhaled?"
    "He ended up with a pane in his stomach!"
    return

label bed_room_bed_look:
    "I can't wait to get to sleep."
    return
label bed_room_bed_interact:
    "Finally, bed time."
    show black with dissolve
    "All in all, it was a good day."
    $ renpy.pop_call()
    return

label bed_room_table_look:
    "Just something you found on the curb after an old neighbor moved out."
    return
label bed_room_table_interact:
    "*knock knock*"
    "Yep, that's some solid wood working."
    return

label bed_room_tomes_look:
    "Some pre-bedtime reading material."
    return
label bed_room_tomes_interact:
    "My favorite books..."
    show black:
        alpha 0.25
    show book_3:
        xpos 0.5 ypos 0.5 xanchor 0.5 yanchor 0.8
    show book_2:
        xpos 0.50 ypos 0.45 xanchor 0.5 yanchor 0.8
    show book_1:
        xpos 0.5 ypos 0.5 xanchor 0.5 yanchor 0.8
    with dissolve

    "Dog Quixote"
    show book_1 at offscreenright with move
    "The Great Danesby"
    show book_2 at offscreenright with move
    "Pup and Prejudice"
    show book_3 at offscreenright with move
    hide black with dissolve
    "You know, the classics"
    return

label bed_room_lamp_look:
    "Your aunt was very excited to give you this lamp."
    "You remember her enthusiasm when you look at it."
    return
label bed_room_lamp_interact:
    "No genies in this lamp."
    return

label bed_room_leave_look:
    return
label bed_room_leave_interact:
    "No, you don't really feel like head out again after you just got home."
    return
