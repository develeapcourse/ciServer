import configparser

class Config:
  def __init__(self, config_file_name):
    self.config = configparser.ConfigParser()

    self.config.read(config_file_name)

  def get(self, path, param):
    return self.config[path][param]
