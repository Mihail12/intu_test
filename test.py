import os
import unittest

from models import db, CategoryType, Category, Retailer, GenderEnum
from app import app

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['BASEDIR'] = os.getcwd()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.init_app(app)
        with app.app_context():
            db.drop_all()
            db.create_all()

        self.category_types = ["jewellery", "florist", "hairdresser", "newsagent", "chemist", "butcher", "baker",
                          "shoe shop",
                          "music shop", "others"]
        for type_name in self.category_types:
            db.session.add(CategoryType(name=type_name))
        db.session.commit()

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_categories(self):
        response = self.app.get('/get_categories_type_list/', follow_redirects=True)
        self.assertEqual(len(response.json), len(self.category_types))

    def test_get_category_type(self):
        response = self.app.get('/get_category_type/3/', follow_redirects=True)
        category_type = CategoryType.query.get(3)
        self.assertEqual(category_type.name, response.json['name'])

    def test_add_category(self):
        response = self.app.post('/add_retailer/', data={"retailer": "men musical instruments"})
        self.assertEqual('OK', response.data)
        retailor = Retailer.query.filter_by(name="men musical instruments")
        self.assertEqual(1, retailor.count())
        category = Category.query.filter_by(retailor=retailor.first())
        self.assertEqual(category.gender, GenderEnum.male.key)


if __name__ == "__main__":
    unittest.main()