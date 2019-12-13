from mycroft import MycroftSkill, intent_file_handler
import subprocess, signal

class Shairport(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.proc = None

    @intent_file_handler('activate.intent')
    def activate_shairport(self, message):
        self.proc = subprocess.Popen(["shairport-sync", "-a", "Mycroft", "-o", "pa"])
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
            self.proc.send_signal(signal.SIGINT)
            self.log.debug("shairport terminated")
            self.speak_dialog('disabled')
        else:
            self.log.debug("shairport error while disabling")
            self.speak_dialog('not_active')

def create_skill():
    return Shairport()

