
import time
import openpyxl as openpyxl
import pymysql
import os
import smtplib
from datetime import datetime
from email import encoders
from email.utils import formataddr
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

countzero = 0
asdfasdf = []

def virusTotal(i, types, jobip, jobdate):
    # virusTotal(sha256, "sha256", jobip, jobdate)
    # virusTotal(sha1, "sha1", jobip, jobdate)

    conn = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
    cur = conn.cursor()
    sql2 = "SELECT no, md5, sha1, sha256 from work_place WHERE " + types + " = '" + str(i) + "' AND ipip ='" + str(
        jobip) + "' AND time = '" + str(jobdate) + "'"
    cur.execute(sql2)
    conn.commit()
    conn.close()

    for a in cur:
        a[1] != 'X'
        print("기존데이터 md5 탐지 : "+a[1])
        continue

    time.sleep(15)
    try:
        url = 'https://www.virustotal.com/vtapi/v2/file/report'
        params = {'apikey': '645c62843256a387939a6ab31b55f4e9a409971cdfe488d78b97881443289e6a', 'resource': i}
        response = requests.get(url, params=params)

        out = response.json()

        if out['md5'] != None:
            setup1Virustotal(out['md5'], i, types, jobip, jobdate)
            sitecountUp(1)
            return out['md5']

    except KeyError:
        print(
            "############################### 데이터 정상조회 실패 시에러처리 ######################################################")
        print("sha1List KeyError :" + i)
        setup1Virustotal("변환실패", i, types, jobip, jobdate)
        sitecountUp(1)



def setup1Virustotal(result, input, types, jobip, jobdate):
    # virusTotal(sha256, "sha256", jobip, jobdate)
    # virusTotal(sha1, "sha1", jobip, jobdate)

    #  setup1Virustotal(out['md5'], i, types, jobip, jobdate)
    #  setup1Virustotal("변환실패", i, types, jobip, jobdate)

    conn = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
    cur = conn.cursor()
    sql2 = "UPDATE work_place SET md5 = '" + str(result) +"' WHERE " + types + " = '" + str(input) + "' AND ipip ='" + str(
        jobip) + "' AND time = '" + str(jobdate) + "'"
    cur.execute(sql2)
    conn.commit()

    sql2 = "UPDATE work_place SET status= 1 WHERE " + types + " = '" + str(input) + "' AND ipip ='" + str(
        jobip) + "' AND time = '" + str(jobdate) + "'"
    cur.execute(sql2)
    conn.commit()
    conn.close()

def setup1(list, type, jobip, jobdate):
    # setup1(md5, "md5", jobip, jobdate)
    #setup1(md5, "md5", jobip, jobdate)

    # md5 변환 완료 (status 0 > 1)
    connq = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
    curq = connq.cursor()
    for i in list:
        sql4 = "UPDATE work_place SET status = '1' WHERE "+type+" = '" + i + "' AND ipip = '" + str(jobip) + "' AND time = '" + str(jobdate) + "'"
        print(sql4)
        curq.execute(sql4)
        connq.commit()
    connq.close()

def setup2(list, type, jobip, jobdate):
    # setup1(md5, "md5", jobip, jobdate)
    #setup1(md5, "md5", jobip, jobdate)

    # md5 변환 완료 (status 0 > 1)
    connq = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
    curq = connq.cursor()
    for i in list:
        sql4 = "UPDATE work_place SET status = '2' WHERE "+type+" = '" + i + "' AND ipip = '" + str(jobip) + "' AND time = '" + str(jobdate) + "' AND status = '1'"
        print(sql4)
        curq.execute(sql4)
        connq.commit()
    connq.close()

def setup3(list, type, jobip, jobdate):
    # setup1(md5, "md5", jobip, jobdate)
    #setup1(md5, "md5", jobip, jobdate)

    # md5 변환 완료 (status 0 > 1)
    connq = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
    curq = connq.cursor()
    for i in list:
        sql4 = "UPDATE work_place SET status = '3' WHERE "+type+" = '" + i + "' AND ipip = '" + str(jobip) + "' AND time = '" + str(jobdate) + "' AND status = '2'"
        print(sql4)
        curq.execute(sql4)
        connq.commit()
    connq.close()


