import streamlit as st
from ollama import chat

def convertToInitialLetters(text):
    CHOSUNG_START_LETTER = 4352
    JAMO_START_LETTER = 44032
    JAMO_END_LETTER = 55203
    JAMO_CYCLE = 588
    
    def isHangul(ch):
        return ord(ch) >= JAMO_START_LETTER and ord(ch) <= JAMO_END_LETTER
    
    result = ""
    for ch in text:
        if isHangul(ch): #한글이 아닌 글자는 걸러냅니다.
            result += unichr((ord(ch) - JAMO_START_LETTER)/JAMO_CYCLE + CHOSUNG_START_LETTER)
        
    return result

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
                    "항상 사용자가 마지막으로 입력한 단어의 마지막 글자로 시작하는 단어를 제시해야해.전에 사용했던 단어를 사용해서는 안돼
                    "예시: '강아지' → '지갑', '고양이' → '이발소'. "
                    "반드시 사용자의 마지막 글자에 집중해서 답변해. 한글자로 답하면 규칙을 어긴거야. "
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
