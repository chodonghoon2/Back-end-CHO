from configparser import ConfigParser
from  cx_Oracle import connect
import os

def connectDatabase():#데이타베이스 연결
    config = ConfigParser()
    # print(os.path.abspath('.'))
    # 데이터 절대경로 찾아주기
    path = os.path.dirname(os.path.abspath(__file__))
    # print(path)
    config.read(path+'/oracle.ini', encoding='utf8')
    # 데이타베이스 연결
    return connect(user=config['ORACLE']['USER'],
                   password=config['ORACLE']['PASSWORD'],
                   dsn=config['ORACLE']['URL'],encoding="UTF-8")
def close(conn):#커넥션객체 닫기
    if conn:
        conn.close()
def selectAll(conn):
    with conn.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM account')
            return cursor.fetchall()
        except Exception as e:
            print('모든 데이타 조회시 오류:',e)
            return None
        
# 식단 추가
def insert(conn,user_id,list_):
    print(user_id,":",list_)
    test = [] #캘린더 테이블
    test.append(user_id)
    test.append(list_['DESCRIPTION'])
    test.append(list_['MEMO'])
    test.append(list_['DIET_IMAGE'])
    test.append(list_['FOOD'])
    test.append(list_['FOOD_WEIGHT'])

    with conn.cursor() as cursor:
        try:

            cursor.execute('INSERT ALL INTO calendar VALUES(SEQ_CALENDAR_CALENDAR_NO.nextval, :1, :2, :3,DEFAULT,default) INTO diet VALUES((SELECT max(calendar_no+1) FROM calendar), :4, :5, :6) SELECT * FROM DUAL',test)
            conn.commit()
            return cursor.rowcount
            '''
                CALENDAR_NO    NOT NULL NUMBER  필요없고       
                ACCOUNT_NO     NOT NULL NUMBER  넌 뭔데 no로 왔냐? user_id를 ACCOUNT_NO로 받아오자  
                DESCRIPTION    NOT NULL NVARCHAR2(100) 제목
                MEMO           NOT NULL NVARCHAR2(100) 내용
                START_POSTDATE          DATE           일정 시작일 (짜피 먹는건데 그냥 디폴트 하루임)
                END_POSTDATE            DATE            일정 끝나는날(날짜가 하루면 디폴트 넣어주셈)
                ----------- -------- -------------- 
                CALENDAR_NO NOT NULL NUMBER             SELECT max(calendar_no) FROM calendar; 로 받아오자
                DIET_IMAGE           NVARCHAR2(50)      사진
                FOOD        NOT NULL NVARCHAR2(100)     음식 예시:닭갈비
                FOOD_WEIGHT NOT NULL NUMBER             음식 용량 예시: 100
            
                INSERT ALL
                    INTO calendar VALUES(
                        SEQ_CALENDAR_CALENDAR_NO.nextval,
                        3,
                        '다중 insert2',
                        '볶음밥',
                        DEFAULT,
                        default  
                    )
                    INTO diet VALUES(
                        (SELECT max(calendar_no) FROM calendar),
                        null,
                        '김치볶음밥1',
                        100
                        )
                    SELECT * FROM DUAL;
            '''

        except Exception as e:
            print("error:",e)
            return 0