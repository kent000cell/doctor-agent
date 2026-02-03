#!/usr/bin/env python3
"""Simple RxNorm API Test Script"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.services.rxnorm_api import rxnorm_client


def test_rxnorm_api():
    """Test RxNorm API functionality"""
    print("=" * 70)
    print("RxNorm API Integration Test")
    print("=" * 70)

    # Test 1: Search for ibuprofen
    print("\n[Test 1] Searching for 'ibuprofen'...")
    try:
        drugs = rxnorm_client.search_drugs("ibuprofen")
        print(f"✓ Found {len(drugs)} results")
        if drugs:
            for i, drug in enumerate(drugs[:3], 1):
                print(f"  {i}. {drug['name']} (RxCUI: {drug['rxcui']})")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 2: Get drug info
    print("\n[Test 2] Getting drug info for Ibuprofen (RxCUI: 5640)...")
    try:
        info = rxnorm_client.get_drug_info("5640")
        if info:
            print(f"✓ Drug: {info.get('name')}")
            print(f"  Type: {info.get('tty')}")
            print(f"  RxCUI: {info.get('rxcui')}")
        else:
            print("✗ No info found")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 3: Check interactions
    print("\n[Test 3] Checking interactions for Aspirin (RxCUI: 1191)...")
    try:
        interactions = rxnorm_client.get_drug_interactions("1191")
        print(f"✓ Found {len(interactions)} interactions")
        if interactions:
            for i, interaction in enumerate(interactions[:5], 1):
                print(f"  {i}. {interaction['drug']}")
                print(f"     Severity: {interaction['severity']}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 4: Search for acetaminophen
    print("\n[Test 4] Searching for 'acetaminophen'...")
    try:
        drugs = rxnorm_client.search_drugs("acetaminophen")
        print(f"✓ Found {len(drugs)} results")
        if drugs:
            print(f"  Top result: {drugs[0]['name']}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 5: Test with tool registry
    print("\n[Test 5] Testing with Tool Registry...")
    try:
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

        print("✓ Tool execution successful")
        print("\nMedication Results:")
        print("-" * 70)
        print(result[:500] + "..." if len(result) > 500 else result)
        print("-" * 70)

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)
    print("All tests completed!")
    print("=" * 70)


if __name__ == "__main__":
    test_rxnorm_api()