def sitecountUp(num):

    conn7 = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
    cur7 = conn7.cursor()

    sql7 = "SELECT count FROM site_status where no = 1"
    cur7.execute(sql7)

    for a in cur7:
        count = a[0]
        if a[0] is None:
            count = 0

    out = 0
    out = count + num

    sql4 = "UPDATE site_status SET count =" + str(out) + " where no = 1"
    cur7.execute(sql4)
    conn7.commit()
    conn7.close()

def loglog(logText):
    connA = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
    curA = connA.cursor()
    sqlA = "select MAX(no) from log"
    curA.execute(sqlA)
    connA.close()

    no = 1
    for rs in curA:
        if rs[0] != None and no > 0:
            no = rs[0]
        else:
            no = 1

    nowTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    connA = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
    curA = connA.cursor()
    sqlA = "INSERT INTO LOG (no, text) values ('" + str(no + 1) + "','" + nowTime+" : " + logText + "')"
    curA.execute(sqlA)
    connA.commit()
    connA.close()



def getList(jobno, jobip, jobdate, jobfilename):
    print("################ IOC 데이터 GET ###########################")
    value = 0
    x = 1
    md5 = []
    sha256 = []
    md5 = []
    sha1 = []
    ip1 = []
    url1 = []

    print("######################## 입력된 데이터 md5, sha1, sha256, ip ,url 획득 ##########################################")
    connq = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
    curq = connq.cursor()
    sqlq = "SELECT md5, sha1, sha256, ip, url ,  no FROM work_place WHERE status = '0' AND ipip = '" + str(jobip) + "' AND time = '" + str(jobdate) + "'"
    curq.execute(sqlq)
    curq.close()

    for row in curq:
        if (row[0] is None or row[0] == ""):
            return 0

        if row[0] != 'X':
            md5.append(row[0])

        if row[1] != 'X':
            sha1.append(row[1])

        if row[2] != 'X':
            sha256.append(row[2])

        if row[3] != 'X':
            a = row[3]
            a = a.replace("[.]",".")
            print("replace [.] > . "+a)
            ip1.append(a)

        if row[4] != 'X':
            a = row[4]
            a = a.replace("hxxp", "http")
            a = a.replace("[.]",".")
            print("replace hxxp [.]> http ."+ a)
            url1.append(a)

    md5Text = ""
    sha1Text = ""
    sha256Text = ""
    ipText  = ""
    urlText = ""

    if len(md5) > 0:
        md5Text = "[md5: " + str(len(md5)) + "] "
    if len(sha1) > 0:
        sha1Text = "[sha1: " + str(len(sha1))  + "] "
    if len(sha256) > 0:
        sha256Text = "[sha256: " + str(len(sha256))+ "] "
    if len(ip1) > 0:
        ipText = "[ip: " + str(len(ip1)) + "] "
    if len(url1) > 0:
        urlText = "[url: " + str(len(url1)) + "] "

    total = []
    total = md5 + sha1 + sha256 + ip1 + url1
    total2  = len(total)


    # 작업번호 [41] 총 [4]개 데이터 처리진행 [md5: 1] [sha1: 1] [sha256: 1] [ip: 1]
    logText = "작업[" + str(jobno) + "] 총 [" + str(total2) + "]개 데이터 등록 " + md5Text +sha1Text + sha256Text + ipText + urlText
    loglog(logText)
    print(logText)
    # 데이터 처리 수 추가

    sitecountUp(total2)

    ###################################################################################################################
    md5List = []
    ipList = []
    urlList = []
    sha256List = []
    sha1List = []

    # sha1, sha256 변환 시작
    if len(md5)> 0:
        for i in md5:
            md5List.append(i)
        print("out md5 " + str(md5List))

    if len(ip1) > 0:
        for i in ip1:
            ipList.append(i)
        print("out ip1 " + str(ipList))

    if len(url1) > 0:
        for i in url1:
            urlList.append(i)
        print("out url1 " + str(urlList))

    if len(sha256) > 0 :
        for i in sha256:
            out = virusTotal(i, "sha256", jobip, jobdate)
            sha256List.append(out)
            print("out sha256 " + str(out))

    if len(sha1) > 0 :
        for i in sha1:
            out2 = virusTotal(i, "sha1", jobip, jobdate)

            sha1List.append(out2)
            print("out sha1 " + str(out2))

    # 변환 완료 (status 0 > 1)
    setup1(md5, "md5", jobip, jobdate)
    setup1(ip1, "ip", jobip, jobdate)
    setup1(url1, "url", jobip, jobdate)

    input = md5 + sha256 + sha1 + ip1 + url1


    output = md5List + sha256List + sha1List + ipList + urlList


    print("output" + str(output))

    md5Text2 = ""
    sha1Text2 = ""
    sha256Text2 = ""
    ipText2 = ""
    urlText2 = ""

    if len(md5List) > 0 :
        md5Text2 = "[md5: " +str(len(md5List))+"/"+ str(len(md5)) + "] "
    if len(sha1List) > 0:
        sha1Text2 = "[sha1: " +str(len(sha1List))+"/"+ str(len(sha1)) + "] "
    if len(sha256List) > 0:
        sha256Text2 = "[sha256: " + str(len(sha256List))+"/"+ str(len(sha256))+"] "
    if len(ipList) > 0:
        ipText2 = "[ip: " + str(len(ipList)) + "/" + str(len(ip1)) + "] "
    if len(urlList) > 0:
        urlText2 = "[url: " + str(len(urlList)) + "/" + str(len(url1)) + "] "

    sum1 = len(output)
    sum2 = len(input)
    sumoutput = str(sum1)
    suminput = str(sum2)

    print("sumoutput " + str(sumoutput))
    print("suminput " + str( suminput))

    logText = "작업["+str(jobno)+ "] 총 [" + sumoutput +"/" + suminput + "]개 데이터 변환완료 "+md5Text2+sha1Text2+sha256Text2+ipText2+urlText2
    print(logText)
    loglog(logText)

    filename =""
    filename2 = ""

    ################################################################################################################

    print("output ######"+str(output))
    if len(output) > 0:
        sumr = []
        sumr = output
        filename2 = writeHX(sumr, jobno, jobfilename)


        outout = []
        for i in output:
           if i == "변환실패" or i is None:
               continue
           else:
               outout.append(i)

        logText = "작업["+str(jobno)+ "] 총 [" + str(len(outout))+ "/" +  str(len(input))  + "]개 데이터 HX 파일 생성 완료 "+md5Text+sha1Text+sha256Text+ipText+urlText
        print(logText)
        loglog(logText)
    else:
        filename2 = 0

        ################################################################################################################
    if len(output) > 0 :
        filename = writeExcel(jobip, jobdate, jobno)
        # 작업번호 [41] 총 [6/4]개 데이터 EXCEL 데이터 작성 완료 [md5: 1/1] [sha1: 2/1] [sha256: 2/1] [ip: 1/1]
        logText = "작업[" + str(
            jobno) + "] 총 [" + suminput + "/" + suminput + "]개 데이터 엑셀 작성 " + md5Text + sha1Text + sha256Text + ipText + urlText
        print(logText)
        loglog(logText)

    sendMail(filename, filename2, jobno, jobip, jobdate, len(output), total2)

    return 1




