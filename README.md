# 🛒 CommerceIQ — E-commerce Analytics & AI Platform

CommerceIQ is an end-to-end **e-commerce analytics and AI platform** that combines business analytics, machine learning, NLP, RAG, LLMs, tool calling, AI agents, multimodal AI, and LLMOps into a single application.

The project was built to demonstrate how raw e-commerce transaction data can be transformed into **business insights, predictive models, semantic search, and an AI-powered analytics assistant**.

## 🌐 Live Demo

🔗 **[Try CommerceIQ](https://commerceiq-ezycwwuc3ix2h3hnjuyuxr.streamlit.app/)**


---

## 📌 Project Overview

CommerceIQ works with e-commerce transaction data and provides:

* Business and revenue analytics
* Customer and product analysis
* RFM-based customer segmentation
* Customer repurchase prediction
* Product NLP and semantic search
* Retrieval-Augmented Generation (RAG)
* LLM-powered business question answering
* Tool calling
* Multi-step AI agent workflows
* LoRA fine-tuning experiments
* QLoRA and DPO workflow exploration
* Multimodal AI analysis
* Evaluation and LLMOps monitoring
* REST API for application access
* Custom CSV dataset upload

The system is designed around a **FastAPI backend + Streamlit frontend**, with Groq-hosted LLM inference.

---

# 🔄 Project Workflow

## 1. 📊 Data Understanding & Business Analytics

The project begins with transaction-level e-commerce data containing:

* Invoice information
* Products
* Quantities
* Prices
* Customers
* Dates
* Countries

The data was cleaned and transformed into customer, product, and order-level analytical datasets.

Business metrics include:

* Revenue
* Orders
* Units sold
* Average Order Value
* Customer activity
* Product performance
* Country-level revenue
* Monthly revenue trends
* RFM customer segmentation

The cleaned production datasets contain:

* **4,335 identifiable customers**
* **3,918 products**
* **19,865 orders**
* **5.56M units**
* **£10.03M net product revenue**

---

## 2. 🤖 Classical Machine Learning

A temporal customer repurchase prediction problem was created to predict whether customers would make a future purchase.

Models evaluated included:

* Logistic Regression
* Random Forest
* XGBoost

The final Random Forest model achieved approximately:

* **F1 Score: 0.58**
* **ROC-AUC: 0.73**

The model selection focused on the business relevance of identifying customers likely to repurchase rather than relying only on accuracy.

---

## 3. 🧠 Transformer & NLP

Product descriptions were processed using Transformer-based embeddings.

A DistilBERT model was used to generate **768-dimensional product representations**.

A lightweight keyword-based category classifier was also developed as a baseline.

Results:

* Category classification accuracy: **~69%**
* Macro F1: **~0.47**

The NLP pipeline enables products to be represented semantically rather than relying only on exact keyword matching.

---

## 4. 🔎 RAG & Semantic Search

CommerceIQ implements a retrieval pipeline using:

* Sentence Transformers
* FAISS
* Cosine similarity
* Cross-encoder reranking

The retrieval knowledge base contains approximately **28K documents**, including:

* Customer profiles
* Product profiles
* Order summaries
* Business summaries

The system retrieves relevant business context before sending information to the LLM.

Defined evaluation results:

* **Retrieval evaluation: 100%**
* **Reranking evaluation: 80%**

These results are based on the project's predefined evaluation datasets and test cases, not a guarantee of performance on unseen production data.

---

## 5. 💬 LLM Integration

CommerceIQ uses the Groq API with:

`openai/gpt-oss-20b`

The LLM receives retrieved business context and generates structured responses containing:

* **Answer**
* **Evidence**
* **Business Implication**

Grounding rules were implemented to reduce unsupported claims and keep responses tied to the available business data.

---

## 6. 🛠️ Tool Calling & AI Agent

The LLM can select and use business tools such as:

* `lookup_customer`
* `lookup_product`
* `revenue_summary`
* `top_revenue_products`

A multi-step CommerceIQ agent was then built around these tools.

The agent can:

1. Understand the user's question
2. Decide which tool is required
3. Execute the tool
4. Store the returned evidence
5. Decide whether additional information is required
6. Generate a grounded final response

Defined evaluation results:

* **Tool calling: 100%**
* **Agent workflow: 100%**

These scores are based on the project's predefined test cases.

---

## 7. 🎯 Fine-Tuning Experiments

CommerceIQ also explores parameter-efficient LLM adaptation.

### LoRA

A small instruction model was adapted using LoRA.

Base model:

`Qwen/Qwen2.5-0.5B-Instruct`

Total parameters:

**~494M**

Trainable LoRA parameters:

**~1.08M**

Approximately **0.22% of the model parameters** were trainable.

The CPU experiment demonstrated parameter-efficient adaptation, although it did **not improve the project's factual evaluation score**.

### QLoRA

The project also documents and prepares the workflow for:

* 4-bit quantization
* NF4
* Double quantization
* LoRA adapters
* Mixed precision

Full QLoRA training was not executed because the available environment did not provide CUDA acceleration.

### DPO

A preference dataset containing **50 prompt/chosen/rejected examples** was prepared for Direct Preference Optimization.

The DPO training workflow was explored, but full DPO training was not executed because of the CPU-only environment.

---

## 8. 🖼️ Multimodal AI

CommerceIQ includes a multimodal experiment using a vision-capable LLM.

The system analyzes a **synthetic product card** containing product and business information.

The model was able to combine:

* Visual information
* Product information
* Revenue information
* Stock information
* Category information

The multimodal evaluation achieved **6/6 on the defined test cases**.

This demonstrates multimodal business reasoning rather than physical product-image recognition.

---

## 9. 📈 Evaluation & LLMOps

CommerceIQ includes an evaluation framework covering multiple components.

| Component        | Result |
| ---------------- | -----: |
| Retrieval        |   100% |
| Reranking        |    80% |
| Tool Calling     |   100% |
| AI Agent         |   100% |
| Grounding        |   100% |
| Multimodal       |   100% |
| Response Quality |   100% |

These results are from predefined datasets/test cases created for the project.

### LLMOps

The application records LLM request information such as:

* Request ID
* Timestamp
* Model
* Latency
* Input tokens
* Output tokens
* Tool calls
* Request status
* Errors

Real Groq inference requests were monitored during development.

The project also separates development/debugging logs from production-style monitoring metadata.

---

# 🏗️ Architecture

```text
                         User
                           │
                           ▼
                    Streamlit Frontend
                           │
                           ▼
                     FastAPI Backend
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       Business Analytics          AI Agent
              │                         │
              │                  ┌──────┴──────┐
              │                  │             │
              ▼                  ▼             ▼
        Data / Features       Tools         Retrieval
                                   │             │
                                   └──────┬──────┘
                                          ▼
                                      RAG Context
                                          │
                                          ▼
                                    Groq LLM
                                          │
                                          ▼
                                  Grounded Response
```

The backend keeps API credentials outside the source code and provides a REST API for the frontend.

---

# 🚀 API

The FastAPI backend provides endpoints including:

### Health

`GET /health`

Checks whether the API is running.

### Customer

`GET /customer/{customer_id}`

Returns customer-level analytics.

### Product

`GET /product/{stock_code}`

Returns product-level analytics.

### Revenue

`GET /revenue`

Returns overall business revenue metrics.

### Top Products

`GET /top-products`

Returns the highest-revenue merchandise products.

### AI Analyst

`POST /ask`

Accepts a business question and returns an AI-generated grounded response.

### Dataset Upload

`POST /upload-dataset`

Accepts a compatible CSV file and processes it through the dataset management pipeline.

---

# ☁️ Deployment

CommerceIQ is deployed using a split architecture:

### Frontend

**Streamlit Community Cloud**

Provides the interactive analytics interface.

### Backend

**AWS EC2**

Hosts the FastAPI application and Docker container.

### Containerization

The backend is packaged using Docker and stored in **Amazon ECR** before deployment to EC2.

### AI Inference

LLM inference is performed through the **Groq API**.

The Groq API key is kept on the backend rather than exposed to the frontend.

---

# 📁 Project Structure

```text
commerceiq/
│
├── data/
│   ├── customer_features.csv
│   ├── product_features.csv
│   └── order_analytics.csv
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_business_analytics.ipynb
│   ├── 03_customer_ml.ipynb
│   ├── 04_product_nlp.ipynb
│   ├── 05_rag.ipynb
│   ├── 06_llm.ipynb
│   ├── 07_finetuning.ipynb
│   ├── 08_agent.ipynb
│   ├── 09_multimodal.ipynb
│   ├── 10_evaluation.ipynb
│   └── 11_llmops.ipynb
│
├── src/
│   ├── agent.py
│   ├── analytics.py
│   ├── api.py
│   ├── config.py
│   ├── data_loader.py
│   └── dataset_manager.py
│
├── test/
│   ├── test_analytics.py
│   ├── test_api.py
│   ├── test_data_loader.py
│   └── ...
│
├── Dockerfile
├── .dockerignore
├── .env.example
├── requirements.txt
├── streamlit_app.py
└── README.md
```

---

# 🧰 Technologies

### Programming & Data

* Python
* Pandas
* NumPy
* Scikit-learn

### Machine Learning

* Logistic Regression
* Random Forest
* XGBoost
* RFM Analysis
* SMOTE
* Temporal validation

### NLP & LLM

* Transformers
* DistilBERT
* Sentence Transformers
* FAISS
* Cross-Encoder
* RAG
* Groq API
* Qwen
* LoRA
* QLoRA concepts
* DPO workflow

### Application

* FastAPI
* Pydantic
* Streamlit
* Plotly

### Deployment & Engineering

* Docker
* AWS EC2
* Amazon ECR
* Git
* GitHub
* LLMOps logging

---

# 🧪 Testing

The project includes automated tests for important backend components and API behavior.

Testing covers areas such as:

* Data loading
* Dataset validation
* Analytics functions
* Customer lookup
* Product lookup
* Revenue calculations
* API endpoints
* Dataset upload
* Input validation
* Error handling

The backend was also tested after Docker deployment on AWS.

---

# ⚠️ Limitations

CommerceIQ is a portfolio and engineering demonstration rather than a production enterprise system.

Current limitations include:

* The primary dataset is a historical e-commerce dataset.
* Uploaded datasets are processed in memory and are not permanently stored.
* Full QLoRA training was not executed because of CPU-only hardware.
* Full DPO training was not executed.
* vLLM was studied architecturally but not deployed.
* Actual INT4 inference benchmarking was not performed.
* Multimodal testing uses a synthetic product card rather than a real product-image catalog.
* Evaluation scores are based on predefined project test cases.
* The system does not claim guaranteed performance on unseen production datasets.

---

# 🔮 Future Improvements

Potential next steps include:

* Persistent user-uploaded datasets
* Authentication and user-specific workspaces
* PostgreSQL or cloud data warehouse integration
* Automated model retraining
* Cloud-based vector database
* Full QLoRA training with GPU infrastructure
* DPO training with a larger preference dataset
* vLLM-based model serving
* Production-grade observability
* CI/CD pipeline
* More extensive evaluation datasets
* Advanced forecasting and recommendation systems

---

# 👩‍💻 Author

**Sadiya Sajid**

MTech Data Science | AI & Machine Learning


---

## ⭐ Why This Project Matters

CommerceIQ goes beyond a standalone machine learning notebook or chatbot.

It demonstrates an end-to-end workflow:

**Raw Data → Analytics → Machine Learning → NLP → Retrieval → LLM → Tool Calling → AI Agent → Multimodal AI → Evaluation → LLMOps → API → Cloud Deployment**

The goal is to show how different AI and data-science components can be integrated into a single business-oriented application.
