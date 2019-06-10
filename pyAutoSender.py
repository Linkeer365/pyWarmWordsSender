import datetime
import requests
import locale
import json
import itchat

'''请修改 
1. 第20行的beginning_date, 换成在一起的第一天
2. 第26行的province和city, 换成你所在的省份和城市
2. 第73行的to_username, 换成发送对象的(用户名/昵称)都可以'''



# get curr date-time
lines=[]
locale.setlocale(locale.LC_CTYPE,'chinese')
present_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

# get duration days

beginning_date=datetime.date(1972,4,20)
now_date=datetime.date.today()
duration=now_date-beginning_date
duration_days=duration.days

# get weather
weather_url='https://wis.qq.com/weather/common?' # api_url
headers={'Referer': 'https://tianqi.qq.com/','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
queryParams={'source':'pc','weather_type':'forecast_24h|air|observe|tips','province':'广东省','city':'深圳市'} # 传参到weather_type里面, 可以访问不同的fields
resp=requests.get(url=weather_url,headers=headers,params=queryParams)
air=resp.json()['data']['air']['aqi']
temps=resp.json()['data']['forecast_24h']
wind_direction_code=resp.json()['data']['observe']['wind_direction'] 
wind_power=resp.json()['data']['observe']['wind_power']+'级'
max_temp=str(max([int(temps[each]['max_degree']) for each in temps if each.isdigit()]))
min_temp=str(min([int(temps[each]['min_degree']) for each in temps if each.isdigit()]))
codes_directions=('北风','东北风','东风','东南风','南风','西南风','西风','西北风')
wind_direction=codes_directions[int(wind_direction_code)]
tip=resp.json()['data']['tips']['observe']['0']

# format weathers

weathers=dict(温度='/'.join([min_temp,max_temp]),空气='{0:.1f}'.format(air))
weathers[wind_direction]=wind_power

# get sweet template

sweet_template_part1='宝贝这是我们在一起的第{}天。\n{}'.format(duration_days,tip)
sweet_template_part2='来自最爱你的我。'

# get one-line quote
quote_url='http://sentence.iciba.com/index.php?'
headers={'Referer': 'http://news.iciba.com/views/dailysentence/daily.html','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
queryParams={'c':'dailysentence','m':'getTodaySentence'}
resp=requests.get(url=quote_url,headers=headers,params=queryParams)
Eng_quote=resp.json()['content']
Chi_quote=resp.json()['note']

# get msg_feed

weather_strs=['{}:{}'.format(key,value) for key,value in weathers.items()]
msg_feed=[present_time,sweet_template_part1]
msg_feed.extend(weather_strs)
msg_feed.append(Eng_quote)
msg_feed.append(Chi_quote)
msg_feed.append(sweet_template_part2)

# get final msg

final_msg='\n'.join(msg_feed)
print(final_msg)

# itchat send msg


to_username='Mr.云景'
itchat.auto_login(hotReload=True)
itchat.send(msg=final_msg,toUserName='filehelper')