def sendMail(filename, filename2,jobno, jobip, jobdate, num1, num3):
    print(
        "############################################## 메일 보내기 ##########################################################")

    name = '보안관제'

    conn = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT no, email FROM jobq WHERE ipip = '"+str(jobip)+"' AND time = '"+str(jobdate)+"'"
    cur.execute(sql)
    conn.commit()
    conn.close()

    address = ""
    for a in cur :
        address = a[1]

    realname =  mailCheck(address)


    yy = datetime.today().strftime('%y')
    mm = datetime.today().strftime('%m')
    dd = datetime.today().strftime('%d')

    ################ 이메일 카운트 증가 ##################
    conn = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT mailcount FROM site_status"
    cur.execute(sql)
    # 여러 줄 출력
    i = 0


    for row in cur:
        value = row[0]

    if value is None:
        value = 0

    sql2 = "UPDATE site_status SET mailcount = " + str(value + 1)
    cur.execute(sql2)
    conn.commit()
    conn.close()
    ###############################################################
    from_addr = formataddr(('업무도우미', 'bh.lee@s-oil.com'))

    # 받는사람
    to_addr = formataddr((name, address))

    session = None
    try:
        # SMTP 세션 생성
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.set_debuglevel(True)

        # SMTP 계정 인증 설정
        session.ehlo()
        session.starttls()
        session.login('igloosoil@gmail.com', 'lougwydyuijffjcd')

        # 메일 콘텐츠 설정
        message = MIMEMultipart("mixed")

        total = num1
        ex = num3-num1
        # 메일 송/수신 옵션 설정
        message.set_charset('utf-8')
        message['From'] = from_addr
        message['To'] = to_addr
        message['Subject'] = "[보안관제] HX 정보등록 데이터_작업[" + str(jobno)+"] "+str(num3) + "건"

        # 메일 콘텐츠 - 내용
        body = " <h4>안녕하세요업무도우미입니다. </h4>  </br><h4><h4>솔루션 주소 : http://222.110.22.168:8080/ioc/main.jsp </h4> <h4> 수행작업 : HX 파일 및 결과보고서 생성</h4> </br></br> 요청 건수(" + str(
            num3) + ")</br> 변환 건수[" + str(total) + "] 제외 건수[" + str(ex) + "]</br> </br> 자세한 사항은 첨부파일을 참조해주세요</br> <h4>HX TOOL에 접속하여 업로드 해주세요(URL : \"https://192.168.36.182:8080/login\"</h4>"

        bodyPart = MIMEText(body, 'html', 'utf-8')
        message.attach(bodyPart)

        # 메일 콘텐츠 - 첨부파일

        if filename2 == 0 :
            attachments = [os.path.join(os.getcwd(), filename)]
        else:
            attachments = [os.path.join(os.getcwd(), filename), os.path.join(os.getcwd(), filename2)]

        for attachment in attachments:
            attach_binary = MIMEBase("application", "octect-stream")
            try:
                binary = open(attachment, "rb").read()  # read file to bytes

                attach_binary.set_payload(binary)
                encoders.encode_base64(attach_binary)  # Content-Transfer-Encoding: base64

                filename = os.path.basename(attachment)
                attach_binary.add_header("Content-Disposition", 'attachment', filename=('utf-8', '', filename))

                message.attach(attach_binary)
            except Exception as e:
                print(e)

        # 메일 발송
        session.sendmail(from_addr, to_addr, message.as_string())

        print('Successfully sent the mail!!!')

        logText = "작업["+str(jobno)+"] IOC 결과 메일 발송 완료(수신:"+realname+")"
        print(logText)
        loglog(logText)

    except Exception as e:
        print(e)
    finally:
        if session is not None:
            session.quit()

    #################################################################################################################

