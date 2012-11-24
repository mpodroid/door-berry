import ConfigParser

class Configuration(ConfigParser.ConfigParser):
    
    def __init__(self):
        self.add_section('extensions')
        self.set('extensions', 'button1', '100')
        self.set('extensions', 'button2', '101')
        with open('example.cfg', 'wb') as configfile:
            self.write(configfile)
            

Configuration()