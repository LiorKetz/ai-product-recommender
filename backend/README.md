# 🧠 Backend Service (FastAPI - Python)

## 🔍 Overview
The backend is the **core logic layer** of the AI Product Recommendation Agent, built with **FastAPI** in Python.  
It handles:
- Chat flow and conversation context.
- Integration with the Large Language Model (LLM).
- Product recommendation logic based on user intent.
- Conversation logging and basic performance monitoring.

---

## 🧩 Agent Architecture and Logic Strategy
The system follows a **Hierarchical Two-Step Retrieval** approach — optimizing both **token efficiency** and **recommendation accuracy**.

### 1️⃣ Initial Flow & Model Setup
- **Provider:** The backend uses the **Groq API**, chosen for its low latency and high throughput — crucial for real-time interactions.  
- **Conversation Memory:** The system ensures consistent context across multiple chat turns, maintaining a natural user experience.

### 2️⃣ Hierarchical Recommendation Flow
#### Step A: Category Identification *(The Pairing Phase)*
- **Goal:** Identify the most relevant product category based on user intent.  
- **Mapping Logic:**  
  Defined manually in `db/categories_map.py`, this mapping connects user intent → product category → dataset (`db/products.json`).  
  ⚠️ *If the product dataset changes, this map must be updated to maintain grounding accuracy.*
- **Structured Output:**  
  The model must return:
  ```json
  {
    "Answer": "<short message to the user>",
    "ready_to_filter": <true or false>,
    "selected_category": "<category name or null>"
  }
  ```

The process proceeds to Step B only when a valid category is identified.

#### Step B: Product Selection *(The Grounding Phase)*
- **Contextual Filtering:**
  Only products within the identified category are loaded into the model’s context.
- **User Needs Summary:**
  Before recommending, the system asks the LLM to summarize the user’s requirements (e.g., “needs powerful GPU, budget under $2000”).
- **Final Recommendation:**
  The model then selects the best-matching product and generates a natural-language explanation.


## 🗂️ Directory Structure
```bash
backend/
├── db/
│   ├── categories_map.py       # Category mapping logic.
│   ├── conversations_log.jsonl # Logs user-agent interactions.
│   └── products.json           # Product dataset.
├── chat.py                     # Conversation flow controller.
├── data_handler.py             # Data loading and filtering.
├── main.py                     # FastAPI entry point.
├── model.py                    # LLM provider integration.
├── prompts.py                  # System prompts and instructions.
├── .env                        # Environment variables (Groq API key).
└── requirements.txt            # Python dependencies.
```

## ⚙️ Key Technologies & Design
* **Framework:** FastAPI — async, fast, and self-documented at `/docs`.
* **LLM Integration:** Modular design for easy provider switching.
* **Validation:** Pydantic models ensure strict schema validation.
* **Grounding:** Product data is loaded from `db/products.json` to anchor recommendations.

## 📡 API Endpoints (FastAPI)
| Method | Path | Description | Data Schemas | 
| --- | --- | --- | --- | 
| `POST` | `/chat`| Submits a user message and retrieves the model’s response & recommendation. | `Message` (in/out) |
| `POST` | `/new_chat` | Starts a new conversation (resets context). | - |
| `POST` | `/feedback` | Submits user feedback for analytics. | `FeedbackData` (in) |
| `GET` | `/logs` | Returns all conversation logs for dashboard or export. | - |

Full API docs available automatically at: `/docs`

## 📊 Monitoring & Evaluation
* **Logging:** Each turn (user ↔ agent) is recorded in `db/conversations_log.jsonl`.
* **Metrics:** Tracks timestamps, latency, number of turns, and feedback results.
* **Export:** `/logs` endpoint provides all stored data for dashboard visualization or offline analysis.

## 🚀 Setup & Run Instructions
### Prerequisites:
* Python 3.10+
* `pip` 

### Environment Configuration:
* Create a `.env` file with Groq API key: 
```bash
GROQ_API_KEY=<your_key_from_(https://console.groq.com/keys)>
```
⚠️ The .env file should not be pushed to version control.

### ▶️ Run the Server:
``` bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
---

✅ The backend is now ready and fully functional.  
- Backend server: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
