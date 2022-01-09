#!/usr/bin/env python

# -*- coding: utf-8 -*-

import nativemessaging

msg = nativemessaging.get_message()
nativemessaging.log_browser_console("received msg: %s" % str(msg))
nativemessaging.send_message("test")

print()
