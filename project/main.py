import streamlit as st
from api import get_prompt_images
from namegen import generate_name_and_description
import random

st.set_page_config(page_title="🌿 상상 생명체 생성기", layout="wide")

# ===========================
# CSS 스타일
# ===========================
st.markdown(
    """
    <style>
    .stApp { background-color: white; color: black; }
    h1, h2, h3, h4 {
        color: #00FFFF;  
        text-shadow: 0 0 5px #00FFFF, 0 0 10px #00FFFF, 0 0 20px #00FFFF,
                     0 0 40px #00FFFF, 0 0 80px #00FFFF;
    }
    .stMarkdown, .stText, .stSelectbox, .stMultiselect, .stTextArea { color: black !important; }
    .stCheckbox > label { color: black !important; text-shadow: none !important; }
    .stButton > button, .stDownloadButton > button {
        background-color: white !important;
        color: #00FFFF !important;
        border: 2px solid #00FFFF !important;
        border-radius: 10px;
        text-shadow: 0 0 5px #00FFFF;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #00FFFF !important;
        color: white !important;
        text-shadow: none;
    }
    div.stButton > button:first-child {
        width: 250px;
        height: 60px;
        font-size: 22px;
        font-weight: bold;
        margin: 20px auto;
        display: block;
        border-radius: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===========================
# session_state 초기화
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
# 탭 생성
# ===========================
tab1, tab2 = st.tabs(["🌱 생명체 생성", "💞 생명체 합성"])

# ===========================
# 탭1: 생명체 생성
# ===========================
with tab1:
    st.title("🌱 상상 생명체 생성기")

    # 랜덤 생성 / 초기화
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

    # 메인 옵션
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

    # 색상 선택
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

    # 특징 선택
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

    # 능력 선택
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

    # 추가 설명
    st.subheader("4️⃣ 추가 설명 (선택)")
    prompt = st.text_area("생명체의 특징을 영어로 입력하세요:", height=120, key="prompt_text")
    st.caption("💡 너무 많은 특징을 입력하면 모두 반영하지 못할 수 있습니다.")

    submitted = st.button("이미지 생성", key="generate_button")

    # ===========================
    # 영어 변환
    # ===========================
    type_translation = {"포유류": "Mammal","파충류": "Reptile","드래곤": "Dragon","외계 생명체": "Alien creature","환상 생물": "Fantasy creature"}
    size_translation = {"소형": "Small","중형": "Medium","대형": "Large","거대": "Huge"}
    pose_translation = {"앉아 있음": "Sitting","날아다님": "Flying","포효": "Roaring","서 있음": "Standing"}
    environment_translation = {"안개": "Fog","비": "Rain","눈": "Snow","불꽃": "Fire","전기": "Electric","맑음": "Clear","황혼": "Twilight"}

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
            st.session_state.history.insert(0, {"name": kor_name, "description": description, "images": images, "creature_data": {
                "type": st.session_state.selected_type,
                "size": st.session_state.selected_size,
                "pose": st.session_state.selected_pose,
                "environment": st.session_state.selected_environment,
                "colors": st.session_state.selected_colors,
                "features": st.session_state.selected_features,
                "abilities": st.session_state.abilities
            }})
            if len(st.session_state.history) > 5:
                st.session_state.history = st.session_state.history[:5]

    # 최근 생성 기록
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

# ===========================
# 탭2: 생명체 합성
# ===========================
with tab2:
    st.title("💞 생명체 합성")
    
    if len(st.session_state.history) < 2:
        st.info("합성을 위해서는 최소 2개의 생성된 생명체가 필요합니다.")
    else:
        # 부모 1 선택
        parent1_name = st.selectbox("부모 1 선택", [c['name'] for c in st.session_state.history])
        parent1 = next(c for c in st.session_state.history if c["name"] == parent1_name)
        st.image(parent1['images'][0], caption=parent1['name'], use_container_width=True)

        # 부모 2 선택
        parent2_name = st.selectbox("부모 2 선택", [c['name'] for c in st.session_state.history if c['name'] != parent1_name])
        parent2 = next(c for c in st.session_state.history if c["name"] == parent2_name)
        st.image(parent2['images'][0], caption=parent2['name'], use_container_width=True)

        # 합성 버튼
        if st.button("💞 생명체 조합"):
            # 부모 데이터 가져오기
            c1_data = parent1["creature_data"]
            c2_data = parent2["creature_data"]

            # 단순 조합 로직: 각 특성을 반반 섞음
            new_creature = {
                "type": random.choice([c1_data["type"], c2_data["type"]]),
                "size": random.choice([c1_data["size"], c2_data["size"]]),
                "pose": random.choice([c1_data["pose"], c2_data["pose"]]),
                "environment": list(set(c1_data["environment"] + c2_data["environment"])),
                "colors": list(set(c1_data["colors"] + c2_data["colors"])),
                "features": list(set(c1_data["features"] + c2_data["features"])),
                "abilities": list(set(c1_data["abilities"] + c2_data["abilities"]))
            }

            # 프롬프트 생성
            full_prompt = "This creature has the following characteristics: " + "; ".join(
                [f"{k}: {', '.join(v) if isinstance(v, list) else v}" for k,v in new_creature.items()]
            )

            with st.spinner("합성 이미지 생성 중..."):
                images = get_prompt_images(full_prompt)

            with st.spinner("이름과 설명 생성 중..."):
                kor_name, description = generate_name_and_description(full_prompt)

            st.success("💫 생명체 조합 완료!")
            st.subheader(f"🧬 이름: {kor_name}")
            st.markdown(f"**설명:** {description}")

            for img in images:
                st.image(img, use_container_width=True)

            # 합성 결과를 history에 저장
            st.session_state.history.insert(0, {
                "name": kor_name,
                "description": description,
                "images": images,
                "creature_data": new_creature
            })

            if len(st.session_state.history) > 5:
                st.session_state.history = st.session_state.history[:5]
