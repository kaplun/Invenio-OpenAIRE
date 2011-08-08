import os.path
from invenio.config import CFG_ETCDIR, CFG_PREFIX, CFG_WEBDIR, CFG_SITE_URL

APP_NAME = "websubmitbezirg"
APP_URL = CFG_SITE_URL + '/' + APP_NAME
APP_ETC_DIR = os.path.join(CFG_ETCDIR, APP_NAME)
APP_WEB_DIR = os.path.join(CFG_WEBDIR, APP_NAME + "-static")
APP_DATA_DIR = os.path.join(CFG_PREFIX, "var", "data", APP_NAME)
