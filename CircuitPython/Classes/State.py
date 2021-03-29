class State(object):

    def __init__(self):
        pass

    @property
    def name(self):
        return ''

    def enter(self, machine):
        pass

    def exit(self, machine):
        pass

    def update(self, machine):
        if switch.fell:
            machine.paused_state = machine.state.name
            machine.pause()
            return False
        return True