def mailCheck(address):
    realname = ""
    if address == "DLZ1160@s-oil.com":
        realname = "보안관제팀"
    if address == "sungwoo.kwon@s-oil.com":
        realname = "부장님"
    if address == "jsh0119@s-oil.com":
        realname = "승환"
    if address == "kmh0816@s-oil.com":
        realname = "명훈"
    if address == "bh.lee@s-oil.com":
        realname = "병호"
    if address == "ksm0117@s-oil.com":
        realname = "성민"
    if address == "lyj0409@s-oil.com":
        realname = "예지"
    if address == "khw1205@s-oil.com":
        realname = "형욱"

    return realname


def findHX(value):

    print("value: " + str(value))
    # eoperator = ""
    # etoken =""
    # etype = ""
    # poperator = ""
    # ptoken =""
    # ptype = ""

    if value is None:
        return
    i = value
    tmp = i
    tmp2 = tmp.replace(".","")

    findHXout = []

    if "." in i and tmp2.isdigit():
        eoperator = "equal"
        etoken = "ipv4NetworkEvent/remoteIP"
        etype = "text"
        poperator = "equal"
        ptoken = "ipv4NetworkEvent/remoteIP"
        ptype = "text"
        findHXout = [eoperator , etoken, etype , poperator,ptoken,ptype]
        print("findHXout IP" + str(findHXout))
        return findHXout

    elif "." in i:
        T = "URL"
        eoperator = "equal"
        etoken = "dnsLookupEvent/hostname"
        etype = "text"
        poperator = "equal"
        ptoken = "urlMonitorEvent/hostname"
        ptype = "text"
        findHXout.append(eoperator)
        findHXout.append(etoken)
        findHXout.append(etype)
        findHXout.append(poperator)
        findHXout.append(ptoken)
        findHXout.append(ptype)
        findHXout = [eoperator , etoken, etype , poperator,ptoken,ptype]
        print("findHXout URL " + str(findHXout))
        return findHXout


    if "." not in i and ":" not in i and "/" not in i and len(i) == 32:
        T = "MD5"
        eoperator = "equal"
        etoken = "processEvent/md5"
        etype = "md5"
        poperator = "equal"
        ptoken = "fileWriteEvent/md5"
        ptype = "md5"
        findHXout = [eoperator , etoken, etype , poperator,ptoken,ptype]
        print("findHXout MD5" + str(findHXout))
        return findHXout




