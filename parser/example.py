from wsparser import WordstatParser
import time


# Задаем URL адрес API Яндекс.Директа
# Адрес песочницы: url ='https://api-sandbox.direct.yandex.ru/v4/json/' 
# Адрес полного доступа: url ='https://api.direct.yandex.ru/v4/json/'
url ='https://api-sandbox.direct.yandex.ru/v4/json/' 
# токен к апи директа
token = 'y0_AgAAAAAbFqcHAAuPJgAAAAEAwoL-AAAh5c-bGthOpLBA6CLu77jz9w5uGA'
# логин моей учетки яндекса
userName = 'Krasnovik1'

minusWords = [
    '-купить', 
    '-дешево',
    '-скачать',
    '-бесплатно',
    '-!что',
    '-!это',
    '-!как',
    '-бесплтно',
    '-бесплатно',
    '-безкоштовно',
    '-!даром',
    '-!free',
    '-!бесплтно',
    '-руками',
    '-самостоятельно',
    '-самодельный',
    '-download',
    '-драйвер',
    '-прошивка',
    '-порно',
    '-порнушка',
    '-вконтакте',
    '-доклад',
    '-porn',
    '-porno',
    '-sex',
    '-форум',
    '-реферат',
    '-статья',
    '-блог',
    '-хитрости',
    '-уловки',
    '-хабр',
    '-хабра',
    '-хабрхабр',
    '-faq',
    '-инструкция',
    '-википедия',
    '-!вики',
    '-!wikipedia',
    '-!wiki',
    '-схема',
    '-состав',
    '-способ',
    '-методы',
    '-технология',
    '-торрент',
    '-торент',
    '-torrent',
    '-torent',
    '-torents',
    '-torrents',
    '-сонник',
    '-приснилось',
    '-прикол',
    '-смешно',
    '-юмор',
    '-анекдот',
    '-эротика',
    '-эротический',
    '-проститутки',
    '-проститутка',
    '-проститутку',
    '-проститутками',
    '-проституток',
    '-проститутке',
    '-девки',
    '-девочки',
    '-девочек',
    '-девочке',
    '-девочками',
    '-тетки',
    '-гей',
    '-геи',
    '-геев',
    '-геями',
    '-геем',
    '-гею',
    '-геям',
    '-голубой',
    '-голубые',
    '-голубому',
    '-голубым',
    '-голубых',
    '-лесби',
    '-лезби',
    '-транс',
    '-трансы',
    '-трансов',
    '-транссексуал',
    '-педофил',
    '-педофилия',
    '-зоофил',
    '-зоофилия',
    '-некрофил',
    '-некрофилия',
    '-инцест',
    '-голые',
    '-голая',
    '-голый',
    '-голой',
    '-голым',
    '-голому',
    '-голым',
    '-голыми',
    '-голых',
    '-голі',
    '-гола',
    '-голий',
    '-голій',
    '-голими',
    '-голих',
    '-оголений',
    '-оголені',
    '-оголена',
    '-топлесс',
    '-топлес',
    '-порно',
    '-порнушка',
    '-порнуха',
    '-порнуху',
    '-порнушку',
    '-порнухой',
    '-порнушкой',
    '-трах',
    '-трахаться',
    '-трахатся',
    '-ебля',
    '-ебли',
    '-ебуться',
    '-ебаться',
    '-ебут',
    '-ебать',
    '-половой',
    '-сношение',
    '-сношаются',
    '-секс',
    '-сексом',
    '-сексуально',
    '-сексуальная',
    '-сексуальный',
    '-сексуальность',
    '-эротика',
    '-эротическая',
    '-эротический',
    '-эротические',
    '-эротическими',
    '-нудисты',
    '-нудист',
    '-нудистами',
    '-нудистов',
    '-нудистам',
    '-ню',
    '-nu',
    '-naked',
    '-6ля',
    '-6лядь',
    '-6лять',
    '-abortion',
    '-adult',
    '-amateur',
    '-anal',
    '-analingus',
    '-aneurysm',
    '-anus',
    '-arousal',
    '-arse',
    '-ass',
    '-asslicking',
    '-attack',
    '-b3ъeб',
    '-bdsm',
    '-bisex',
    '-bisexual',
    '-bitch',
    '-blowjob',
    '-bondage',
    '-bukkаkе',
    '-burial',
    '-bоndаgе',
    '-camgirls',
    '-cancer',
    '-casino',
    '-casket',
    '-cekc',
    '-cekс',
    '-cerebral',
    '-ceкc',
    '-ceкс',
    '-children',
    '-clitoris',
    '-cocaine',
    '-cock',
    '-cocksucker',
    '-condom',
    '-creampie',
    '-cumshot',
    '-cumswap',
    '-cunninglus',
    '-cunt',
    '-cеkc',
    '-cеkс',
    '-cекc',
    '-cекс',
    '-deceased',
    '-deepthroat',
    '-demise',
    '-desanguinated',
    '-dies',
    '-dildo',
    '-disfigured',
    '-doggystyle',
    '-dosug',
    '-drown',
    '-drowned',
    '-drugs',
    '-dying',
    '-ebal',
    '-eblan',
    '-electrocuted',
    '-electrocution',
    '-embolism',
    '-erection',
    '-erotic',
    '-erotico',
    '-escorts',
    '-eskort',
    '-etoile',
    '-execution',
    '-exhibitionism',
    '-exhibitionist',
    '-expire',
    '-eбaл',
    '-eбaть',
    '-eбать',
    '-eблантий',
    '-eбёт',
    '-facial',
    '-fellatio',
    '-fetish',
    '-fuck',
    '-funeral',
    '-gambling',
    '-gangbang',
    '-gay',
    '-gays',
    '-generic',
    '-gjhyj',
    '-gonzo',
    '-groupsex',
    '-hairy',
    '-handjob',
    '-hardcore',
    '-hedonist',
    '-hemorrhage',
    '-heroin',
    '-homosexual',
    '-horror',
    '-incarcerated',
    '-jail',
    '-johnson',
    '-juego',
    '-kill',
    '-killed',
    '-killer',
    '-latex',
    '-lesbi',
    '-lesbian',
    '-lesbians',
    '-lesbo',
    '-levaquin',
    '-levitra',
    '-licking',
    '-livesex',
    '-maimed',
    '-manslaughter',
    '-marijuana',
    '-masochism',
    '-masturbation',
    '-mature',
    '-medication',
    '-miscarriage',
    '-morphine',
    '-murder',
    '-murdered',
    '-murderer',
    '-naked',
    '-nude',
    '-orgy',
    '-overdose',
    '-oxycodone',
    '-oxycontin',
    '-panties',
    '-pantyhose',
    '-paralyzed',
    '-pedophile',
    '-pedophilia',
    '-penetration',
    '-penis',
    '-penthouse',
    '-perished',
    '-pharmaceutical',
    '-pharmacy',
    '-pissing',
    '-planker',
    '-playboy',
    '-plonker',
    '-poisoned',
    '-poisoning',
    '-poker',
    '-pom',
    '-pov',
    '-porn',
    '-porno',
    '-pornographic',
    '-pornstars',
    '-prison',
    '-prostitutk',
    '-pussy',
    '-sadism',
    '-sadomasochism',
    '-schlong',
    '-schoolgirl',
    '-sdilong',
    '-sex',
    '-sexual',
    '-sexuality',
    '-sexually',
    '-пися'
    ]


