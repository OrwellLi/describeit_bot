from wsparser import WordstatParser
import time
from user_info import url, token, userName, geo
from minus_words import minusWords


def keywords(request: str, left_column_length :int, right_column_lenght: int):

    # phrases = [
    #     'мачалка',
    #     'для ванны'
    #     ]

    phrases = [request]

    data = []
    for i in range(len(phrases)):
        data.append(phrases[i])
        for j in range(len(minusWords)):
            data[i] += ' ' + minusWords[j]


    parser = WordstatParser(url, token, userName)

    try:

        units = parser.getClientUnits()
        if 'data' in units:
            print('>>> Баллов осталось: ', units['data'][0]['UnitsRest'])
        else:
            raise Exception('Не удалось получить баллы', units)

        response = parser.createReport(data, geo)

        if 'data' in response:
            reportID = response['data']
            print('>>> Создается отчет с ID = ', reportID)
        else:
            # raise Exception('Не удалось создать отчет', response)
            return (), ()

        reportList = parser.getReportList()
        if 'data' in reportList:
            lastReport = reportList['data'][len(reportList['data'])-1]
            i = 0
            while lastReport['StatusReport'] != 'Done':
                print('>>> Подготовка отчета, ждите ... (' + str(i) + ')')
                time.sleep(2)
                reportList = parser.getReportList()
                lastReport = reportList['data'][len(reportList['data'])-1]
                i += 1
            print('>>> Отчет ID = ', lastReport['ReportID'], ' получен!')
        else:
            raise Exception('Не удалось прочитать список отчетов', reportList)


        report = parser.readReport(reportID)

        if 'data' in report:
            print('>>> Результаты парсига успешно сохранены в файлы!')
            right, left = parser.saveReportToTxt(report, True)
            return right[:right_column_lenght], left[1: left_column_length + 1]

        else:
            # raise Exception('Не удалось прочитать отчет', report)
            return (), ()

        report = parser.deleteReport(reportID)
        if 'data' in report:
            print('>>> Отчет с ID = ', reportID, ' успешно удален с сервера Яндекс.Директ')
        else:
            raise Exception('Не удалось удалить отчет', report)

        print('>>> Все готово!')

    except Exception as e:
        print('>>> Поймано исключение:', e)

