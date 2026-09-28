# Production-Grade Credit Card Dispute & Chargeback Resolution Agentic Workflow

An end-to-end, multi-agent automated dispute resolution system and operational supervisor dashboard engineered for high-volume banking environments (e.g., Capital One). This architecture transitions complex, document-heavy, and compliance-sensitive manual workflows into structured, auditable machine logic.

## 🏗️ Technical Architecture & System Workflow

The framework operates via distinct operational layers designed to mimic core enterprise structures:

1. **Data Layer (Core Ledger Systems):** Evaluates baseline datasets mirroring transaction systems (`mock_transactions.csv`) and initial user complaints (`mock_intake.csv`).
2. **Intake & Classification Agent (Agent 1):** Ingests raw customer complaint narratives and applies categorical intent constraints to classify disputes into standardized categories (`DUPLICATE_CHARGE`, `MERCHANT_ISSUE`, `FRAUD`).
3. **Transaction Retrieval Agent (Agent 2):** Runs a case-insensitive database pipeline (`transaction_retrieval_agent.py`) to filter core transaction systems and merge ledger data with complaints into a unified `evidence_file.json`.
4. **Policy, Compliance, & Reasoning Agents (Agents 3 & 4):** Evaluates evidence arrays against explicit bank regulations and outputs status decisions accompanied by detailed logic strings and numeric confidence scores.
5. **Action, Drafting, & Audit Log Agents (Agents 5 & 6):** An deployment script (`action_and_audit_agent.py`) that acts on compliance flags, compiles localized immutable log archives, and auto-drafts customer correspondence text files (`_audit_and_email.txt`).
6. **Human-in-the-Loop Operations Workspace:** A multi-threaded web application GUI built with Streamlit (`app.py`) providing live analytics, dataframes tracking, and an interactive override interface for high-risk manual review exceptions.

---

## 🛡️ Enterprise Operational Controls

### 🧠 Accuracy via Grounded Context (RAG Concepts)
By programmatically compiling and feeding raw structured JSON data blocks (`evidence_file.json`) directly into the model context layer, the system's determinations are strictly grounded in verified ledger data and explicit bank regulations. This structural design eliminates hallucinations and ensures recommendations mirror factual records rather than probabilistic guesses.

### 📜 Compliance & Immutable Audit Trails
Every individual stage transition within the orchestration layer yields a permanent, explicit local data asset (`.csv`, `.json`, `.txt`). This creates a complete file-based audit trail tracking data mutations across the intake, retrieval, and reasoning phases, allowing compliance auditors to inspect exactly why an automated recommendation or action took place at any given moment.

---

## 🛠️ Technology Stack & Demonstrated Skills
* **Languages & Frameworks:** Python, Pandas, Streamlit Data Architecture.
* **AI Architecture:** Multi-Agent System Design, Retrieval-Augmented Generation (RAG) Concepts, Prompt Engineering, Human-in-the-Loop (HITL) Workflows.
* **Data Interchange:** JSON Mapping, CSV Parsing, Case-Insensitive Relational Merging.

---

## 🚀 Local Installation & Execution

1. **Clone the Repository:**
   ```bash
   git clone https://github.com
   cd credit_card_dispute
   ```

2. **Generate Baseline Ledger Data:**
   ```bash
   python mock_data_generator.py
   ```

3. **Execute the Agentic Retrieval and Reasoning Pipelines:**
   ```bash
   python transaction_retrieval_agent.py
   python action_and_audit_agent.py
   ```

4. **Launch the Free Operations Workspace Dashboard:**
   ```bash
   pip install streamlit pandas
   streamlit run app.py
   ```
