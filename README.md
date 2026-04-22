
# 🏗️ InfraEscrow

**A Decentralized Protocol for Automated Infrastructure Payouts**

[](https://xrpl.org/)
[](https://deepmind.google/technologies/gemini/)
[](https://streamlit.io/)

## 🌟 The Vision

InfraEscrow replaces slow, manual municipal bureaucracy with a **Trustless Infrastructure Pipeline**. By combining **XRP Ledger (XRPL)** smart escrows with **Gemini AI** visual verification, we ensure that municipal funds are only released to contractors when the work is mathematically and technically verified.

## 🛡️ The Triple-Layer Trust Architecture

InfraEscrow operates on three distinct layers of verification:

1.  **Legal Trust (Identity):** Utilizing the **XRPL Credentials** standard, we verify the subject's professional engineering license on-chain. Only certified inspectors can initiate the diagnostic process.
2.  **Financial Trust (Escrow):** Funds are locked in a cryptographic **Smart Escrow** vault. The XRP is physically removed from the City Treasury and held by the ledger, guaranteed to be paid out only upon completion or returned if the work is never verified.
3.  **Technical Trust (AI Oracle):** We employ **Gemini 2.5 Flash** as a technical oracle. The AI performs a multimodal analysis of structural scans (dams, bridges, tunnels) and issues a cryptographically triggered "Verified" verdict to release the funds.

## 🛠️ Tech Stack

  - **Blockchain:** XRP Ledger (XRPL) via `xrpl-py`
  - **AI Oracle:** Google Gemini 2.5 Flash (Multimodal)
  - **Smart Contracts:** XRPL Escrows & Credentials
  - **Frontend:** Streamlit
  - **Backend:** Python 3.14

## 🚀 Getting Started

### Prerequisites

  - Python 3.10+
  - An [XRPL Testnet Faucet](https://xrpl.org/resources/dev-tools/xrp-faucets) account (handled automatically in the app)
  - A [Google Gemini API Key](https://aistudio.google.com/)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rass89/InfraEscrow.git
    cd InfraEscrow
    ```
2.  **Set up the virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install xrpl-py cryptography streamlit google-generativeai pillow
    ```
4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 📈 Demo Workflow

1.  **Certification:** Issue and accept an on-chain engineering credential.
2.  **Escrow:** Lock 10 XRP in the municipal vault for a specific infrastructure task.
3.  **Analysis:** Upload a structural scan (e.g., a steel bridge joint or concrete dam wall).
4.  **Payout:** Watch the AI Oracle verify the integrity and trigger the instant settlement on the XRP Ledger.
This project represents the intersection of Structural Health Monitoring (SHM) and Decentralized Finance (DeFi) to build safer, more efficient smart cities.



Your repository is now pitch-ready\! Is there anything else you want to add to the "Future Vision" section before you submit to the HackKU portal?
