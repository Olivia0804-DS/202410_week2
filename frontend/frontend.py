# frontend/app.py
import streamlit as st
import requests

# 设置页面配置
st.set_page_config(
    page_title="Python Learning Assistant",
    page_icon="🐍",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a Bug': 'https://www.example.com/bug',
        'About': 'This is a Python Learning Assistant application.'
    }    
)

# 初始化session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

def send_message(message):
    """发送消息并获取响应"""
    try:
        response = requests.get(f"http://backend:5000/chat", params={"message": message})
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def main():
    st.title("Python Learning Assistant 🐍")
    
    # 创建两列布局
    left, right = st.columns(2)
    
    with left:
        # 显示聊天历史
        for message in st.session_state.messages:
            if message["is_user"]:
                st.info(f"You: {message['text']}")
            else:
                st.success(f"Assistant: {message['text']}")
        
        # 用户输入区域
        input_col, space, button_col = st.columns([7,1,2])
        
        with input_col:
            user_input = st.text_input("Ask something:")
        
        with button_col:
            send_clicked = st.button("Send")
        
        # 处理发送逻辑
        if send_clicked and user_input:
            # 添加用户消息
            st.session_state.messages.append({
                "is_user": True,
                "text": user_input
            })
            
            # 获取响应
            response = send_message(user_input)
            if response:
                st.session_state.messages.append({
                    "is_user": False,
                    "text": response['response']
                })
            st.rerun()
    
    with right:
        # Quick Python Examples
        st.subheader("Quick Python Examples")
        with st.expander("List Operations", expanded=False):
            st.code("""
            numbers = [1, 2, 3, 4, 5]
            numbers.append(6)      # Add to end
            numbers.pop()         # Remove last
            numbers.insert(0, 0)  # Insert at position
            """)
        st.write("---")
        with st.expander("Dictionary Operations", expanded=True):
            st.code("""     
            person = {'name': 'Alice', 'age': 25}
            person['city'] = 'Beijing'  # Add new key
            del person['age']          # Remove key
            """)
        
        with st.expander("Function Example", expanded=True):
            st.code("""
            def greet(name):
                return f"Hello, {name}!"

                # Call the function
                message = greet("World")
            """)

        # Recent History
        st.subheader("Recent History")
        if st.session_state.messages:
            for msg in st.session_state.messages[-5:]:  # 显示最近5条消息
                if msg["is_user"]:
                    st.text(f"Q: {msg['text']}")
                else:
                    st.text(f"A: {msg['text']}")

if __name__ == "__main__":
    main()