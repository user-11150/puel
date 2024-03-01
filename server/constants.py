import configparser

__all__ = ["STATIC_PATH",
           "IP",
           "PORT"]

parser = configparser.ConfigParser()
parser.readfp(open('configuration/config.ini',"rt",encoding="UTF-8"))

#STATIC_PATH = "./static"
#PORT = 2501

STATIC_PATH = "./static"
IP = parser.get('address',"IP")
PORT = parser.getint('address',"PORT")
