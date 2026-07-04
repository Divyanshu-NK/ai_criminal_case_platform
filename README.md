# AI Criminal Case Platform

A highly advanced, AI-powered legal research and case-analysis workspace tailored for Indian Criminal Law (BNS, BNSS, BSA). Designed as a professional tool for legal workflows, this platform moves beyond traditional "chatbots" to provide a dense, 3-panel workspace for deep investigation, evidence matrices, and charge validation.

## 🏗 Architecture Overview

The platform follows a "Everything is a Pipeline" philosophy. Rather than relying on a single mega-prompt, the system utilizes a **10-agent collaborative LangGraph pipeline**.

### Core Stack
- **Backend:** FastAPI, Python 3.12+
- **Agent Orchestration:** LangGraph, LangChain
- **LLM Engine:** Groq (Llama-3-70b) / Google Gemini (1.5 Flash), interchangeable via `.env`
- **Vector Database:** Qdrant (Dockerized) for RAG
- **Frontend:** Vanilla JS Single Page Application (SPA), zero-dependency, served statically by FastAPI.

## 🧠 The Agentic Pipeline
When a case scenario is submitted, it is processed sequentially by highly specialized, stateless agents:

1. **Scenario Parser:** Standardizes the raw user narrative into a structured timeline and jurisdiction constraint.
2. **Fact Extractor:** Identifies discrete, verifiable facts (who, what, when, where).
3. **Offence Discovery:** Maps the extracted facts to potential criminal charges.
4. **Law Retrieval (RAG):** Queries the local Qdrant vector database to pull the exact statutory text (BNS sections) and ingredients for the potential offences.
5. **Evidence Agent:** Categorizes available evidence and identifies missing evidentiary gaps.
6. **Charge Validator:** Strictly cross-references the retrieved statutory ingredients against the available facts to validate whether a charge is "Strong", "Weak", or "Insufficient".
7. **Case Retrieval (RAG):** Finds analogous Supreme Court or High Court precedents from the vector store.
8. **Strategy Agent:** Formulates prosecution and defense arguments based on the validated charges and evidence gaps.
9. **Procedural Agent:** Outlines the next statutory steps (e.g., filing FIR, taking cognizance) under BNSS.
10. **Report Generator:** Synthesizes the entire pipeline's output into a cohesive executive summary.

## 🖥 Professional Workspace UI
The frontend abandons the chat-paradigm in favor of a 3-panel analytical dashboard:
- **Left Navigation Panel:** Context switching between Facts, Offences, Applicable Laws, Evidence, and Strategy.
- **Center Analysis Panel:** Dense analytical tables showing exactly which charges are validated and an Evidence Matrix separating verified vs. missing evidence.
- **Right Inspector Panel (Trace):** A real-time trace of the LangGraph agents as they process the case, ensuring the AI's logic is fully transparent and inspectable.

---

# 🚀 Next Phases (Roadmap)

To easily pick up tomorrow, here is the comprehensive plan for the upcoming phases:

### Phase 4: Document Drafting Generation (V2 Features)
- [ ] **Dedicated Endpoints:** Create discrete API routes or LangGraph pathways to specifically generate legal documents (FIRs, Charge Sheets, Bail Applications) based on the highly structured `CaseContext`.
- [ ] **Document UI:** Add a "Drafts" tab to the UI workspace that dynamically renders formatted legal templates filled with the AI's analysis.

### Phase 5: RAG Robustness & Data Expansion
- [ ] **Full BNSS & BSA Ingestion:** Expand the scraping and ingestion scripts to cover the Bharatiya Nagarik Suraksha Sanhita (Procedure) and Bharatiya Sakshya Adhiniyam (Evidence) acts.
- [ ] **Real Precedent Pipeline:** Connect the Qdrant ingestion to a real legal database API or a massive scraper for Supreme Court judgments to feed the Case Retrieval Agent.

### Phase 6: Interactive Court Simulation
- [ ] **Simulation Engine:** Build an interactive sub-graph in LangGraph where the user can roleplay as Prosecution/Defense examining a witness.
- [ ] **Simulation UI:** Implement the "Court Simulation" interface detailed in the UX specs, keeping track of objections, evidence introduced, and witness credibility.

### Phase 7: Document Upload & OCR
- [ ] **Multi-Modal Intake:** Allow users to upload PDFs of existing FIRs or witness statements. Use Gemini's multi-modal capabilities or an OCR library to parse these documents directly into the `Scenario Parser` agent.

---

## 🛠 Setup & Installation

1. **Clone the repository and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Environment Setup:**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY="your_gemini_key"
   GROQ_API_KEY="your_groq_key"
   ```
3. **Start Qdrant (Docker):**
   ```bash
   docker-compose up -d
   ```
4. **Ingest Initial Law Data (Optional if already populated):**
   ```bash
   python scripts/ingest_laws.py
   ```
5. **Run the FastAPI Server:**
   ```bash
   python -m uvicorn main:app --reload --port 8000
   ```
6. Open your browser and navigate to `http://localhost:8000`.
