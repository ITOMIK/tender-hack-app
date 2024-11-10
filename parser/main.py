from  gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
from pdfParser import get_main_name, get_presition, get_ser_lic, get_addres
from tableparser import parse_pdf_tocsv
import csv
import re
# Правильные значения для проверки, хранящиеся в переменной card

def compare_addresses(addr1, addr2):
    if addr1 == None or addr2 ==None:
        return False
    # Define regular expression patterns for address components
    street_pattern = r"(?:ул\.?|улица)\s+([а-яА-Я]+)"
    house_pattern = r"(д\.?|дом)\s+(\d+)"
    city_pattern = r"(г\.?|город)\s+([а-яА-Я]+)"
    postal_code_pattern = r"(\d+)"
    addr2=addr2.replace("г г","г. ")
    addr1=addr1.replace("г г","г. ")
    # Compile the patterns
    street_regex = re.compile(street_pattern)
    house_regex = re.compile(house_pattern)
    city_regex = re.compile(city_pattern)
    postal_code_regex = re.compile(postal_code_pattern)

    # Extract address components from addr1 and addr2
    addr1_street = street_regex.search(addr1)
    addr1_house = house_regex.search(addr1)
    addr1_city = city_regex.search(addr1)
    addr1_postal_code = postal_code_regex.search(addr1)

    addr2_street = street_regex.search(addr2)
    addr2_house = house_regex.search(addr2)
    addr2_city = city_regex.search(addr2)
    addr2_postal_code = postal_code_regex.search(addr2)

    if (addr1_street and addr2_street and addr1_street.group(1) == addr2_street.group(1)) and \
       (addr1_house and addr2_house and addr1_house.group(2) == addr2_house.group(2)) and \
       (addr1_city and addr2_city and addr1_city.group(2) == addr2_city.group(2)):
        return True
    else:
        return False

file_name="tz2.pdf"

def parse_csv_to_object():
    a= parse_pdf_tocsv(file_name)
    res= []
    with open(a[0], 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            q = row.get("Наименование \nтовара") 
            if q==None:
                q= row.get("Наименование")
            res.append(q.replace("\n"," "))
        return res

card = {
    "name": get_main_name(file_name),
    "isContractGuaranteeRequired": get_presition(file_name),
    "licenseFiles": get_ser_lic(file_name),
    "delivery_place": get_addres(file_name),
    "startCost": 1364.0,
    "spec":parse_csv_to_object()
}



def sentence_similarity(sentence1, sentence2):
    # Токенизируем предложения и приводим к нижнему регистру
    tokens1 = sentence1.lower().split()
    tokens2 = sentence2.lower().split()

    # Создаем корпус из двух предложений для обучения модели Word2Vec
    sentences = [tokens1, tokens2]

    # Создаем и обучаем модель Word2Vec на текущем корпусе
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)

    # Функция для вычисления среднего вектора предложения
    def sentence_vector(tokens):
        vectors = [model.wv[word] for word in tokens if word in model.wv]
        if vectors:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(model.vector_size)

    # Получаем усредненные векторы для каждого предложения
    vec1 = sentence_vector(tokens1)
    vec2 = sentence_vector(tokens2)

    # Вычисляем косинусное сходство между векторами предложений
    similarity = cosine_similarity([vec1], [vec2])[0][0]
    return similarity


# Функция для проверки значений в data с эталоном из card
def check_data_with_card(data, card):
    results = {}
    # 1. Проверка наименования закупки
    results['Наименование закупки'] = sentence_similarity(data.get('name'),card["name"]) >0.50

    # 2. Обеспечение исполнения контракта
    results['Обеспечение контракта'] = data.get("isContractGuaranteeRequired") == card["isContractGuaranteeRequired"]


    # 3. Наличие сертификатов/лицензий
    results['Сертификаты/лицензии'] = data.get("licenseFiles") == card["licenseFiles"]


    # 4. График поставки
    delivery = data.get("deliveries", [{}])[0]
    results['Место Поставки'] = compare_addresses(delivery.get("deliveryPlace"),card['delivery_place'])

    # 5. Начальная цена
    #results['Начальная цена'] = data.get("startCost") == card['startCost']

    # 6. Наличие и корректность технического задания

    # 7. Сравнение спецификации
    count = 0
    lOne = [item['name'] for item in data['items'] if item != ""]
    lTwo = [item for item in card["spec"] if item != ""]
    lOne.sort()
    lTwo.sort()
    results['спецификация']=lOne==lTwo
            
    return results

# Запрос к API и проверка
url = "https://zakupki.mos.ru/newapi/api/Auction/Get"
params = {"auctionId": 9862366}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    # Сравнение значений
    results = check_data_with_card(data, card)
    # Вывод результатов проверки
    for requirement, passed in results.items():
        status = "соответствует" if passed else "не соответствует"
        print(f"{requirement}: {status}")
else:
    print(f"Failed to retrieve data: {response.status_code}")
