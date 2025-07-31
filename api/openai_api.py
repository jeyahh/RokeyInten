import json
import re
import base64
from openai import OpenAI
from utils.file_handler import OPENAI_API_KEY
from db.image_log import DBManager   # 여기만 바꿨습니다

client = OpenAI(api_key=OPENAI_API_KEY)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def clean_json_string(s):
    pattern = r"```json(.*?)```"
    match = re.search(pattern, s, re.DOTALL)
    if match:
        return match.group(1).strip()
    return s.strip()

def get_player_info_from_image(image_path):
    base64_image = encode_image_to_base64(image_path)

    prompt = (
        "이미지에는 축구 선수의 유니폼이 있습니다. "
        "해당 선수의 이름, 팀 이름, 등번호를 각각 'name', 'team', 'number' 필드로 포함한 JSON 형식으로 추출하세요. "
        "정보가 없으면 '정보 없음'으로 기입하세요."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        description = response.choices[0].message.content
        print("[GPT 응답 결과]", description)

        cleaned = clean_json_string(description)
        player_info = json.loads(cleaned)

        name = player_info.get("name", "정보 없음")
        team = player_info.get("team", "정보 없음")
        number = player_info.get("number", "정보 없음")

        # 유니폼 관련 정보가 하나라도 제대로 추출되지 않았다면 저장 안함
        if name == "정보 없음" and team == "정보 없음" and number == "정보 없음":
            print("[⚠️ 저장 안함] 선수 정보가 없습니다.")
            return None

        if number == "정보 없음":
            number = None
        elif isinstance(number, str) and number.isdigit():
            number = int(number)

        db_manager = DBManager()
        db_manager.insert_player(name, team, number)
        db_manager.close()
        print("[✅ DB 저장 완료]")

        return {
            "name": name,
            "team": team,
            "number": number
        }

    except Exception as e:
        print("[❌ 오류 발생]", e)
        return None