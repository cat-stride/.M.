#!/usr/bin/env python
# coding: utf-8
from wxbot import *

class OneShot_Robot(WXBot):
    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            self.send_msg_by_uid('test', msg['user']['id'])





def create_wxrobot():
    osr = OneShot_Robot()
    osr.DEBUG ==True
    osr.conf['qr'] = 'png'
    osr.is_big_contact = False
    return osr


if __name__ == '__main__':
    bot = create_wxrobot()
    bot.run()
