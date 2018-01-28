image transparent:
    '#000'
    alpha 0.0

image inventory_cover:
    '#000'
    alpha 0.0
    size (930, 120)

define inv_ypos_min = -40
define inv_ypos_mid = -200
define inv_ypos_max = 0

transform inventory_hover:
    on show:
        ypos inv_ypos_mid
        linear 0.5 ypos inv_ypos_max
    on hide:
        ypos inv_ypos_max
        linear 0.5 ypos inv_ypos_mid

transform inventory_tab_hover:
    on show:
        ypos inv_ypos_min
        linear 0.5 ypos inv_ypos_mid
    on hide:
        ypos inv_ypos_mid
        linear 0.5 ypos inv_ypos_min

init python:
    class Inventory(object):
        def __init__(self):
            self.items = []
        def add(self, item, refuse_text="I don't need another one."):
            if item.name not in [i.name for i in self.items]:
                self.items.append(item)
                return True
            else:
                p(refuse_text)
                return False
        def remove(self, item_name):
            self.items = [i for i in self.items if i.name != item_name]
        def contains(self, item_name):
                return item_name in [i.name for i in self.items]

    class Item(object):
        def __init__(self, name, image=None, look='Just some junk',  use_on_interact=False):
            self.name = name
            if image is None:
                self.image = Image('images/inventory/'+name+'.png')
            else:
                self.image = image

            self.use_on_interact = use_on_interact
            self.look = look
        def use(self, other=None):
            if other is None:
                pass
            else:
                pass

screen inventory_look_screen(txt):
    modal True
    frame:
        text txt
        align (0.5, 0.5)
    imagebutton:
        idle 'transparent'
        action Hide('inventory_look_screen')

screen inventory():
    use inventory_tab

screen inventory_tab():
    use inventory_contents(tab=True)

screen inventory_contents(tab=False):
    frame:
        ypos inv_ypos_mid
        xpos 0.5
        anchor (0.5, 0.0)
        xysize (1100, 260)
        if tab:
            at inventory_tab_hover
        else:
            at inventory_hover
        mousearea:
            if tab:
                hovered Show('inventory_container')
            else:
                unhovered Hide('inventory_container')
        hbox:
            align (0.5, 0.15)
            spacing 10
            $ num_items = len(inventory.items)
            # box_wrap True
            for i in range(0, 4):
                frame:
                    xysize (260, 180)
                    if i < num_items:
                        $ item = inventory.items[i]
                        imagebutton:
                            idle item.image
                            align (0.5, 0.5)
                            action Show('inventory_look_screen', txt=item.look)
                            if item.use_on_interact is True:
                                alternate Function(item.use)
                            else:
                                alternate [SetVariable('held', item), ShowTransient('held_item')]

screen inventory_container():
    use inventory_contents(tab=False)