phrases = [
    'мачалка',
    'для ванны'
    ]


geo = [225]


# Код скрипта парсинга

data = []
for i in range(len(phrases)):
    data.append(phrases[i])
    for j in range(len(minusWords)):
        data[i] += ' '+minusWords[j]


parser = WordstatParser(url, token, userName)

try:

    units = parser.getClientUnits()
    if 'data' in units:
        print ('>>> Баллов осталось: ', units['data'][0]['UnitsRest'])
    else:
        raise Exception('Не удалось получить баллы', units)


    response = parser.createReport(data, geo)
    if 'data' in response:
        reportID = response['data']
        print('>>> Создается отчет с ID = ', reportID)
    else:
        raise Exception('Не удалось создать отчет', response)

    reportList = parser.getReportList()
    if 'data' in reportList:
        lastReport = reportList['data'][len(reportList['data'])-1]
        i = 0
        while lastReport['StatusReport'] != 'Done':
            print ('>>> Подготовка отчета, ждите ... ('+str(i)+')')
            time.sleep(2)
            reportList = parser.getReportList()
            lastReport = reportList['data'][len(reportList['data'])-1]
            i+=1
        print ('>>> Отчет ID = ', lastReport['ReportID'], ' получен!')
    else:
        raise Exception('Не удалось прочитать список отчетов', reportList)


    report = parser.readReport(reportID)
    if 'data' in report:

        parser.saveReportToTxt(report, True)
        print ('>>> Результаты парсига успешно сохранены в файлы!')
    else:
        raise Exception('Не удалось прочитать отчет', report)

    report = parser.deleteReport(reportID)
    if 'data' in report:
        print ('>>> Отчет с ID = ', reportID, ' успешно удален с сервера Яндекс.Директ')
    else:
        raise Exception('Не удалось удалить отчет', report)
    
    print ('>>> Все готово!')

except Exception as e:
    print ('>>> Поймано исключение:', e)