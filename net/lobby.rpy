default character = ""
default game_room_name = "foo"
define url = 'http://18.218.226.41/game/'

init python:
    import requests
    import json

    def poll():
        requests.get(url+game_room_name)

    def push():
        pass

    def create_room(char, room):
        data = {'character' : char,
                'room' : room}
        requests.post(url+room, data=json.dumps(data))

    def request_room():
        pass

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
    jump wait_to_start

label wait_to_start:
    $ create_room(char=character, room=game_room_name)
    call screen wait_to_start

screen wait_to_start():
    timer 0.5 action Function(poll)
    frame:
        text "Your game is named [game_room_name]. Tell a friend to join your game using the name [game_room_name]."

label join_game:
    $ pass
