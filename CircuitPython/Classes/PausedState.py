class PausedState(State):

    def __init__(self):
        self.switch_pressed_at = 0
        self.paused_servo = 0

    @property
    def name(self):
        return 'paused'

    def enter(self, machine):
        State.enter(self, machine)
        self.switch_pressed_at = time.monotonic()
        if audio.playing:
            audio.pause()
        self.paused_servo = servo.throttle
        servo.throttle = 0.0

    def exit(self, machine):
        State.exit(self, machine)

    def update(self, machine):
        if switch.fell:
            if audio.paused:
                audio.resume()
            servo.throttle = self.paused_servo
            self.paused_servo = 0.0
            machine.resume_state(machine.paused_state)
        elif not switch.value:
            if time.monotonic() - self.switch_pressed_at > 1.0:
                machine.go_to_state('raising')