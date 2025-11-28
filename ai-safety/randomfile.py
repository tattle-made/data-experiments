from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, PatternRecognizer
from presidio_analyzer.nlp_engine import SpacyNlpEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.predefined_recognizers import EmailRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer import EntityRecognizer, RecognizerResult
import re


# -------------------------------------------------------
# 2. Wrap HF NER into a custom Presidio recognizer
# -------------------------------------------------------
class HFNERRecognizer(EntityRecognizer):
    """
    A custom recognizer that uses a HuggingFace NER model.
    """

    def load(self):
        pass  # Already loaded

    def analyze(self, text, ner_pipeline, entities, nlp_artifacts=None):
        results = []

        hf_entities = ner_pipeline(text)

        for ent in hf_entities:
            entity_type = ent["entity_group"].upper()

            # Map HF labels → Presidio labels
            if entity_type == "PER":
                label = "PERSON"
            elif entity_type == "ORG":
                label = "ORGANIZATION"
            elif entity_type == "LOC":
                label = "LOCATION"
            else:
                continue

            results.append(
                RecognizerResult(
                    entity_type=label,
                    start=ent["start"],
                    end=ent["end"],
                    score=float(ent["score"])
                )
            )

        return results


# -------------------------------------------------------
# 3. Create SPAcy engine (for tokenization + regex)
# -------------------------------------------------------

spacy_config = {
    "model_registry": {
        "en": "en_core_web_sm"
    },
    "models": [
        {"lang_code": "en", "model_name": "en_core_web_sm"}
    ]
}

nlp_engine = SpacyNlpEngine(spacy_config)
registry = RecognizerRegistry()


# -------------------------------------------------------
# 4. Add the custom HF NER recognizer
# -------------------------------------------------------

hf_recognizer = HFNERRecognizer(supported_entities=["PERSON", "LOCATION", "ORGANIZATION"])
registry.add_recognizer(hf_recognizer)


# -------------------------------------------------------
# 5. Add India-specific regex recognizers (phone, Aadhaar, PAN, etc.)
# -------------------------------------------------------

# Phone number
phone_pattern = PatternRecognizer(
    supported_entity="PHONE_NUMBER",
    patterns=[
        {"name": "phone_number", "regex": r"\b[6-9]\d{9}\b", "score": 0.7}
    ]
)
registry.add_recognizer(phone_pattern)

# Aadhaar
aadhaar_pattern = PatternRecognizer(
    supported_entity="AADHAAR",
    patterns=[
        {"name": "aadhaar", "regex": r"\b\d{4}\s\d{4}\s\d{4}\b", "score": 0.8}
    ]
)
registry.add_recognizer(aadhaar_pattern)

# PAN
pan_pattern = PatternRecognizer(
    supported_entity="PAN",
    patterns=[
        {"name": "pan", "regex": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", "score": 0.8}
    ]
)
registry.add_recognizer(pan_pattern)


# -------------------------------------------------------
# 6. Create Analyzer + Anonymizer
# -------------------------------------------------------

analyzer = AnalyzerEngine(
    nlp_engine=nlp_engine,
    registry=registry
)

anonymizer = AnonymizerEngine()


# -------------------------------------------------------
# 7. Test text (English + Romanized Hindi + Hindi)
# -------------------------------------------------------

text = """
My name is Anjali and my phone number is 9876543210.
mera aadhaar 1234 5678 9123 hai
मेरा नाम रोहन है और मेरा आधार 1234 5678 9123 है
"""

results = analyzer.analyze(text=text, language="en")
print("Detected PII:\n", results)

anonymized = anonymizer.anonymize(text, results)
print("\nAnonymized text:\n", anonymized.text)




# LANGUAGES_CONFIG_FILE = "./docs/analyzer/languages-config.yml"

# # Create NLP engine based on configuration file
# provider = NlpEngineProvider(conf_file=LANGUAGES_CONFIG_FILE)
# nlp_engine_with_spanish = provider.create_engine()

# # Setting up an English Email recognizer:
# email_recognizer_en = EmailRecognizer(supported_language="en", context=["email", "mail"])
# registry = RecognizerRegistry()

# # Add recognizers to registry
# registry.add_recognizer(email_recognizer_en)

# # Set up analyzer with our updated recognizer registry
# analyzer = AnalyzerEngine(
#     registry=registry,
#     supported_languages=["en","es"],
#     nlp_engine=nlp_engine_with_spanish)

# analyzer.analyze(text="My name is David", language="en")