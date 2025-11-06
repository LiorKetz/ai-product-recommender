# ai-product-recommender

### Work Flow

1. Choose a free API Key (Groq API: https://console.groq.com/keys)
2. Connect backend to API.
3. Create Chat in backend (http://127.0.0.1:8000/)
4. Create frontend (http://localhost:3000/)
5. Connect frontend to backend.

### AI Assistant Architecture

6. Built core AI assistant architecture in backend:
   - Created modular steps for handling model responses.
   - Designed prompts for each steps.
   - Integrated model-driven decision logic to automatically determine product categories.
   - Tested assistant end-to-end to ensure proper flow from user input to model output.

7. Prompts
   - Initial prompt to get information from user.
   - Summary prompts for extracting user needs.
   - Recommendation prompts for selecting product categories.

### Next Steps
- Improve model answers.
- Add more detailed logging and analytics for conversation flow.
