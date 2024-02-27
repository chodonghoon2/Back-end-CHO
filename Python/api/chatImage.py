from openai import OpenAI
import os,base64,json,requests
import urllib.request
import model.image_oracledb.image_model as imagedb
from flask_restful import Resource,reqparse
from flask import jsonify, request


# OpenAI 객체를 생성 api_key는 환경 변수
client = OpenAI(
    # 환경변수 api키
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class ChatImage(Resource):
    def get(self, user_id):
        try:
            # 사용자 ID를 기반으로 데이터베이스에서 이미지 정보를 가져옵니다.
            conn = imagedb.connectDatabase()
            image_info = imagedb.select(conn, user_id)
            imagedb.close(conn)

            # 이미지 정보가 없다면 에러 메시지를 반환합니다.
            if image_info is None:
                return {"error": "이미지 정보가 존재하지 않습니다!"}, 404

            # 이미지 파일의 경로를 가져옵니다.
            # image_path = image_info[1]  # 데이터베이스에서 가져온 이미지 경로

            #한번 테스트 해보자
            for i in range(len(image_info)):
                str1 = 'C:\\Users\\user\\Upload\\' + image_info[i][3] + '.png'

                # 이미지 파일을 열고, base64로 인코딩
                with open(str1, "rb") as f:
                    image_data = base64.b64encode(f.read())
                    # 식품 정보와 인코딩된 이미지를 foodDiary 리스트에 추가
                    image_data_str = "data:image/png;base64," + str(image_data)[2:-2]

            # 인코딩된 이미지 데이터를 반환합니다.
            return jsonify({"image_data": image_data_str})

        except Exception as e:
            return {"error": str(e)}, 500
    def post(self):
        # 요청 본문에서 메시지를 가져 온다.
        prompt = request.json['message']
        # 메시지를 바탕으로 이미지를 생성
        print('받은 메세지:', prompt)

        # 이미지의 경로와 이름을 반환
        image_path, image_name = generate_image(prompt, client)

        # 만약 이미지 생성에 실패한 경우, 에러 메시지를 반환
        if image_path is None or image_name is None:
            return jsonify({"error": "이미지 생성 실패!!"})

        # 이미지 파일을 읽어서 base64 형태로 인코딩
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # # 이미지 정보를 데이터베이스에 저장
        # conn = imagedb.connectDatabase()
        # # base64로 인코딩된 이미지 데이터를 디코딩해서 데이터베이스에 저장
        # imagedb.insert(conn, base64.b64decode(encoded_image.encode()))
        # imagedb.close(conn)

        # base64 인코딩된 이미지 데이터와 이미지의 이름을 JSON 형식으로 반환
        return jsonify({"image_data": encoded_image, "image_name": image_name})    
        '''
        # 이미지 데이터를 base64로 인코딩
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # 이미지의 경로와 이름, 인코딩된 이미지 데이터를 JSON 형식으로 반환
        return jsonify({"image_url": image_url, "image_name": image_name, "image_data": encoded_string})
        '''


# 폴더가 존재하지 않으면 새 폴더를 생성하는 함수
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# 텍스트 메시지를 이미지로 변환하는 함수
def create_image(client, model, messages):
    response = client.chat.completions.create(model=model, messages=messages)
    return response

# 이미지 생성을 위한 전체 프로세스를 담당하는 함수
def generate_image(prompt, client):
    model = 'gpt-3.5-turbo'
    folder_path = './uploads' # 이미지를 저장할 폴더의 경로
    create_folder(folder_path)  # 폴더를 생성
    image_name = 'id.png'  # 이미지의 초기 이름
    image_path = os.path.join(folder_path, image_name)  # 이미지의 전체 경로

    # 이미지 이름이 중복되지 않도록 처리하는 부분
    # 이미 같은 이름의 이미지가 있다면, 이름 뒤에 숫자를 붙여서 중복을 방지
    '''
    index = 1
    while os.path.exists(image_path):
        print('파일 존재한다')  # 파일이 이미 존재하는 경우 메시지를 출력
        image_name = f'id_{index}.png'
        image_path = os.path.join(folder_path, image_name)
        index += 1
    '''
    # 이미지 생성과 관련된 부분은 예외가 발생할 수 있으므로, try-except 문으로 감싼다
    try:
        # 이미지 생성 요청을 위한 메시지를 준비
        messages = [
            {"role": "system", "content": "you are a translation expert who translates korean into english"},
            {"role": "user", "content": prompt}
        ]
        # 이미지를 생성하고, 그 결과를 받는다
        response = create_image(client, model, messages)
        prompt = response.choices[0].message.content
        # 생성된 이미지를 다운
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            response_format='url',
            n=1,
        )

        # 이미지의 URL을 가져 온다
        image_url = response.data[0].url
        # 이미지를 다운로드 받아 지정한 경로에 저장
        urllib.request.urlretrieve(image_url, f"./uploads/{image_name}")

    # 예외가 발생한 경우, 에러 메시지를 출력하고 None을 반환
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return None, None

    # 이미지의 경로와 이름을 반환
    return image_path, image_name