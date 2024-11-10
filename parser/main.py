from  gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
from pdfParser import get_main_name, get_presition, get_ser_lic, get_addres
from tableparser import parse_pdf_tocsv
import csv
# Правильные значения для проверки, хранящиеся в переменной card

file_name="tz.pdf"

def parse_csv_to_object():
    a= parse_pdf_tocsv(file_name)
    res= []
    with open(a[0], 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            res.append(row.get("Наименование \nтовара").replace("\n"," "))
        return res

card = {
    "name": get_main_name(file_name),
    "isContractGuaranteeRequired": get_presition(file_name),
    "licenseFiles": get_ser_lic(file_name),
    "delivery_period_from": 1,
    "delivery_period_to": 10,
    "delivery_place": get_addres(file_name),
    "startCost": 1364.0,
    "tech_spec_file": "техническое задание шпагат.docx",
    "contract_file": "Проект контракта.pdf",
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
    results['Наименование закупки'] = sentence_similarity(data.get('name'),card["name"]) >0.15

    # 2. Обеспечение исполнения контракта
    results['Обеспечение контракта'] = data.get("isContractGuaranteeRequired") == card["isContractGuaranteeRequired"]


    # 3. Наличие сертификатов/лицензий
    results['Сертификаты/лицензии'] = data.get("licenseFiles") == card["licenseFiles"]


    # 4. График поставки
    delivery = data.get("deliveries", [{}])[0]
    results['График поставки'] = (
        delivery.get("periodDaysFrom") == card['delivery_period_from'] and
        delivery.get("periodDaysTo") == card['delivery_period_to'] and
        delivery.get("deliveryPlace") == card['delivery_place']
    )

    # 5. Начальная цена
    results['Начальная цена'] = data.get("startCost") == card['startCost']

    # 6. Наличие и корректность технического задания
    tech_spec_files = [file.get("name") for file in data.get("files", [])]
    results['Техническое задание'] = card['tech_spec_file'] in tech_spec_files
    results['Проект контракта'] = card['contract_file'] in tech_spec_files

    # 7. Сравнение спецификации
    count = 0
    results['спецификация']=card["spec"].sort()==[item['name'] for item in data['items']].sort()
            
    return results

# Запрос к API и проверка
url = "https://zakupki.mos.ru/newapi/api/Auction/Get"
params = {"auctionId": 9864533}

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
