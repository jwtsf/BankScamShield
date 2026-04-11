# BankScamShield: Agentic Security Verification Portal

**BankScamShield** is an AI-driven, multi-agent security platform designed to protect banking customers from sophisticated phishing and social engineering attacks. By utilizing a "Defense-in-Depth" architecture, the system employs specialized AI agents to perform real-time forensic linguistic analysis and technical infrastructure audits on suspicious communications.

## 1. Project Overview

In the modern threat landscape, single-layer filters often fail to catch "Zero-Day" scams. **BankScamShield** addresses this by orchestrating a "Crew" of autonomous agents:

* **Forensic Linguist Agent**: Analyzes psychological triggers, urgency markers, emotional manipulation, and "Get Rich Quick" narratives. Produces a Manipulation Score from 1–10.
* **Technical Security Auditor**: Validates sender metadata against the **Singapore SSIR Registry**, detects foreign number spoofing, and performs deep-link analysis for typosquatting and suspicious URLs.
* **Final Recommendation**: The Technical Security Auditor consolidates both agents' findings into a structured **RISK LEVEL: HIGH/LOW** verdict with analysis bullets and recommended actions.

### Key Features:
* **Agentic Orchestration**: Powered by `CrewAI` and `Llama 3.3-70B` (via Groq LPU) for fast inference.
* **Custom Security Tools**: `SGSSIRChecker` and `URLTechnicalAnalyser` — purpose-built tools for Singapore-specific scam detection.
* **Persistence Layer**: Integrated **SQLite** database (`scams.db`) for scan history and community threat tracking.
* **Web Dashboard**: A clean dashboard built with Flask and Bootstrap 5, showing per-scan analysis and recent scan history.

---

## 2. Installation & Setup

### Prerequisites:
* **Python 3.10+**
* A **Groq API Key** (Get one at [console.groq.com](https://console.groq.com/))

### Steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/jwtsf/BankScamShield.git
    cd BankScamShield
    ```

2. **Create and activate the virtual environment:**
    ```bash
    # On Windows
    python -m venv .venv
    .venv\Scripts\activate

    # On Mac/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install the package and dependencies:**
    ```bash
    pip install -e .
    ```

4. **Configure Environment Variables:**
    Create a `.env` file in the root directory:
    ```text
    GROQ_API_KEY=your_actual_key_here
    MODEL=groq/llama-3.3-70b-versatile
    ```

---

## 3. How to Run the App

### Web Portal (Recommended)

```bash
python app.py
```

Then open your browser to `http://127.0.0.1:5000`.

### CLI (for testing the crew directly)
```bash
crewai run
```

---

## 4. Technical Architecture

The system follows a modular architecture where the **Logic Layer** (CrewAI) is decoupled from the **Presentation Layer** (Flask).

```
app.py (Flask)
    └── BankScamShieldCrew (CrewAI)
            ├── forensic_linguist        → linguistic_analysis_task
            ├── technical_security_auditor → technical_audit_task
            │       ├── SGSSIRChecker (custom tool)
            │       └── URLTechnicalAnalyser (custom tool)
            └── technical_security_auditor → final_recommendation_task
                    └── RISK LEVEL: HIGH / LOW
```

Every scan result is persisted to `scams.db`, powering the "Recent Community Scans" history table on the dashboard.

---

## 5. Scam Detection Logic

The final risk verdict is **HIGH** if any of the following are true:
- The sender is a personal mobile number **and** the message claims to be from a bank or financial institution
- The Manipulation Score is 6 or above
- Malicious or suspicious URLs are detected
- The sender ID contains a "Likely-SCAM" header or unregistered tag
- The sender is a foreign mobile number contacting about Singapore financial matters

Otherwise the verdict is **LOW**.

---

## 6. Notes

* **Explainable AI**: Unlike binary "Scam/Not Scam" filters, this portal provides a detailed Security Briefing explaining *why* a message was flagged.
* **Singapore-specific**: Detection logic is tuned for the Singapore context — SSIR registry rules, local bank domains (DBS, OCBC, UOB), and MAS regulations.
