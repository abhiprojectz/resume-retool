import requests
from retry import retry
import textwrap
import PyPDF2
import pandas as pd
from sentence_transformers.util import semantic_search
import torch
from datasets import load_dataset
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = "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"

api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages) 

        for page_num in range(num_pages):
            page = reader.pages[page_num] 
            text += page.extract_text()

    return text


def semantic_matching(paragraph, text_list):
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    paragraph_tokens = tokenizer.tokenize(paragraph.lower())
    text_list_tokens = [tokenizer.tokenize(text.lower()) for text in text_list]

    paragraph_str = ' '.join(paragraph_tokens)
    text_list_str = [' '.join(tokens) for tokens in text_list_tokens]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([paragraph_str] + text_list_str)

    similarity_scores = cosine_similarity(vectors[0], vectors[1:]).flatten()

    most_similar_index = similarity_scores.argmax()

    return text_list[most_similar_index]



def extract_pages_pdf(pdf_path):
    text_list = []
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            text_list.append(text)

    return text_list


@retry(tries=3, delay=10)
def query(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts})
    result = response.json()
    if isinstance(result, list):
      return result
    elif list(result.keys())[0] == "error":
      raise RuntimeError(
          "The model is currently loading, please re-run the query."
          )



def build_embeddings(_file_path):
  txt = extract_text_from_pdf(_file_path)
  chunks = textwrap.wrap(txt, 4000)
  output = query(chunks)

  csv_ = _file_path.split(".")[0] + '.csv'

  # Save the embeddings to disk
  embeddings = pd.DataFrame(output)
  embeddings.to_csv(csv_, index=False)
  print("Embeddings saved to disk...")



def search_query(text, _file_path, txt):
  chunks = textwrap.wrap(txt, 4000)
  csv_ = _file_path.split(".")[0] + '.csv'

  pdf_index = load_dataset("csv", data_files = csv_)
  embeddings = torch.from_numpy(pdf_index["train"].to_pandas().to_numpy()).to(torch.float)
  question = [text]
  query_embeddings = torch.FloatTensor(query(question))

  hits = semantic_search(query_embeddings, embeddings, top_k=2)
  results = [chunks[hits[0][i]['corpus_id']] for i in range(len(hits[0]))]

  if len(results[0]) > 9000:
    results[0] = results[0][:9000]
  return results[0]

