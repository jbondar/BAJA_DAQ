class StateMachine(object):

    def __init__(self):
        self.state = None
        self.states = {}
        self.firework_color = 0
        self.firework_step_time = 0
        self.burst_count = 0
        self.shower_count = 0
        self.firework_stop_time = 0
        self.paused_state = None
        self.pixels = []
        self.pixel_index = 0

    def add_state(self, state):
        self.states[state.name] = state

    def go_to_state(self, state_name):
        if self.state:
            log('Exiting %s' % (self.state.name))
            self.state.exit(self)
        self.state = self.states[state_name]
        log('Entering %s' % (self.state.name))
        self.state.enter(self)

    def update(self):
        if self.state:
            log('Updating %s' % (self.state.name))
            self.state.update(self)

    # When pausing, don't exit the state
    def pause(self):
        self.state = self.states['paused']
        log('Pausing')
        self.state.enter(self)

    # When resuming, don't re-enter the state
    def resume_state(self, state_name):
        if self.state:
            log('Exiting %s' % (self.state.name))
            self.state.exit(self)
        self.state = self.states[state_name]
        log('Resuming %s' % (self.state.name))

    def reset_fireworks(self):
        """As indicated, reset the fireworks system's variables."""
        self.firework_color = random_color()
        self.burst_count = 0
        self.shower_count = 0
        self.firework_step_time = time.monotonic() + 0.05
        strip.fill(0)
        strip.show()