# https://github.com/openai/openai-cookbook/blob/66b988407d8d13cad5060a881dc8c892141f2d5c/examples/Obtain_dataset.ipynb

import os
import openai
import pandas as pd
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

df = pd.read_csv('./data/products.csv')
embedding_model = "text-embedding-ada-002"

# You would probably need to tokenize the descriptions first

df["embedding"] = df["description"].apply(
    lambda c: get_embedding(c, engine=embedding_model))

df.to_csv("./data/products_with_embedding.csv")
