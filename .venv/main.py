import requests

url = "https://oem-catalog.rossko.ru/api/unit/info?catalogId=GM_OP201809&ssd=%24%2AKwEeMxILWEhYfU1BWX5HOzxxU2RKWnsYSwEDJ1cPSQkWHBMfQUJTHB5XVXlDQ1wjSQRYVWpQDkQIEkZNVx4bHwcOXQgSRkNfFRsTHRgBCFxXQUV_D1dVekhCfkcYE1RtUQlJDxAZRk5XHAEIWw4XCG84JCh8DwYJWg8QCiJLKxxsYmcYFRMaRUlXGhscCVFTdWgGIi5WWWFbQ2QHHFQFOHNtHRkeGlR3BQgTbHtvY2VuZm08PyJieXl_fmRkbwskF19banwcYRppPTdTFBQYGx4dHB5DBQ5BSn9ZQHsYaEZNVx4bHwAAAAB24C7e%24&unitId=638221954&deliveryType=000000001¤cyCode=643&addressGuid=&catalogType=LightWeight&catalogAggregator=Laximo"

headers = {
    "Authorization-Domain": "https://don.rossko.ru",
    "Authorization-Session": "K-nMjOn2LUC2nSy2fLnJPMywn0CwDIDMvVBZ", # ***ВАЖНО:  Этот токен может истечь.***
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://don.rossko.ru/",
    "Origin": "https://don.rossko.ru",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Поднимает исключение, если код ответа не 2xx

    data = response.json()
    print(data)

except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")