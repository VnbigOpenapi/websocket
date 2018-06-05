#!/usr/bin/python
#coding=utf-8
from gevent import monkey
monkey.patch_all(select=False)

import gevent
from ws4py.client.geventclient import WebSocketClient

ws = WebSocketClient('ws://ws.vnbig.com/ws', protocols=['http-only', 'chat'])
ws.connect()

def reqParam():
    coin = ['_eth_ltc', '_usdt_csi', '_btc_csi', '_eth_eos', '_usdt_ltc', '_eth_bch', '_btc_eos', '_eth_csi'
        , '_usdt_btc', '_btc_bch', '_btc_etc', '_btc_eth', '_btc_ltc', '_usdt_bch', '_usdt_eth']
    period = ['_1min', '_5min', '_15min', '_30min', '_1hour', '_4hour', '_6hour', '_12hour', '_1day'
        , '_1week', '_1month']

    list_param = []
    for i in coin:
        for j in period:
            list_param.append("{'event':'addChannel','channel':'vnbig%s%s_ticker'}"% (i, j))
        list_param.append("{'event':'addChannel','channel':'vnbig%s_depth'}"% i)
        list_param.append("{'event':'addChannel','channel':'vnbig%s_trade'}"% i)

    return list_param

def incoming():
    """
    Greenlet waiting for incoming messages
    until ``None`` is received, indicating we can
    leave the loop.
    """
    while True:
        m = ws.receive()
        print(m)

def send_a_bunch():
    for d in reqParam():
        ws.send(d)
        print(d)

greenlets = [gevent.spawn(send_a_bunch)
    , gevent.spawn(incoming)
    ,]
gevent.joinall(greenlets)
