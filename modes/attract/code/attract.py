"""Test scriptlet identify lights"""
from collections import deque
from mpf.core.mode import Mode
#from mpf.system.scriptlet import Scriptlet
import threading

class Attract(Mode):
    def mode_start(self, **kwargs):
        #self.config_name = None
        #led_config_file = open("leds.txt", "w") # to create a new file for writing
        self.led_list = deque(sorted(self.machine.lights, key=lambda x: x.config['number']))
        #self.led_list = deque(sorted(self.machine.leds, key=lambda x: int(x.config['number_str'].split('-')[1])))
        self.lednum = 0
        self.machine.events.add_handler('s_left_flipper_active', self.step_down)
        self.machine.events.add_handler('s_right_flipper_active', self.step_up)
        open("led_list.txt", 'w')

    def step_down(self, **kwargs):
        self.turn_off_led()
        self.led_list.rotate(1)
        self.light_led()

    def step_up(self, **kwargs):
        self.turn_off_led()
        self.led_list.rotate(-1)
        self.light_led()

    def turn_off_led(self, **kwargs):
        self.led_list[0].off()

    def light_led(self, **kwargs):
        self.led_list[0].on()
        t1 = threading.Thread(target=self.collect_input)

    def collect_input(self, **kwargs):
    # This doesn't work. Can't get a prompt. Need to find a way to do that.
    # Maybe have to use a QT window, like Monitor? Maybe Monitor can be extended
    # since all the lights are in there anyway. Click on one in the list to turn
    # it on, then rename it right away? That would rock. Maybe that's even
    # possible now??

    # No luck with that. Plus, it's reading config from the config dict, so it's
    # not really interacting with the config file. Tough to alter, I think.

    # Still...might be something there to build on, even if it's a new app/mode

    # Or, maybe I can just do it from here? Fire up the QT window as the prompt
    # and the rest is the same?

    # I want it to show the current config name for the light, and, if possible
    # show that I've been to it before. Maybe an index or something? Maybe That
    # index can also show up in the text file? Ugh. One thing at a time.
    
        config_name = input('Light name:')
        print("l_" + config_name)
        with open("led_list.txt", 'a+') as f:
            f.write("l_" + (config_name.lower()) + ":\n")
            f.write("    number: " + self.led_list[0].config['number_str'] + "\n")
