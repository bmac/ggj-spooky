init -1 python:
    class Room(object):
        def __init__(self, name, objects):
            self.name = name
            self.objects = objects
            self._sort()
        def add(self, o, sort=True):
            self.objects.append(o)
            if sort:
                self._sort()
        def remove(self, o):
            if isinstance(o, basestring):
                self.objects = [i for i in self.objects if i['name'] != o]
        def contains(self, o):
            if isinstance(o, basestring):
                obj = [i for i in self.objects if i['name'] == o]
                if obj: return True
                else: return False
        def get(self, o):
            if isinstance(o, basestring):
                obj = [i for i in self.objects if i['name'] == o]
                if obj: return obj[0]
                else: return None
        def _sort(self):
            self.objects.sort(key=lambda x: x.get('layer', 0), reverse=True)
        def __eq__(self, o):
            if isinstance(o, Room):
                if self.name == o.name: return True
            elif isinstance(o, basestring):
                if self.name == o: return True
            return False
    # Should this be combined with an inventory object?
    class RoomObject(object):
        def __init__(self):
            pass
    def get_image(item_name, room_name):
        store_name = '_'.join([room_name, item_name])
        img = getattr(store, store_name, None)
        if img is None:
            img_path = 'images/'+room_name+'/'+item_name+'.png'
            img = renpy.displayable(img_path)
            setattr(store, store_name, img)
        return img
label draw_room:
    python:
        held = None
        renpy.scene()
        img = get_image('bg', room.name)
        renpy.show('bg '+'_'.join([room.name, 'bg']), what=img)
        for i in room.objects:
            img_name = i.get('image', None)
            if img_name:
                img_name = i['image']
                renpy.show(img_name, at_list=[truecenter])
            else:
                img_name = '_'.join([room.name, i['name']])
                img = get_image(i['name'], room.name)
                renpy.show(img_name, what=img, at_list=[truecenter])
    return

label room_loop:
    call draw_room from _call_draw_room
    call screen room_screen(room, show_inventory=True)
    with dissolve
    return
