from flask import request

from schemas import CategoryTypeListSchema
from models import CategoryType, GenderEnum, Retailer, Category, db
from config import create_app

app = create_app()

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get_categories_type_list/')
def get_categories_type_list():
    type_schema = CategoryTypeListSchema()
    category_types = CategoryType.query.all()
    return type_schema.jsonify(category_types, many=True)


@app.route('/get_category_type/<typeid>/')
def get_category_type(typeid):
    category_type = CategoryType.query.filter_by(id=typeid)
    if category_type.count():
        type_schema = CategoryTypeListSchema()
        return type_schema.jsonify(category_type.first())
    return f"CategoryType with this id: {typeid} haven't found"


# POST:
# {
#   "retailer": "woman bracelets"
# }
@app.route('/add_retailer/', methods=['POST'])
def add_retailer():
    gender = GenderEnum.all_genders
    category_type = CategoryType.query.filter_by(name='others').first()
    content_input = request.get_json()
    if not content_input.get('retailer', None):
        return 'There is no data with retailer'

    if any(word in content_input['retailer'] for word in ["woman", "women", "female"]):
        gender = GenderEnum.female
    elif any(word in content_input['retailer'] for word in ["man", "men", "male"]):
        gender = GenderEnum.male

    if any(word in content_input['retailer'] for word in ['rings', 'bracelets', 'necklaces']):
        category_type = CategoryType.query.filter_by(name='jewellery').first()
    elif any(word in content_input['retailer'] for word in ['haircut', 'shave', 'barber']):
        category_type = CategoryType.query.filter_by(name='hairdresser').first()
    elif any(word in content_input['retailer'] for word in ['CD', 'records', 'musical', 'instruments']):
        category_type = CategoryType.query.filter_by(name='music shop').first()

    # todo continue to write if statements or create table for words to compare

    retailer = Retailer(
        name=content_input['retailer'],
        gender=gender,
        type=category_type
    )
    db.session.add(retailer)
    category = Category(
        name=f"{gender.value}/{category_type.name.capitalize()}",
        gender=gender,
        type=category_type,
        retailer=retailer
    )
    db.session.add(category)
    db.session.commit()
    return 'OK'


if __name__ == '__main__':
    app.run()
