# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import datetime
from typing import Optional, List, Union, Dict

import requests

import json

import time

from ads.douyin_daren.mysql_util import MysqlUtil


def parse_josn() -> dict:
    """
    read json config from file
    :return: url requests infos
    """
    with open('url_info.json', 'r') as f:
        url_info_dict = json.loads(f.read())

    return url_info_dict


def parse_url(url: str):
    """
    parse url to base_url(schema+host) and params(query to dict)
    :param url:
    :return:
    """
    if len(url.split('?')) > 1:
        base_url, query = url.split('?')
        param = query_to_dict(query)
        return {'base_url': base_url, 'param': param}
    return url


def query_to_dict(query: str) -> dict:
    """
    parse url query(like a=1&b=2) to dict format({"a":1,"b":2})
    :param query:
    :return:
    """
    param = {}
    param_str_list = query.split('&')
    for param_str in param_str_list:
        k, v = param_str.split('=', 1)
        if str(k).endswith('[]'):
            exists_value = param.get(k, [])
            exists_value.append(v)
            param.update({k: exists_value})
        else:
            param[k] = v
    return param


def dict_to_query(param_dict):
    """
    parse dict format to query format(like a=1&b=2)
    :param param_dict:
    :return:
    """
    query = "?"
    for k, v in param_dict.items():
        if isinstance(v, list):

            for sub_value in v:
                query += f'{k}={sub_value}&'
        else:
            query += f"{k}={v}&"
    return query.rstrip('&')


def update_param(param_dict: Dict[str, str], url: str):
    """update url`s query param value"""
    base_url, query = url.split('?')
    param = query_to_dict(query)
    param.update(param_dict)
    new_query = dict_to_query(param)
    return base_url + new_query


def get_search_config() -> dict:
    """return config from search config file"""
    with open("search_config.json", 'r', encoding='utf8') as f:
        search_config = json.loads(f.read())
    return search_config


def get_author_list(start_page, end_page):
    """ return author info list"""
    url_info_dict = parse_josn()
    url = url_info_dict.get('author_url')
    headers = url_info_dict.get('headers')
    headers.update({"Cookie": url_info_dict.get("cookies")})

    user_list = []
    for i in range(start_page, end_page + 1):
        other_config = get_search_config().get('other_config')
        other_config.update({'page': i})
        new_url = update_param(other_config, url)
        try:
            time.sleep(0.1)
            res = requests.get(new_url, headers=headers)
            page_list = json.loads(res.text).get('data').get('list')
            no_repeat_list = remove_repeat(page_list)
            user_list.extend(no_repeat_list)
        except Exception as e:
            print(e)
            print(f'get users failed of page {i}')
        print(f"{new_url}  get users success")
    return user_list


def get_invite_successed_authors_info(start_page, end_page) -> List[Dict[str, str]]:
    """
    :return: [{"uid":uid,"create_date":time,.....}]
    """
    url_info_dict = parse_josn()
    url = url_info_dict.get('invite_success_url')
    headers = url_info_dict.get('headers')
    headers.update({"Cookie": url_info_dict.get("cookies")})
    invited_list = []
    for page in range(start_page, end_page + 1):
        new_url = update_param({'page_no': str(page)}, url)
        res = requests.get(new_url, headers=headers)
        invited_list.extend(json.loads(res.text).get('data').get('invite_list'))

    author_info_list = []
    for invited in invited_list:
        result_author_info = {}
        create_time = invited.get('invite_base').get('create_time')
        author_info = invited.get('author_info')
        uid = author_info.get('author_base').get('uid')
        nickname = author_info.get('author_base').get('nickname')
        city = author_info.get('author_base').get('city')
        gender = author_info.get('author_base').get('gender')
        fans_num = author_info.get('author_base').get('fans_num')
        level = author_info.get('author_base').get('author_level')
        phone = author_info.get('author_contact').get('phone')
        wechat = author_info.get('author_contact').get('wechat')
        convert_rate = author_info.get('author_live').get('convert_rate')
        avatar = author_info.get('author_base').get('avatar')
        sale_low = author_info.get('author_live').get('sale_low')
        sale_high = author_info.get('author_live').get('sale_high')
        intention_category = author_info.get('author_tag').get('main_cate')

        result_author_info.update({"intention_category": intention_category})
        result_author_info.update({"avatar": avatar})
        result_author_info.update({"live_sale_low": sale_low})
        result_author_info.update({"live_sale_high": sale_high})
        result_author_info.update({"uid": uid})
        result_author_info.update({"nickname": nickname})
        result_author_info.update({"gender": gender})
        result_author_info.update({"city": city})
        result_author_info.update({"convert_rate": convert_rate})
        result_author_info.update({"wechat": wechat})
        result_author_info.update({"phone": phone})
        result_author_info.update({"fans_sum": fans_num})
        result_author_info.update({"level": level})
        result_author_info.update({"create_time": create_time})
        author_info_list.append(result_author_info)
    return author_info_list


