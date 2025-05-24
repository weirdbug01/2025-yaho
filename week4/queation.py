import uuid
import ollama
import streamlit as st
from utils import check_ollama

# 모델 초기화
if "model_qt" not in st.session_state:
    check_ollama()
    st.session_state.model_qt = ""

# 학년 및 키워드 기반 system_prompt 자동 생성
grades = [
    "초등학교 1학년", "초등학교 2학년", "초등학교 3학년", "초등학교 4학년",
    "초등학교 5학년", "초등학교 6학년",
    "중학교 1학년", "중학교 2학년", "중학교 3학년",
    "고등학교 1학년", "고등학교 2학년", "고등학교 3학년"
]

with st.sidebar:
    st.sidebar.title("Settings")

    # 모델 선택
    models = [model['model'] for model in ollama.list()["models"]]
    st.session_state.model_qt = st.sidebar.selectbox(
        "Choose your model", 
        models,
        help="모델을 선택하세요.",
    )

    # 학년 선택
    grade = st.sidebar.selectbox("학년을 선택하세요", grades)

    # 문제 키워드 입력
    keyword = st.sidebar.text_input("문제 키워드", placeholder="예: 분수, 과거시제, 광합성")

    # 학년 + 키워드 포함한 시스템 프롬프트 자동 생성
    base_prompt = f"너는 {grade} 수준의 선생님이야. "
    if keyword:
        base_prompt += f"{keyword}'와 관련된 내용을 기반으로 {grade} 수준의 시험문제를 만들어줘. "
    else:
        base_prompt += f"{grade} 수준의 시험문제를 만들어줘. "
    base_prompt += "문제만 내고 해석, 정답, 힌트는 절대 알려주지 마. 서술형 문제는 내지마. 답은 반드시 보기 중 하나로 만들어줘. 보기는 5개야."


    system_prompt = st.sidebar.text_area(
        "System Prompt",
        value=base_prompt,
        help="시스템 프롬프트는 모델의 행동을 조절합니다."
    )

# 채팅 히스토리 초기화
if "chats_qt" not in st.session_state:
    st.session_state.chats_qt = {}
if "current_chat_id_qt" not in st.session_state:
    st.session_state.current_chat_id_qt = None

with st.sidebar:
    if st.session_state.chats_qt:
        st.sidebar.markdown("---")
        st.sidebar.title("Chat History")
        if st.sidebar.button("➕ New Chat", type="tertiary"):
            chat_id_qt = str(uuid.uuid4())
            st.session_state.chat_qt[chat_id_qt] = {
                "name": f"새로운 채팅",
                "messages": [{"role": "system", "content": system_prompt}]
            }
            st.session_state.current_chat_id_qt = chat_id_qt

        # 채팅 목록 버튼 생성
        for cid, chat_info in st.session_state.chats_qt.items():
            if st.sidebar.button(chat_info["name"], key=f"chat_{cid}", type="tertiary"):
                st.session_state.current_chat_id_qt = cid

# 현재 채팅 ID
chat_id_qt = st.session_state.current_chat_id_qt

# 채팅 화면
if chat_id_qt:
    chat = st.session_state.chats_qt[chat_id_qt]
    st.title(chat["name"])

    for message in chat["messages"]:
        if message['role'] != "system":
            with st.chat_message(message['role']):
                st.markdown(message['content'])
else:
    st.title("오늘의 아젠다는 무엇인가요?")

# 문제 생성 버튼 (텍스트 입력과 별개)
if st.button("문제 생성"):
    chat_id_qt = str(uuid.uuid4())
    st.session_state.current_chat_id_qt = chat_id_qt
    st.session_state.chats_qt[chat_id_qt] = {
        "name": f"{grade} - {keyword if keyword else '문제'}",
        "messages": [{"role": "system", "content": system_prompt}]
    }
    chat = st.session_state.chats_qt[chat_id_qt]

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = ""
        stream = ollama.chat(
            model=st.session_state.model_qt,
            messages=[{"role": m["role"], "content": m["content"]} for m in chat["messages"]],
            stream=True
        )
        for chunk in stream:
            response += chunk.message.content
            placeholder.markdown(response)

    chat["messages"].append({"role": "assistant", "content": response})

# 기존 텍스트 입력 (유저 자유 대화)
if prompt := st.chat_input("Write something"):

    if chat_id is None:
        chat_id = str(uuid.uuid4())
        st.session_state.current_chat_id_qt = chat_id_qt
        st.session_state.chats_qt[chat_id_qt] = {
            "name": f"새로운 채팅",
            "messages": [{"role": "system", "content": system_prompt}]
        }
        chat = st.session_state.chats_qt[chat_id]

    chat["messages"].append({'role': 'user', 'content': prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = ""
        stream = ollama.chat(
            model=st.session_state.model_qt,
            messages=[{"role": m["role"], "content": m["content"]} for m in chat["messages"]],
            stream=True
        )
        for chunk in stream:
            response += chunk.message.content
            placeholder.markdown(response)

    chat["messages"].append({"role": "assistant", "content": response})

    # 채팅 제목 자동 생성 (기존 코드 유지)
    if len(chat["messages"]) == 3:
        summary_prompt = [
            {"role": "system", "content": "You are a helpful assistant that creates concise chat titles."},
            {"role": "user", "content": 
                f"Generate a short (max 5 words) title summarizing the conversation:\nUser: {chat['messages'][1]['content']}\nAssistant: {chat['messages'][2]['content']}"
            }
        ]
        try:
            new_title = ""
            stream = ollama.chat(
                model=st.session_state.model_qt,
                messages=summary_prompt,
                stream=True,
            )
            for chunk in stream:
                new_title += chunk.message.content
            chat["name"] = new_title
        except:
            pass

        st.rerun()
