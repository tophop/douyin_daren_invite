# -*- coding:utf-8 -*-
import time
from mitmproxy import *
import subprocess
import os, sys, signal
import webbrowser
import winreg
import threading


def setup_cert():
    if not find_cert_path():
        init_dump()
    p = subprocess.Popen("certutil -addstore -f root %s" % find_cert_path(), shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    a, b = p.communicate()
    print(a.decode('GBK'), b.decode('GBK'))


def find_cert_path():
    user_dir = os.listdir('C:\\Users')
    cert_dir = ""
    for dir in user_dir:
        cur_path = os.path.join('C:\\Users', dir)
        try:
            os.listdir(cur_path)
            if ".mitmproxy" in os.listdir(cur_path):
                cert_dir = os.path.join(cur_path, '.mitmproxy')
        except Exception as e:
            pass
    cert_path = os.path.join(cert_dir, "mitmproxy-ca-cert.cer")
    if os.path.exists(cert_path):
        return cert_path
    return None


def init_dump():
    loop = 0
    while True:
        if not find_cert_path():
            p = subprocess.Popen("mitmdump", shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            time.sleep(loop)
            loop += 1
            print(loop)
            os.kill(p.pid, signal.SIGTERM)
        else:
            break


def get_browser_path():
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Classes\http\shell\open\command") as key:
        path = winreg.QueryValue(key, None).split("--")[0]
    return path


def start_dump():
    force_end_dump()

    def run_mitm():
        os.system("mitmdump -s daren_filter.py")

    t = threading.Thread(target=run_mitm)
    t.daemon = True
    print('start dump')
    t.start()
    # run_mitm()

def start_browser():
    browser_path = get_browser_path()
    print('start browser')
    print(browser_path)
    cmd = f'{browser_path} --proxy-server=127.0.0.1:8080 --ignore-certificate-errors'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    print(cmd)


def force_end_dump():
    os.system("taskkill /F /IM mitmdump.exe")
    os.system("taskkill /F /IM mitmproxy.exe")


if __name__ == '__main__':
    setup_cert()
    force_end_dump()
    # start_browser()
    start_dump()
