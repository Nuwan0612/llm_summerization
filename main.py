import streamlit as st
import app as langchain_app_backend
from htmlTemplate import css, bot_template


def main():
  
  st.set_page_config(page_title="Summarization")
  st.write(css, unsafe_allow_html=True)
  st.header("Summarization of PDF's")
  
  with st.sidebar:
    st.subheader("Your documents")
    pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Summarize'")

    if st.button("Summarize"):
      if pdf_docs:
        with st.spinner("Processing"):
          #get pdf text
          content = langchain_app_backend. get_pdf_files(pdf_docs)
          st.write(content)
          print(content)
          # create the chuncks
          # chunks = langchain_app_backend.split_to_chuncks(content)
          
          # #Summerized text
          # output = langchain_app_backend.summarize_text(chunks)
          # st.session_state['output'] = output
      else:
        st.write("Please upload the document")
        
  if 'output' in st.session_state:
    output = st.session_state['output']
    st.write(bot_template.replace("{{MSG}}", output['output_text']), unsafe_allow_html=True)
        

if __name__ == "__main__":
  main()