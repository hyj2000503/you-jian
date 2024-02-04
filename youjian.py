import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 城市名称到城市代码的映射
city_codes = {
    # 完整的城市代码映射
    '北京': '101010100',
    '上海': '101020100',
    '广州': '101280101',
    '深圳': '101280601',
    '安庆': '101220601',
    '南京': '101190101',
    '沈阳': '101070101',

    '蚌埠': '101220201',
    '亳州': '101220901',
    '巢湖': '101221601',
    '池州': '101221701',
    '滁州': '101221101',
    '阜阳': '101220801',
    '合肥': '101220101',
    '淮北': '101221201',
    '淮南': '101220401',
    '黄山': '101221001',
    '六安': '101221501',
    '马鞍山': '101220501',
    '宿州': '101220701',
    '铜陵': '101221301',
    '芜湖': '101220301',
    '宣城': '101221401',

    '无锡': '101190201',
    '镇江': '101190301',
    '苏州': '101190401',
    '南通': '101190501',
    '扬州': '101190601',
    '盐城': '101190701',
    '徐州': '101190801',
    '淮安': '101190901',
    '连云港': '101191001',
    '常州': '101191101',
    '泰州': '101191201',
    '宿迁': '101191301',
}


def get_weather(city_name):
    city_code = city_codes.get(city_name)
    weather_info = ""  # 用于收集天气信息的字符串
    if not city_code:
        return f"{city_name} 城市名称不在列表中。\n"

    url = f"http://www.weather.com.cn/weather/{city_code}.shtml"
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        weather_list = soup.find('ul', class_='t clearfix').find_all('li')
        weather_info += f"{city_name}的天气：\n"
        for day_weather in weather_list:
            try:
                date = day_weather.find('h1').text
                weather = day_weather.find('p', class_='wea').text
                temperature = day_weather.find('p', class_='tem').text.strip()
                weather_info += f"  {date}: {weather}, 温度: {temperature}\n"
            except AttributeError:
                continue
        weather_info += "\n"  # 在每个城市的天气信息后添加空行
    else:
        weather_info += f"获取{city_name}的天气信息失败。\n"

    return weather_info


def get_multiple_cities_weather(cities):
    all_cities_weather = ""
    for city in cities:
        all_cities_weather += get_weather(city)
    return all_cities_weather


def send_email(sender_email, sender_password, receiver_email, subject, body):
    smtp_server = "smtp-mail.outlook.com"
    port = 587  # Outlook使用的端口，适用于STARTTLS

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # 启用TLS加密
            server.login(sender_email, sender_password)
            server.send_message(message)
            print("邮件已成功发送！")
    except Exception as e:
        print(f"发送邮件时出错：{e}")


if __name__ == "__main__":
    sender_email = "youjianfasongzhushou@outlook.com"  # 发件人邮箱
    sender_password = "dsC4sUiYVT2eqqzo"  # 发件人邮箱密码
    receiver_email = "2112002539@qq.com"  # 收件人邮箱

    cities = ["沈阳", "上海", "南京", "安庆", "合肥"]  # 需要获取天气信息的城市列表
    weather_info = get_multiple_cities_weather(cities)
    subject = "城市天气报告"

    send_email(sender_email, sender_password, receiver_email, subject, weather_info)
