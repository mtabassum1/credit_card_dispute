import pandas as pd
import json

def generate_mock_data():
    transactions = [
        {"transaction_id": "TXN1001", "customer_id": "CUST99", "amount": 250.00, "merchant": "Amazon", "date": "2026-07-15", "status": "Settled", "signature_present": True},
        {"transaction_id": "TXN1002", "customer_id": "CUST99", "amount": 250.00, "merchant": "Amazon", "date": "2026-07-15", "status": "Settled", "signature_present": True},
        {"transaction_id": "TXN2005", "customer_id": "CUST44", "amount": 1200.50, "merchant": "BestBuy", "date": "2026-07-18", "status": "Settled", "signature_present": False},
        {"transaction_id": "TXN3009", "customer_id": "CUST12", "amount": 45.00, "merchant": "Uber", "date": "2026-07-20", "status": "Pending", "signature_present": True}
    ]
    pd.DataFrame(transactions).to_csv("mock_transactions.csv", index=False)
    print("✓ Created mock_transactions.csv")

    intake = [
        {"case_id": "CASE-001", "customer_id": "CUST99", "complaint_text": "I was charged twice for the same $250 transaction on Amazon on July 15th."},
        {"case_id": "CASE-002", "customer_id": "CUST44", "complaint_text": "There is a massive charge from BestBuy for $1200.50 that I never authorized."},
        {"case_id": "CASE-003", "customer_id": "CUST12", "complaint_text": "The merchant Uber promised a refund for my $45 ride but I haven't received it."}
    ]
    pd.DataFrame(intake).to_csv("mock_intake.csv", index=False)
    print("✓ Created mock_intake.csv")

    classified = [
        {"case_id": "CASE-001", "customer_id": "CUST99", "complaint_text": "I was charged twice for the same $250 transaction on Amazon on July 15th.", "dispute_category": "DUPLICATE_CHARGE"},
        {"case_id": "CASE-002", "customer_id": "CUST44", "complaint_text": "There is a massive charge from BestBuy for $1200.50 that I never authorized.", "dispute_category": "FRAUD"},
        {"case_id": "CASE-003", "customer_id": "CUST12", "complaint_text": "The merchant Uber promised a refund for my $45 ride but I haven't received it.", "dispute_category": "MERCHANT_ISSUE"}
    ]
    with open("classified_cases.json", "w") as f:
        json.dump(classified, f, indent=4)
    print("✓ Created classified_cases.json")

if __name__ == "__main__":
    generate_mock_data()
