# -*- coding:utf-8 -*-
class Author:
    def __init__(self, **kwargs):
        self.nickname = kwargs.get('nickname')
        self.account_douyin = kwargs.get('account_douyin')
        self.phone = kwargs.get('phone')
        self.wechat = kwargs.get('wechat')
        self.fans_num = kwargs.get('fans_num')
        self.gender = kwargs.get('gender')
        self.works_type = kwargs.get('works_type')
        self.city = kwargs.get('city')
        self.score = kwargs.get('score')
        self.convert_rate = kwargs.get('convert_rate')
        self.avatar = kwargs.get('avatar')
        self.intention_category = kwargs.get('intention_category')
