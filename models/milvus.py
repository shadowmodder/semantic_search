from pymilvus import connections, FieldSchema, CollectionSchema, DataType, IndexType
from pymilvus_orm import Collection, utility
import numpy as np

class MilvusClient:
    def __init__(self):
        # ToDo - move these to sops pattern to remove keys from code.
        milvus_server_address = "https://in03-96fad67f16b625d.api.gcp-us-west1.zillizcloud.com"
        api_key = "42b6893a9c0f4e610c0a51845841cdff55a0543672d02d709ada192eb37e80dc981206d20d120098c849b9102939944affefcd3f"

        connections.add_connection(
        default={ "uri": milvus_server_address}
        )
        connections.list_connections()
        connections.connect(uri=milvus_server_address, api_key=api_key)



        self.collection = self.create_or_load_collection()

    def create_or_load_collection(self):
        collection_name = "text_embeddings"
        dimension = 768  # Adjust this based on the dimensionality of your embeddings

        if utility.has_collection(collection_name):
            return Collection(collection_name)
        
        # Define the collection schema
        fields = [
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dimension),
            FieldSchema(name="filename", dtype=DataType.STRING),
            FieldSchema(name="context", dtype=DataType.STRING)
        ]
        collection_schema = CollectionSchema(fields=fields, description="Text Embeddings")

        # Create the collection
        collection = Collection(collection_schema, collection_name=collection_name)
        
        # Create an index on the collection
        index_params = {"index_type": IndexType.IVF_FLAT, "metric_type": "L2", "params": {"nlist": 16384}}
        index = collection.create_index(index_params=index_params)
        
        return collection

    def insert_data(self, ids, embeddings, filenames, context):
        # Insert data into the collection
        data = {
            "embedding": embeddings,
            "filename": filenames,
            "context": context
        }
        self.collection.insert(data=data, ids=ids)

    def search(self, query_embedding, limit=10):
        # Search for similar embeddings
        results = self.collection.search(data={"embedding": [query_embedding]}, anns_field="embedding", param={"nprobe": 32}, limit=limit)
        return results

    def get_all_data(self):
        # Retrieve all data (embeddings, filenames, context) from the collection
        data = self.collection.query([], output_fields=["embedding", "filename", "context"])
        return data
