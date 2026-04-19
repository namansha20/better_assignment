from marshmallow import Schema, fields, validate


class EnumValueField(fields.Str):
    """Serializes SQLAlchemy enums to their .value string."""
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if hasattr(value, 'value'):
            return value.value
        return super()._serialize(value, attr, obj, **kwargs)

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    color = fields.Str(load_default='#6366f1', validate=validate.Regexp(r'^#[0-9A-Fa-f]{6}$', error='Color must be a valid hex color (e.g. #ff0000)'))
    created_at = fields.DateTime(dump_only=True)

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(load_default=None, allow_none=True)
    status = EnumValueField(load_default='todo', validate=validate.OneOf(['todo', 'in_progress', 'done']))
    priority = EnumValueField(load_default='medium', validate=validate.OneOf(['low', 'medium', 'high']))
    due_date = fields.Date(load_default=None, allow_none=True, format='%Y-%m-%d')
    category_id = fields.Int(load_default=None, allow_none=True)
    category = fields.Nested(CategorySchema, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
