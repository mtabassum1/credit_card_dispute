import streamlit as st
import pandas as pd
import json
import os

# Update the page configuration layout title right here
st.set_page_config(page_title="ABC Banking Ops - Dispute Dashboard", layout="wide")

st.title("🏦 Production-Grade Credit Card Dispute Operations Dashboard")
st.subheader("Human-in-the-Loop Review & System Health Workspace")

# Ingest backend database files
if os.path.exists("final_recommendations.json") and os.path.exists("evidence_file.json"):
    with open("final_recommendations.json", "r") as f:
        recs = json.load(f)
    with open("evidence_file.json", "r") as f:
        evidence = json.load(f)

    # 1. State-tracking high-level analytical metrics
    total_cases = len(recs)
    approved = sum(1 for c in recs if c["compliance_status"] == "APPROVED")
    rejected = sum(1 for c in recs if c["compliance_status"] == "REJECTED")
    pending_hitl = sum(1 for c in recs if c["compliance_status"] == "MANUAL_REVIEW_REQUIRED")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Ingested Cases", total_cases)
    col2.metric("Auto-Approved", approved)
    col3.metric("Auto-Rejected", rejected)
    col4.metric("Pending Human Review (HITL)", pending_hitl)

    st.markdown("---")

    # 2. Interactive Database Dataframe Display
    st.write("### 📊 Ingested System Evidence & AI Recommendations Ledger")
    df_display = pd.DataFrame(recs)
    st.dataframe(df_display, use_container_width=True)

    st.markdown("---")

    # 3. Isolate High-Risk Edge Cases / Human-in-the-Loop Override Panel
    st.write("### 🛡️ High-Risk Case Validation & Supervisor Overrides")
    
    manual_cases = [c for c in recs if c["compliance_status"] == "MANUAL_REVIEW_REQUIRED"]
    
    if manual_cases:
        for m_case in manual_cases:
            with st.expander(f"⚠️ Action Required: {m_case['case_id']} ({m_case['dispute_category']})"):
                case_ev = next((e for e in evidence if e["case_id"] == m_case["case_id"]), None)
                st.write(f"**Customer Narrative:** {case_ev['complaint_text'] if case_ev else 'N/A'}")
                st.write(f"**System Flag Reasoning:** {m_case['explanation']}")
                st.slider("Confidence Verification Threshold", 0.0, 1.0, float(m_case["confidence_score"]), disabled=True)
                
                c_btn1, c_btn2 = st.columns(2)
                if c_btn1.button("Force Approve Dispute", key=f"app_{m_case['case_id']}"):
                    st.success(f"Case {m_case['case_id']} manually APPROVED.")
                if c_btn2.button("Force Deny Dispute", key=f"den_{m_case['case_id']}"):
                    st.error(f"Case {m_case['case_id']} manually REJECTED.")
    else:
        st.info("Excellent! No outstanding edge cases require physical human overrides.")
else:
    st.warning("⚠️ Critical system database files are missing.")
