import time
from datetime import datetime
import pymysql
import requests
from bs4 import BeautifulSoup
import openpyxl
from googletrans import Translator
from datetime import datetime
import connect

line = 2

def trans(TEXT):
    trans= Translator()
    result = trans.translate(TEXT,src="en",dest="ko")
    return result.text

while 1:
    print("START")
    time.sleep(1)

    print("##################################### 이메일 발송을 위한 명단 획득 #######################################")
    connq = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc',
                            charset='utf8')
    curq = connq.cursor()
    sql4 = "SELECT address FROM site_status WHERE no = 1"
    curq.execute(sql4)
    connq.close()

    for r in curq:
        if r[0] == None or r[0].strip() == "":
            address = 'dlz1160@s-oil.com'
        address = r[0]
    print("메일 수신대상 : " + address)
    ######################################################################################################

    connq = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
    curq = connq.cursor()
    sql4 = "SELECT count(status) FROM cve WHERE status = '0'"
    curq.execute(sql4)
    connq.close()

    for r in curq:
        if r[0] > 0:
            print("################CVE 데이터 탐지 ###########################")

            print(
                "################################################## 처리 가능한 데이터가 있음 ##########################################")
            print("###################### log log 처리 가능한 데이터를 얻는다 ########################")
            connq = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
            curq = connq.cursor()
            sql4 = "SELECT address, time  FROM site_status WHERE no = '1'"
            curq.execute(sql4)
            connq.close()

            fromAddress = ""
            fromTime = ""
            fromIp = ""
            fromMail = ""
            fromCount = ""
            fromDateDate = ""

            fromFrom = ""
            fromTo = ""

            for rs in curq:
                fromAddress = rs[0]
                fromTime = rs[1]

            fromTime = fromTime.strip()
            connq = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
            curq = connq.cursor()
            sql4 = "SELECT ip, mail, count, date  FROM log WHERE date = '" + str(fromTime) + "'"
            curq.execute(sql4)
            connq.close()

            for rs in curq:
                fromIp = rs[0]
                fromMail = rs[1]
                fromCount = rs[2]
                fromDateDate = rs[3]

            ######################################################################

            time.sleep(60)
            list = connect.getList(fromIp, fromMail, fromCount, fromDateDate)

            if len(list) >= 1:
                print("DATA IN")
                count = 1
                url = 'https://nvd.nist.gov/vuln/detail/'
                url2 = 'https://translate.google.com/?hl=ko&sl=en&tl=ko&op=translate&text='

                filename = datetime.today().strftime('%Y.%m')+"_CVE_CVSS_List("+datetime.today().strftime('%y%m%d')+")_백데이터.xlsx"
                wb = openpyxl.Workbook()
                sheet = wb.active

                sheet['A1'] = '번호'
                sheet['B1'] = '년월'
                sheet['C1'] = '발표일'
                sheet['D1'] = 'CVE'
                sheet['E1'] = 'CVSS Score'
                sheet['F1'] = '중요도'
                sheet['G1'] = '해당 여부'
                sheet['H1'] = '출처(URL)'
                sheet['I1'] = '내용'
                sheet['J1'] = '비고'

                for i in list:
                    time.sleep(1)
                    response = requests.get(url+i)
                    if response.status_code == 200:
                        if 'Not Found' in response.text:

                            print(str(count) + " " + i + " : " + "Not Found 수동조회 진행")

                            sheet['A' + str(line)] = str(count)
                            sheet['B' + str(line)] = "수동조회 대상"
                            sheet['C' + str(line)] = "수동조회 대상"
                            sheet['D' + str(line)] = i
                            sheet['E' + str(line)] = "수동조회 대상"
                            sheet['F' + str(line)] = "수동조회 대상"
                            sheet['G' + str(line)] = "수동조회 대상"
                            sheet['H' + str(line)] = url + i
                            sheet['I' + str(line)] = "수동조회 대상"
                            sheet['J' + str(line)] = ''
                            continue

                        html = response.text
                        soup = BeautifulSoup(html, 'html.parser')
                        cvss = soup.select_one('a[id="Cvss3NistCalculatorAnchor"]')
                        date = soup.select_one('span[data-testid="vuln-published-on"]')
                        cve = soup.select_one('a[data-testid="vuln-cve-dictionary-entry"]')
                        info = soup.select_one('p[data-testid="vuln-description"]')
                        cvss_text =""
                        try:
                            cvss_text = cvss.get_text()

                        except AttributeError:
                            cvss = soup.select_one('a[id="Cvss3CnaCalculatorAnchor"]')
                            cvss_text = cvss.get_text()

                        tmp = cvss_text.split(" ")
                        score_text = tmp[0]
                        severity_text = tmp[1]
                        date_text = date.get_text()
                        tmp2 = date_text.split("/")
                        mm_text = tmp2[0]
                        dd_text = tmp2[1]
                        yy_text = tmp2[2]
                        cve_text = cve.get_text()
                        info_text = info.get_text()

                        yymm_text = yy_text+"."+mm_text
                        yymmdd_text = yy_text+"."+mm_text+ "." + dd_text

                        infokr_text = trans(info_text)

                        print(str(count) + " " +yymm_text+" "+yymmdd_text + " "+ i + " "+ score_text +  " "+ severity_text + " "+ "O/X" + url + i + " "+infokr_text)

                        sheet['A'+str(line)] = str(count)
                        sheet['B'+str(line)] = yymm_text
                        sheet['C'+str(line)] = yymmdd_text
                        sheet['D'+str(line)] = i
                        sheet['E'+str(line)] = score_text
                        sheet['F'+str(line)] = severity_text
                        sheet['G'+str(line)] = 'O/X'
                        sheet['H'+str(line)] = url + i
                        sheet['I'+str(line)] = infokr_text
                        sheet['J'+str(line)] = ''

                    count += 1
                    line += 1

                wb.save(filename)

                yy=datetime.today().strftime('%y')
                mm=datetime.today().strftime('%m')
                dd=datetime.today().strftime('%d')
                name='보안관제'

                ############################# loglog 메시지 입력 ###############################

                connA = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc',
                                        charset='utf8')
                curA = connA.cursor()
                sqlA = "select MAX(no) from log"
                curA.execute(sqlA)
                connA.close()
                no = 1

                for rs in curA:
                    if rs[0] != None:
                        no = rs[0]

                no + 1
                ############## fromIp, fromMail, fromCount,fromDateDate #####

                nowTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                text = nowTime + " :  CVE 데이터" + str(len(list)) + "건 변환 완료."

                connA = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc',
                                        charset='utf8')
                curA = connA.cursor()
                sqlA = "INSERT INTO LOG (no, text) values ('" + str(no + 1) + "','" + text + "')"
                curA.execute(sqlA)
                connA.commit()
                connA.close()
                #############################################################################################

                connect.sendMail(filename, name, address, yy, mm, dd, count, fromIp, fromMail, fromCount,fromDateDate)

        print("END")