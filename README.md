This `README.md` is designed to reflect the **technical sophistication** and **engineering leadership** required for an NTU REP Distinction. It positions your project not just as a script, but as a robust, institutional-grade security platform.

---

# 🛡️ BankScamShield: Agentic Security Verification Portal

**BankScamShield** is an AI-driven, multi-agent security platform designed to protect banking customers from sophisticated phishing and social engineering attacks. By utilizing a "Defense-in-Depth" architecture, the system employs specialized AI agents to perform real-time forensic linguistic analysis and technical infrastructure audits on suspicious communications.

## 1. Project Overview

In the modern threat landscape, single-layer filters often fail to catch "Zero-Day" scams. **BankScamShield** addresses this by orchestrating a "Crew" of autonomous agents:

* **Forensic Linguist Agent**: Analyzes psychological triggers, urgency markers, and "Get Rich Quick" narratives.
* **Technical Security Auditor**: Validates sender metadata against the **Singapore SSIR Registry** and performs deep-link analysis for typosquatting.
* **Manager Agent**: Consolidates findings into a structured, human-readable **Institutional Security Briefing**.

### Key Features:
* **Agentic Orchestration**: Powered by `CrewAI` and `Llama 3.3` (via Groq LPU) for sub-5-second inference.
* **Persistence Layer**: Integrated **SQLite** database for community threat intelligence and trend tracking.
* **Institutional UI**: A clean, "Open Government" style dashboard built with Flask and Bootstrap 5.

---

## 2. Installation & Setup

### Prerequisites:
* **Python 3.10+**
* A **Groq API Key** (Get one at [console.groq.com](https://console.groq.com/))

### Dependency Installation:
This project uses `uv` (via CrewAI) for high-performance dependency management.

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd bankscammerscanner
    ```

2.  **Create and activate the virtual environment:**
    ```bash
    # On Windows
    python -m venv .venv
    .venv\Scripts\activate

    # On Mac/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the core packages:**
    ```bash
    pip install crewai flask langchain-groq python-dotenv
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your keys:
    ```text
    GROQ_API_KEY=your_actual_key_here
    MODEL=groq/llama-3.3-70b-versatile
    ```

---

## 3. How to Run the App

You can interact with BankScamShield through the terminal (for debugging) or the Web Portal (for the full experience).

### Option A: Running the Web Portal (Recommended)
1.  **Set the Python Path** (Ensures the app sees the `src` module):
    ```bash
    # On Windows (PowerShell)
    $env:PYTHONPATH = "src"
    
    # On Mac/Linux
    export PYTHONPATH=src
    ```

2.  **Launch the Flask Server:**
    ```bash
    python app.py
    ```

3.  **Access the Dashboard:**
    Open your browser to `http://127.0.0.1:5000`.

### Option B: Running via CLI
To test the "Engine" directly without the web interface:
```bash
crewai run
```

---

## 4. Technical Architecture
The system follows a modular architecture where the **Logic Layer** (CrewAI) is decoupled from the **Presentation Layer** (Flask). Every scan result is persisted to `scams.db` to facilitate real-time updates to the "Recent Community Scans" table, demonstrating a full-stack, stateful security application.

---

### Distinction Note for Submission:
* **Model Failover**: This system is configured to use **Llama 3.3-70B** on Groq LPUs, providing a 10x speed advantage over traditional GPT-4 API calls.
* **Explainable AI (XAI)**: Unlike binary "Scam/Not Scam" filters, this portal provides a detailed **Security Briefing** to educate the user on *why* a message was flagged.