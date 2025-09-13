import streamlit as st
from api import get_prompt_images
from namegen import generate_name_and_description
import random

st.set_page_config(page_title="🌿 상상 생명체 생성기", layout="wide")

# ===========================
# 네온 스타일 (CSS)
# ===========================
st.markdown(
    """
    <style>
    /* 전체 배경 흰색, 기본 글자 검정 */
    .stApp {
        background-color: white;
        color: black;
    }

    /* 제목 네온 효과 */
    h1, h2, h3, h4 {
        color: #00FFFF;  /* 진한 전기 블루 */
        text-shadow: 
            0 0 5px #00FFFF,
            0 0 10px #00FFFF,
            0 0 20px #00FFFF,
            0 0 40px #00FFFF,
            0 0 80px #00FFFF;
    }

    /* 일반 텍스트, 선택 박스 글자 검정 */
    .stMarkdown, .stText, .stSelectbox, .stMultiselect, .stTextArea {
        color: black !important;
    }

    /* 체크박스 글자 검정 */
    .stCheckbox > label {
        color: black !important;
        text-shadow: none !important;
    }

    /* 버튼 스타일 */
    .stButton > button {
        background-color: white !important;
        color: #00FFFF !important;
        border: 2px solid #00FFFF !important;
        border-radius: 10px;
        text-shadow: 0 0 5px #00FFFF;
    }
    .stButton > button:hover {
        background-color: #00FFFF !important;
        color: white !important;
        text-shadow: none;
    }

    /* 다운로드 버튼 */
    .stDownloadButton > button {
        background-color: white !important;
        color: #00FFFF !important;
        border: 2px solid #00FFFF !important;
        border-radius: 10px;
        text-shadow: 0 0 5px #00FFFF;
    }
    .stDownloadButton > button:hover {
        background-color: #00FFFF !important;
        color: white !important;
        text-shadow: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌿 상상 생명체 생성기")

# ===========================
# session_state 초기값
# ===========================
if "selected_type" not in st.session_state:
    st.session_state.selected_type = "포유류"
if "selected_size" not in st.session_state:
    st.session_state.selected_size = "중형"
if "selected_pose" not in st.session_state:
    st.session_state.selected_pose = "서 있음"
if "selected_environment" not in st.session_state:
    st.session_state.selected_environment = []
if "selected_colors" not in st.session_state:
    st.session_state.selected_colors = []
if "selected_features" not in st.session_state:
    st.session_state.selected_features = []
if "abilities" not in st.session_state:
    st.session_state.abilities = []
if "history" not in st.session_state:
    st.session_state.history = []

# ===========================
# 랜덤 생성 / 초기화 버튼
# ===========================
st.subheader("⚙️ 생성 옵션")
col1, col2 = st.columns(2)

with col1:
    if st.button("🔀 랜덤 생성"):
        creature_types = ["포유류", "파충류", "드래곤", "외계 생명체", "환상 생물"]
        size_options = ["소형", "중형", "대형", "거대"]
        pose_options = ["앉아 있음", "날아다님", "포효", "서 있음"]
        environment_options = ["안개", "비", "눈", "불꽃", "전기", "맑음", "황혼"]
        color_options_keys = ["빨강","주황","노랑","초록","파랑","보라","검정","흰색","갈색","회색"]
        feature_options_values = [
            "Has horns","Has claws","Has wings","Has tail","Has fins",
            "Has sharp teeth","Has tentacles","Has scales","Has fur","Has spiky back"
        ]
        abilities_options_values = [
            "Fire breathing", "Transparency", "Water control", "Electric shock",
            "Invisibility", "Teleportation", "Ice control", "Earth manipulation",
            "Mind reading", "Regeneration"
        ]
        st.session_state.selected_type = random.choice(creature_types)
        st.session_state.selected_size = random.choice(size_options)
        st.session_state.selected_pose = random.choice(pose_options)
        st.session_state.selected_environment = random.sample(environment_options, k=random.randint(1,3))
        st.session_state.selected_colors = random.sample(color_options_keys, k=random.randint(1,3))
        st.session_state.selected_features = random.sample(feature_options_values, k=random.randint(1,5))
        st.session_state.abilities = random.sample(abilities_options_values, k=random.randint(1,3))

with col2:
    if st.button("♻️ 초기화"):
        st.session_state.selected_type = "포유류"
        st.session_state.selected_size = "중형"
        st.session_state.selected_pose = "서 있음"
        st.session_state.selected_environment = []
        st.session_state.selected_colors = []
        st.session_state.selected_features = []
        st.session_state.abilities = []

# ===========================
# 메인 화면 선택 옵션
# ===========================
creature_types = ["포유류", "파충류", "드래곤", "외계 생명체", "환상 생물"]
st.session_state.selected_type = st.selectbox(
    "생명체 유형 선택", creature_types, index=creature_types.index(st.session_state.selected_type)
)

size_options = ["소형","중형","대형","거대"]
st.session_state.selected_size = st.selectbox(
    "체형/크기 선택", size_options, index=size_options.index(st.session_state.selected_size)
)

pose_options = ["앉아 있음", "날아다님", "포효", "서 있음"]
st.session_state.selected_pose = st.selectbox(
    "포즈 선택", pose_options, index=pose_options.index(st.session_state.selected_pose)
)

environment_options = ["안개", "비", "눈", "불꽃", "전기", "맑음", "황혼"]
st.session_state.selected_environment = st.multiselect(
    "환경 효과 선택", environment_options, default=st.session_state.selected_environment
)

# ===========================
# 색상 선택
# ===========================
st.subheader("1️⃣ 색상 선택")
color_options = {
    "빨강": "Red", "주황": "Orange", "노랑": "Yellow", "초록": "Green",
    "파랑": "Blue", "보라": "Purple", "검정": "Black", "흰색": "White",
    "갈색": "Brown", "회색": "Gray"
}
st.session_state.selected_colors = st.multiselect(
    "색상을 선택하세요 (여러 개 선택 가능):",
    list(color_options.keys()),
    default=st.session_state.selected_colors
)

# ===========================
# 특징 선택
# ===========================
st.subheader("2️⃣ 신체 특징 선택")
feature_options = {
    "뿔 있음": "Has horns", "발톱 있음": "Has claws", "날개 있음": "Has wings",
    "꼬리 있음": "Has tail", "지느러미 있음": "Has fins", "날카로운 이빨 있음": "Has sharp teeth",
    "촉수 있음": "Has tentacles", "비늘 있음": "Has scales", "털 있음": "Has fur", "뾰족한 등 있음": "Has spiky back"
}
cols = st.columns(2)
selected_features = []
for i, (k, v) in enumerate(feature_options.items()):
    if cols[i % 2].checkbox(k, value=(v in st.session_state.selected_features)):
        selected_features.append(v)
st.session_state.selected_features = selected_features

# ===========================
# 능력 선택
# ===========================
st.subheader("3️⃣ 특별한 능력 선택")
abilities_options = {
    "불뿜기": "Fire breathing",
    "투명화": "Transparency",
    "물 조종": "Water control",
    "전기 충격": "Electric shock",
    "투사 이동": "Invisibility",
    "순간 이동": "Teleportation",
    "얼음 조종": "Ice control",
    "대지 조종": "Earth manipulation",
    "마음 읽기": "Mind reading",
    "재생": "Regeneration"
}

selected_abilities_kor = st.multiselect(
    "능력 선택 (여러 개 선택 가능):",
    list(abilities_options.keys()),
    default=[k for k,v in abilities_options.items() if v in st.session_state.abilities]
)
st.session_state.abilities = [abilities_options[k] for k in selected_abilities_kor]

# ===========================
# 추가 설명
# ===========================
st.subheader("4️⃣ 추가 설명 (선택)")
with st.form("prompt_form"):
    prompt = st.text_area("생명체의 특징을 영어로 입력하세요:", height=120)
    submitted = st.form_submit_button("이미지 생성")

# 주석 문구 추가 (작게, 구석 느낌)
st.caption("💡 너무 많은 특징을 입력하면 모두 반영하지 못할 수 있습니다.")

# ===========================
# 영어 변환 딕셔너리
# ===========================
type_translation = {
    "포유류": "Mammal",
    "파충류": "Reptile",
    "드래곤": "Dragon",
    "외계 생명체": "Alien creature",
    "환상 생물": "Fantasy creature"
}

size_translation = {
    "소형": "Small",
    "중형": "Medium",
    "대형": "Large",
    "거대": "Huge"
}

pose_translation = {
    "앉아 있음": "Sitting",
    "날아다님": "Flying",
    "포효": "Roaring",
    "서 있음": "Standing"
}

environment_translation = {
    "안개": "Fog",
    "비": "Rain",
    "눈": "Snow",
    "불꽃": "Fire",
    "전기": "Electric",
    "맑음": "Clear",
    "황혼": "Twilight"
}

# ===========================
# 이미지 생성 및 결과
# ===========================
if submitted:
    user_prompt = prompt.strip() if prompt.strip() else "No additional description"

    option_descriptions = []
    if st.session_state.selected_colors:
        option_descriptions.append(
            "Colors: " + ", ".join([color_options[c] for c in st.session_state.selected_colors])
        )
    if st.session_state.selected_features:
        option_descriptions.extend(st.session_state.selected_features)
    if st.session_state.abilities:
        option_descriptions.append("Ability: " + ", ".join(st.session_state.abilities))
    
    option_descriptions.append(
        f"Type: {type_translation[st.session_state.selected_type]}, "
        f"Size: {size_translation[st.session_state.selected_size]}, "
        f"Pose: {pose_translation[st.session_state.selected_pose]}"
    )
    if st.session_state.selected_environment:
        option_descriptions.append(
            "Environment: " + ", ".join([environment_translation[e] for e in st.session_state.selected_environment])
        )

    full_prompt = "This creature has the following characteristics: " + "; ".join(option_descriptions) + ". "
    full_prompt += user_prompt

    with st.spinner("이미지를 생성하는 중입니다..."):
        images = get_prompt_images(full_prompt)

    with st.spinner("이름과 설명을 생성 중입니다..."):
        kor_name, description = generate_name_and_description(full_prompt)

    if images:
        st.success("🌱 생명체 생성 완료!")
        st.markdown("---")
        st.subheader(f"🧬 이름: {kor_name}")
        st.markdown(f"**설명:** {description}")
        st.markdown("### 🖼️ 생성된 이미지")
        for i in range(0, len(images), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(images):
                    cols[j].image(images[i + j], use_container_width=True)
        
        st.markdown("---")
        st.download_button("💾 다운로드 이미지", data=images[0], file_name=f"{kor_name}.png", mime="image/png")

        st.session_state.history.insert(0, {"name": kor_name, "description": description, "images": images})
        if len(st.session_state.history) > 5:
            st.session_state.history = st.session_state.history[:5]

# ===========================
# 최근 생성 기록
# ===========================
if st.session_state.history:
    st.subheader("🕘 최근 생성 기록")
    for idx, record in enumerate(st.session_state.history):
        st.markdown(f"**{record['name']}** - {record['description']}")
        cols = st.columns(2)
        for i in range(min(2, len(record['images']))):
            cols[i].image(record['images'][i], use_container_width=True)
        st.download_button(
            label=f"💾 다운로드: {record['name']}",
            data=record['images'][0],
            file_name=f"{record['name']}.png",
            mime="image/png",
            key=f"download_{idx}"
        )
        st.markdown("---")