def isIP(value):
    if value is None:
        return "NO"
    i = value
    tmp = i
    tmp2 = tmp.replace(".", "")

    if "." in i and tmp2.isdigit():
        print("isIP value : "+value)
        return True


############################## HX 데이터 파일 만들기 #################################################################
def writeHX(output, jobno, jobfilename):
    filename = jobfilename[8:len(jobfilename) - 3]


    yy = datetime.today().strftime('%y')
    mm = datetime.today().strftime('%m')
    dd = datetime.today().strftime('%d')
    print(
        "###########################################[생성] HX 텍스트 작성 ######################################################")
    tmp = ""
    tmp2 = ""



    # 1줄 로직
    if len(output) == 1 and output[0] != '변환실패':
        value = ""
        value = output[0]

        findHXout = []
        findHXout = findHX(value)
        eoperator = findHXout[0]
        etoken = findHXout[1]
        etype = findHXout[2]
        poperator = findHXout[3]
        ptoken = findHXout[4]
        ptype = findHXout[5]

        ioc1 = "{\"igloo\":{\"execution\":["
        ioc2 = "[{\"operator\":\""+str(eoperator)+"\",\"token\":\""+str(etoken)+"\",\"type\":\""+str(etype)+"\",\"value\":\"" + str(value) + "\"}]"
        ioc11 = "{\"igloo\":{\"presence\":["
        ioc3 = "],\"presence\":["
        ioc4 = "[{\"operator\":\""+str(poperator)+"\",\"token\":\""+str(ptoken)+"\",\"type\":\""+str(ptype)+"\",\"value\":\"" + str(value) + "\"}]"
        ioc5 = "],\"name\":\"" + str(filename) + "\",\"category\":\"Custom\",\"platforms\":[\"win\",\"osx\"]}}"


        if "NO" != isIP(value):
            ioc = ioc11 + ioc4 + ioc5
        else:
            ioc = ioc1 + ioc2 + ioc3 + ioc4 + ioc5

        print("output 1 : " + str(ioc))

        filename2 = "HX 파일_작업[" + str(jobno) + "]_" + str(len(output)) + "건_.hx"
        f = open(filename2, 'w')
        f.write(str(ioc))
        f.close()

    # 2줄 이상 로직

    if len(output) >= 2:
        count = 0
        count2 = 0
        ioc1 = "{\"igloo\":{\"execution\":["

        ipnum = 0
        rere = 1
        for value in output:
            if value is None:
                rere += 1
                continue

            if value == '변환실패':
                rere += 1
                continue

            #해당값이 IP냐? 그럼 continue
            if isIP(value):
                print("################value is IP : " + value)
                rere += 1
                continue

            findHXout  = []
            findHXout = findHX(value)
            print("AAAAA : "+str(findHXout))
            outhx = findHXout
            eoperator = outhx[0]
            etoken = outhx[1]
            etype = outhx[2]

            ioc2 = "[{\"operator\":\""+str(eoperator)+"\",\"token\":\""+str(etoken)+"\",\"type\":\""+str(etype)+"\",\"value\":\"" + str(value) + "\"}]"
            rere += 1
            print("rere : " + str(rere))
            print("count : " + str(count))
            print("output : " + str(len(output)))
            if len(output) == rere:
                tmp = tmp + ioc2
            else:
                tmp = tmp + ioc2 + ","

        ioc2 = tmp

        ioc3 = "],\"presence\":["

        for value in output:
            if value is None:
                continue

            if value == '변환실패':
                continue

            print("value 1 : " + str(value))
            findHXout  = []
            findHXout = findHX(value)
            eoperator = findHXout[0]
            etoken = findHXout[1]
            etype = findHXout[2]
            poperator = findHXout[3]
            ptoken = findHXout[4]
            ptype = findHXout[5]

            ioc4 = "[{\"operator\":\""+str(poperator)+"\",\"token\":\""+str(ptoken)+"\",\"type\":\""+str(ptype)+"\",\"value\":\"" + str(value) + "\"}]"
            count2 += 1

            if len(output) == count2:
                tmp2 = tmp2 + ioc4
            else:
                tmp2 = tmp2 + ioc4 + ","
        ioc4 = tmp2

        ioc5 = "],\"name\":\"" + filename + "\",\"category\":\"Custom\",\"platforms\":[\"win\",\"osx\"]}}"
        filename2 = ""
        ioc11 = "{\"igloo\":{\"presence\":["

        iplen = 0
        valuelen= 0
        for value in output:
            aa = value
            tmp0 = aa.replace(".","")
            if value is not None and value !="변환실패" and "NO" != isIP(value) and tmp0.isdigit():
                iplen += 1
            if value is not None and value != "변환실패":
                valuelen += 1

        print("iplen : "+str(iplen))
        print("valuelen : " + str(valuelen))

        if iplen == valuelen:
            ioc = ioc11 + ioc4 + ioc5
            print("output IPs : " + ioc)

        else:
            ioc = ioc1 + ioc2 + ioc3 + ioc4 + ioc5
            print("output : " + ioc)

    #filename2 = "HX 파일_작업[" + str(jobno) + "]_" + str(len(output)) + "건_.hx"

    filename2 = jobfilename[8:len(jobfilename) - 3] + ".hx"
    f = open(filename2, 'w')
    f.write(str(ioc))
    f.close()

    return filename2
        ##################################################################################################################

