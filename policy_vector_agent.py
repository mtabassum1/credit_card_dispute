import json
import os
import chromadb
from chromadb.utils import embedding_functions

def run_policy_rag():
    print("🤖 Initializing Local ChromaDB Vector Store Engine...")
    
    # 1. Setup local persistent database file layout
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    # 2. Use a free, high-performance localized embedding engine running locally
    default_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # 3. Create or clear the internal rules ledger collection
    try:
        chroma_client.delete_collection(name="banking_policies")
    except Exception:
        pass
    collection = chroma_client.create_collection(name="banking_policies", embedding_function=default_ef)

    # 4. Ingest raw banking policy rules into the vector store
    policies = [
        "POLICY-101 (Duplicate Charges): If two transactions occur within a 24-hour window from the same merchant with identical exact dollar amounts, the system must auto-approve the dispute if a signature duplicate is verified.",
        "POLICY-202 (Fraud Mitigation): High-value unauthorized dispute claims exceeding $1,000.00 require absolute signature documentation validation. If no signature is present on the store merchant file, flag the case for immediate human-in-the-loop manual review exception.",
        "POLICY-303 (Merchant Cancellation Returns): Refund claims concerning missing merchant items require the customer to attach a copy of the explicit cancellation receipt or written refund confirmation text from the vendor store."
    ]
    
    collection.add(
        documents=policies,
        ids=["p101", "p202", "p303"]
    )
    print("✓ Successfully indexed bank regulations into local vector storage.")

    # 5. Read our compiled transaction evidence from Phase 1
    if not os.path.exists("evidence_file.json"):
        print("Error: Run transaction_retrieval_agent.py first to establish baseline case streams.")
        return

    with open("evidence_file.json", "r") as f:
        evidence_data = json.load(f)

    # 6. Run Semantic Vector Lookups for each case
    final_rag_prompt_package = []
    
    print("\n🔍 Running Semantic Searches across vector indexes...")
    for case in evidence_data:
        complaint = case["complaint_text"]
        case_id = case["case_id"]
        
        # Search the database for the 1 most mathematically relevant rule
        results = collection.query(
            query_texts=[complaint],
            n_results=1
        )
        matched_policy = results['documents']
        
        # Construct the final prompt wrap context block
        prompt_block = {
            "case_id": case_id,
            "system_instruction": "You are a senior banking compliance evaluation engineer. You must review the provided case files using only the attached policy rules. Do not hallucinate external conditions.",
            "customer_complaint": complaint,
            "verified_ledger_transactions": case["associated_transactions"],
            "retrieved_factual_policy": matched_policy
        }
        final_rag_prompt_package.append(prompt_block)
        print(f"-> Case {case_id}: Matched with {matched_policy[0][:40]}...")

    # 7. Output the complete context file pack
    with open("rag_prompt_package.json", "w") as f:
        json.dump(final_rag_prompt_package, f, indent=4)
    print("\n🌟 Phase 2 Complete! Output saved to: rag_prompt_package.json")

if __name__ == "__main__":
    run_policy_rag()
