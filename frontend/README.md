# 💻 Frontend Service (React / TypeScript)

## 🔍 Overview
The Frontend service is a **Single Page Application (SPA)** built with **React** and **TypeScript**. Its primary role is to provide the user interface for interacting with the AI product recommendation agent and to display the system's monitoring logs.

The application is structured around two main **views (routes)**:
1.  **Chat Interface:** The core component for real-time, multi-turn conversation with the agent.
2.  **Dashboard:** A dedicated view for displaying the minimal evaluation metrics and conversation logs retrieved from the Backend API.

--- 

## 🗂️ Directory Structure
```bash
frontend/
└── src/
    ├── components/
    │   ├── ChatWindow/
    │   │   ├── ChatWindow.tsx   # Main chat container and conversation state manager.
    │   │   ├── InputBox.tsx     # Handles user input and new message submission.
    │   │   └── Message.tsx      # Renders individual chat messages (user/agent) and recommendations.
    │   ├── Button.tsx           # Reusable UI component.
    │   └── Dashboard.tsx        # Fetches and displays the /logs data from the backend.
    ├── App.tsx                  # Main application router and layout.
    └── types.tsx                # Centralized TypeScript interfaces for API schemas (e.g., Message, FeedbackData).
```

## ⚙️ Key Technologies & Design
* **Framework**: **React** (v18+)
* **Language**: **TypeScript** (preferred for strong typing and data integrity).
* **State Management**: Local component state (potentially using React Hooks) manages the conversation history.
* **API Communication**: Uses standard browser Fetch API or a library like Axios to interact with the backend running on `http://127.0.0.1:8000`.

## 🛠️ Key Features & Navigation
| Feature | URL Path | Description |
| :--- | :--- | :--- |
| **Chat Interface** | [http://localhost:3000/](http://localhost:3000) | Main application view. Handles real-time communication with the `/chat`, `/new_chat`, and `/feedback` backend endpoints. |
| **Monitoring Dashboard** | [http://localhost:3000/dashboard](http://localhost:3000/dashboard) | **Dedicated view** for minimal evaluation. Fetches and displays the full conversation logs retrieved from the backend's `/logs` endpoint. |
| **Data Consistency** | - | Uses **TypeScript interfaces (`types.tsx`)** to ensure data structures used for API communication are strongly typed. |


## 🚀 Setup and Running
### Prerequisites:
* Node.js (v18+)
* `npm`
* ⚠️ Make sure the **Backend service is running** on [http://127.0.0.1:8000](http://127.0.0.1:8000) (see `backend/README.md`).

### Run Frontend:
```bash
cd frontend
npm install
npm start
```

---

✅ The frontend is now ready and fully functional.  
- Chat Interface: [http://localhost:3000](http://localhost:3000)  
- Dashboard: [http://localhost:3000/dashboard](http://localhost:3000/dashboard)
