import configparser

""" This parser reads config ini for respective environment"""


class MyParser(configparser.ConfigParser):

    def readconfig(self, filename, section):
        # create template parser
        # read config file
        self.read(filename)

        configuration = {}
        if self.has_section(section):
            params = self.items(section)
            for param in params:
                configuration[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return configuration
