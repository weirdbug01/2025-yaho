import random

# 설명 템플릿 (서식지 제거)
DESCRIPTION_TEMPLATES = [
    "{kor_name}은 신비로운 생명체입니다.",
    "{kor_name}은 독특한 특징을 지닌 생명체입니다.",
    "{kor_name}은 전설 속에서 자주 언급되는 신비로운 존재입니다.",
    "{kor_name}은 평화롭게 살아가며, 상상력을 자극하는 생명체입니다.",
    "신비로운 생명체 {kor_name}은 독특한 특징이 돋보입니다."
]

# 한글 이름 생성 (랜덤 음절만 사용)
def generate_korean_name():
    syllables = ["라", "리", "루", "노", "미", "아", "시", "엘", "온", "라니", "루아", "마엘", "나르"]
    name_parts = []
    
    while len("".join(name_parts)) < random.randint(3, 6):
        name_parts.append(random.choice(syllables))

    # 최종 이름 최대 6글자
    kor_name = "".join(name_parts)[:6]
    return kor_name

# 이름과 설명 생성
def generate_name_and_description(prompt=None):
    kor_name = generate_korean_name()
    template = random.choice(DESCRIPTION_TEMPLATES)
    description = template.format(
        kor_name=kor_name
    )
    return kor_name, description

# 테스트 예시
if __name__ == "__main__":
    name, desc = generate_name_and_description()
    print("한글 이름:", name)
    print("설명:", desc)
