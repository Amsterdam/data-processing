from configparser import ConfigParser


def config(section):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read('config.ini')
    # read all sections
    # sections = parser.sections()
    # print(parser.items(section))
    settings = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            settings[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return settings