def writeExcel(jobip,jobdate,jobno):
    print("######################################### 변환된 데이터를 excel 작성하기##############################################")
    excelfilename = "HX_DATA_결과파일_작업["+str(jobno)+"].xlsx"
    wb = openpyxl.Workbook()
    sheet = wb.active

    connq = pymysql.connect(host='localhost', user='root', password='!Hg1373002934', db='ioc', charset='utf8')
    curq = connq.cursor()
    ########### 초기 엑셀 작성 세팅
    sql4 = "SELECT no, md5, sha256, sha1, ip, url FROM work_place WHERE status = '1' AND ipip = '" + str(
        jobip) + "' AND time = '" + str(jobdate) + "'"
    curq.execute(sql4)
    connq.close()

    sheet['A1'] = "no"
    sheet['B1'] = "md5"
    sheet['C1'] = "값"
    sheet['D1'] = "유형"
    sheet['E1'] = "비고"
    no = 1
    line = 2

    print("########### 액셀 내용 작성")
    for r in curq:
        print("row after : " + str(r[0]) + " " + r[1] + " " + r[2] + " " + r[3]+ " " + r[4]+ " " + r[5])

        # no
        sheet['A' + str(line)] = no

        # 원본데이터(sha1, sha256)
        if r[2] != 'X':
            sheet['B' + str(line)] = r[1]
            sheet['C' + str(line)] = r[2]
            sheet['D' + str(line)] = "sha256"

        if r[3] != 'X':
            sheet['B' + str(line)] = r[1]
            sheet['C' + str(line)] = r[3]
            sheet['D' + str(line)] = "sha1"

        # md5 데이터 입력 처리
        if r[1] != 'X' and r[2] == 'X' and r[3] == 'X':
            sheet['B' + str(line)] = r[1]
            sheet['C' + str(line)] = r[1]
            sheet['D' + str(line)] = "md5"

        if r[4] != 'X':
            sheet['B' + str(line)] = r[4]
            sheet['C' + str(line)] = r[4]
            sheet['D' + str(line)] = "ip"

        if r[5] != 'X':
            sheet['B' + str(line)] = r[5]
            sheet['C' + str(line)] = r[5]
            sheet['D' + str(line)] = "url"

        line += 1
        no += 1
    wb.save(excelfilename)
    return excelfilename