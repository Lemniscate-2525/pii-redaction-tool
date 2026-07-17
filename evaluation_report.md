# Evaluation Report : 

## Objective : 

The objective was to measure the effectiveness of the PII detection component used in the redaction pipeline.

Since no labeled benchmark dataset was provided with the assignment, I used a manually annotated sample of the prospectus as ground truth.

---

## Evaluation Methodology : 

The evaluation process:

1. Selects a section of the prospectus.
2. Manually identifies sensitive entities.
3. Stores these entities in `ground_truth.json`.
4. Runs the detector on that same sample.
5. Compares detected entities against the manually annotated ground truth.
6. Computes evaluation metrics.

---

## Metrics : 

### Precision : 

Measures how many detected entities were actually correct. 

```
Precision = TP / (TP + FP) 
```

Higher precision indicates fewer false positives.

---

### Recall : 

True entities that were successfully detected.

```
Recall = TP / (TP + FN)
```

Higher recall means less missed entities.

---

### F1 Score : 

The harmonic mean of precision and recall.

```
F1 = 2PR / (P + R)
```

---

### Accuracy : 

An approximate accuracy value is also reported based on detected entities within the evaluation sample.

---

## Detection Strategy : 

The detector uses:

- Microsoft Presidio NER.
- spaCy language model.
- Regular expression matching.

Structured entities such as PAN and Aadhaar are detected using regex, while contextual entities such as person names and organizations are detected using NER.

Duplicate detections and overlapping entities are removed before replacement.

---

## Observations : 

The combined NER and regex approach performs well on structured identifiers such as email addresses, phone numbers, PAN numbers and Aadhaar numbers.

Some organization names may not always be detected due to limitations of the underlying language model.

Overall, combining NER with regex improves detection coverage compared to using either technique independently.

---

## Disadvantages : 

- Evaluation is based on a manually annotated sample rather than the complete document.
- Performance depends on the underlying spaCy NER model.
- Financial documents may contain organization names that require custom recognizers for improved accuracy.

---

## Future Improvements : 

- Training a custom NER model for financial documents.
- Adding additional Presidio recognizers.
- Improving formatting preservation for complex Word documents.
- Supporting PDF and scanned documents.
- Providing REST API and Docker deployment.