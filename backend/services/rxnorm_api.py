"""RxNorm API Client

RxNorm is a normalized naming system for drugs provided by the U.S. National Library of Medicine.
API Documentation: https://lhncbc.nlm.nih.gov/RxNav/APIs/
"""

import requests
from typing import List, Dict, Optional
from backend.logger import get_logger

logger = get_logger("rxnorm_api")


class RxNormAPI:
    """RxNorm API Client for drug information"""

    BASE_URL = "https://rxnav.nlm.nih.gov/REST"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "AI-Doctor-Agent/1.0"
        })

    def search_drugs(self, query: str) -> List[Dict]:
        """Search drugs by name

        Args:
            query: Drug name to search

        Returns:
            List of drug information dictionaries
        """
        try:
            url = f"{self.BASE_URL}/drugs.json"
            params = {"name": query}

            logger.info(f"Searching drugs: {query}")
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data.get("drugGroup"):
                logger.warning(f"No drugs found for: {query}")
                return []

            concepts = data["drugGroup"].get("conceptGroup", [])
            drugs = []

            for concept_group in concepts:
                if "conceptProperties" in concept_group:
                    for drug in concept_group["conceptProperties"]:
                        drugs.append({
                            "rxcui": drug.get("rxcui"),
                            "name": drug.get("name"),
                            "synonym": drug.get("synonym", ""),
                        })

            logger.info(f"Found {len(drugs)} drugs for: {query}")
            return drugs[:5]  # Return top 5 results

        except requests.exceptions.RequestException as e:
            logger.error(f"RxNorm API error: {str(e)}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"Unexpected error in search_drugs: {str(e)}", exc_info=True)
            return []

    def get_drug_info(self, rxcui: str) -> Optional[Dict]:
        """Get detailed drug information by RxCUI

        Args:
            rxcui: RxNorm Concept Unique Identifier

        Returns:
            Drug information dictionary or None
        """
        try:
            url = f"{self.BASE_URL}/rxcui/{rxcui}/properties.json"

            logger.info(f"Getting drug info for RxCUI: {rxcui}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data.get("properties"):
                return None

            props = data["properties"]
            return {
                "rxcui": props.get("rxcui"),
                "name": props.get("name"),
                "synonym": props.get("synonym", ""),
                "tty": props.get("tty"),  # Term type (e.g., IN, BN, SCD)
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"RxNorm API error for RxCUI {rxcui}: {str(e)}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_drug_info: {str(e)}", exc_info=True)
            return None

    def get_drug_interactions(self, rxcui: str) -> List[Dict]:
        """Get drug interactions

        Args:
            rxcui: RxNorm Concept Unique Identifier

        Returns:
            List of drug interaction information
        """
        try:
            url = f"{self.BASE_URL}/interaction/interaction.json"
            params = {"rxcui": rxcui}

            logger.info(f"Getting interactions for RxCUI: {rxcui}")
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data.get("interactionTypeGroup"):
                return []

            interactions = []
            for group in data["interactionTypeGroup"]:
                if "interactionType" in group:
                    for interaction_type in group["interactionType"]:
                        if "interactionPair" in interaction_type:
                            for pair in interaction_type["interactionPair"]:
                                interactions.append({
                                    "drug": pair["interactionConcept"][1]["minConceptItem"]["name"],
                                    "severity": pair.get("severity", "Unknown"),
                                    "description": pair.get("description", "No description available")
                                })

            logger.info(f"Found {len(interactions)} interactions for RxCUI: {rxcui}")
            return interactions[:10]  # Return top 10

        except requests.exceptions.RequestException as e:
            logger.error(f"RxNorm API error for interactions: {str(e)}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"Unexpected error in get_drug_interactions: {str(e)}", exc_info=True)
            return []

    def get_related_drugs(self, rxcui: str, relation: str = "SCD") -> List[Dict]:
        """Get related drugs (e.g., generic/brand equivalents)

        Args:
            rxcui: RxNorm Concept Unique Identifier
            relation: Relation type (SCD, BN, IN, etc.)

        Returns:
            List of related drug information
        """
        try:
            url = f"{self.BASE_URL}/rxcui/{rxcui}/related.json"
            params = {"tty": relation}

            logger.info(f"Getting related drugs for RxCUI: {rxcui}, type: {relation}")
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data.get("relatedGroup"):
                return []

            related = []
            for group in data["relatedGroup"].get("conceptGroup", []):
                if "conceptProperties" in group:
                    for drug in group["conceptProperties"]:
                        related.append({
                            "rxcui": drug.get("rxcui"),
                            "name": drug.get("name"),
                            "tty": drug.get("tty")
                        })

            return related

        except requests.exceptions.RequestException as e:
            logger.error(f"RxNorm API error for related drugs: {str(e)}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"Unexpected error in get_related_drugs: {str(e)}", exc_info=True)
            return []


# Singleton instance
rxnorm_client = RxNormAPI()
