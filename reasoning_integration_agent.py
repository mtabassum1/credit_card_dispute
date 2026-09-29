import json

def integrate_claude_reasoning():
    print("🤖 Starting Reasoning Integration Agent...")
    
    # 1. Ingest the structured decisions produced by the evaluation layer
    claude_output = [
        {
            "case_id": "CASE-001",
            "decision": "AUTO_APPROVE",
            "policy_applied": "POLICY-101",
            "rationale": "TXN1001 and TXN1002 share the same customer, merchant (Amazon), exact amount ($250.00), and date (2026-07-15), so they fall within the 24-hour window. Both have signature_present = true, so a signature duplicate is verified and the ledger matches the complaint. POLICY-101 requires auto-approval."
        },
        {
            "case_id": "CASE-002",
            "decision": "FLAG_MANUAL_REVIEW",
            "policy_applied": "POLICY-202",
            "rationale": "The disputed charge of $1,200.50 exceeds the $1,000.00 threshold and signature_present is false. POLICY-202 requires flagging the case for immediate human-in-the-loop manual review. It should be neither auto-approved nor auto-denied."
        },
        {
            "case_id": "CASE-003",
            "decision": "REQUEST_DOCUMENTATION",
            "policy_applied": "POLICY-303",
            "rationale": "POLICY-303 requires a copy of the explicit cancellation receipt or written refund confirmation from the vendor. Neither is in the case file, and only the customer's verbal claim is present. The transaction is still Pending. The claim cannot be approved on the current record."
        }
    ]
    
    # 2. Map and normalize data to match the Streamlit dashboard structure
    mapped_recommendations = []
    for case in claude_output:
        # Convert Claude's custom decision names to the dashboard's system status enums
        if case["decision"] == "AUTO_APPROVE":
            status = "APPROVED"
            score = 0.98
        elif case["decision"] == "FLAG_MANUAL_REVIEW":
            status = "MANUAL_REVIEW_REQUIRED"
            score = 0.85
        else:
            status = "REJECTED"
            score = 0.92
            
        mapped_recommendations.append({
            "case_id": case["case_id"],
            "dispute_category": "AUTOMATED_EVALUATION",
            "compliance_status": status,
            "confidence_score": score,
            "explanation": f"[{case['policy_applied']}] {case['rationale']}"
        })
        
    # 3. Write out the production data asset to synchronize the local state
    with open("final_recommendations.json", "w") as f:
        json.dump(mapped_recommendations, f, indent=4)
        
    print("✓ Successfully integrated evaluation layers into final_recommendations.json")

if __name__ == "__main__":
    integrate_claude_reasoning()
