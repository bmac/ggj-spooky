default character = ""
default game_room_name = "foo"
define url = 'http://18.218.226.41/game/'
default latest_poll = {}

init python:
    import requests
    import json

    def poll():
        global latest_poll

        data = requests.get(url+game_room_name).json()
        if data != latest_poll:
            latest_poll = data

    def update_game(**kwargs):
        # Use a named store so we don't need to keep a local store and a copy of the server info
        global latest_poll
        latest_poll.update(kwargs)
        requests.post(url+game_room_name, data=json.dumps(latest_poll))

    def create_room(char, room):
        data = {
            'energy': 3,
            'character' : char,
            'secondary_character' : '',
            'is_daytime' : False,
            'day': 0,
            'ghost_position': '',
            'human_position': '',
            'seen_bad_ghost': False,
            'room' : room,
            }
        requests.post(url+room, data=json.dumps(data))

    def request_room(room):
        poll()
        data = requests.get(url+game_room_name).json()
        if data.get('secondary_character', None):
            return False
        else:
            global character
            if data.get('character', None) == 'ghost':
                character = 'human'
            elif data.get('character', None) == 'human':
                character = 'ghost'
            update_game(secondary_character=character)
            return True


label lobby:
    call screen lobby

screen lobby():
    vbox:
        align (0.5, 0.5)
        frame:
            textbutton "Create Game":
                action Jump("create_game")
        frame:
            textbutton "Join Game":
                action Jump("join_game")

label create_game:
    jump choose_char

label choose_char:
    call screen choose_char

screen choose_char:
    hbox:
        align (0.5, 0.5)
        textbutton "Ghost":
            action [SetVariable('character', 'ghost'), Jump('name_game')]
            background frame
        frame:
            textbutton "Human":
                action [SetVariable('character', 'human'), Jump('name_game')]

label name_game:
    $ game_room_name = renpy.input("What do you want to name your lobby?")
    $ game_room_name = game_room_name.strip()
    jump request_new_room

label request_new_room:
    $ create_room(char=character, room=game_room_name)
    jump wait_to_start

label wait_to_start:
    if latest_poll.get('secondary_character', None):
        jump connected
    else:
        call screen wait_to_start

screen wait_to_start():
    timer 0.5 action [Function(poll), Jump('wait_to_start')]
    frame:
        text "Your game is named [game_room_name]. Tell a friend to join your game using the name [game_room_name]."

label join_game:
    $ game_room_name = renpy.input("What is the name of the game you are trying to join?")
    $ game_room_name = game_room_name.strip()
    $ connected = request_room(game_room_name)
    if not connected:
        jump not_connected
    else:
        jump connected

label not_connected:
    "Connection failed."
    return

label connected:
    call screen connected_screen

screen connected_screen():
    timer 0.5 action Jump('end_day')
    add "black"
    text "Conneciton sucessful you are now ready to play the game.\n You are playing as the "+character+"."
