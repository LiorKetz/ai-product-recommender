# 🤖 AI Product Recommendation Agent

## 🔍 Overview
This project delivers a Full-Stack, End-to-End (E2E) web application where users can interact with an AI agent that recommends products based on a multi-turn conversation. The system is designed to demonstrate ability in designing and integrating an LLM-based agent, backend logic, and a responsive frontend.

| Component | Technology | Primary Role |
| --- | --- | --- |
| **[Backend](backend/README.md)** | Python (FastAPI) | Manages agent logic, conversation state, product grounding, and minimal monitoring. |
| **[Frontend](frontend/README.md)** | React (TypeScript) | Provides interactive chat and monitoring dashboard. | 
| **Model** | Groq API | Low latency LLM for responsive recommendations. |

---

## ⚙️ Development Methodology
The project was developed using an **iterative, layered approach (Agile/Spiral)**. i prioritized establishing a working E2E baseline (Frontend/Backend/Basic Chat) before moving to complex features like the Hierarchical Retrieval and Monitoring. This approach ensured **continuous functionality** and **resilience to change**, allowing the core requirements to be met efficiently.

## 🧩 Core Agent Architecture
The backend implements a sophisticated architecture to ensure accurate and grounded recommendations from the LLM, managing the small product catalog efficiently.

### 1️⃣ Hierarchical Two-Step Retrieval
To prevent token overflow and ensure recommendations are limited to the available catalog, the system uses a Hierarchical Two-Step Retrieval process:
* **Step A: Category Identification:** The LLM first identifies the user's high-level needs and maps them to a specific category (e.g., 'Laptop', 'Monitor'). This output is strictly controlled via JSON Structured Output.
* **Step B: Product Selection (Grounding):** Only products belonging to the identified category are dynamically injected into the prompt context for the LLM to make the final, informed choice.

### 2️⃣ Strategic Technical Choices
* **Low Latency LLM:** Groq was selected as the LLM provider for its extremely low latency and high-throughput capabilities, which ensures a fast and responsive user experience crucial for conversational interfaces.
* **Design Constraint (Coupling):** The category mapping logic in `backend/db/categories_map.py` is manually maintained and directly coupled to the current product set. A mandatory update of the MAP file is required if the product data set changes, to preserve the agent's functional grounding and recommendation accuracy.

## 📊 Monitoring and Evaluation
In line with the requirements, the system includes minimal monitoring capabilities:
* **Conversation Logging:** Every turn is logged to a `conversations_log.jsonl` file, capturing messages, recommendations, and reasoning.
* **Metric Tracking:** Basic metrics like Latency, number of turns, and user feedback (via the /feedback endpoint) are tracked.
* **Dedicated Dashboard:** The frontend exposes a separate route (`/dashboard`) for viewing the contents of the conversation logs in a simple dashboard format.


## 🔮 Future Improvements & Technical Debt
While the core requirements are met, the following opportunities for enhancement and refactoring have been identified:

* **Conversational Refinement Phase:** The current flow immediately recommends a product after identifying the category. A key future enhancement would be to insert an **intermediate conversational loop** (Refinement Phase) where the agent uses the summarized requirements and the newly filtered product list to ask clarifying questions before finalizing the recommendation. This would lead to higher user satisfaction and better accuracy.
* **Recommendation Saturation / Chat Reset Logic:** The current implementation achieves the recommendation goal, but continuous conversation post-recommendation often results in **recommendation saturation** (the agent repeatedly suggests the initial product). This requires the user to manually initiate a new session via the `/new_chat` endpoint. Future development should integrate a programmatic **Conversation Reset Mechanism** in the backend, either by locking the chat input or by modifying the agent's logic to automatically return to **Step A (Category Identification)** upon detecting a new, separate query.
* **Code Modularization:** Due to the time constraints of the assignment, certain refactoring opportunities were noted but deferred. Files like `main.py` (Backend) or `App.tsx` (Frontend) would benefit from further **modularization and separation of concerns** to improve long-term maintainability.

## 🚀 E2E Setup & Run
To run the entire system, both the Backend and Frontend services must be started separately.

### Prerequisites
* Python 3.10+ (for Backend)
* Node.js (v18+) and npm (for Frontend)
* A Groq API Key.

### Step 1: Backend Setup & Run
```bash
cd backend
# Create a .env file with your Groq API key
# GROQ_API_KEY=your_key_from(https://console.groq.com/keys)
pip install -r requirements.txt
uvicorn main:app --reload
```

✅ The backend is now ready and fully functional.  
- Backend server: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


### Step 2: Frontend Setup & Run
```bash
cd frontend
npm install
npm start
```

✅ The frontend is now ready and fully functional.  
- Chat Interface: [http://localhost:3000](http://localhost:3000)  
- Dashboard: [http://localhost:3000/dashboard](http://localhost:3000/dashboard)

---

✅ The full-stack AI Product Recommendation Agent is now ready and fully functional.

---

## 📚 Detailed Documentation
For specific file structures, API endpoints, and detailed design notes for each service, please refer to the internal documentation:
* [Backend Documentation](backend/README.md)
* [Frontend Documentation](frontend/README.md)
