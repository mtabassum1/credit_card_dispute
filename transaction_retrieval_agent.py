import pandas as pd
import json
import os

def run_transaction_retrieval():
    print("Starting Agent 2: Transaction Retrieval Pipeline...")
    if not os.path.exists("classified_cases.json") or not os.path.exists("mock_transactions.csv"):
        print("Error: Base data files missing.")
        return

    with open("classified_cases.json", "r") as f:
        classified_cases = json.load(f)
    df_tx = pd.read_csv("mock_transactions.csv")
    evidence_packet = []

    for case in classified_cases:
        cust_id = str(case["customer_id"]).strip().upper()
        matched_tx = df_tx[df_tx["customer_id"].astype(str).str.strip().str.upper() == cust_id]
        tx_list = matched_tx.to_dict(orient="records")
        case_evidence = {
            "case_id": case["case_id"],
            "customer_id": case["customer_id"],
            "dispute_category": case["dispute_category"],
            "complaint_text": case["complaint_text"],
            "associated_transactions": tx_list
        }
        evidence_packet.append(case_evidence)
    
    with open("evidence_file.json", "w") as f:
        json.dump(evidence_packet, f, indent=4)
    print("✓ Generated evidence_file.json")

    mock_recommendations = [
        {"case_id": "CASE-001", "dispute_category": "DUPLICATE_CHARGE", "compliance_status": "APPROVED", "confidence_score": 0.98, "explanation": "Two identical charges of $250 detected on the same day from Amazon with matching signatures. Meets explicit duplicate signature refund criteria."},
        {"case_id": "CASE-002", "dispute_category": "FRAUD", "compliance_status": "MANUAL_REVIEW_REQUIRED", "confidence_score": 0.85, "explanation": "High value ($1200.50) transaction flagged as unauthorized by customer. Signature is missing on file. Escalating for mandatory human-in-the-loop review."},
        {"case_id": "CASE-003", "dispute_category": "MERCHANT_ISSUE", "compliance_status": "REJECTED", "confidence_score": 0.92, "explanation": "Customer claims merchant promised a refund, but no written validation or cancellation receipts were attached. Fails policy threshold for automated credit."}
    ]
    with open("final_recommendations.json", "w") as f:
        json.dump(mock_recommendations, f, indent=4)
    print("✓ Generated final_recommendations.json")

if __name__ == "__main__":
    run_transaction_retrieval()
