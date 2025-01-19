import streamlit as st
import pandas as pd
from src.scripts.course_manager import CourseManager

st.set_page_config(page_title="Faculty Finder URMS")
# Initialize session state
if 'course_manager' not in st.session_state:
    st.session_state.course_manager = None

# File upload
st.title("Faculty Finder URMS")
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, dtype = str)
        st.session_state.course_manager = CourseManager(df)
        st.success("File uploaded and processed successfully")
    except Exception as e:
        st.error(f"Error processing file: {e}")

# Query form
if st.session_state.course_manager is not None:
    st.header("Query Faculty")
    course_code = st.text_input("Course Code")
    section = st.text_input("Section")

    if st.button("Get Faculty"):
        if course_code and section:
            try:
                faculty_name = st.session_state.course_manager.faculty_finder(course_code, section)
                st.write(f"Faculty Name: {faculty_name}")
            except Exception as e:
                st.error(f"Error finding faculty: {e}")
        else:
            st.error("Please enter both course code and section")