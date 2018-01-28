default character = ""
default game_room_name = "foo"
define url = 'http://18.218.226.41/game/'
default latest_poll = {}
default started = False

init python:
    import requests
    import json

    def process_data(data):
        hud.actions = data.get('energy', hud.actions)
        if data.get('axe_taken', None):
            pass
        if data.get('secondary_character', None):
            global started
            started = True

    def poll():
        global latest_poll

        data = requests.get(url+game_room_name).json()
        if data != latest_poll:
            process_data(data)
            latest_poll = data

    def push():
        data = {'axe_taken' : True}
        requests.post(url+game_room_name, data=json.dumps(data))

    def update_game(**kwargs):
        global latest_poll
        latest_poll.update(kwargs)
        requests.post(url+game_room_name, data=json.dumps(latest_poll))

    def create_room(char, room):
        data = {'character' : char,
                'room' : room}
        requests.post(url+room, data=json.dumps(data))

    def request_room(room):
        data = requests.get(url+game_room_name).json()
        if data.get('secondary_character', None):
            return False
        else:
            global character
            if data.get('character', None) == 'ghost':
                character = 'human'
            elif data.get('character', None) == 'human':
                character = 'ghost'
            data = {'secondary_character' : character}
            requests.post(url+room, data=json.dumps(data))
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
    if started:
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
    "Conneciton sucessful you are now ready to play the game."
    "You are playing as the [character]."
    jump forest_scene
