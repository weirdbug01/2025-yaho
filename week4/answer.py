import uuid

import ollama
import streamlit as st

from utils import check_ollama


# 모델 초기화
if "model_an" not in st.session_state:
    check_ollama()
    st.session_state.model_an = ""

# 설정 표시
with st.sidebar:
    st.sidebar.title("Settings")
    # 모델 목록 가져오기
    models = [model['model'] for model in ollama.list()["models"]]
    st.session_state.model_in = st.sidebar.selectbox(
        "Choose your model", 
        models,
        help="모델을 선택하세요.",
    )

    # 시스템 프롬프트
    system_prompt = st.sidebar.text_area(
        "System Prompt",
        value="너는 선생님이야. 사용자가 입력한 문제를 풀어서 상세하게 알려줘. ",
        help="시스템 프롬프트는 모델의 행동을 조절합니다."
    )

# 채팅 히스토리 초기화
if "chats_an" not in st.session_state:
    st.session_state.chats_an = {}
if "current_chat_id_an" not in st.session_state:
    st.session_state.current_chat_id_an = None

with st.sidebar:
    # 새로운 채팅 생성 버튼
    if st.session_state.chats_an:
        st.sidebar.markdown("---")
        st.sidebar.title("Chat History")
        if st.sidebar.button("➕ New Chat", type="tertiary"):
            chat_id_an = str(uuid.uuid4())
            st.session_state.chats_an[chat_id_an] = {
                "name": f"새로운 채팅",
                "messages": [{"role": "system", "content": system_prompt}]
            }
            st.session_state.current_chat_id_an = chat_id_an

        # 채팅 히스토리 표시 버튼
        for cid, chat_info in st.session_state.chats_an.items():
            if st.sidebar.button(chat_info["name"], key=f"chat_{cid}", type="tertiary"):
                st.session_state.current_chat_id_an = cid_an

# 처음 시작할 때 채팅 기록이 없으면 새로운 채팅 자동 생성
chat_id_an = st.session_state.current_chat_id_an

# 채팅 기록 표시
if chat_id_an:
    chat_an = st.session_state.chats_an[chat_id_an]
    st.title(chat["name"])

    # 이전 기록에서 채팅 메시지 표시
    for message in chat["messages"]:
        if message['role'] != "system":
            with st.chat_message_an(message['role']):
                st.markdown(message['content'])
else:
    st.title("오늘의 아젠다는 무엇인가요?")

# 유저 프롬프트 입력
if prompt := st.chat_input("Write something"):

    # 신규 채팅인 경우, 채팅 ID 생성
    if chat_id_an is None:
        chat_id_an = str(uuid.uuid4())
        st.session_state.current_chat_id_an = chat_id_an
        st.session_state.chats_an[chat_id_an] = {
            "name": f"새로운 채팅",
            "messages": [{"role": "system", "content": system_prompt}]
        }
        chat = st.session_state.chats_an[chat_id_an]

    # 채팅 히스토리에 사용자 입력 추가 후 표시
    chat["messages"].append({'role': 'user', 'content': prompt})
    with st.chat_message_an("user"):
        st.markdown(prompt)

    # 인공지능의 응답 생성 및 추가
    with st.chat_message_an("assistant"):
        placeholder = st.empty()
        response = ""
        stream = ollama.chat(
            model=st.session_state.model_an,
            messages = [
                {"role": m["role"], "content": m["content"]}
                for m in chat["messages"]
            ],
            stream=True
        )
        for chunk in stream:
            response += chunk.message.content
            placeholder.markdown(response)
    
    chat["messages"].append({"role": "assistant", "content": response})

    # 채팅 제목 생성 및 수정
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
                model=st.session_state.model_an,
                messages=summary_prompt,
                stream=True,
            )
            for chunk in stream:
                new_title += chunk.message.content
            chat["name"] = new_title
        except:
            pass

        st.rerun()


