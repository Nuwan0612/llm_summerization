from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
import os
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

# from langchain_core.prompts import ChatPromptTemplate
# from langchain.docstore.document import Document
# from typing_extensions import Concatenate

load_dotenv()

llm = ChatAnthropic(temperature=0.7, api_key=os.environ.get("ANTHROPIC_API_KEY"), model_name="claude-3-opus-20240229")

# get the content of pdf files
def get_pdf_files(pdf_docs):
  pdfReader = PdfReader(pdf_docs)

  text=''

  for i, page in enumerate(pdfReader.pages):
    content = page.extract_text()
    if content:
      text+=content

  return text

#Split te text into chunks
def split_to_chuncks(text):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
  chunks = text_splitter.create_documents([text])

  return chunks

def summarize_text(chunks):
  chunks_prompt = """
  Please summerize the below speech:
  Speech: `{text}`
  Summary:
  """

  map_prompt_template = PromptTemplate(
    input_variables=['text'],
    template = chunks_prompt
  )

  final_combine_prompt = """
  Provide a final summary of the entire speech with these important points.Add a Generic Title,
  Start the precise summary with an introduction and provide the summary in number points for the speech.
  Speech: `{text}`
  Summary: 
  """

  final_combine_prompt_template = PromptTemplate(
    input_variables = ['text'],
    template = final_combine_prompt
  )

  summary_chain = load_summarize_chain(
    llm=llm,
    chain_type='map_reduce',
    map_prompt=map_prompt_template,
    combine_prompt=final_combine_prompt_template, 
    verbose=False
  )

  output = summary_chain.invoke(chunks)

  return output
