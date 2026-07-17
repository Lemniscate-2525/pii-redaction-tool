# Enterprise PII Redaction Tool : 

## Overview : 

This is a Python-based Personally Identifiable Information (PII) redaction tool developed as part of a take-home Software Engineering Assignment.

It processes Microsoft Word (.docx) documents, detects sensitive information using a combination of Named Entity Recognition (NER) and regular expressions(regex), and replaces the detected PII with realistic fake alternatives while preserving the overall structure of the document.

This approach maintains the readability and usability of the document without exposing sensitive information.

---

## Features : 

Detects and replaces :

  - Person names
  - Email addresses
  - Phone numbers
  - Company / Organization names
  - Physical addresses
  - PAN numbers
  - Aadhaar numbers
  - Credit card numbers
  - IP addresses
  - URLs

- Uses fake replacements instead of deleting information. 

- It maintains consistent replacements throughout the document.

  - For eg :

    - If we replace John Doe → Michael Smith;
    - Then every future occurrence of John Doe is also replaced by Michael Smith.

- It preserves document structure including tables and paragraphs.

---

## Project Structure : 

```
pii-redaction-tool/
│
├── input/
│   └── Red Herring Prospectus.docx
│
├── output/
│   └── redacted_prospectus.docx
│
├── src/
│   ├── config.py
│   ├── detector.py
│   ├── document_processor.py
│   ├── mapper.py
│   └── models.py
│
├── evaluation/
│   ├── evaluator.py
│   ├── ground_truth.json
│   └── evaluation_report.txt
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Approach : 

Combination of multiple detection strategies : 

### 1. Named Entity Recognition (NER) : 

Microsoft Presidio with spaCy (`en_core_web_sm`) is used to detect :

- Person names
- Organizations
- Locations
- Email addresses
- Phone numbers
- URLs
- IP addresses

---

### 2. Regex-based Detection : 

Regular expressions are used for entities that are easier to detect using patterns; 

For eg :

- PAN
- Aadhaar
- Phone numbers
- Email addresses

Regex improves recall for structured identifiers that may not always be recognized by NER.

---

### 3. Fake Identity Generation : 

The Faker library generates realistic replacements instead of masking information.

For eg:

Original -> Fake : 

Name :  John Doe
            ↓
      Michael Smith

Original -> Fake : 

Email : john@gmail.com
            ↓
      michael.smith@example.org

This preserves readability of the doc while protecting sensitive information.

---

### 4. Consistent Mapping : 

Each unique entity is mapped only once.

For eg : 

John Doe
↓
Michael Smith

Every future occurrence of John Doe is replaced with Michael Smith instead of generating a different fake identity.

---

## Technologies Used : 

- Python 3.11+
- Microsoft Presidio
- spaCy
- Faker
- python-docx

---

## Installation : 

Creating a virtual environment; 

```bash
python -m venv venv
```

Activating it; 

Windows

```bash
venv\Scripts\activate
```

Installing dependencies; 

```bash
pip install -r requirements.txt
```

Downloading spaCy model;

```bash
python -m spacy download en_core_web_sm
```
---

## Running the Project : 

```bash
python main.py
```

The redacted document will be generated inside; 

```
output/
```

---

## Evaluation : 

Run

```bash
python -m evaluation.evaluator
```

The evaluator compares detected entities against a manually annotated representative sample and reports :

- Precision
- Recall
- F1 Score
- Approximate Accuracy

Results are stored in; 

```
evaluation/evaluation_report.txt
```

---

## Design Decisions : 

The project intentionally combines NER with regex : 

1. NER performs well on contextual entities such as names and organizations, whereas 
Regex performs better on structured identifiers such as PAN, Aadhaar and phone numbers.

2. Using both provides us with better overall detection than either used alone.


The implementation also removes duplicate detections and overlapping entities before replacement to improve precision.

---

## Trade-offs : 

Advantages : 

- Easy to extend with additional PII types
- Modular architecture
- Good balance between precision and recall
- Consistent fake identity generation

Dis-advantages : 

- Some organization names may not always be detected by the underlying NER model.
- Evaluation is based on a manually annotated sample because no labeled benchmark dataset was provided.
- Paragraph formatting may be simplified when replacements span multiple text runs.

---

## Improvements : 

- Support for PDF documents.
- FastAPI REST API.
- Docker deployment.
- Batch document processing. 
- Custom NER model for financial documents. 

---

## Author : 

Akshat Mishra