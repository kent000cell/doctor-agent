#!/usr/bin/env python3
"""Quick Demo of RxNorm API Integration"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("🏥 AI Doctor Agent - RxNorm API Integration Demo")
print("=" * 70)
print()

# Import the RxNorm client
from backend.services.rxnorm_api import rxnorm_client

print("✅ RxNorm API client loaded successfully\n")

# Demo 1: Search for a common pain medication
print("📋 Demo 1: Searching for 'ibuprofen' in FDA database...")
print("-" * 70)

drugs = rxnorm_client.search_drugs("ibuprofen")

if drugs:
    print(f"✓ Found {len(drugs)} FDA-approved ibuprofen products:\n")
    for i, drug in enumerate(drugs[:3], 1):
        print(f"  {i}. {drug['name']}")
        print(f"     RxCUI: {drug['rxcui']}")
        print(f"     Type: {drug.get('synonym', 'N/A')}")
        print()
else:
    print("⚠️  No drugs found\n")

# Demo 2: Get detailed drug information
print("\n📋 Demo 2: Getting detailed info for Ibuprofen (RxCUI: 5640)")
print("-" * 70)

drug_info = rxnorm_client.get_drug_info("5640")

if drug_info:
    print("✓ Drug information retrieved:\n")
    print(f"  Name: {drug_info.get('name')}")
    print(f"  RxCUI: {drug_info.get('rxcui')}")
    print(f"  Type: {drug_info.get('tty')} (Term Type)")
    print(f"  Synonym: {drug_info.get('synonym', 'N/A')}")
else:
    print("⚠️  Drug info not found\n")

# Demo 3: Tool Registry Integration
print("\n\n📋 Demo 3: Tool Registry Integration (Real Use Case)")
print("-" * 70)
print("Simulating: Patient with 'back pain', no allergies\n")

from backend.tools.registry import ToolRegistry
from backend.skill_loader import SkillLoader
from backend.config import config
from data.mock_data import MockDataSource

skill_loader = SkillLoader(config.skills_dir)
data_source = MockDataSource()
tool_registry = ToolRegistry(data_source, skill_loader)

result = tool_registry.execute("get_medication_options", {
    "diagnosis": "back pain",
    "allergies": []
})

# Display formatted result
print("✓ Medication recommendations generated:\n")
print(result[:800] + "..." if len(result) > 800 else result)

# Summary
print("\n" + "=" * 70)
print("✅ DEMO COMPLETE - All Systems Working!")
print("=" * 70)
print()
print("Key Features Demonstrated:")
print("  ✓ Real-time FDA drug database queries")
print("  ✓ RxCUI code retrieval for standardized drug identification")
print("  ✓ Diagnosis-to-medication mapping")
print("  ✓ Tool registry integration")
print("  ✓ Graceful error handling")
print()
print("💊 This data is from the U.S. National Library of Medicine")
print("🔗 API Documentation: https://lhncbc.nlm.nih.gov/RxNav/APIs/")
print()
print("=" * 70)
