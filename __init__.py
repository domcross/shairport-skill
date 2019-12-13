from mycroft import MycroftSkill, intent_file_handler
from subprocess import Popen, PIPE, STDOUT
from signal import SIGINT

class Shairport(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.proc = None
        self.output = None

    def initialize(self):
        # check if and which PulseAudio backend is available, 
        # differs by shairport-sync version
        p = Popen(["shairport-sync", "-V"], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        o = p.stdout.read()
        if "-pa-" in str(o):
            self.output = "pa"
        elif "-pulse-" in str(o):
            self.output = "pulse"
        self.log.info("Shairport audio output: '{}'".format(self.output))

    @intent_file_handler('activate.intent')
    def activate_shairport(self, message):
        if not self.output:
            self.log.debug("no suitable audio backend, please compile shairport-sync with PulseAudio support")
            self.speak_dialog('error')
            return
        self.log.debug("Shairport audio output: {}".format(self.output))
        self.proc = Popen(["shairport-sync", "-a", "Mycroft", "-o", self.output])
        self.log.debug("proc: {}".format(self.proc))
        if self.proc:
            self.log.debug("proc.pid: {}".format(self.proc.pid))
        if self.proc and self.proc.pid:
            self.log.debug("shairport pid: {}".format(self.proc.pid))
            self.speak_dialog('activated')
        else:
            self.log.debug("shairport error while enabling")
            self.speak_dialog('error')

    @intent_file_handler('disable.intent')
    def disable_shairport(self, message):
        if self.proc and self.proc.pid:
            self.proc.send_signal(SIGINT)
            self.proc = None
            self.log.debug("shairport terminated")
            self.speak_dialog('disabled')
        else:
            self.log.debug("shairport error while disabling")
            self.speak_dialog('not_active')

    def shutdown(self):
        if self.proc and self.proc.pid:
            self.proc.send_signal(SIGINT)
            self.proc = None

def create_skill():
    return Shairport()

