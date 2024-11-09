import PyPDF2
from gensim.models import Word2Vec

def parse_file(file_name):
    with open("tz.pdf", 'rb') as pdffileobj:
        pdfreader = PyPDF2.PdfReader(pdffileobj)

        with open('output.txt', 'w', encoding='utf-8') as txtfile:
            # Проходим по всем страницам PDF
            for page_num in range(len(pdfreader.pages)):
                # Извлекаем текст с каждой страницы
                page = pdfreader.pages[page_num]
                text = page.extract_text()

                if text:
                    txtfile.write(text)
    print("Текст успешно извлечен и сохранён в output.txt")


def get_main_name():
    parse_file("tz.pdf")
    with open('output.txt', 'r', encoding='utf-8') as main_file:
        content = main_file.read()
        content = content.replace('\xa0', ' ')
        # Заменяем переносы строк на пробелы
        content = content.replace('\n', ' ').replace('\r\n', ' ')
        index = content.find("Техническое задание")+len("Техническое задание")
        _index = content.find("1.")
        return (content[index:_index].strip())

def get_presition():
    parse_file("tz.pdf")
    with open('output.txt', 'r', encoding='utf-8') as main_file:
        content = main_file.read()
        content = content.replace('\xa0', ' ')
        # Заменяем переносы строк на пробелы
        content = content.replace('\n', ' ').replace('\r\n', ' ')
        return ("Обеспечение исполнения контракта" in content)

def get_ser_lic():
    parse_file("tz.pdf")
    with open('output.txt', 'r', encoding='utf-8') as main_file:
        content = main_file.read()
        content = content.replace('\xa0', ' ')
        # Заменяем переносы строк на пробелы
        content = content.replace('\n', ' ').replace('\r\n', ' ')
        return ("Наличие сертификатов/лицензий" in content)

def get_max_cost():
    parse_file("tz.pdf")
    with open('output.txt', 'r', encoding='utf-8') as main_file:
        content = main_file.read()
        content = content.replace('\xa0', ' ')
        # Заменяем переносы строк на пробелы
        content = content.replace('\n', ' ').replace('\r\n', ' ')
        index = content.find("Максимальное значение цены контракта") + len("Максимальное значение цены контракта")
        return 0
get_main_name()
print(get_presition())
print(get_ser_lic())

