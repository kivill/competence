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


def validate_phone(phone, locale=None):
    try:
        parsed_phone = phonenumbers.parse('+' + str(phone), locale)

        if phonenumbers.is_valid_number(parsed_phone):
            return int(phone)
        else:
            return None
    except NumberParseException as e:
        return None


def sms_code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def email_code_generator(user):
    hashstring = str.encode(str(user.id) + user.email)
    hash = hashlib.sha1(hashstring)
    return hash.hexdigest()


def generate_verification_sms(phone, code):
    text = _('sms.verification').format(
        service_name=environ.get('SERVICE_NAME'), code=code)
    sms = [
        {
            'phone': phone,
            'text': text,
            'channel': 'char',
            'sender': environ.get('P1SMS_SENDER')
        }
    ]
    return sms


def generate_recover_sms(phone, code):
    text = _('sms.restore').format(
        service_name=environ.get('SERVICE_NAME'), code=code)
    sms = [
        {
            'phone': phone,
            'text': text,
            'channel': 'char',
            'sender': environ.get('P1SMS_SENDER')
        }
    ]
    return sms


def getaddrinfoIPv4(host, port, family=0, type=0, proto=0, flags=0):
    """
    Monkey patch for force use IPv4 protocol on requests library
    """
    return getaddrinfo(host=host, port=port, family=socket.AF_INET, type=type, proto=proto, flags=flags)


def send_sms(sms, api_key=None):
    headers = {'accept': 'application/json',
               'content-type': 'application/json'}
    params = {
        'apiKey': api_key if api_key else environ.get('P1SMS_APIKEY'),
        'sms': sms
    }

    with patch('socket.getaddrinfo', side_effect=getaddrinfoIPv4):
        return requests.post(environ.get('P1SMS_ADMIN_PANEL') + environ.get('P1SMS_CREATE_PATH'),
                             data=json.dumps(params),
                             timeout=15,
                             headers=headers)


def send_call(calls, delivery, template):
    calls_arr = []
    for call in calls:
        calls_arr.append(call.phone)
    panel = environ.get('F1CALL_ADMIN_PANEL')
    api_key = environ.get('F1CALL_APIKEY')
    path = environ.get('F1CALL_CREATE_CALL_PATH')
    headers = {'accept': 'application/json',
               'content-type': 'application/json'}
    json_string = json.dumps(template.json)

    json_string = re.sub(r'"name": ".*?", ', "", json_string,
                         flags=re.UNICODE)  # if in the start of string
    # if in the middle or end of string
    json_string = re.sub(r', "name": ".*?"', "", json_string, flags=re.UNICODE)
    # if it is the only one parameter
    json_string = re.sub(r'"name": ".*?"', "", json_string, flags=re.UNICODE)
    json_string = re.sub(r'"extend": true, ', "", json_string,
                         flags=re.UNICODE)  # if in the start of string
    # if in the middle or end of string
    json_string = re.sub(r', "extend": true', "",
                         json_string, flags=re.UNICODE)
    # if it is the only one parameter
    json_string = re.sub(r'"extend": true', "", json_string, flags=re.UNICODE)
    json_string = re.sub(r'"extend": false, ', "", json_string,
                         flags=re.UNICODE)  # if in the start of string
    # if in the middle or end of string
    json_string = re.sub(r', "extend": false', "",
                         json_string, flags=re.UNICODE)
    # if it is the only one parameter
    json_string = re.sub(r'"extend": false', "", json_string, flags=re.UNICODE)

    logging.info(json_string)

    params = json.loads(json_string)
    params['apiKey'] = api_key
    params['phones'] = calls_arr
    params['webhookUrl'] = environ.get('APP_URL') + '/api/webhook/update_call'
    if delivery.from_duty_phone:
        params['dutyPhone'] = 1
    else:
        params['outgoingPhone'] = str(delivery.outgoing_phone)

    check_tree_element(params, delivery.source, delivery.id)

    logging.info('Json for calls: ' + json.dumps(params))
    return requests.post(panel + path,
                         data=json.dumps(params),
                         timeout=15,
                         headers=headers)


def check_tree_element(element, utm_source, delivery_id):
    if element['ivrs']:
        for node in element['ivrs']:
            check_tree_element(node, utm_source, delivery_id)
            if node['webhookParameters']:
                node['webhookParameters']['utm_source'] = utm_source
                if delivery_id != 0:
                    node['webhookParameters']['delivery_id'] = str(delivery_id)
                node['webhookParameters'] = json.dumps(
                    node['webhookParameters'])
            if node['webhookUrl']:
                node['webhookUrl'] = environ.get(
                    'APP_URL') + node['webhookUrl']


