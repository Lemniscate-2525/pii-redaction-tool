from dataclasses import dataclass


@dataclass
class DetectedEntity:
    text: str
    entity_type: str
    start: int
    end: int
    confidence: float


@dataclass
class FakeIdentity:
    fake_name: str
    fake_email: str
    fake_phone: str
    fake_address: str
    fake_company: str