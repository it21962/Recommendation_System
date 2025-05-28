import pytest
from marshmallow import Schema, fields
from app.utils.schema_mapper import (
    infer_field_type,
    generate_schema,
    generate_schema_from_config,
)


@pytest.mark.parametrize("field_name,expected_type", [
    ("user_id", "int"),
    ("session_id", "string"),
    ("odds_home", "float"),
    ("stake", "float"),
    ("home_team", "string"),
    ("participants", "string"),
    ("random_field", "string"),
])
def test_infer_field_type(field_name, expected_type):
    assert infer_field_type(field_name) == expected_type


def test_generate_schema_with_label_map():
    fields_list = ["user_id", "home_team", "stake"]
    label_map = {"user_id": "uid", "home_team": "team", "stake": "bet_amount"}

    schema_class = generate_schema(fields_list, label_map)
    schema = schema_class()

    assert isinstance(schema, Schema)
    assert isinstance(schema.fields["user_id"], fields.Int)
    assert schema.fields["user_id"].data_key == "uid"
    assert schema.fields["home_team"].data_key == "team"
    assert isinstance(schema.fields["stake"], fields.Float)


def test_generate_schema_from_config_with_source_fields():
    config = {
        "user_id": {"type": "int", "source_field": "uid"},
        "team_name": {"type": "string", "source_field": "home_team"},
        "stake": {"type": "float"},
    }

    schema_class = generate_schema_from_config(config)
    schema = schema_class()

    assert isinstance(schema.fields["user_id"], fields.Int)
    assert schema.fields["user_id"].attribute == "uid"
    assert schema.fields["team_name"].attribute == "home_team"
    assert schema.fields["stake"].attribute == "stake"  # fallback to label
