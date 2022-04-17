# -*- coding:utf-8 -*-
import os
from mitmproxy import http
from mitmproxy.coretypes.multidict import MultiDictView
import json


def filter_query(param):
    if isinstance(param, list) and len(param) > 0:
        return param[0]
    if isinstance(param, int):
        return param

    return ''


def query_to_dict(query: str):
    param = {}
    param_str_list = query.split('&')
    for param_str in param_str_list:
        try:
            k, v = param_str.split('=',1)
            param[k] = v
        except:
            print(param_str)
            print('*'*100)
    return param


def parse_url(url: str):
    if len(url.split('?')) > 1:
        base_url, query = url.split('?')
        param = query_to_dict(query)
        return {'base_url': base_url, 'param': param}
    return url


def cookie_dict_to_str(cookies: MultiDictView):
    cookie_str = ''
    for k, v in cookies.items(multi=True):
        cookie_str += f"{k}={v};"
    return cookie_str


def read_url_info():
    with open('url_info.json', 'r', encoding='utf8') as f:
        url_info = f.read()
    if len(url_info.strip()) > 100:
        return json.loads(url_info)
    else:
        return {}


def write_url_info(url_info):
    with open("url_info.json", 'w', encoding='utf8') as f:
        f.write(json.dumps(url_info))


def request(flow: http.HTTPFlow) -> None:
    cookies = flow.request.cookies
    flow_url = flow.request.url

    if "https://buyin.jinritemai.com/api/notice/getPopupMessages" in flow_url:
        url_info = read_url_info()
        param = parse_url(flow_url).get('param')
        url_info.update({'signature': param.get('_signature')})
        write_url_info(url_info)
    # invite info
    if "https://buyin.jinritemai.com/api/kolSquare/invite/shopApply" in flow_url and flow.request.method == "POST":
        print(flow.request.data)
        print(flow_url)
        url_info = read_url_info()
        param = parse_url(flow_url).get('param')
        url_info.update({'signature': param.get('_signature')})
        # url_info.update({'invite_id': param.get('invite_id')})
        # url_info.update({'invite_id': flow.request.query.get('invite_id')})
        url_info.update({'invite_url': flow_url})
        # url_info.update({'msToken': param.get('msToken')})
        # url_info.update({'X-Bogus': param.get('X-Bogus')})
        url_info.update({'invite_headers': dict(flow.request.headers)})
        url_info.update({'invite_cookies': cookie_dict_to_str(cookies)})
        write_url_info(url_info)
    # author list info
    # if "https://buyin.jinritemai.com/api/authorStatData/authorList" in flow_url:
    #     print('*' * 1000)
    #     from ads.douyin_daren.daren_query import query_to_dict
    #     print(flow_url)
    #     url_info = read_url_info()
    #     # url = flow.request.url
    #     # query_params=query_to_dict(str(flow.request.query))
    #     print(flow.request.query.get('msToken'))
    #     headers = flow.request.headers
    #     url_info.update({'msToken': flow.request.query.get('msToken')})
    #     url_info.update({'X-Bogus': flow.request.query.get('X-Bogus')})
    #     url_info.update({'_signature': flow.request.query.get('_signature')})
    #     url_info.update({'author_url': flow_url})
    #     url_info.update({'cookies': cookie_dict_to_str(cookies)})
    #     url_info.update({'headers': dict(headers)})
    #     write_url_info(url_info)

    # invite successed author info
    if "https://buyin.jinritemai.com/api/kolSquare/invite/shopInviteList?status=2" in flow_url:
        url_info = read_url_info()
        url = flow.request.url
        headers = flow.request.headers
        url_info.update({'invite_success_url': url})
        url_info.update({'cookies': cookie_dict_to_str(cookies)})
        url_info.update({'headers': dict(headers)})
        write_url_info(url_info)
    if "https://buyin.jinritemai.com/api/promotion/getList" in flow_url:
        url_info = read_url_info()
        url = flow.request.url
        print('*' * 1000)

        print(url)
        headers = flow.request.headers
        # url_info.update({'invite_success_url': url})
        param = parse_url(flow_url).get('param')
        url_info.update({'promotion_url': url})
        url_info.update({'promotion_signature': param.get('_signature')})
        url_info.update({'promotion_cookies': cookie_dict_to_str(cookies)})
        url_info.update({'promotion_headers': dict(headers)})
        write_url_info(url_info)
    if 'https://buyin.jinritemai.com/api/contact/contact_info' in flow_url:
        url_info = read_url_info()
        url = flow.request.url
        headers = flow.request.headers
        url_info.update({'contact_url': flow_url})
        url_info.update({'contact_cookies': cookie_dict_to_str(cookies)})
        url_info.update({'contact_headers': dict(headers)})
        write_url_info(url_info)
    if "https://fxg.jinritemai.com/api/order/searchlist" in flow_url:
        print(flow_url)
        url_info = read_url_info()
        url = flow.request.url
        headers = flow.request.headers
        url_info.update({'order_url': flow_url})
        url_info.update({'order_cookies': cookie_dict_to_str(cookies)})
        url_info.update({'order_headers': dict(headers)})
        write_url_info(url_info)

    if "https://fxg.jinritemai.com/api/order/receiveinfo" in flow_url:
        print(flow_url)
        url_info = read_url_info()
        url = flow.request.url
        headers = flow.request.headers
        url_info.update({'receiveinfo_url': flow_url})
        url_info.update({'receiveinfo_cookies': cookie_dict_to_str(cookies)})
        url_info.update({'receiveinfo_headers': dict(headers)})
        write_url_info(url_info)

    if "https://buyin.jinritemai.com/api/authorStatData/seekAuthor" in flow_url:
        print(flow_url)
        # from ads.douyin_daren.daren_query import query_to_dict
        print(flow_url)
        url_info = read_url_info()
        # url = flow.request.url
        # query_params=query_to_dict(str(flow.request.query))
        print(flow.request.query.get('msToken'))
        headers = flow.request.headers
        url_info.update({'msToken': flow.request.query.get('msToken')})
        url_info.update({'X-Bogus': flow.request.query.get('X-Bogus')})
        url_info.update({'_signature': flow.request.query.get('_signature')})
        url_info.update({'author_url': flow_url})
        url_info.update({'cookies': cookie_dict_to_str(cookies)})
        url_info.update({'headers': dict(headers)})
        write_url_info(url_info)


    if "https://mobile.yangkeduo.com/proxy/api/api/aristotle/order_list" in flow_url:
        print(flow_url)
        # from ads.douyin_daren.daren_query import query_to_dict
        url_info = read_url_info()
        print(flow.request.data)
        # query_params=query_to_dict(str(flow.request.query))
        headers = flow.request.headers
        url_info.update({'pdd_order_url': flow_url})
        url_info.update({'pdd_cookies': cookie_dict_to_str(cookies)})
        url_info.update({'pdd_headers': dict(headers)})
        write_url_info(url_info)

    if "https://mobile.yangkeduo.com/orders.html" in flow_url:
        url_info = read_url_info()
        # url = flow.request.url
        # query_params=query_to_dict(str(flow.request.query))
        headers = flow.request.headers
        url_info.update({'pdd_order_detail_url': flow_url})
        url_info.update({'pdd_detail_cookies': cookie_dict_to_str(cookies)})
        url_info.update({'pdd_detail_headers': dict(headers)})
        write_url_info(url_info)