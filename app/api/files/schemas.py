from marshmallow import Schema, fields, EXCLUDE


class FileSchema(Schema):
    key = fields.Str(attribute='Key')
    size = fields.Integer(attribute='Size')
    last_modified = fields.Str(attribute='LastModified')

    class Meta:
        unknown = EXCLUDE


class FilesSchema(Schema):
    items = fields.Nested(FileSchema, many=True)

    class Meta:
        unknown = EXCLUDE


class FilesUploadSchema(Schema):
    upload_id = fields.String()
    size = fields.Integer()
    created = fields.String()
    filename = fields.String()


class FilesDeleteSchema(Schema):
    key = fields.Str(required=True)
