import streamlit as st

# 添加一个标题
st.set_page_config(
    page_title="CMakeLists.txt生成器",
    page_icon="🔧",
    layout="wide"
)
st.title("CMakeLists.txt Generator")

with st.sidebar:
    st.header("项目配置")
    project_name = st.text_input("项目名称", value="MyProject")
    project_version = st.text_input("项目版本", value="1.0.0")
    project_type = st.selectbox(
        "项目类型",options=["可执行文件","静态库","动态库"],index=0
    )
    cpp_standard = st.selectbox(
        "C++标准", options=["11","14","17","20"],index=2
    )
    st.header("源码文件")
    source_files = st.text_area(
        "源码文件（每行一个）",value="src/main.cpp\\nsrc/utils.cpp"
    ).split("\\n")
    source_files = [f.strip() for f in source_files if f.strip()] #?
    st.header("头文件目录")
    include_dirs = st.text_area(
        "头文件目录（每行一个）",
        value="include"
    ).split("\\n")
    include_dirs = [d.strip() for d in include_dirs if d.strip()]

def generate_cmake():
    cmake_content = f"# CMakeLists.txt for {project_name}\\n"
    cmake_content += "cmake_minimum_required(VERSION 3.10)\\n\\n"
    cmake_content += f"project({project_name} VERSION {project_version})\\n\\n"
    cmake_content += f"set(CMAKE_CXX_STANDARD {cpp_standard})\\n"
    cmake_content += "set(CMAKE_CXX_STANDARD_REQUIRD ON)\\n\\n"
    if project_type == "可执行文件":
        cmake_content += f"add_executeable({project_name} \\n"
    elif project_type == "静态库":
        cmake_content += f"add_library({project_name} STATIV \\n"
    elif project_type == "动态库":
        cmake_content += f"add_library({project_name} SHARED \\n"

    for f in source_files:
        cmake_content += f"    {f}\\n"
    cmake_content += ")\\n\\n"

    if include_dirs:
        cmake_content += f"target_include_directories({project_name} PRIVATE \\n"
        for d in include_dirs:
            cmake_content += f"    {d}\\n"
        cmake_content += ")\\n"
    return cmake_content

cmake_text = generate_cmake()

st.subheader("CMakeLists.txt 预览")
st.code(cmake_text, language="cmake", line_numbers=True)
st.download_button(
    label="下载CMakeLists.txt",
    data=cmake_text,
    file_name="CMakeLists.txt",
    mime="text/plain"
)