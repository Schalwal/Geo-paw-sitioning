import streamlit as st
from PIL import Image
from utils import init

init()
st.title("Geo-:pink[paw]-sitioning")

st.markdown(
    "[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/Schalwal/Geo-paw-sitioning)"
)

image = Image.open("images/gentle.jpg")

st.image(image, use_column_width=True)

code = """
# install

pip install streamlit
"""

st.code(code, language="bash", line_numbers=False)
