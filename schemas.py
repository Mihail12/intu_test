from flask_marshmallow import Marshmallow

from models import CategoryType

ma = Marshmallow()


class CategoryTypeListSchema(ma.ModelSchema):
    class Meta:
        model = CategoryType
        fields = ('id', 'name')