def get_author_detail(uid: Union[List[str], str]):
    author_info_list = []
    url_info_dict = parse_josn()
    headers = url_info_dict.get('headers')
    signature = url_info_dict.get('signature')
    headers.update({"Cookie": url_info_dict.get("cookies")})
    profile_url = f'https://buyin.jinritemai.com/api/authorStatData/authorProfile?uid={uid}&works_type=&special_price_id=&_signature={signature}'
    if isinstance(uid, str):
        res = requests.get(url=profile_url, headers=headers)
        a = (json.loads(res.text))
        author_info_list.append(a)
    if isinstance(uid, list):
        for id in uid:
            get_author_detail(id)

    return author_info_list


def author_list_filter(filter, author_list):
    """filter the result of get_author_list()
    :param filter: like {"convert_rate":{">":80},"promotion_main_price_range":{'in':'100-500'},}
    """
    return_author_list = []
    for author_dict in author_list:
        flag = 0
        for filter_key, filter_content in filter.items():
            for all_dict in list(author_dict.values()):
                if all_dict.get(filter_key):
                    actual_value = all_dict.get(filter_key)
                    break
            # if not actual_value:
            #     continue
            filter_condition, filter_value = (list(filter_content.items())[0])
            if filter_condition in ['>', '<', '!=', '==']:
                # filter_value is str
                condition = eval(str(actual_value) + str(filter_condition) + str(filter_value))
            if filter_condition in ['not']:
                # not [a,b,],filter_value should be a list
                condition = eval(str(sum([actual_value.find(i) for i in filter_value]) == -len(filter_value)))
            if condition:
                flag += 1
            else:
                flag -= 1
        if flag == len(filter.keys()):
            return_author_list.append(author_dict)
    return return_author_list


def remove_repeat(author_list):
    no_repeat_list = []
    for author_dict in author_list:
        invition_status = author_dict.get('author_tag').get('invitaiton_status')
        if invition_status not in [2, 3, 4]:
            no_repeat_list.append(author_dict)
    return no_repeat_list


def get_product_list():
    url_info_dict = parse_josn()
    headers = url_info_dict.get('promotion_headers')
    promotion_url = url_info_dict.get('promotion_url')
    signature = url_info_dict.get('promotion_signature')
    headers.update({"Cookie": url_info_dict.get("promotion_cookies")})
    url = update_param({'_signature': signature}, promotion_url)
    res = requests.get(url, headers=headers)
    print(json.loads(res.text).get('data'))


def invite_post(author_id):
    """
    author_id: 6f5d86d89179942daafa394412964332
    discount: 9
    cos_ratio: 8
    contact_phone:
    contact_name:
    contact_wechat:
    desc: 邀请语
    promotion_sort_type: 1
    sample_back: 1
    promotions: [{"institution_activity_id": 0, "promotion_id": "需要填写promotion_id", "custom_rate": 0}]
"""
    url_info_dict = parse_josn()
    _signature = url_info_dict.get("signature")
    invite_url = url_info_dict.get("invite_url")
    msToken = url_info_dict.get("msToken")
    X_Bogus = url_info_dict.get("X-Bogus")
    # invite_id = url_info_dict.get("invite_id")

    new_url = update_param({"signature": _signature, "X-Bogus": X_Bogus, "msToken": msToken, },
                           invite_url)
    headers = url_info_dict.get("invite_headers", url_info_dict.get('headers'))
    headers.update({"Cookie": url_info_dict.get("invite_cookies", url_info_dict.get('cookies'))})
    # new_url=update_param({''})
    # headers.update({"referer": "https://buyin.jinritemai.com/dashboard/servicehall/daren-profile?uid=6f5d86d89179942daafa394412964332&log_id=202112042323040101330380800495318D&enter_from=1&previous_page_name=0,5&previous_page_type=0,101&search_id=2021120423222001021214815623A49333"})
    # headers.update({"x-secsdk-csrf-token": "000100000001d0b297707aed166f118b51d9f3524b9b9eede5491af39914d47787f9113385a716bd969b1c0c5820"})
    # headers.update({"Cookie": url_info_dict.get("cookies")})
    body = {
        "author_id": author_id,
        "discount": 9,
        "cos_ratio": 20,
        "contact_phone": "18463583538",
        "contact_name": "李先生",
        "contact_wechat": "alaskgo",
        "desc": "挂车提供免费抖加投放，品质保障售后无忧，低价高佣",
        "promotion_sort_type": "1",
        "sample_back": "1",
        "promotions": json.dumps(
            [
                # {"institution_activity_id":0,"promotion_id":"3526831385576877968","custom_rate":0,"coop_desc":"短视频带货","no_audit_sample":2},

                # {"institution_activity_id": 0, "promotion_id": "3525426319238253778", "custom_rate": 0},
                # {"institution_activity_id": 0, "promotion_id": '3520241344054432494', "custom_rate": 0},
                # {"institution_activity_id": 0, "promotion_id": '3525432432973193706', "custom_rate": 0},
                # {"institution_activity_id": 0, "promotion_id": '3525438774492409248', "custom_rate": 0},
                # {"institution_activity_id": 0, "promotion_id": '3525989509240067574', "custom_rate": 0},
                # #
                {"institution_activity_id":0,"promotion_id":"3520241344054432494","is_trusteeship":True,"custom_rate":0,"coop_desc":"","no_audit_sample":2}
                ,{"institution_activity_id":0,"promotion_id":"3532477465958180125","is_trusteeship":True,"custom_rate":0,"coop_desc":"","no_audit_sample":2}
                # {"institution_activity_id": 0, "promotion_id": '3521678713278301346', "coop_desc": "短视频带货", "custom_rate": 0},

            ])
    }

    res = requests.post(new_url, data=body, headers=headers)
    print(res.text)
    return res.text


