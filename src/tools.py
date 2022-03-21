import os
import base64
import json
import time

import src.config as cfg


# image bytes str to base64 str
def img_to_base64(img_bytes):
    base64_str = base64.b64encode(img_bytes).decode("utf8")
    return base64_str
