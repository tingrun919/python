#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
import time
from bs4 import BeautifulSoup
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler


class everyDay:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    }
    account_sid = 'ACe9a421577ebe39960157fd3f6d2078d0'
    auth_token = 'f936b3790eda1f66bb3ae983b30d9a94'
    base_number = '+12702154642'

    content_url = "http://wufazhuce.com/"
    weather_url = "http://t.weather.sojson.com/api/weather/city/"

    def tigger_cron(self):
        scheduler = BlockingScheduler()
        scheduler.add_job(self.fetch_one_sentence, 'cron', hour='15', minute="59")
        scheduler.start()

    def send_message(self, send_content):
        print(f"发送的话语是：\n",send_content)
        client = Client(self.account_sid, self.auth_token)
        numbers_to_message = ['+8617753102990']
        for number in numbers_to_message:
            mst = client.messages.create(
                body = send_content,
                from_ = self.base_number,
                to = number
            )
            print(mst)

    def fetch_weather(self, one_sentence='', city_code='101120101', sms_from='from:田三岁', sms_to="to:涵涵小宝贝"):
        response = requests.get(
            self.weather_url+city_code, headers=self.headers)
        if response.status_code == requests.codes.ok and self.check_json(response):
            #今日天气
            today_weather = response.json().get('data').get('forecast')[0]
            #日期
            today_date = time.strftime("%Y{Y}%m{m}%d{d} %H:%M:%S", time.localtime()).format(Y = '年',m = '月',d = '日')
            #配合天气的话语
            today_content = f"天气：{today_weather.get('type')} —— {today_weather.get('notice')}"
            #温度 低温 / 高温
            today_temperature = f"温度：{today_weather.get('low').split(' ')[1]} / {today_weather.get('high').split(' ')[1]}"
            #风
            today_wind = f"风力/风向：{today_weather.get('fx')} / {today_weather.get('fl')}"
            #空气质量情况
            today_aqi = f"空气质量：{self.switch_aqi(today_weather.get('aqi'))}"

            today_msg = f'{sms_to}\n\n{today_date}\n{today_content}\n{today_temperature}\n{today_wind}\n{today_aqi}\n{one_sentence}\n\n{sms_from}'
            print("获取天气信息成功！")
            self.send_message(today_msg)

    def fetch_one_sentence(self):
        response = requests.get(self.content_url, headers=self.headers)
        soup = BeautifulSoup(response.text, "lxml")
        content = soup.find_all(
            'div', class_="fp-one-cita")[0].find('a').get_text()
        print("获取每日暖心话语成功！")
        self.fetch_weather(content)

    def check_json(self, arg):
        try:
            arg.json()
            return True
        except:
            print("获取天气信息失败!")
            return False

    def switch_aqi(self, aqi):
        if aqi < 50:
            return '优'
        elif aqi > 50 and aqi < 100:
            return '良'
        elif aqi > 100 and aqi < 150:
            return '轻度污染'
        elif aqi > 150 and aqi < 200:
            return '中度污染'
        elif aqi > 200 and aqi < 300:
            return '重度污染'
        else:
            return '严重污染'

if __name__ == '__main__':
    everyDay().tigger_cron()
