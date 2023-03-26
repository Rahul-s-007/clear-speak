import openai
import numpy as np

resp = openai.Embedding.create(
    input=["feline friends go", "football"], #meow
    engine="text-similarity-davinci-001")

embedding_a = resp['data'][0]['embedding']
embedding_b = resp['data'][1]['embedding']

similarity_score = np.dot(embedding_a, embedding_b)
print(similarity_score)
print((100 + (100*similarity_score))//2)