def get_contact_info(uid):
    url_info_dict = parse_josn()
    headers = url_info_dict.get('contact_headers')
    url = url_info_dict.get('contact_url')
    signature = url_info_dict.get('signature')
    headers.update({"Cookie": url_info_dict.get("contact_cookies")})
    param = {
        'origin_uid': uid,
        'contact_mode': 1,  # wechat is 2, phone is 1
        '_signature': signature
    }

    url = 'https://buyin.jinritemai.com/api/contact/contact_info?origin_uid=xxx&app_id=1128&contact_mode=1&check_mode=2&_signature=asd'
    new_url = update_param(param, url)

    res = requests.get(new_url, headers=headers)
    data1 = json.loads(res.text).get('data')
    param.update({'contact_mode': 2})
    new_url = update_param(param, url)
    res = requests.get(new_url, headers=headers)
    data2 = json.loads(res.text).get('data')
    if data1:
        data1 = data1.get('contact_info').get('contact_value')
    if data2:
        data2 = data2.get('contact_info').get('contact_value')

    return json.dumps({'phone': data1, 'wechat': data2})


def insert(author_list, connect, invited=True):
    for author in author_list:
        uid = author.get('uid')
        try:
            detail = get_author_detail(uid)[0].get('data')
        except:
            continue
        res = {}
        if not invited:
            res = json.loads(get_contact_info(uid))
        #
        author_dict = {
            'nickname': author.get('nickname'),
            'account_douyin': detail.get('account_douyin'),
            'phone': author.get('phone') if author.get('phone') else res.get('phone'),
            'wechat': author.get('wechat') if author.get('wechat') else res.get('wechat'),
            'fans_num': author.get('fans_sum'),
            'gender': detail.get('gender'),
            'works_type': detail.get('works_type'),
            'city': detail.get('city'),
            'score': detail.get('score', '-1'),
            'live_sale_low': author.get('live_sale_low'),
            'live_sale_high': author.get('live_sale_high'),
            'convert_rate': author.get('convert_rate'),
            'avatar': author.get('avatar') if author.get('avatar') else detail.get('avatar'),
            'intention_category': detail.get('intention_catgory') if detail.get('intention_catgory') else author.get(
                'intention_category'),
            'create_time': datetime.datetime.now(),
            'share_url_douyin': "https://api.pwmqr.com/qrcode/create/?url=" + detail.get('share_url_douyin', 'failed'),
        }
        if not (author_dict.get('phone') or author_dict.get('wechat')):
            continue
        if invited:
            author_dict.update({'invited_time': author.get('create_time')})
            connect.insert_invited_author_data(connect.connect(), **author_dict)
        else:
            connect.insert_author_data(connect.connect(), **author_dict)
import re
def get_pdd_order(pages):
    url_info_dict = parse_josn()
    headers = url_info_dict.get('pdd_headers')
    url = url_info_dict.get('pdd_order_url')
    headers.update({"Cookie": url_info_dict.get("pdd_cookies")})
    for page in pages:
        offset=0
        param = {

                "offset": 0,
                "origin_host_name": "mobile.yangkeduo.com",
                "page": 1,
                "page_from": 1,
                "size": 20,
                "type": "unreceived"

        }

        res = requests.post(url, data=param, headers=headers)
        order_sn=[i.get('order_sn') for i in json.loads(res.text).get('orders')]
        offset = order_sn[-1]
        detail_url='https://mobile.yangkeduo.com/order.html?order_sn=%s'
        pdd_detail_headers = url_info_dict.get('pdd_detail_headers')
        # url = url_info_dict.get('pdd_order_url')
        pdd_detail_headers.update({"Cookie": url_info_dict.get("pdd_detail_cookies")})
        for sn in order_sn:

            try:
                new_url=detail_url%sn
                detail_page_res = requests.get(new_url, headers=pdd_detail_headers).text
                address=re.findall('<div class="_3GeQUL0R _3D2XMwAz" role="link" aria-label="(.*?)>',detail_page_res,re.S)[0]
                name=re.findall('class="Be3oUxVQ">(.*?)<',detail_page_res,re.S)[0]
                status=re.findall('<p class="x86glo_R" aria-hidden="true">(.*?)</p>',detail_page_res,re.S)[0]
                deliver_num=re.findall('"快递单号： (.*?) "',detail_page_res,re.S)
                order_sn=re.findall('"订单编号： (.*?) "',detail_page_res,re.S)
                print(name,status, order_sn,deliver_num,address,)
            except:
                print(sn)
if __name__ == '__main__':
    get_pdd_order([1,1])