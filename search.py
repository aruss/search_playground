# https://github.com/openai/openai-cookbook/blob/main/examples/Semantic_text_search_using_embeddings.ipynb

import sys
import json
import os
import openai
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding, cosine_similarity

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def search_products(df, term, n=3):
    term_embedding = get_embedding(
        term,
        engine="text-embedding-ada-002"
    )
    df["similarity"] = df.embedding.apply(
        lambda x: cosine_similarity(x, term_embedding))

    results = (
        df.sort_values("similarity", ascending=False)
        .head(n)
    )

    return results



search_term = sys.argv[1]
datafile_path = "data/products_with_embedding.csv"

df = pd.read_csv(datafile_path)
df["embedding"] = df.embedding.apply(eval).apply(np.array)

results = search_products(df, search_term, n=1)
results = results[['name', 'link', 'image_url']]
data = results.to_dict('records')
json_data = json.dumps(data)
print(json_data)

