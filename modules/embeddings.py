from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def create_embeddings(texts):
    model = get_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    return embeddings