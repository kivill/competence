import json
import uuid
import random
import string
import pprint
import socket
import requests
import logging
import hashlib
import phonenumbers
from unittest.mock import patch
from phonenumbers import NumberParseException
from os import environ
from flask import Response
from importlib import import_module
import re


getaddrinfo = socket.getaddrinfo


def debug(variable):
    pp = pprint.PrettyPrinter(indent=4, depth=6)
    debug_message = pp.pprint(variable)
    return Response(debug_message, mimetype="text/text")
