import streamlit as st

def create_download_button(markdown_string, filename):
    # Convert the Markdown string to bytes
    markdown_bytes = markdown_string.encode('utf-8')

    # Create a download button
    st.download_button(
        label="Download Markdown",
        data=markdown_bytes,
        file_name=filename,
        key='download_button'
    )