define p = Character(None, what_color="#FFF")

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

    default forest_room = Room("forest", [RoomObject("axe",
                                                     pos=(1500, 600)),
                                          RoomObject("letter",
                                                     pos=(400, 400))])

image black = "#000"

label end_day:
    $ day = latest_poll.get('day', 0)
    if day >=3 and character == 'human':
        # end game
        $ pass
    else:
        call screen seance_screen

screen seance_screen:
    add "black"
    timer 0.5 action [Function(poll), Jump('end_day')]
    if latest_poll.get('seance_over', False):
        timer 0.000001 action [Jump('start_day')]
    # séance
    $ energy = latest_poll.get('energy', 0)
    if character == "human":
        if energy is 0:
            text "You wanted to hold a seance, but you are too tired."
        else:
            text "You are holding a seance."

        frame:
            align (0.5, 0.5)
            textbutton "end seance":
                action Jump('start_day')
    else:
        if energy is 0:
            text "You waited all night for someone to reach out to you through a seance, but no one did."
        elif energy is 1:
            text "Someone is holding a seance and trying to talk to you.\n Show them a single card."
        else:
            text "Someone is holding a seance and trying to talk to you.\n Show them up to "+str(energy)+" cards."

label start_day:
    $ poll()
    if character == 'human':
        $ update_game(seance_over=True)
    elif character == 'ghost':
        $ update_game(day=latest_poll['day']+1, seance_over=False, energy=6)

    call screen start_day_screen

screen start_day_screen():
    add 'black'
    if character == 'human':
        text "You end the seance and go to bed. The next day you wake up refreshed."
    else:
        text "The seance ends and you take a spooky map. You wake up spooky and refreshed."
    timer 2.0 action Jump('world_map')

label forest_scene:
    $ room = forest_room
    jump room_loop

label start:
    play music "music/night_theme.mp3"
    # $ dialogue_box["dog"] = {'x':0.35, 'y':180}
    $ inventory = Inventory()
    $ hud = HUD()
    # join screen
    # jump world_map
    # jump forest_scene
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

label forest_axe_look:
    if character == 'human':
        "Hmm, a rust axe...wait is that rust or BLOOD?!"
    else:
        "I am a spooky ghost and that is a spooky axe."
    return

label forest_axe_interact:
    "Ehhh, naaah, I'm good. I don't really want to lug around a murder axe."
    return

label forest_letter_look:
    if character == 'human':
        "\"Dear Jane,\""
        "\"I think Phil is going to kill me with an axe.\""
        "\"WEIRD, right?\""
        "\"Love, John.\""
        "Huh, you might have been onto something, John..."
    else:
        "An old letter. I cannot read this because it's folded up and I am incorporeal and unable to unfold it."
        "Darn."
    return

label forest_letter_interact:
    "There's no inventory asset for this letter yet so you can't pick it up."
    return
