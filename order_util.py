# -*- coding:utf-8 -*-
import json

from ads.douyin_daren.daren_query import *
from ads.douyin_daren.xls_util import *

def _get_receive_info(shop_oder_id,skip=False):
    if skip:
        return 0
    url_info_dict = parse_josn()
    receiveinfo_url = url_info_dict.get('receiveinfo_url')
    receiveinfo_cookies = url_info_dict.get('receiveinfo_cookies')
    receiveinfo_headers = url_info_dict.get('receiveinfo_headers')
    new_receiveinfo_url = update_param({'order_id': shop_oder_id}, receiveinfo_url)
    receiveinfo_headers.update({"Cookie": url_info_dict.get("order_cookies")})
    res = requests.get(new_receiveinfo_url, headers=receiveinfo_headers)
    while json.loads(res.text).get('msg')!="":
        print(json.loads(res.text))
        time.sleep(20)
        res = requests.get(new_receiveinfo_url, headers=receiveinfo_headers)

    receive_info = json.loads(res.text).get('data').get('receive_info')
    post_receiver = receive_info.get('post_receiver')
    post_tel = receive_info.get('post_tel')
    post_addr = receive_info.get('post_addr')
    province = post_addr.get('province').get('name')
    city = post_addr.get('city').get('name')
    town = post_addr.get('town').get('name')
    street = post_addr.get('street').get('name')
    detail = post_addr.get('detail')

    res_str = f"{post_receiver},{post_tel},{province}{city}{town}{street}{detail}"
    return res_str


def get_author_list(start_page, end_page,order_id=None,order_common=None,skip=False):
    """ return author info list"""
    url_info_dict = parse_josn()
    url = url_info_dict.get('order_url')
    if order_id:
        url=update_param({"order_id":order_id},url)
    if order_common:
        url = update_param({"order_common": order_common}, url)
        skip=True
    headers = url_info_dict.get('order_headers')

    headers.update({"Cookie": url_info_dict.get("order_cookies")})

    res = requests.get(url, headers=headers)
    order_list = json.loads(res.text).get('data')
    export_order_info = []
    for order in order_list:
        time.sleep(1)
        shop_oder_id = order.get('shop_order_id')
        create_time = order.get('create_time')
        product_item = order.get('product_item')
        export_product_info = []
        for product in product_item:
            sku_spec = product.get('sku_spec')[0]
            product_name = sku_spec.get('value')
            combo_num = product.get('combo_num')
            export_product_info.append({product_name:combo_num})
        addr = _get_receive_info(shop_oder_id,skip)
        order_info={'shop_oder_id': shop_oder_id, 'product': export_product_info, 'addr': addr}
        print(order_info)
        export_order_info.append(order_info)
    with open('export_product_info.json','w',encoding='utf8') as f:
        f.write(json.dumps(export_order_info))
    return export_order_info


def get_order_by_users(user_info_list):
    url_info_dict = parse_josn()
    url = url_info_dict.get('order_url')
    headers = url_info_dict.get('order_headers')
    headers.update({"Cookie": url_info_dict.get("order_cookies")})
    for user_info in user_info_list:
        if user_info:
            url = update_param({"order_common": int(user_info)}, url)
            skip = True
        res = requests.get(url, headers=headers)
        order_list = json.loads(res.text).get('data')
        export_order_info = []
        for order in order_list:
            time.sleep(1)
            shop_oder_id = order.get('shop_order_id')
            create_time = order.get('create_time')
            product_item = order.get('product_item')
            order_status_text = order.get('order_status_info').get('order_status_text')
            export_product_info = []
            for product in product_item:
                sku_spec = product.get('sku_spec')[0]
                product_name = sku_spec.get('value')
                combo_num = product.get('combo_num')
                export_product_info.append({product_name: combo_num})
            order_info = {'shop_oder_id': shop_oder_id, 'product': export_product_info,'order_status_text':order_status_text}
            print(shop_oder_id)


if __name__ == '__main__':
    # get_author_list(1, 1,order_common=18587768137)
    # get_order_by_users([18587768137])




    # _get_receive_info(4896835923784527173)
    phone_list=get_phone_list()
    get_order_by_users(phone_list)