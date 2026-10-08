import faiss
import numpy as np

from modules.embeddings import create_embeddings


class VectorStore:

    def __init__(self):
        self.index = None
        self.documents = []

    def build(self, documents):
        self.documents = documents

        if not documents:
            self.index = None
            return

        texts = [doc["text"] for doc in documents]

        embeddings = create_embeddings(texts)

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

    def search(self, question, top_k=3):

        if self.index is None:
            return []

        question_embedding = create_embeddings([question])

        question_embedding = np.asarray(
            question_embedding,
            dtype="float32"
        )

        faiss.normalize_L2(question_embedding)

        k = min(top_k, len(self.documents))

        scores, indexes = self.index.search(
            question_embedding,
            k
        )

        results = []

        for score, index in zip(scores[0], indexes[0]):

            if index < 0:
                continue

            document = self.documents[index].copy()

            document["score"] = float(score)

            results.append(document)

        return results