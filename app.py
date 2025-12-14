import streamlit as st

# 添加一个标题
st.title("我的第一个 Streamlit 应用")

# 添加一个滑块，返回用户选择的值
x = st.slider("请选择一个数字", 0, 100, 50)

# 显示计算结果
st.write(f"你选择的数字是 {x}，它的平方是 {x**2}")