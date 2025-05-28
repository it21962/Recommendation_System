from marshmallow import Schema, fields
from typing import List, Dict

# Μονάδες μετατροπής ονομάτων => τύπων
FIELD_TYPE_MAP = {
    "int": fields.Int,
    "float": fields.Float,
    "string": fields.String,
    "list": lambda: fields.List(fields.Raw()),
}


def infer_field_type(field_name: str):
    """Απλή Heuristic για να μαντεύουμε τύπο"""
    if "user_id" in field_name:
        return "int"
    elif "id" in field_name:
        return "string"
    elif "odds" in field_name or "stake" in field_name:
        return "float"
    elif "team" in field_name or "participants" in field_name:
        return "string"
    else:
        return "string"


def generate_schema(fields_list: List[str], label_map: Dict[str, str]):
    schema_fields = {}

    for f in fields_list:
        field_type_key = infer_field_type(f)
        marshmallow_field = FIELD_TYPE_MAP.get(field_type_key, fields.String)

        schema_fields[f] = marshmallow_field(data_key=label_map.get(f, f))

    return type("DynamicRecommendationSchema", (Schema,), schema_fields)

def generate_schema_from_config(fields_config: dict):
    schema_fields = {}
    for label, props in fields_config.items():
        field_type = props.get("type", "string")
        source_field = props.get("source_field", label)
        marshmallow_field = FIELD_TYPE_MAP.get(field_type, fields.String)
        schema_fields[label] = marshmallow_field(attribute=source_field)
    return type("DynamicRecommendationSchema", (Schema,), schema_fields)



