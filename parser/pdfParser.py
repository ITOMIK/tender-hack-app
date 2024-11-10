import PyPDF2
import re

file_status = {"parsed":False}
def parse_file(file_name):
    with open(file_name, 'rb') as pdffileobj:
        pdfreader = PyPDF2.PdfReader(pdffileobj)

        with open('output.txt', 'w', encoding='utf-8') as txtfile:
            for page_num in range(len(pdfreader.pages)):
                page = pdfreader.pages[page_num]
                text = page.extract_text()

                if text:
                    txtfile.write(text)
    print("Текст успешно извлечен и сохранён в output.txt")
    file_status["parsed"]=True


def get_info_from_txt(func):
    def wrapper(file_name):
        if not file_status["parsed"]:
            parse_file(file_name)

        with open('output.txt', 'r', encoding='utf-8') as main_file:
            content = main_file.read()
            content = content.replace('\xa0', ' ')
            content = content.replace('\n', ' ').replace('\r\n', ' ')
            return func(content)

    return wrapper


@get_info_from_txt
def get_main_name(content):
    left_index = content.find("Техническое задание") + len("Техническое задание")
    right_index = content.find("1.")
    return content[left_index:right_index].strip()


@get_info_from_txt
def get_presition(content):
    return "Обеспечение исполнения контракта" in content


@get_info_from_txt
def get_ser_lic(content):
    if "Наличие сертификатов/лицензий" in content:
        return ["pizda", "penis"]
    else:
        return []


@get_info_from_txt
def get_max_cost(content):
    index = content.find("Максимальное значение цены контракта") + len("Максимальное значение цены контракта")
    if index != -1:
        cost = content[index:index + 100].split()[0]
        return cost
    return None


@get_info_from_txt
def get_addres(content):
    pattern = r'г\.\s*[А-Яа-яёЁ]+\s*ул\.\s*[А-Яа-яёЁ]+\s*[А-Яа-яёЁ]*,\s*д\.\s*\d+[А-Яа-яёЁ]*'

    addresses = re.findall(pattern, content)
    if len(addresses) >= 1:
        return addresses[0]
    return None
