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


def search_products(df, term, n=3, threshold=0):
    term_embedding = get_embedding(
        term,
        engine="text-embedding-ada-002"
    )

    df["similarity"] = df.embedding.apply(
        lambda x: cosine_similarity(x, term_embedding))

    df = df[df['similarity'] >= threshold]
    results = (
        df.sort_values("similarity", ascending=False)
        .head(n)
    )

    return results


search_term = sys.argv[1]
json_output = True if len(sys.argv) >= 3 else False

datafile_path = "./data/products_with_embedding.csv"

df = pd.read_csv(datafile_path, encoding='utf-8')
df["embedding"] = df.embedding.apply(eval).apply(np.array)

results = search_products(df, search_term, n=3, threshold=0.73)
results = results[['app_id', 'name', 'url', 'similarity']]

if json_output:
    print(json.dumps(results.to_dict('records'), ensure_ascii=False))
else:
    template = "\n  AppId:      {app_id}\n  Name:       {name}\n  URL:        {url}\n  Similarity: {similarity}\n"
    items = results.values.tolist()
    for item in items:
        print(template.format(
            app_id=item[0], name=item[1], url=item[2], similarity=item[3]))
