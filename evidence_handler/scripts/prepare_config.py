from evidence_handler.core.fields import (
    BooleanField,
    DateTimeField,
    EmailField,
    IntegerField,
    StrConcatFields,
    StringField,
)
from evidence_handler.core.serializer import Serializer
from evidence_handler.scripts.utils import dump_config

if __name__ == "__main__":
    # in this example I supported nested fields (e.g., "user_details.id"). The nesting of objects can be as many levels
    #  as you wish
    # Also there is support for composite fields that are structured and combined from other fields
    #  (StrConcatFields for example)

    evidence_id_to_serializer = {
        1: Serializer(
            fields=[
                IntegerField(field_name="user_details.id", output_field="Id"),
                StrConcatFields(
                    fields=[
                        StringField(field_name="user_details.first_name"),
                        StringField(field_name="user_details.last_name"),
                    ],
                    output_field="Full name",
                ),
                EmailField(field_name="user_details.email", output_field="Email"),
                DateTimeField(field_name="user_details.updated_at", output_field="Updated at"),
                BooleanField(field_name="security.mfa_enabled", output_field="MFA Enabled"),
            ]
        ),
        2: Serializer(
            fields=[
                StringField(field_name="name", output_field="Name"),
                StringField(field_name="id", output_field="ID"),
                StringField(field_name="status", output_field="Authentication status"),
            ]
        ),
    }

    dump_config(evidence_id_to_serializer)
