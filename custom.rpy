init python:
    @renpy.pure
    class Call(Action, DictEquality):
        # There is a bug in the current latest realease but it's fixed on github so I'm copying this in for now.
        args = tuple()
        kwargs = dict()

        def __init__(self, label, *args, **kwargs):
            self.label = label
            self.args = args
            self.kwargs = kwargs

        def __call__(self):
            renpy.call(self.label, *self.args, **self.kwargs)
