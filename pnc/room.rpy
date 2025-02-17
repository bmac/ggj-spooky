init -1 python:
    class Room(object):
        def __init__(self, name, objects):
            self.name = name
            self.objects = objects
            self._sort()
            self.background = "images/"+name+"/bg.png"
        def add(self, o, sort=True):
            self.objects.append(o)
            if sort:
                self._sort()
        def remove(self, o):
            if isinstance(o, basestring):
                self.objects = [i for i in self.objects if i.name != o]
        def contains(self, o):
            if isinstance(o, basestring):
                obj = [i for i in self.objects if i.name == o]
                if obj: return True
                else: return False
        def get(self, o):
            if isinstance(o, basestring):
                obj = [i for i in self.objects if i.name == o]
                if obj: return obj[0]
                else: return None
        def _sort(self):
            self.objects.sort(key=lambda x: getattr(x, 'layer', 0), reverse=True)
        def __eq__(self, o):
            if isinstance(o, Room):
                if self.name == o.name: return True
            elif isinstance(o, basestring):
                if self.name == o: return True
            return False
    # Should this be combined with an inventory object?
    class RoomObject(object):
        def __init__(self, name, description=None, image=None, anchor=(0.5, 0.5), pos=(0.5, 0.5)):
            self.name = name
            self.description = description if description != None else name.replace('_', ' ')

            self.anchor = anchor
            self.pos = pos

        @property
        def image(self):
            return 'images/' + room.name +"/" + self.name + ".png"

label call_room:
    call screen room_screen(interactable=True)
    with dissolve

label room_loop:
    $ held = None
    jump call_room

screen room_screen(interactable=True):
    if interactable:
        timer 0.5 action [Function(poll), Function(renpy.restart_interaction)]
    add room.background:
        align (0.5, 0.5)
    for i in room.objects:
        imagebutton:
            idle i.image
            focus_mask True
            anchor i.anchor
            pos i.pos
            if interactable:
                action [SetVariable('action', 'interact'),
                        SetVariable('target', i.name),
                        Hide('mouseover'),
                        Hide('inventory'),
                        Jump('start_action')]
                hovered [SetVariable('description', i.description),
                         Show('mouseover')]
                unhovered [Hide('mouseover'),
                           SetVariable('description', None)]
    # Should I tag this with an id for transfering state between scenes?
    if interactable:
        use hud
        use inventory
        frame:
            align (1.0, 1.0)
            textbutton "back to map":
                action Jump("world_map")
