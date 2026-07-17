from faker import Faker


class IdentityMapper:
    """
    Maintains a consistent mapping between original PII values
    and generated fake values.
    """

    def __init__(self):

        self.faker = Faker()

        # (entity_type, original_value) -> fake_value
        self.mapping = {}

    def get_fake_value(self, original_value: str, entity_type: str) -> str:

        entity_type = entity_type.upper()

        key = (entity_type, original_value)

        if key in self.mapping:
            return self.mapping[key]

        fake_value = self._generate(entity_type, original_value)

        self.mapping[key] = fake_value

        return fake_value

    def _generate(self, entity_type: str, original_value: str) -> str:

        # ---------------- PERSON ----------------

        if entity_type == "PERSON":
            return self.faker.name()

        # ---------------- ORGANIZATIONS ----------------

        elif entity_type in [
            "ORGANIZATION",
            "ORG",
            "COMPANY",
            "COMPANY_NAME"
        ]:
            return self.faker.company()

        # ---------------- EMAIL ----------------

        elif entity_type in [
            "EMAIL",
            "EMAIL_ADDRESS"
        ]:
            return self.faker.email()

        # ---------------- PHONE ----------------

        elif entity_type in [
            "PHONE",
            "PHONE_NUMBER"
        ]:
            return "+91 " + self.faker.numerify("##########")

        # ---------------- ADDRESS ----------------

        elif entity_type in [
            "ADDRESS",
            "LOCATION",
            "LOC"
        ]:
            return self.faker.address().replace("\n", ", ")

        # ---------------- URL ----------------

        elif entity_type in [
            "URL",
            "WEBSITE"
        ]:
            return self.faker.url()

        # ---------------- IP ----------------

        elif entity_type == "IP_ADDRESS":
            return self.faker.ipv4()

        # ---------------- DATE ----------------

        elif entity_type == "DATE_TIME":
            return str(self.faker.date())

        # ---------------- CREDIT CARD ----------------

        elif entity_type == "CREDIT_CARD":
            return self.faker.credit_card_number()

        # ---------------- PAN ----------------

        elif entity_type == "PAN":
            return (
                self.faker.lexify("?????").upper()
                + self.faker.numerify("####")
                + self.faker.lexify("?").upper()
            )

        # ---------------- AADHAAR ----------------

        elif entity_type == "AADHAAR":
            return self.faker.numerify("#### #### ####")

        # ---------------- PASSPORT ----------------

        elif entity_type == "PASSPORT":
            return self.faker.bothify("?#???????").upper()

        # ---------------- BANK ACCOUNT ----------------

        elif entity_type in [
            "BANK_ACCOUNT",
            "ACCOUNT_NUMBER"
        ]:
            return self.faker.numerify("################")

        # ---------------- ROUTING / IFSC ----------------

        elif entity_type in [
            "IFSC",
            "ROUTING_NUMBER"
        ]:
            return (
                self.faker.lexify("????").upper()
                + "0"
                + self.faker.lexify("??????").upper()
            )

        # ---------------- SSN ----------------

        elif entity_type == "US_SSN":
            return self.faker.ssn()

        # ---------------- FALLBACKS ----------------

        # If Presidio detects an unknown organization-like entity,
        # don't show <REDACTED>. Produce something realistic.

        elif "ORG" in entity_type:
            return self.faker.company()

        elif "COMPANY" in entity_type:
            return self.faker.company()

        elif "ADDRESS" in entity_type:
            return self.faker.address().replace("\n", ", ")

        elif "EMAIL" in entity_type:
            return self.faker.email()

        elif "PHONE" in entity_type:
            return "+91 " + self.faker.numerify("##########")

        elif "PERSON" in entity_type:
            return self.faker.name()

        elif "DATE" in entity_type:
            return str(self.faker.date())

        # LAST RESORT
        return self.faker.word().title()