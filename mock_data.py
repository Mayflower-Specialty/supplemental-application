"""
Mock data for generating a filled example of the Mayflower AI Liability Supplemental Application.
This represents a realistic but fictitious application submission.
"""

# Company: Acme AI Solutions, Inc. - A mid-sized enterprise AI software company
# Profile: Provides AI-powered business intelligence and document automation tools
# Risk Profile: Medium - Good governance, some third-party dependencies, clean loss history

MOCK_DATA = {
    # Coverage selection (indices)
    "coverage_modules": [0, 2],  # AI-D&O and AI-E&O

    # Section I - Applicant Information
    "named_insured": "Acme AI Solutions, Inc. and its wholly-owned subsidiaries",
    "dba": "Acme AI",
    "state_incorporation": "Delaware",
    "address": "1234 Innovation Drive, Suite 500",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94103",
    "phone": "(999) 999-9999",
    "email": "info@acmeai.example",
    "website": "www.acmeai.example",
    "industry": "Enterprise AI Software & Services",
    "naics": "541512",
    "year_founded": "2019",
    "annual_revenue": "$12,500,000",
    "total_employees": "87",
    "num_locations": "3",
    "policy_period": "March 1, 2026 - March 1, 2027",
    "aggregate_limit": "$5,000,000",
    "contact_name": "John Doe, Chief Risk Officer",
    "contact_email_phone": "john.doe@acmeai.example / (999) 999-9999",
    "ownership_structure": [0],  # Privately Held
    "business_type": [0],  # Corporation
    "geographic_scope": [1],  # US and EU/UK

    # Section II - AI Systems Overview
    "q2_1_systems": [1],  # 1 to 2
    "q2_2_schedule": "See attached AI System Inventory spreadsheet. Primary system: DocuMind AI (NLP document processing), deployed March 2023, last updated Dec 2025.",
    "q2_3_integration": [1],  # Semi-Autonomous
    "q2_4_materiality": [1],  # Medium
    "q2_5a_decisions": "~850,000",
    "q2_5b_individuals": "~12,000",
    "q2_5c_revenue": "$8,200,000",
    "q2_5d_usage": [("customer-facing (%)", 1, "65"), ("business-to-business (%)", 1, "30"), ("internal-only (%)", 1, "5")],
    "q2_6_deployment": [1],  # AI Provider, embedded
    "q2_7_generative": [1],  # Yes, internal only
    "q2_7a_models": "Claude 3.5 Sonnet (Anthropic API), GPT-4 (Azure OpenAI private deployment) - used for document summarization and draft generation.",
    "q2_7b_guardrails": [0, 1, 2, 4, 5],  # Input validation, output moderation, RAG, rate limiting, logging
    "q2_8_third_party": [2],  # Critical, supported vendor
    "q2_8a_vendor": [0, 1, 2, 5],  # Written contract, security attestation, DPA, fallback plan
    "q2_9_autonomous": "No",
    "q2_9a_autonomous_desc": "",
    "q2_10_agents": [0],  # No agents in production
    "q2_10a_agents_desc": "",
    "q2_11_prohibited": [6],  # None of the above

    # Section III - AI Governance
    "q3_1_framework": [0],  # Yes, fully implemented
    "q3_2_frameworks": [0, 7],  # NIST AI RMF, Internal framework
    "q3_2_other": "",
    "q3_3_oversight": [0],  # Yes
    "q3_3a_oversight_desc": "AI Governance Committee: CTO (chair), CRO, General Counsel, Head of AI, Data Governance Lead. Reports to CEO quarterly. Meets monthly. Last meeting: January 15, 2026.",
    "q3_4_board_reporting": [1],  # Yes, quarterly
    "q3_5_ethics_policy": [0],  # Yes
    "q3_6_standards": [0],  # Yes
    "q3_7_documentation": [1],  # Partial
    "q3_8_xai": [0],  # Yes, global and local
    "q3_8_xai_desc": "SHAP values for all classification models; attention visualization for NLP models.",
    "q3_9_human_oversight": [2],  # Human-on-the-Loop
    "q3_10_vendor_mgmt": [0],  # Yes
    "q3_11_change_mgmt": [0],  # Yes, formal
    "q3_12_predeployment": [0, 1, 3, 4, 6],  # Risk assessment, bias eval, security review, legal review, business sign-off
    "q3_13_training": [0],  # Yes, mandatory
    "q3_14_accountabilities": [0, 1, 4, 5, 7],  # Exec sponsor, Head of AI, Data governance, AI security, AI legal

    # Section IV - Data Governance
    "q4_1_lineage": [1],  # Partial
    "q4_2_quality": [1],  # Partial
    "q4_3_bias": [1],  # Partial
    "q4_3a_bias_desc": "Demographic parity and equal opportunity metrics tested quarterly on gender, age, geography. Most recent test: December 2025.",
    "q4_4_data_categories": [0, 6],  # PII, Geolocation
    "q4_5_compliance": [1],  # Full compliance, attested
    "q4_5a_regulations": [0, 1],  # GDPR, CCPA/CPRA
    "q4_6_retention": [0],  # Yes
    "q4_7_provenance": [0, 2, 4],  # First-party/licensed, fair-use, PII screening
    "q4_8_subject_rights": [0],  # Yes

    # Section V - Operations
    "q5_1_criticality": [1],  # Tier 2, Important
    "q5_2_external_infra": [1],  # Critical, multi-provider
    "q5_3_fallback": [0],  # Yes
    "q5_4_monitoring": [0],  # Yes, real-time with alerting
    "q5_5_retrain": [1],  # Periodically
    "q5_6_testing": [1],  # Yes, for high-materiality systems only
    "q5_7_override_logging": [0],  # Yes, logged with reason code

    # Section VI - AI Incident Response
    "q6_1_ir_plan": [0],  # Yes, dedicated AI IR plan
    "q6_2_detection": [0, 1, 2, 3],  # Automated alerts (metrics), automated alerts (content), user reporting, employee reporting
    "q6_3_tabletop": [1],  # Yes, one
    "q6_4_complaint": [0],  # Yes, published with stated response time
    "q6_5_appeal": [0],  # Yes, documented with defined timelines
    "q6_6_rca": [0],  # Yes, formal
    "q6_7_incidents": [0],  # 0
    "q6_7a_incident_desc": "",

    # Section VII - Regulatory Environment
    "q7_1_eu_ai_act": [2],  # Yes, Minimal Risk
    "q7_2_us_regs": [1],  # Illinois BIPA
    "q7_3_sector_regs": [3],  # N/A
    "q7_3a_sector_desc": "",
    "q7_4_external_audit": [1],  # Yes, consultant review
    "q7_5_iso_42001": [2],  # Planned
    "q7_6_regulatory_inquiries": "No",
    "q7_6a_inquiries_desc": "",

    # Section VIII - Claims and Loss History
    "q8_1_ai_claims": "No",
    "q8_1a_ai_claims_desc": "",
    "q8_2_other_claims": "No",
    "q8_2a_other_claims_desc": "",
    "q8_3_circumstances": "No",
    "q8_3a_circumstances_desc": "",
    "q8_4_declined": "No",
    "q8_4a_declined_desc": "",

    # Section IX - Prior and Current Insurance
    # (Table data would be filled via a different mechanism)
    "prior_insurance": [
        ["D&O", "Example Insurance Co.", "3/1/25-3/1/26", "$5,000,000", "$250,000", "$78,500"],
        ["EPL", "Example Insurance Co.", "3/1/25-3/1/26", "$2,000,000", "$100,000", "$32,400"],
        ["E&O", "Professional Liability Ins.", "3/1/25-3/1/26", "$3,000,000", "$150,000", "$45,800"],
    ],
    "retro_date": "January 1, 2019",
    "expiration_date": "March 1, 2026",

    # Section XI - Signature
    "signature": "John Doe",
    "signature_date": "February 15, 2026",
    "printed_name": "John Doe",
    "title": "Chief Risk Officer",
    "organization": "Acme AI Solutions, Inc.",
    "sig_email": "jon.doe@acmeai.example",
}
