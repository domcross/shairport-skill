from mycroft import MycroftSkill, intent_file_handler


class Shairport(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('shairport.intent')
    def handle_shairport(self, message):
        self.speak_dialog('shairport')


def create_skill():
    return Shairport()

