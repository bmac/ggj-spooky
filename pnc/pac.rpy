default point_and_click_config = {
    'inventory': {
        # Should be a frame or a 915 by 110 image.
        'container_bg': Frame('gui/frame.png', 5, 5),
        # Should be a frame or an 80x80 image.
        'item_bg': Frame('gui/frame.png', 5, 5)
        }
    }

define frame = Frame('gui/frame.png', 5, 5)

init python:
    import requests
    config.keymap['game_menu'] = [ 'K_ESCAPE', 'K_MENU']

    def poll():
        pass
