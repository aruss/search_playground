# https://github.com/openai/openai-cookbook/blob/66b988407d8d13cad5060a881dc8c892141f2d5c/examples/Obtain_dataset.ipynb

import os
import openai
import pandas as pd
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

df = pd.read_csv('./data/products.csv', encoding='utf-8')
df = df[["app_id", "name", "url", "purpose",
         "product_description", "tool_description"]]
df = df.dropna()
df["combined"] = (
    "Purpose: " + df.app_id.str.strip() + "ProductDescription" + df.product_description.str.strip() +
    "tool_description" + df.tool_description.str.strip()
)

embedding_model = "text-embedding-ada-002"

# You would probably need to tokenize the descriptions first

df["embedding"] = df["combined"].apply(
    lambda c: get_embedding(c, engine=embedding_model))

df.to_csv("./data/products_with_embedding.csv")
