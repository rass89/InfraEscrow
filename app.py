import streamlit as st
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl_helper import issue_credential, accept_credential, create_inspection_escrow, release_escrow
from ai_verification import analyze_bridge_scan

st.set_page_config(page_title="Trustless Infrastructure", layout="wide")
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

# --- State Management ---
if "funder_wallet" not in st.session_state:
    with st.spinner("Loading Pre-Funded Testnet Wallets..."):
        # Your permanent, successfully funded wallets!
        st.session_state.funder_wallet = Wallet.from_seed("sEd7Q7t71m6EdjrUHLifzpPKeQMbp4R")
        st.session_state.inspector_wallet = Wallet.from_seed("sEd7Msd65yEVvp56qub6AYXnxEFWBXe")
        
        st.session_state.escrow_data = None
        st.session_state.has_credential = False

funder = st.session_state.funder_wallet
inspector = st.session_state.inspector_wallet

# --- Sidebar ---
st.sidebar.title("🔐 Configuration")
gemini_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
if not gemini_key:
    st.sidebar.warning("Please enter your Gemini API key to enable the AI Oracle.")

st.sidebar.divider()
st.sidebar.info(f"**City Treasury:**\n`{funder.address}`")
st.sidebar.info(f"**Inspector:**\n`{inspector.address}`")

# --- Main UI ---
st.title("🏗️ Decentralized Civic Infrastructure")
st.markdown("Automating municipal payouts using **Gemini AI Visual Verification** and **XRPL Credentials + Smart Escrows**.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("🏢 City Treasury & Licensing")
    
    # 1. Credentials
    st.subheader("Step 1: Engineering Credential")
    if not st.session_state.has_credential:
        if st.button("Issue & Accept Credential"):
            with st.spinner("Writing W3C-Compatible Credential to Ledger..."):
                issue_credential(funder.seed, inspector.address)
                accept_credential(inspector.seed, funder.address)
                st.session_state.has_credential = True
                st.success("✅ On-Chain Credential Issued & Accepted!")
    else:
        st.success("✅ Inspector holds valid Engineering Credential.")

    # 2. Smart Escrow
    st.subheader("Step 2: Lock Funds (Smart Escrow)")
    if st.button("Initialize Smart Escrow"):
        if not st.session_state.has_credential:
            st.error("Inspector must hold a valid credential first!")
        else:
            with st.spinner("Locking 50 XRP via Cryptographic Escrow..."):
                escrow_data = create_inspection_escrow(funder.seed, inspector.address, amount_xrp=10)
                st.session_state.escrow_data = escrow_data
                st.success("Escrow Created! Awaiting AI verification.")
                st.write(f"**Transaction Hash:** `{escrow_data['hash']}`")

with col2:
    st.header("👷 AI Visual Verification")
    uploaded_file = st.file_uploader("Upload Steel Bridge Scan", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None and st.session_state.escrow_data is not None:
        st.image(uploaded_file, caption="Captured Structural Scan", width=300)
        
        if st.button("Step 3: Run Diagnostics & Claim"):
            if not gemini_key:
                st.error("API Key missing! Check the sidebar.")
            else:
                with st.spinner("Gemini AI Analyzing Structural Data..."):
                    ai_result = analyze_bridge_scan(uploaded_file, gemini_key)
                
                if ai_result["status"] == "Verified":
                    st.success(f"✅ Status: {ai_result['status']} (Confidence: {ai_result['confidence']})")
                    st.info(f"AI Notes: {ai_result['details']}")
                    
                    with st.spinner("Submitting Preimage to execute Escrow..."):
                        data = st.session_state.escrow_data
                        finish_hash = release_escrow(funder.address, data["sequence"], data["condition"], data["preimage"], funder.seed)
                    
                    st.balloons()
                    st.success("💸 Smart Contract Executed! Funds Released.")
                    st.write(f"**Release TX Hash:** `{finish_hash}`")
                else:
                    st.error(f"❌ Status: {ai_result['status']}. AI Notes: {ai_result['details']}")
    elif uploaded_file is not None and st.session_state.escrow_data is None:
        st.warning("The City must lock the funds before work can be verified.")