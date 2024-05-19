import xlwings as xw
import xlrd
import datetime
#from web_scraper import scraper_main


def convert_date_to_excel_ordinal(dia, mes, ano):
    # Specifying offset value i.e.,
    # the date value for the date of 1900-01-00
    offset = 693594  # Valor da data para 01/01/1900
    current = datetime.datetime(ano, mes, dia)

    n = current.toordinal()
    return (n - offset)

def read_sheet():
    wb = xw.Book("PlanilhaAutomacao.xlsx")
    sheet1 = wb.sheets[0]
    whole_sheet = "A1:CM25"
    #init_date = "01/01/2024"
    #dia = int(init_date[0:2])
    #mes = int(init_date[3:5])
    #ano = int(init_date[6:])
    #ord_init_date = init_date.replace("/", "-")
    #ord_init_date = convert_date_to_excel_ordinal(dia, mes, ano)
    #print(ord_init_date)
    for cell in sheet1.range(whole_sheet):
        if cell.value == "Ticker":
            ticker_loc = cell

    new_range = sheet1.range(ticker_loc).expand()
    return new_range, ticker_loc


def extract_data():
    new_data_raw = read_sheet()[0].value

    # Encontrando os tickers que serão usados como referências
    tickers = []
    for list in new_data_raw:
        tickers.append(list[0])
    tickers.remove('Ticker')

    # Alterando as datas
    i = 0
    header_excel = new_data_raw[0]
    header_normal = new_data_raw[0]
    for item in header_excel:
        if isinstance(item, datetime.datetime):
            header_excel.pop(i)
            item = item.strftime("%m/%d/%Y")
            header_excel.insert(i, item)
        i += 1

    j = 0
    for item in header_normal:
        if isinstance(item, datetime.datetime):
            header_normal.pop(j)
            item = item.strftime("%d/%m/%Y")
            header_normal.insert(j, item)
        j += 1
    return new_data_raw, tickers


def mod_sheet():
    wb = xw.Book("PlanilhaAutomacao.xlsx")
    sheet1 = wb.sheets[0]
    header = extract_data()[0][0]
    ticker_loc = read_sheet()[1]
    #print(len(header))
    #print(len([sheet1.range(ticker_loc).end('right').value]))
    sheet1.range("C4:CK4").value = header
    #print(header)
    #print(sheet1.range("C4:CK4").value)


    #tickers = extract_data()[1]
    # for row in extract_data()[0]:
    #     print(row)
    #data = scraper_main(tickers)

mod_sheet()
#extract_data()