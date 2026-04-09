# 🧠 Multitasking Text Utility - LLM Pipeline with Feedback & Refinement

A production-style LLM pipeline designed to process customer support requests using structured outputs, evaluation feedback loops, and conditional refinement, with full observability through metrics tracking.

---

## 🚀 Overview

This project implements a multi-step AI pipeline that:

1. Generates an initial structured response using an LLM  
2. Evaluates the response quality using a feedback model  
3. Conditionally refines the response if needed  
4. Tracks and persists metrics such as tokens, cost, and latency  

---

## 🧩 Architecture

```text
User Input
    ↓
Initial LLM Response
    ↓
Feedback Evaluation (scores + issues)
    ↓
Conditional Refinement (if needed)
    ↓
Final Response
    ↓
Metrics Tracking (CSV)

```


##  ⚙️ Key Features

✅ Structured Output (JSON)

- Uses controlled schema for consistent responses
- Ensures relable downstream processing

---

🔁 Feedback Loop

Evaluates response quality across:

- category
- priority
- answer quality
- actions
- status
  
🧠 Conditional Refinement

- Avoids unnecessary LLM calls
- Triggers refinement only when:
    - any score < 0.8
  

📊 Metrics Tracking

- Token usage
- Estimated cost
- Latency
- Refinement usage
 - Stored in CSV for analysis

📁 Project Structure

```bash
src/
├── llm_client.py      # 🤖 Initial LLM call logic
├── feedback.py        # ⚖️ Response evaluation & scoring
├── refiner.py         # 🔧 Conditional refinement logic
├── openai_runner.py   # 🏎️ Shared execution + metrics engine
├── metrics_store.py   # 💾 CSV persistence layer
├── run_query.py       # 🚀 Main pipeline entry point
└── schema.py          # 🏗️ Pydantic & JSON schemas

```

📊 Example Output

```json
{
  "support_output": {
    "category": "billing",
    "priority": "high",
    "answer": "We understand your concern regarding unusual charges...",
    "actions": [
      "Check your billing history",
      "Verify subscription status",
      "Contact support with details"
    ],
    "status": "needs_human_review"
  }
}
```

📈 Metrics Example (CSV)

```text
timestamp;user_input;total_tokens;total_cost_usd;total_latency_ms;refinement_applied
2026-04-08T10:00:00;login issue;968;0.00022;5210;true
```

---

🧠 Technical Highlights

- Modular LLM architecture
- Defensive JSON parsing
- Prompt engineering (few-shot ready)
- Cost-aware execution
- Observability layer (LLMOps concept)
- Clean separation of concerns

---

🛠️ Tech Stack

- Python
- OpenAI API
- Pydantic
- CSV (for metrics storage)
  

---

▶️ How to Run

1. Clone the repository

```Shell
git clone <repo-url>
cd multitasking-text-utility
```

2. Create .env file

```Shell
```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o-mini
```

3. Run the pipeline

```Shell   
python src/run_query.py
```

---

💡 Future Improvements

- Retry / fallback strategies for LLM failures
- Dashboard visualization for metrics
- Automated evaluation benchmarks
- Multi-turn conversation support
- Integration with real support systems

---

🧑‍💻 Author

Juan Manuel Balaguera
AI Engineer in training | Backend | LLM Systems

---

⭐ Key Takeaway

This project demonstrates how to move from simple LLM calls to a production-ready AI pipeline with:

- evaluation
- optimization
- cost control
- observability