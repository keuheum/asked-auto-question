import random
import requests
from tqdm import tqdm#https://www.koreaminecraft.net/dev_lecture/1200155
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

#question lists
koQuestion = [
    "너희 시험 언제야?",
    "무슨 학원 다녀? 과목이랑 이름 좀",
    "좋아하는 사람이나 관심있는 사람 있어?",
    "연상 연하 동갑",
    "즐똥",
    "너희 반 괜찮은 것 같아? 맘에 들어?",
    "공부 잘해?",
    "카페 좋아해?",
    "키 몇이야?",
    "취미가 뭐야?",
    "동아리 뭐야?",
    "mbti 뭐야?",
    "모솔이야?",
    "이상형 머야?",
    "너 인기 많은거 알지?",
    "생일 언제야?",
    "지금 뭐하는중?",
    "안녕",
    "친하게 지내자",
    "무슨 학교 다녀?",
    "걔랑 친해??",
    "피방 가본적 있음?"
]

enQuestion = [
    "when is your exam?",
    "what school did you go to? subject and name",
    "Do you have someone you like or are interested in?",
    "older, younger, same age",
    "fun",
    "Do you think your class is okay? Like it?",
    "study well?",
    "do you like cafes?",
    "How tall are you?",
    "What's your hobby?",
    "what is a club",
    "what is your mbti?",
    "Have you ever been in love?",
    "Who is your ideal type?",
    "you know you're popular",
    "when is your birthday",
    "What are you doing now?",
    "hi",
    "let's be friendly",
    "what school did you go to",
    "Are you friends with him??",
    "Have you ever been to a PC room?"
]

configDict = {
    "한국어" : {
        "system" : [
            "asked의 아이디를 적어주세요",
            "*이(가) 원하는 계정의 이름이 맞나요?",
            "= = 종류를 골라주세요 = =\n0 단순 반복형 질문\n1 답변 가능 질문",
            "답변 가능 질문은 최대 *개까지 가능합니다. 그래도 진행 하시겠습니까?",
            "몇개의 질문을 원하는지 적어주세요",
            "질문 업로드중",
            "모든 질문이 성공적으로 업로드 되었습니다"
        ],
        "err" : [
            "asked의 아이디는 5자~12자입니다",
            "asked의 아이디에는 영어와 숫자만 존재합니다",
            "asked의 아이디를 찾지 못하였습니다",
            "값들중에서 선택하세요",
            "웹 요청이 정상적으로 처리되지 못했습니다. 상태 코드: *"
        ],
        "question" : koQuestion
    },
    "English" : {
        "system" : [
            "please write the ID of asked",
            "* is what you want account's name?",
            "= = select type = =\n0 simple repeat question\n1 answerable Questions",
            "up to * answerable questions are allowed. would you like to proceed though?",
            "please write how many questions you would like",
            "Uploading question",
            "all questions have been successfully uploaded"
        ],
        "err" : [
            "ID of asked is 5 to 12 characters long",
            "only English and numbers exist in asked ID",
            "couldn't find the ID of asked",
            "please select within the value",
            "web request could not be successfully processed. Status code: *"
        ], 
        "question" : enQuestion
    }
}

def questionUpload(askedId, questionContent, langNum):
    headers ={'User-Agent': UserAgent().chrome}
    data = {'id': askedId, 'content': questionContent, 'makarong_bat': '-1', 'show_user': '0'}
    askedRes = requests.post(
        url=f"https://asked.kr/query.php?query=100",
        headers=headers,
        data=data
        )
    if askedRes.status_code != 200:
        print(f">>> {configDict[list(configDict.keys())[langNum]] ['err'] [4].replace('*', str(askedRes.status_code))}")
        exit()

def questionSettingProcess(langNum, askedId, questionType, questionCount):
    langNum = int(langNum)
    questionList = configDict[list(configDict.keys())[langNum]] ['question']
    if int(questionType) == 0:
        for x in tqdm(range(int(questionCount)), desc=configDict[list(configDict.keys())[langNum]] ['system'] [5]):
            questionUpload(askedId, '.', langNum)
    else:
        for x in tqdm(range(int(questionCount)), desc=configDict[list(configDict.keys())[langNum]] ['system'] [5]):
            questionContent = questionList[random.randint(0, len(questionList)-1)]
            questionList.remove(questionContent)
            questionUpload(askedId, questionContent, langNum)

    print(configDict[list(configDict.keys())[langNum]] ['system'] [6])
        

