class EmbedModel(ModelGeneral):
    def __init__(self):
        self.table = "embeddings"

    def insert_embed(self,data):
        return self.insert({
            "chunk_id": data.chunk_id,
            "embedding": data.embedding,
            "model": data.model,
            "dimension": data.dimension
        })