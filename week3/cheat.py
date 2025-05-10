import streamlit as st
from ollama import chat

# set page info
st.set_page_config(page_title='Test')
st.title("My Personal Assistant")

# create chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# accept user input
if prompt := st.chat_input("Please Write the word"):
    # add user message to chat history
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    # display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # display assistant response
    with st.chat_message("PlayerBot"):
        placeholder = st.empty()
        response = ""
        stream = chat(
            model='gemma3:12b',
            messages = [
                {"role": "system", "content": "너는 끝말잇기 전문가야. 사용자가 제시한 마지막 글자로 시작하는 단어를 제시해. "
                    "너는 끝말잇기 전문가야. "
                    "항상 사용자가 마지막으로 입력한 단어의 마지막 글자로 시작하는 단어를 제시해야해.전에 사용했던 단어를 사용해서는 안돼."
                    "예시: '강아지' → '지갑', '고양이' → '이발소'. "
                    "반드시 사용자의 마지막 글자에 집중해서 답변해. 한글자로 답하면 규칙을 어긴거야. 네가 만든 단어의 첫글자의 초성이 'ㄹ'이면 'ㅇ'으로 바꿀 수 있어"
                    "만약 사용자가 한 말이 규칙에 어긋나면 '규칙에 맞지 않습니다.'라고 정확하게 답변해. 만약 네가 한말이 규칙에 어긋나면 '제가 졌습니다.' 라고 말해."
                    "한국어로만 대답하고, 두 글자 이상의 한 단어로만 답해."}, {'role': 'user', 'content': prompt},
                *[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            ],
            stream=True
        )
        for chunk in stream:
            response += chunk.message.content
            placeholder.markdown(response)
    # add assistant message to chat history 
    st.session_state.messages.append({"role": "assistant", "content": response})
