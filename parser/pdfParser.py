import PyPDF2
def parse_file(file_name):
    with open(file_name, 'rb') as pdffileobj:
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


def get_main_name(name):
    with open('output.txt', 'r', encoding='utf-8') as main_file:
        content = main_file.read()
        content = content.replace('\xa0', ' ')
        # Заменяем переносы строк на пробелы
        content = content.replace('\n', ' ').replace('\r\n', ' ')
        return name if name in content else None

print(get_main_name("ГБОУ «ЦСиО «Самбо-70» Москомспорта"))
print(get_main_name("Обеспечения исполнения контракта"))