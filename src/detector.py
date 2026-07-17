import re
from typing import List

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

from .models import DetectedEntity


class PIIDetector:

    def __init__(self):

        configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {
                    "lang_code": "en",
                    "model_name": "en_core_web_sm"
                }
            ]
        }

        provider = NlpEngineProvider(nlp_configuration=configuration)
        nlp_engine = provider.create_engine()

        self.analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine,
            supported_languages=["en"]
        )

        # Entity types we actually want
        self.allowed_entities = {
            "PERSON",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "ORGANIZATION",
            "LOCATION",
            "ADDRESS",
            "IP_ADDRESS",
            "URL",
            "DATE_TIME",
            "CREDIT_CARD"
        }

        self.generic_words = {

            "registrar",
            "limited",
            "private",
            "public",
            "equity",
            "shares",
            "offer",
            "issue",
            "book",
            "manager",
            "lead",
            "stock",
            "exchange",
            "india",
            "sebi",
            "board",
            "company",
            "corporate",
            "office",
            "contact",
            "telephone",
            "website",
            "promoters",
            "risk",
            "general",
            "section",
            "chapter",
            "table",
            "financial",
            "prospectus",
            "chapter",
            "annexure",
            "schedule",
            "merchant",
            "banker",
            "depository",
            "investor",
            "listing",
            "application",
            "shares",
            "issue",
            "offer"
        }

        self.patterns = {

            "PAN": re.compile(
                r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
            ),

            "AADHAAR": re.compile(
                r"\b\d{4}\s?\d{4}\s?\d{4}\b"
            ),

            "PHONE_NUMBER": re.compile(
                r"(\+91[\-\s]?)?[6-9]\d{9}\b"
            ),

            "EMAIL_ADDRESS": re.compile(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
            )
        }

    def detect(self, text: str) -> List[DetectedEntity]:

        entities = []

        presidio_results = self.analyzer.analyze(
            text=text,
            language="en"
        )

        for result in presidio_results:

            if result.score < 0.65:
                continue

            if result.entity_type not in self.allowed_entities:
                continue

            entity_text = text[result.start:result.end]

            if not self._keep_entity(entity_text, result.entity_type):
                continue

            entities.append(
                DetectedEntity(
                    text=entity_text,
                    entity_type=result.entity_type,
                    start=result.start,
                    end=result.end,
                    confidence=result.score
                )
            )

        entities.extend(self._regex_entities(text))

        entities = self._remove_duplicates(entities)

        entities = self._remove_overlaps(entities)

        entities.sort(key=lambda x: x.start)

        return entities

    def _regex_entities(self, text):

        output = []

        for entity_type, pattern in self.patterns.items():

            for match in pattern.finditer(text):

                output.append(
                    DetectedEntity(
                        text=match.group(),
                        entity_type=entity_type,
                        start=match.start(),
                        end=match.end(),
                        confidence=1.0
                    )
                )

        return output

    def _keep_entity(self, value, entity_type):

        value = value.strip()

        if len(value) <= 2:
            return False

        if entity_type == "PERSON":

            if value.lower() in self.generic_words:
                return False

            if any(ch.isdigit() for ch in value):
                return False

            if len(value.split()) > 6:
                return False

        if entity_type == "ORGANIZATION":

            if len(value) < 3:
                return False

        if entity_type == "DATE_TIME":

            return False

        return True

    def _remove_duplicates(self, entities):

        unique = {}

        for entity in entities:

            key = (
                entity.start,
                entity.end,
                entity.entity_type
            )

            if key not in unique:
                unique[key] = entity

        return list(unique.values())

    def _remove_overlaps(self, entities):

        entities.sort(
            key=lambda e: (
                e.start,
                -(e.end - e.start),
                -e.confidence
            )
        )

        filtered = []

        occupied = []

        for entity in entities:

            keep = True

            for s, e in occupied:

                if entity.start < e and entity.end > s:
                    keep = False
                    break

            if keep:

                filtered.append(entity)

                occupied.append((entity.start, entity.end))

        return filtered