def send_email(to, subject, html, body='', email_uuid=None):
    email = email_factory.create(environ.get('EMAIL_PROVIDER', 'smtp'),
                                 to=to, subject=subject, html=html, body=body, email_uuid=email_uuid)
    return email.send()


def send_verification_email(user, code):
    url = '{app_url}/api/profile/check_verification_code?uuid={uuid}&hash={code}'.format(app_url=environ.get('APP_URL'),
                                                                                         uuid=user.uuid, code=code)
    body = HTMLGenerator(
        logo_path=environ.get('APP_URL') + environ.get('LARGE_LOGO_PATH'),
        img_path='',
        title='',
        description='',
        affiliate_url='',
        panel_url=url,
        email=user.email
    )
    html_body = body.generate_email_verification()
    subject = _('email.verification').format(
        service_name=environ.get('SERVICE_NAME'))
    return user.send_email(subject, html_body, source='verificataion_email')


def send_restore_code(user, code):
    subject = _('email.restore.subject').format(
        service_name=environ.get('SERVICE_NAME'))
    body = _('email.restore.body').format(code=code)
    return user.send_email(subject, body, source='restore')


def get_short_url(url, **kwargs):
    headers = {'accept': 'application/json',
               'content-type': 'application/json'}
    params = {
        'apiKey': environ.get('SHORTENER_APIKEY'),
        'url': url,
        "meta": kwargs,
        "webhook_url": '{app_url}/api/webhook/shortener'.format(app_url=environ.get('APP_URL'))
    }
    r = requests.post(environ.get('SHORTENER_PATH') + environ.get('SHORTENER_CREATE_PATH'),
                      data=json.dumps(params),
                      timeout=5,
                      headers=headers)
    domain_list = ['omfa.ru', '1mfa.ru', 'ilnk.net']
    domain = environ.get('SHORTENER_DOMAIN')
    if environ.get('SHORTENER_DOMAIN', False):
        domain = random.choice(domain_list)
    return '{domain}/{hash}'.format(domain=domain,
                                    hash=r.json()['hash'])


def send_push(device, title, body, url, icon, img_url=None):
    platforms = {
        'web': environ.get('FCM_KEY_WEB'),
        'android': environ.get('FCM_KEY_ANDROID_{application}'.format(application=device.application)),
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key={fcm_key}'.format(fcm_key=platforms[device.platform])
    }
    params = {
        "notification": {
            "title": title,
            "body": body,
            "icon": icon,
        },
        "registration_ids": [device.identificator],
    }

    if device.platform == 'web':
        params['notification']['click_action'] = url
    if device.platform == 'android':
        params['data'] = {
            "title": title,
            "body": body,
            "url": url,
            "icon": icon
        }
    if img_url:
        params['notification']['image'] = img_url

    r = requests.post(environ.get('FCM_SEND_URL'),
                      data=json.dumps(params),
                      timeout=5,
                      headers=headers)
    return r.json()


def generate_key(length=64):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def dadata_hint(query, resource, count=10):
    BASE_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/{}"
    url = BASE_URL.format(resource)
    headers = {"Authorization": "Token {}".format(environ.get(
        'DADATA_APIKEY')), "Content-Type": "application/json"}
    data = {"query": query, "count": count}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()


def operator_checker(phone, api_key=None):
    params = {
        'apiKey': api_key if api_key else environ.get('P1SMS_APIKEY'),
        'phones[]': phone,
    }
    with patch('socket.getaddrinfo', side_effect=getaddrinfoIPv4):
        r = requests.get(environ.get('P1SMS_ADMIN_PANEL') + environ.get('P1SMS_OPERATOR_CHECK_PATH'),
                         params=params,
                         timeout=5)
    return r.json()


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" %
                          dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        ) from err


def rand_replace(str: str, repeat=1):
    r = ")(&%$!-=+/>”;#^~"
    for i in range(repeat):
        index = random.randint(0, len(str))
        str = str[:index] + random.choice(r) + str[index:]
    return str


def random_replace(template):
    tmp = template
    repl_dict = {}
    replacements = re.findall(r'\[([0-9А-Яа-яё\.\,\s\|]*)\]', template)
    for i, replacement in enumerate(replacements, start=0):
        repl_dict['f'+str(i)] = replacement.split('|')
        tmp = tmp.replace('['+replacement+']', "{f"+str(i)+"}")
    repl_dict['short_link'] = ['{short_link}']

    for key in repl_dict.keys():
        tmp = tmp.replace(
            '{'+key+'}', rand_replace(random.choice(repl_dict[key]), repeat=1) if key != 'short_link' else random.choice(repl_dict[key]))
    return tmp
