# -*- coding: utf-8 -*-

import json
import sys
import struct

def log_browser_console(message):
    '''
    Log a message in the browser console
    '''
    sys.stderr.write(message + '\n')


# from https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Native_messaging
def get_message():
    '''
    Receive a native message from the browser
    '''
    raw_length = sys.stdin.buffer.read(4)
    if len(raw_length) == 0:
        raise Exception("Message is empty")
    message_length = struct.unpack("@I", raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode("utf-8")
    return json.loads(message)


def send_message(message):
    '''
    Send a native message to the browser
    '''
    encoded_content = json.dumps(message).encode("utf-8")
    encoded_length = struct.pack("@I", len(encoded_content))
    sys.stdout.buffer.write(encoded_length)
    sys.stdout.buffer.write(encoded_content)
    sys.stdout.buffer.flush()
