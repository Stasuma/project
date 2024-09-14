#https://sky.pro/media/kak-sozdat-virtualnoe-okruzhenie-python/ - про venv
#https://dev.to/eskabore/pip-freeze-requirementstxt-a-beginners-guide-5e2m - про Pip Freeze > Requirements.txt

#pip install virtualenv
#python3 -m venv myenv, где myenv название пространства
#myenv\Scripts\activate
#pip freeze > requirements.txt
#pip freeze - потом можно проверить пакеты
#import urllib3 - для отключения предупреждений о том, что не проверяются серты


#также в консоли ввести библиотеки
#pip install requests - Чтобы установить пакеты в активированном виртуальном окружении
# pip install countryinfo
# pip install goslate
# pip install googletrans

import requests
from countryinfo import CountryInfo #для использования библиотеки countryinfo (столица + код валюты)
import json
import urllib3 #- для отключения предупреждений о том, что не проверяются серты
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#1 готово Ввод страны, сначала уже введена Japan
#2 готово - По введенной стране - определить столицу
#3 готово - По определенной столице - определить погоду в столице
#4 готово - По орпеделенной столице - определить время в столице
#5 готово - Определить курс валюты введенной страны к рублю
#6 Определить цену чашки кофе в стране


#1 Ввод страны
#country_name = "Japan"
country_name_ru = str(input('Введите название страны на русском, например Япония: '))

#перевод на русский, если использовать country_name_ru
# https://dev.to/kalebu/how-to-do-language-translation-in-python-1ic6
# pip install goslate
import sys

try:
        import goslate
        gs = goslate.Goslate()
        country_name = gs.translate(country_name_ru, 'en')
except :
        sys.exit("Запрос на перевод с русского на английский вернул HTTP Error 429: Too Many Requests")


#print(country_name )


#2 По введенной стране - определить столицу (использовала библиотеку)
#https://habr.com/ru/articles/794540/
#https://github.com/porimol/countryinfo?tab=readme-ov-file#install
find_capital = CountryInfo(country_name)
capital_name = find_capital.capital()
print("Столица:", capital_name)

        
#перевод с анлийского на русский
#pip install googletrans - для пеервода
from googletrans import Translator
# translator = Translator()
# capital_name1= translator.translate(capital_name, src='en', dest='ru')

# print("Столица:", capital_name1.text)




#4 определить время в столице
url_zone = "https://api.ipgeolocation.io/timezone?"
Key = "ea37d5f6fa6c4a69af087f4e7f3ca5ae"
par ={
        "apiKey": Key,
        "location": capital_name
}
re = requests.get(url_zone, verify=False, params=par)

if re.status_code == 200:
        re1 = re.json()
        data2 = re1['time_24']
        print(f'Текущее время:', data2)
else:
        print("Error:", re.status_code)




#5 Определить курс валюты введенной страны к рублю
#from countryinfo import CountryInfo # импорт библиотеки
#country = CountryInfo(country_name)

cur_cer = find_capital.currencies()
cur_cer1 = str(cur_cer)[:-2][-3:]

url_currency = "https://www.cbr-xml-daily.ru/daily_json.js"

resp = requests.get(url_currency, verify=False)
if resp.status_code == 200:
        resp1 = resp.json()
        x = resp1.get("Valute").get(cur_cer1).get('Value')
        print(f'Курс {cur_cer1} к рублю: ', x)
else:
        print("Error:", resp.status_code)





# аэропорт
api_url = 'https://api.api-ninjas.com/v1/airports?name={}'.format(capital_name)
response1 = requests.get(api_url, verify=False, headers={'X-Api-Key': 'PG6s1kO4eqVQsLvdQMRNhzBIhH6gAIP48qldwGyK'})
if response1.status_code == 200:
        response2 = response1.json()
        data1 = response2[0]["name"]
        print(f'Главный аэропорт города - {data1}')
else:
        print("Error:", response1.status_code)
        



#3 погода
try:
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        api_key = "9d106a9374ae63ef0f912185822e0ff3"

        params = {
        "q": capital_name,
        "appid": api_key,
        "units": "metric"
        }

        response = requests.get(base_url,  verify=False, params=params)
        data = response.json()
        temperature = data["main"]["temp"]

        print(f"Температура в {capital_name}: {temperature}  Celsius ")
except:
        print("Error:", response.status_code)







# capital_of_country_url = "http://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/currency"
# capital_of_country_headers = {
# "Authorization": "Token 38a170ed8f9eae2640a217c7a88c22158a9837f3"
# }

# body = { 
#         "query": country_name 
#         }

# response = requests.post(capital_of_country_url, json=body, headers=capital_of_country_headers)
# print(response.json())
