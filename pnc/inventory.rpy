image transparent:
    '#000'
    alpha 0.0

image inventory_cover:
    '#000'
    alpha 0.0
    size (930, 120)

transform inventory_hover:
    on show:
        ypos -100
        linear 0.5 ypos -10
    on hide:
        ypos -10
        linear 0.5 ypos -100

transform inventory_tab_hover:
    on show:
        ypos -150
        linear 0.5 ypos -100
    on hide:
        ypos -100
        linear 0.5 ypos -150

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
        # def look(self, other=None):
        #     renpy.call_in_new_context('inventory_look', 'An item flyer')

screen inventory():
    frame:
        # The tab that hangs down part way while the inventory is hidden.
        # Copied from the container screen as a suuuuuuper lazy way to size them up.
        at inventory_tab_hover
        background point_and_click_config['inventory']['container_bg']
        ypos -100
        xpos 0.5
        xanchor 0.5
        yanchor 0.0
        padding (20, 20)
        hbox:
            spacing 10
            $ num_items = len(inventory.items)
            for i in range(0, 10):
                frame:
                    maximum (80, 80)
                    minimum (80, 80)
                    if i < num_items:
                        $ item = inventory.items[i]
                        imagebutton:
                            idle item.image
                            align (0.5, 0.5)
                            action NullAction()
    mousearea:
        area (40, 0, 1200, 80)
        hovered Show('inventory_container')
        unhovered Hide('inventory_container')

screen inventory_look_screen(txt):
    modal True
    frame:
        text txt
        align (0.5, 0.5)
    imagebutton:
        idle 'transparent'
        action Hide('inventory_look_screen')

screen inventory_container():
    frame:
        at inventory_hover
        xpos 0.5
        xanchor 0.5
        yanchor 0.0
        background Frame('transparent', 20, 20)
        imagebutton:
            idle 'inventory_cover'
            action NullAction()
            xpos 0.5
            xanchor 0.5
            yanchor 0.0
    frame:
        at inventory_hover
        background point_and_click_config['inventory']['container_bg']
        xpos 0.5
        xanchor 0.5
        yanchor 0.0
        padding (20, 20)
        hbox:
            spacing 10
            $ num_items = len(inventory.items)
            for i in range(0, 10):
                frame:
                    maximum (80, 80)
                    minimum (80, 80)
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
