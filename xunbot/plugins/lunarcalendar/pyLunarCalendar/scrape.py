# coding=gbk
# coding=UTF-8
# ��������ģ��
# author: cuba3
# github: https://github.com/OPN48/pyLunarCalendar
from .solar24 import zipSolarTermsList
from .tools import not_empty

# �����ȡ�������̨����
def hkweather(year):
    import requests
    url='http://data.weather.gov.hk/gts/time/calendar/text/T'+str(year)+'c.txt'
    r = requests.get(url)
    r.encoding = 'Big5'
    temp=r.text.replace('  ',',').replace(',,',',')
    return temp.split('\n')[3:]
# �������ȡ��������ϴ
def getHkWeather(beginYear=1901,endYear=2100):
    outputDataList=[]
    for year in range(beginYear,endYear+1):
        print('���ڻ�ȡ��Ԫ%i���ʮ�Ľ���' % year)
        tempList=hkweather(year)
        modelList=['date','lunarDate','week','solarTerms']
        yearSolarTermsList=[]
        for line in tempList:
            lineTemp=list(filter(not_empty, line.split(',')))
            dic=dict(zip(modelList,lineTemp))
            try:
                dic['solarTerms']=dic['solarTerms'].strip() or ''
                if dic['solarTerms'].strip():
                    dateTemp = dic['date'].replace('��', '-').replace('��', '-').replace('��', '').split('-')
                    yearSolarTermsList.append(int(dateTemp[2]))
            except:
                pass
        print('��ȡ���' + str(yearSolarTermsList))
        outputDataList.append(zipSolarTermsList(yearSolarTermsList)[0])
    return outputDataList
