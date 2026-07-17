import sys
from pathlib import Path

from src.detector import PIIDetector
from src.mapper import IdentityMapper
from src.document_processor import DocumentProcessor


def print_banner():

    print("=" * 60)
    print("Enterprise Data PII Redaction Tool")
    print("=" * 60)


def validate_paths(input_path: str):

    path = Path(input_path)

    if not path.exists():

        raise FileNotFoundError(
            f"Input document not found:\n{input_path}"
        )


def main():

    print_banner()

    INPUT_FILE = "input/Red Herring Prospectus.docx"

    OUTPUT_FILE = "output/redacted_prospectus.docx"

    try:

        validate_paths(INPUT_FILE)

        detector = PIIDetector()

        mapper = IdentityMapper()

        processor = DocumentProcessor(
            detector=detector,
            mapper=mapper
        )

        processor.process_document(
            input_path=INPUT_FILE,
            output_path=OUTPUT_FILE
        )

        print("\nPipeline completed successfully.")

    except Exception as e:

        print("\nPipeline Failed")
        print("-" * 60)
        print(type(e).__name__)
        print(e)
        print("-" * 60)

        sys.exit(1)


if __name__ == "__main__":

    main()