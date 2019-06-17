"""Test scriptlet identify lights"""
from collections import deque
from mpf.core.mode import Mode

#from mpf.system.scriptlet import Scriptlet
import threading

class Attract(Mode):
    # The point of this mode code is to step through individual lights and give
    # them names for the config. You navigate the light list forward or backward
    # with flipper buttons, then (hopefully) type in the "real" name of the light,
    # which is then written to a text file that can simply be copied/pasted as the
    # new lights: config in machine_config.

    # This is a work in progress.

    def mode_start(self, **kwargs):
        self.led_list = deque(sorted(self.machine.lights, key=lambda x: x.config['number']))
        self.lednum = 0
        self.machine.events.add_handler('s_left_flipper_active', self.step_down)
        self.machine.events.add_handler('s_right_flipper_active', self.step_up)
        # open("led_list.txt", 'w')

    def step_down(self, **kwargs):
        self.turn_off_led()
        self.led_list.rotate(1)
        self.light_led()
        self.machine.events.post('update_light_slide', current_light=self.led_list[0].config['number'])

    def step_up(self, **kwargs):
        self.turn_off_led()
        self.led_list.rotate(-1)
        self.light_led()
        self.machine.events.post('update_light_slide', current_light=self.led_list[0].config['number'])

    def turn_off_led(self, **kwargs):
        self.led_list[0].off()

    def light_led(self, **kwargs):
        self.led_list[0].on()
        #t1 = threading.Thread(target=self.collect_input)

    # def collect_input(self, **kwargs):
    # This doesn't work. Can't get a prompt like you would if running python
    # from the command line, even with a separate thread.
    #
    # Or, maybe I can just do it in the MC? Not sure how to go about it, but
    # kivy supports an interactive text box via kivy.uix.textinput
    #
    # If I could do that and place it in the MC window, then pass the textinput
    # string to something like this function that writes it to a file, that
    # would be perfect.
    #
    # Even better - if this could be a separate mode altogether and not part
    # of Attract. Only reason it's here is because I was getting errors that a
    # game needed to be running in order to run another mode.
    #
    #     config_name = input('Light name:')
    #     print("l_" + config_name)
    #     with open("led_list.txt", 'a+') as f:
    #         f.write("l_" + (config_name.lower()) + ":\n")
    #         f.write("    number: " + self.led_list[0].config['number'] + "\n")
