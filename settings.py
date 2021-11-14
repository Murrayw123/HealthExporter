from Parsers.garmin_connect_parser import GarminConnectParser
from Parsers.myfitnesspal_parser import MyFitnessPalParser
from Parsers.repcount_parser import RepcountParser

PARSERS = [MyFitnessPalParser, RepcountParser]

# needed for repcount
DROP_BOX_APP_KEY = ""
DROP_BOX_APP_SECRET = ""
DROP_BOX_OAUTH_TOKEN = ""

# needed for MFP
MYFITNESSPAL_EMAIL = ""
MYFITNESSPAL_PASSWORD = ""

# needed for Garmin
GARMIN_CONNECT_EMAIL = ""
GARMIN_CONNECT_PASSWORD = ""

# needed for influxdb
INFLUXDB_TOKEN = ""
INFLUXDB_ORG = ""
INFLUX_DB_BUCKET = ""
INFLUXDB_URL = ""


