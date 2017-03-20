#!/usr/bin/env python
# coding: utf-8
from wxbot import *
import oneshot
import json
import random

class OneShot_Robot(WXBot):
    def handle_msg_all(self, msg):
        print(msg['msg_type_id'])
        if msg['msg_type_id'] == 4:
            # # 联系人消息
            if msg['content']['type'] == 0: # 文本
                user_message = msg['content']['data'].strip()
                print(msg['msg_type_id'],msg['user']['id'],msg['user']['name'])
                if oneshot.ping() != 200:
                    self.send_msg_by_uid('服务没有启动，请耐心等待。', msg['user']['id'])
                    return
                else:
                    if user_message in ['get','GET','取','要']:
                        self.last_msg = 'get'
                        rt = oneshot.get_list()
                        self.send_msg_by_uid(rt, msg['user']['id'])

                    elif user_message in ['1','2','3','4','5','6','7']:
                        if len(self.temp_record) == 0 or self.last_msg in ['get','help','number']:
                            self.send_msg_by_uid('想唠嗑？请继续。。。', msg['user']['id'])
                            return
                        rt = oneshot.save_oneshot(user_message, self.temp_record)
                        self.send_msg_by_uid(rt, msg['user']['id'])
                        self.last_msg = 'number'
                    elif user_message in ['help','HELP','帮助','?','？']:
                        self.last_msg = 'help'
                        rt = oneshot.help()
                        self.send_msg_by_uid(rt, msg['user']['id'])
                    else:
                        self.last_msg = 'other'
                        self.temp_record = user_message
                        rt = oneshot.select_oneshot() 
                        self.send_msg_by_uid(rt, msg['user']['id'])
            elif msg['content']['type'] == 1: # 地理位置
                rt = '我在广州等你:-O'
                self.send_msg_by_uid(rt, msg['user']['id'])
            elif msg['content']['type'] == 3: # 图片
                no = random.randint(1, 8)
                rt = '/pic/' + str(no) + '.jpg'
                self.send_img_msg_by_uid(rt, msg['user']['id'])
            elif msg['content']['type'] == 4: # 语音
                rt = '不是说了么，我只认识文字呢'
                self.send_msg_by_uid(rt, msg['user']['id'])
            elif msg['content']['type'] == 5: # 名片
                rt = '只聊天，不谈感情'
                self.send_msg_by_uid(rt, msg['user']['id'])
            elif msg['content']['type'] == 6: # 动画
                rt = '要求这么高，有红包吗？'
                self.send_msg_by_uid(rt, msg['user']['id'])
            elif msg['content']['type'] == 7: # 分享
                rt = '感谢分享'
                self.send_msg_by_uid(rt, msg['user']['id'])
            elif msg['content']['type'] == 8: # 视频
                rt = '要求这么高，有红包吗？'
                self.send_msg_by_uid(rt, msg['user']['id'])
            elif msg['content']['type'] == 9: # 视频电话
                self.send_msg_by_uid(rt, msg['user']['id'])
            elif msg['content']['type'] == 10: # 撤回消息
                rt = '有话好好说，莫急'
                self.send_msg_by_uid(rt, msg['user']['id'])
            elif msg['content']['type'] == 11: # 空内容
                rt = 'what?'
                self.send_msg_by_uid(rt, msg['user']['id'])
            elif msg['content']['type'] == 12: # 红包
                rt = '谈钱伤感情'
                self.send_msg_by_uid(rt, msg['user']['id'])
            elif msg['content']['type'] == 13: # 小视频
                rt = '一个人偷偷看就好'
                self.send_msg_by_uid(rt, msg['user']['id'])
            else: # 99 unkown type message
                print(msg['msg_type_id'],msg['user']['id'],msg['user']['name'])
                self.send_msg_by_uid('我只识字哇(=@__@=)', msg['user']['id'])
            # self.send_msg_by_uid('contact message', msg['user']['id'])
        elif msg['msg_type_id'] == 37: # 通过好友认证
            RecommendInfo = {}
            ticket = msg['content']['data']['Ticket']
            username = msg['content']['data']['UserName']
            nickname = msg['content']['data']['NickName']
            RecommendInfo['UserName'] = username
            RecommendInfo['Ticket'] = ticket
            self.apply_useradd_requests(RecommendInfo)
            self.get_big_contact()
            print('self.get_big_contact()')

            # 注册用户
            return
            # self.send_msg(username,'hello, ' + nickname, isfile=False)
        else:
            self.send_msg_by_uid('wait a moment...', msg['user']['id'])


def create_wxrobot():
    osr = OneShot_Robot()
    osr.DEBUG ==True
    osr.conf['qr'] = 'png'#'tty' #png
    osr.is_big_contact = False
    osr.temp_record = ''
    osr.last_msg = ''
    return osr


if __name__ == '__main__':
    bot = create_wxrobot()
    bot.run()


# handle_msg_all 函数的参数 msg 是代表一条消息的字典。字段的内容为：

# 字段名                      字段内容
# msg_type_id            整数，消息类型，具体解释可以查看 消息类型表
# msg_id                 字符串，消息id
# content                字典，消息内容，具体含有的字段请参考 消息类型表 ，一般含有 type(数据类型)与 data(数据内容)字段，type 与 data的对应关系可以参考 数据类型表
# user                   字典，消息来源，字典包含 name(发送者名称,如果是群则为群名称，如果为微信号，有备注则为备注名，否则为微信号或者群昵称)字段与 id(发送者id)字段，都是字符串



#  消息类型表

# 类型号    消息类型                content
# 0        初始化消息，内部数据      无意义，可以忽略
# 1        自己发送的消息           无意义，可以忽略
# 2        文件消息                字典，包含 type 与 data 字段
# 3        群消息                  字典， 包含 user (字典，包含 id 与 name字段，都是字符串，表示发送此消息的群用户)与 type 、 data 字段，红包消息只有 type 字段， 文本消息还有detail、desc字段， 参考 群文本消息
# 4        联系人消息              字典，包含 type 与 data 字段
# 5        公众号消息              字典，包含 type 与 data 字段
# 6        特殊账号消息            字典，包含 type 与 data 字段
# 99       未知账号消息            无意义，可以忽略


# 数据类型表

# type    数据类型            data
# 0   文本                  字符串，表示文本消息的具体内容
# 1   地理位置               字符串，表示地理位置
# 3   图片                  字符串，图片数据的url，HTTP POST请求此url可以得到jpg文件格式的数据
# 4   语音                  字符串，语音数据的url，HTTP POST请求此url可以得到mp3文件格式的数据
# 5   名片                  字典，包含 nickname (昵称)， alias (别名)，province (省份)，city (城市)， gender (性别)字段
# 6   动画                  字符串， 动画url, HTTP POST请求此url可以得到gif文件格式的数据
# 7   分享                  字典，包含 type (类型)，title (标题)，desc (描述)，url (链接)，from (源网站)字段
# 8   视频                  不可用
# 9   视频电话               不可用
# 10  撤回消息               不可用
# 11  空内容                空字符串
# 12  红包                  不可用
# 13  小视频                字符串，视频数据的url，HTTP POST请求此url可以得到mp4文件格式的数据
# 99  未知类型              不可用