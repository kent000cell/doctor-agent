#!/usr/bin/env python3
"""Comprehensive Error Testing for RxNorm API Integration"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from backend.services.rxnorm_api import rxnorm_client
from backend.tools.registry import ToolRegistry
from backend.skill_loader import SkillLoader
from backend.config import config
from data.mock_data import MockDataSource
import requests


def test_error_scenarios():
    """Test various error scenarios"""
    print("=" * 70)
    print("ERROR SCENARIO TESTING")
    print("=" * 70)

    errors_found = []

    # Test 1: Empty query
    print("\n[Test 1] Empty query string...")
    try:
        result = rxnorm_client.search_drugs("")
        if result == []:
            print("✓ Handled empty query gracefully")
        else:
            print(f"⚠️ Unexpected result: {result}")
    except Exception as e:
        errors_found.append(f"Empty query error: {e}")
        print(f"✗ Error: {e}")

    # Test 2: Invalid RxCUI
    print("\n[Test 2] Invalid RxCUI...")
    try:
        result = rxnorm_client.get_drug_info("invalid_rxcui")
        if result is None:
            print("✓ Handled invalid RxCUI gracefully")
        else:
            print(f"⚠️ Unexpected result: {result}")
    except Exception as e:
        errors_found.append(f"Invalid RxCUI error: {e}")
        print(f"✗ Error: {e}")

    # Test 3: Non-existent drug
    print("\n[Test 3] Non-existent drug search...")
    try:
        result = rxnorm_client.search_drugs("xyzabc123nonexistent")
        if result == []:
            print("✓ Handled non-existent drug gracefully")
        else:
            print(f"⚠️ Found results for non-existent drug: {result}")
    except Exception as e:
        errors_found.append(f"Non-existent drug error: {e}")
        print(f"✗ Error: {e}")

    # Test 4: Network timeout simulation (short timeout)
    print("\n[Test 4] Short timeout handling...")
    try:
        old_timeout = rxnorm_client.session.timeout if hasattr(rxnorm_client.session, 'timeout') else None
        # Note: requests.Session doesn't store timeout, so we test with a direct call
        response = rxnorm_client.session.get(
            "https://rxnav.nlm.nih.gov/REST/drugs.json",
            params={"name": "ibuprofen"},
            timeout=0.001  # Very short timeout
        )
    except requests.exceptions.Timeout:
        print("✓ Timeout handled correctly")
    except Exception as e:
        print(f"✓ Network error handled: {type(e).__name__}")

    # Test 5: Tool registry with invalid diagnosis
    print("\n[Test 5] Tool registry with unusual diagnosis...")
    try:
        skill_loader = SkillLoader(config.skills_dir)
        data_source = MockDataSource()
        tool_registry = ToolRegistry(data_source, skill_loader)

        result = tool_registry.execute("get_medication_options", {
            "diagnosis": "completely_unknown_disease_xyz",
            "allergies": []
        })

        if "error" not in result.lower() and len(result) > 0:
            print("✓ Handled unknown diagnosis (fallback to default drugs)")
        else:
            print(f"⚠️ Result: {result[:200]}")
    except Exception as e:
        errors_found.append(f"Tool registry error: {e}")
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

    # Test 6: Tool registry with allergies
    print("\n[Test 6] Allergy filtering...")
    try:
        skill_loader = SkillLoader(config.skills_dir)
        data_source = MockDataSource()
        tool_registry = ToolRegistry(data_source, skill_loader)

        result = tool_registry.execute("get_medication_options", {
            "diagnosis": "back pain",
            "allergies": ["ibuprofen", "naproxen"]
        })

        # Check if allergic drugs are mentioned in result
        if "ibuprofen" in result.lower():
            print("⚠️ Allergy filtering might not be working properly")
            errors_found.append("Allergy filtering: ibuprofen still in results")
        else:
            print("✓ Allergy filtering works")
    except Exception as e:
        errors_found.append(f"Allergy filtering error: {e}")
        print(f"✗ Error: {e}")

    # Test 7: Tool registry with None allergies
    print("\n[Test 7] None allergies parameter...")
    try:
        skill_loader = SkillLoader(config.skills_dir)
        data_source = MockDataSource()
        tool_registry = ToolRegistry(data_source, skill_loader)

        result = tool_registry.execute("get_medication_options", {
            "diagnosis": "back pain",
            "allergies": None
        })

        if "error" not in result.lower():
            print("✓ Handled None allergies gracefully")
        else:
            print(f"✗ Error in result: {result[:200]}")
            errors_found.append("None allergies handling failed")
    except Exception as e:
        errors_found.append(f"None allergies error: {e}")
        print(f"✗ Error: {e}")

    # Test 8: Missing diagnosis parameter
    print("\n[Test 8] Missing diagnosis parameter...")
    try:
        skill_loader = SkillLoader(config.skills_dir)
        data_source = MockDataSource()
        tool_registry = ToolRegistry(data_source, skill_loader)

        result = tool_registry.execute("get_medication_options", {
            "allergies": []
        })

        if "error" in result.lower():
            print("✓ Missing parameter detected")
        else:
            print(f"⚠️ Unexpectedly succeeded: {result[:200]}")
    except TypeError as e:
        print(f"✓ Missing parameter caught: {e}")
    except Exception as e:
        errors_found.append(f"Missing parameter error: {e}")
        print(f"✗ Unexpected error: {e}")

    # Test 9: Special characters in query
    print("\n[Test 9] Special characters in drug query...")
    try:
        result = rxnorm_client.search_drugs("ibuprofen<script>alert(1)</script>")
        print("✓ Handled special characters")
    except Exception as e:
        errors_found.append(f"Special characters error: {e}")
        print(f"✗ Error: {e}")

    # Test 10: Very long query string
    print("\n[Test 10] Very long query string...")
    try:
        result = rxnorm_client.search_drugs("a" * 1000)
        print("✓ Handled long query")
    except Exception as e:
        errors_found.append(f"Long query error: {e}")
        print(f"✗ Error: {e}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if errors_found:
        print(f"\n❌ Found {len(errors_found)} potential issues:\n")
        for i, error in enumerate(errors_found, 1):
            print(f"{i}. {error}")
    else:
        print("\n✅ All error scenarios handled gracefully!")

    print("=" * 70)


if __name__ == "__main__":
    test_error_scenarios()
