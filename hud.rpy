image transparent:
    '#000'
    alpha 0.0

transform hud_pos:
    xpos 1.0
    xanchor 1.0

init python:
    class HUD(object):
        def __init__(self):
            self.maxActions = 6

        @property
        def actions():
            global latest_poll
            return latest_poll.get('energy', 0)

        @property
        def is_daytime():
            global latest_poll
            return latest_poll.get('is_daytime', True)

        @property
        def day():
            global latest_poll
            return latest_poll.get('day', 0)

screen hud():
    frame:
        at hud_pos
        padding(25,25)
        # The tab that hangs down part way while the inventory is hidden.
        # Copied from the container screen as a suuuuuuper lazy way to size them up.
        $ hudText = ("Actions: \n" + str(hud.actions) + " / " + str(hud.maxActions) + "\n\n"
                     +"Day: \n" + str(hud.day)
                    )
        label hudText
