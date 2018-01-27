init:
    $ config.rollback_enabled = False
    default description = ''
    default action = 'look'
    default held = None
    default target = ''
    default room = ''
image null = Null()
init python:
    # mouseover_transform = Transform(Text('default'))
    def update_mouseover_text(t, tt, **kwargs):
        if renpy.get_screen('mouseover'):
            # I tried recycling a text object instead of creating a new one
            # And it was super buggy, must investigate more later
            mouse_pos=renpy.get_mouse_pos()
            # mouseover_transform.pos = mouse_pos
            # mouseover_transform.child.text = description
            # return(mouseover_transform, 0.01)
            return (Text(description,
                         anchor=(0.5, 0.5),
                         pos=(mouse_pos[0],
                              mouse_pos[1]-45),
                         # I need to block out a style prefix for all this.
                         # font='NothingYouCouldSay.ttf',
                         color='#FFF',
                         outlines=[(absolute(4), '#000', absolute(0), absolute(0))]),
                    0.01)
        else:
            return ('null', None)
    mouse_transform = None
    def update_mouse_image(t, tt, **kwargs):
        global mouse_transform
        if renpy.get_screen('held_item'):
            if mouse_transform is None or mouse_transform.child is not held:
                mouse_transform = Transform(held.image)
                mouse_transform.align = (0.5, 0.5)
            mouse_transform.pos = renpy.get_mouse_pos()
            return (mouse_transform,
                    0.01)
        else:
            return ('null', None)

image mouse_image = DynamicDisplayable(update_mouse_image)
image mouseover_text = DynamicDisplayable(update_mouseover_text)

screen mouseover():
    imagebutton:
        idle 'mouseover_text'

screen held_item():
    $ mouse_pos=renpy.get_mouse_pos()
    imagebutton:
        idle 'mouse_image'

label start_action:
    python:
        if (held is not None):
            action = 'use'
        # First check for a response specified in the data.
        obj = room.get(target)
        data_response_label = getattr(obj, 'action', None)
        selected_response_label = ''
        if data_response_label:
            selected_response_label = data_response_label
        else:
            gen_response_label = '_'.join([room.name, target, action])
            response_exists = renpy.has_label(gen_response_label)
            room_response_label = '_'.join([room.name, action])
            room_response_exists = renpy.has_label(room_response_label)
            if response_exists:
                # Check for explicit object response
                selected_response_label = gen_response_label
            elif room_response_exists:
                # Look for a room specific response
                selected_response_label = room_response_label
            else:
                # General default response
                selected_response_label = 'default_' + action

    $ renpy.call(selected_response_label)
    $ renpy.jump('_'.join([room.name, 'scene']))

screen room_screen(room, show_inventory=True):
    $ img_dir = 'images/' + room.name + '/'
    for i in room.objects:
        $ name = i.name
        $ desc = i.description
        $ img = i.image
        $ img_is_null = isinstance(img, Null)
        imagebutton:
            idle img
            if not img_is_null:
                focus_mask True
            anchor (0.5, 0.5)
            pos (0.5, 0.5)
            action [SetVariable('action', 'look'),
                    SetVariable('target', name),
                    Hide('mouseover'),
                    Hide('inventory'),
                    Jump('start_action')]
            alternate [SetVariable('action', 'interact'),
                       SetVariable('target', name),
                       Hide('mouseover'),
                       Hide('inventory'),
                       Jump('start_action')]
            hovered [SetVariable('description', desc),
                     Show('mouseover')]
            unhovered [Hide('mouseover')]
    # Should I tag this with an id for transfering state between scenes?
    if show_inventory is True:
        use inventory
    use hud
