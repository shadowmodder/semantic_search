import pandas as pd

# Load the Parquet file
parquet_filename = "data_with_embeddings.parquet"
df = pd.read_parquet(parquet_filename)

# Example: Accessing the first few rows
print(df.head())

# Example: Accessing metadata (filename) for a specific row
index_to_check = 2400  # Replace with the index you want to check
print("Text Chunk:", df.at[index_to_check, "Chunk"])
print("Filename:", df.at[index_to_check, "Filename"])
print("Embeddings:", df.at[index_to_check, "Embedding"])