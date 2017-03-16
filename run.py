#!/usr/bin/env python
# coding: utf-8
from wxbot import *
import oneshot
import json

class OneShot_Robot(WXBot):
    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            # 联系人消息  文本消息
            print(msg['user']['name']+":"+msg['content']['data'])
            msg['content']['data']
            

            if msg['content']['data'] in ['get','GET','取','要']:
                oneshots = oneshot.get_oneshot()
                rt = ''
                for shot in oneshots:
                    rt += '子弹id :' + str(shot['bid']) + '\n' + "符号名：" + shot['sym_name']  + '\n' + \
                     "内容：" + shot['content']  + '\n' +  " 日期：" +str(shot['timestamp']) + '\n'
                if len(oneshots) == 0:
                    rt = '没有记录'
                self.send_msg_by_uid(rt, msg['user']['id'])
            elif msg['content']['data'] in ['y','Y','yes','是','是的']:
                print('temp:',self.temp_record)
                data = {}
                data["sym_name"] = "todo"
                data["content"] = self.temp_record      
                post_data = json.dumps(data)
                r = oneshot.post_oneshot(post_data)
                if r != 200:
                    self.send_msg_by_uid('Post failed', msg['user']['id'])
                else:
                    self.send_msg_by_uid('Saved', msg['user']['id'])
            else:
                self.temp_record = msg['content']['data'].strip()
                self.send_msg_by_uid('是否将上述内容保存为一条笔记？', msg['user']['id'])
        else:
            self.send_msg_by_uid('是不是在考验我？可以发文本消息吗？', msg['user']['id'])





def create_wxrobot():
    osr = OneShot_Robot()
    osr.DEBUG ==True
    osr.conf['qr'] = 'tty' #png
    osr.is_big_contact = False
    osr.temp_record = ''
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