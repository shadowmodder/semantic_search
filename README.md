# semantic_search
semantic_text_search

#Features impletmented:

* [/search] /search/<your_search_query> e.g. for keyword "legal": http://localhost:8080/search/legal  (This loads fast)
* [/health] /health e.g.: http://localhost:8080/health 
* [/search] another endpoint with query params: http://localhost:8080/search?q=legal (Slow loading at this time)
* [/search] using search edit box, navigate to http://localhost:8080/search  use the edit box for query. (Slow loading at this time due to redirects)

# Backend implementation 
* For generating Embeddings, we are using "SentenceTransformers" (Library) https://www.sbert.net/
* Simple Flask server for API serving
* Instead of vector DB we are using Parquet files (this can be a future improvement that boosts the results)
* Data access is already abstracted - so we can switch between Vector Databases or use multiple,
* /health is implemented with DB connection health and CPU/resources utilization (can scale to include upstream and downstream services) 

#Screenshots
![Search_API](/res/assets/Search_API.png)
![Search_box](/res/assets/Search_box.png)

# ToDo: architecture that considers scaling of search application:
* Write an ADR, 
* Improve Docker performance and reduce size (Currently container is bloating due to dependancy pip installs that can be pruned)
* Load server faster when running locally - through  prod server using WSGI server /Flask.
* Add basic metrics.
* Add params to /search? e.g. Pagination from results: /search?page=1 - currently we are returning top 10 results.
* Add unit tests


1. **Microservices Architecture**: microservices architecture provides flexibility and scalability but also adds complexity, so it's essential to consider your project's specific requirements and constraints.
   - **Semantic Search Service**: This microservice would be responsible for the core semantic search functionality. It handles the vector embeddings, similarity scoring, and ranking of search results based on semantic similarity. This service can use Elasticsearch with a vector-scoring plugin or a specialized vector database.
   - **Data Ingestion Service**: To populate the search engine with data, you may have a separate microservice for data ingestion. This service preprocesses and indexes the text data, generating vector embeddings for documents and storing them in the database used by the Semantic Search Service.
   - **API Gateway**: An API gateway is the entry point for client applications. It routes requests to the appropriate microservices, such as semantic search or data ingestion, and handles authentication and load balancing.
   - **User Interface**: The frontend application communicates with the API gateway to submit search queries and retrieve search results.
   - **Authentication and Authorization Service**: If your semantic search engine requires user access control, you might have a separate service for authentication and authorization.
   - **Database**: I would abstract out a DB that includes vector embeddings and metadata.
   - **Message Queue (Optional)**: In a high-throughput scenario, you can use a message queue to decouple tasks like data ingestion and indexing from the search service.

2. **Vector Embeddings**:
3. **Semantic Search Algorithm**:
   - Implement a semantic search algorithm that computes the similarity between query vectors and document vectors using methods like cosine similarity or dot product. Rank the documents by similarity score.
   - Depending on the size of data and the complexity of the search, indexing, caching, or more efficient data structures to speed up search operations.

4. **Data Preprocessing**:
   - Implement data preprocessing steps to clean and tokenize text data, remove stopwords, and handle stemming or lemmatization.

5. **Scalability and Load Balancing**:
   - Ensure that your microservices are designed for scalability and can handle increased load. You can use container orchestration tools like Kubernetes to manage and scale your microservices.

6. **Monitoring and Logging**:
   - Implement Prometheus and Grafana can help with this.

7. **Caching  and compression**:
   - Redis
   - Transferring a large amount of data from the server to the client,  compressing the data before sending it over the network.

8. **Asynchronous Processing**: 
   - If search operations involve heavy computation, offloading the search to a background task or worker. Return an initial response to the user and update the results when they are ready.

9. **Profiling**
10. **CDN**
11. **Load testing and dedicated DB conn pools**
12. **Continuous Integration/Continuous Deployment (CI/CD)**:
   - ArgoCD pipeline for this gitops pattern
13. **Security**:
   - Search engine deals with sensitive data SSL/data encryption, secure APIs, and access control.

