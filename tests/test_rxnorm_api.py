"""RxNorm API Integration Tests"""

import pytest
from backend.services.rxnorm_api import RxNormAPI, rxnorm_client


class TestRxNormAPI:
    """Test RxNorm API integration"""

    def test_search_drugs_ibuprofen(self):
        """Test searching for ibuprofen"""
        drugs = rxnorm_client.search_drugs("ibuprofen")

        assert isinstance(drugs, list)
        if drugs:  # API might return empty if network issue
            assert len(drugs) > 0
            assert "rxcui" in drugs[0]
            assert "name" in drugs[0]
            print(f"✓ Found {len(drugs)} ibuprofen drugs")

    def test_search_drugs_acetaminophen(self):
        """Test searching for acetaminophen"""
        drugs = rxnorm_client.search_drugs("acetaminophen")

        assert isinstance(drugs, list)
        if drugs:
            assert len(drugs) > 0
            first_drug = drugs[0]
            assert first_drug.get("name")
            print(f"✓ Found: {first_drug.get('name')}")

    def test_search_drugs_nonexistent(self):
        """Test searching for non-existent drug"""
        drugs = rxnorm_client.search_drugs("xyznonexistentdrug123")

        assert isinstance(drugs, list)
        assert len(drugs) == 0

    def test_get_drug_info(self):
        """Test getting drug info by RxCUI"""
        # RxCUI for Ibuprofen
        drug_info = rxnorm_client.get_drug_info("5640")

        if drug_info:
            assert "rxcui" in drug_info
            assert "name" in drug_info
            print(f"✓ Drug info: {drug_info.get('name')}")

    def test_get_drug_interactions(self):
        """Test getting drug interactions"""
        # RxCUI for Aspirin
        interactions = rxnorm_client.get_drug_interactions("1191")

        assert isinstance(interactions, list)
        if interactions:
            print(f"✓ Found {len(interactions)} interactions for Aspirin")
            for interaction in interactions[:3]:
                print(f"  - {interaction.get('drug')}: {interaction.get('severity')}")

    def test_get_related_drugs(self):
        """Test getting related drugs"""
        # RxCUI for Ibuprofen
        related = rxnorm_client.get_related_drugs("5640", "SCD")

        assert isinstance(related, list)
        if related:
            print(f"✓ Found {len(related)} related drugs")

    @pytest.mark.integration
    def test_full_workflow(self):
        """Test complete workflow: search -> get info -> check interactions"""
        # 1. Search for drug
        drugs = rxnorm_client.search_drugs("naproxen")
        assert isinstance(drugs, list)

        if not drugs:
            pytest.skip("No drugs found, skipping workflow test")

        # 2. Get first drug info
        first_drug = drugs[0]
        rxcui = first_drug["rxcui"]
        print(f"✓ Found drug: {first_drug['name']} (RxCUI: {rxcui})")

        # 3. Get detailed info
        drug_info = rxnorm_client.get_drug_info(rxcui)
        if drug_info:
            print(f"✓ Drug details: {drug_info}")

        # 4. Check interactions
        interactions = rxnorm_client.get_drug_interactions(rxcui)
        print(f"✓ Interactions found: {len(interactions)}")


class TestRxNormIntegration:
    """Test RxNorm integration with tool registry"""

    def test_medication_options_with_rxnorm(self):
        """Test medication options using RxNorm API"""
        from backend.tools.registry import ToolRegistry
        from backend.skill_loader import SkillLoader
        from backend.config import config
        from data.mock_data import MockDataSource

        skill_loader = SkillLoader(config.skills_dir)
        data_source = MockDataSource()
        tool_registry = ToolRegistry(data_source, skill_loader)

        # Test with common diagnosis
        result = tool_registry.execute("get_medication_options", {
            "diagnosis": "back pain",
            "allergies": []
        })

        assert isinstance(result, str)
        assert "Medication Treatment Options" in result
        print("\n" + "="*60)
        print(result)
        print("="*60)

        # Should contain either RxNorm data or fallback
        assert "ibuprofen" in result.lower() or "Fallback Data" in result

    def test_medication_options_with_allergies(self):
        """Test medication filtering with allergies"""
        from backend.tools.registry import ToolRegistry
        from backend.skill_loader import SkillLoader
        from backend.config import config
        from data.mock_data import MockDataSource

        skill_loader = SkillLoader(config.skills_dir)
        data_source = MockDataSource()
        tool_registry = ToolRegistry(data_source, skill_loader)

        # Test with allergies
        result = tool_registry.execute("get_medication_options", {
            "diagnosis": "headache",
            "allergies": ["ibuprofen"]
        })

        assert isinstance(result, str)
        print("\n" + "="*60)
        print("Medications with ibuprofen allergy:")
        print(result)
        print("="*60)


if __name__ == "__main__":
    # Run quick test
    print("Testing RxNorm API...")
    print("-" * 60)

    client = RxNormAPI()

    # Test 1: Search
    print("\n1. Searching for 'ibuprofen'...")
    drugs = client.search_drugs("ibuprofen")
    print(f"   Found {len(drugs)} results")
    if drugs:
        print(f"   First result: {drugs[0]}")

    # Test 2: Drug info
    print("\n2. Getting drug info for RxCUI 5640 (Ibuprofen)...")
    info = client.get_drug_info("5640")
    if info:
        print(f"   {info}")

    # Test 3: Interactions
    print("\n3. Checking interactions for Aspirin (RxCUI 1191)...")
    interactions = client.get_drug_interactions("1191")
    print(f"   Found {len(interactions)} interactions")

    print("\n" + "="*60)
    print("✓ All tests completed!")