def askLangSetting():
    print("= = select language = =")
    for index, (key, elem) in enumerate(configDict.items()):
        print(index, key)
    langConfig = input(": ")
    if langConfig.isnumeric() == True and int(langConfig) in list(range(0, len(configDict))):
        return langConfig
    else:
        print(">>> please select within the value")
        return askLangSetting()

def askedExistCheck(id: str):
    askedLink = f"https://asked.kr/{id}"
    headers ={
    'User-Agent': UserAgent().chrome
    }
    askedRes = requests.get(
        url=askedLink,
        headers=headers
        )
    askedRes.encoding='UTF-8'
    if (len(askedRes.history) != 0) or ('location.href="./logout.php";' in askedRes.text):
        return None
    else:
        return BeautifulSoup(askedRes.text, 'lxml').title.string.split(" -")[0]#https://stackoverflow.com/questions/51233/how-can-i-retrieve-the-page-title-of-a-webpage-using-python

def askIdSetting(langSet):
    langSet = int(langSet)
    askedId = input(configDict[list(configDict.keys())[langSet]] ['system'] [0] + ": ")

    askedIdCheck = askedId
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"#(새 변수에서) 아이디 영어&숫자 제거
    for i in list(alphabet) + list(alphabet.lower()) + list("1234567890"):
        table = askedIdCheck.maketrans({i: ''})#https://engineer-mole.tistory.com/238
        askedIdCheck = askedIdCheck.translate(table)

    if (5 <= len(askedId) <= 12) == False:#아이디 길이 체크
        print(f">>> {configDict[list(configDict.keys())[langSet]] ['err'] [0]}")

    elif askedIdCheck != "":#아이디 영어&숫자만 있는지 확인
        print(f">>> {configDict[list(configDict.keys())[langSet]] ['err'] [1]}")
    else:
        askedName = askedExistCheck(askedId)#아이디 존재 여부 확인&이름 가져오기
        if askedName == None:
            print(f">>> {configDict[list(configDict.keys())[langSet]] ['err'] [2]}")
        else:
            askedNameCheck = input(f"{configDict[list(configDict.keys())[langSet]] ['system'] [1].replace('*', f'`{askedName}`')} (Y/N): ")
            if askedNameCheck.upper() == "Y":
                return askedId
            elif askedNameCheck.upper() == "N":
                pass
            else:
                print(f">>> {configDict[list(configDict.keys())[langSet]] ['err'] [3]}")
    return askIdSetting(langSet)

def askCountSetting(langSet):
    langSet = int(langSet)
    questionType = input(configDict[list(configDict.keys())[langSet]] ['system'] [2] + "\n: ")
    if questionType.isnumeric():
        questionType = int(questionType)
        if questionType == 0:
            questionNum = input(configDict[list(configDict.keys())[langSet]] ['system'] [4] + ": ")
            if int(questionNum) < 20:##########혹시 모를 신고 방지 추가(저는 20개 제한 넣었습니다..ㅎ)
                if questionNum.isnumeric() and int(questionNum) != 0:
                    return (questionType, questionNum)
            else:##########혹시 모를 신고 방지 추가
                print("적당한 값 넣으세영..!")##########혹시 모를 신고 방지 추가

        elif questionType == 1:
            questionNoti = input(configDict[list(configDict.keys())[langSet]] ['system'] [3].replace("*", str(len(configDict[list(configDict.keys())[langSet]] ['question']))) + " (Y/N): ")
            if questionNoti.upper() == "Y":
                questionNum = input(configDict[list(configDict.keys())[langSet]] ['system'] [4] + f" (1~{len(configDict[list(configDict.keys())[langSet]] ['question'])}): ")
                if questionNum.isnumeric() and int(questionNum) != 0 and int(questionNum) <= len(configDict[list(configDict.keys())[langSet]] ['question']):
                    return (questionType, questionNum)
            elif questionNoti.upper() == "N":
                return askCountSetting(langSet)

    print(f">>> {configDict[list(configDict.keys())[langSet]] ['err'] [3]}")
    return askCountSetting(langSet)
            
def settings():
    langSet = askLangSetting()
    askedId = askIdSetting(langSet)
    questionType, questionNum = askCountSetting(langSet)
    print("= = 세팅값 = =")
    print("언어: " + list(configDict.keys())[int(langSet)])
    print("아디: " + askedId)
    print("질문 타입: " + str(questionType))
    print("질문 수: " + str(questionNum))

    questionSettingProcess(
        langNum=langSet,
        askedId=askedId,
        questionType=questionType,
        questionCount=questionNum
    )

if __name__ == "__main__":
    settings()
