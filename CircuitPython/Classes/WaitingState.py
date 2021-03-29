class WaitingState(State):

    @property
    def name(self):
        return 'waiting'

    def enter(self, machine):
        State.enter(self, machine)

    def exit(self, machine):
        State.exit(self, machine)

    def almost_NY(self):
        t = rtc.datetime
        return (t.tm_mday == 31 and
                t.tm_mon == 12 and
                t.tm_hour == 23 and
                t.tm_min == 59 and
                t.tm_sec == 50)

    def update(self, machine):
        if switch.fell or self.almost_NY():
            machine.go_to_state('dropping')