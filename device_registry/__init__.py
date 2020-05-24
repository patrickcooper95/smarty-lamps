# Import the framework
import os
import sqlite3 as sql
from sqlite3 import Error

from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
from flask_swagger_ui import get_swaggerui_blueprint
import markdown
from yaml import Loader, load


# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)


SWAGGER_URL = '/swagger'
swagger_yml = load(open("swagger.yml", 'r'), Loader=Loader)
blueprint = get_swaggerui_blueprint(SWAGGER_URL, swagger_yml, config={'spec': swagger_yml})
app.register_blueprint(blueprint, url_prefix=SWAGGER_URL)


def get_db():
    """create a database connection to a SQLite database"""
    try:
        conn = sql.connect('devices.db')
        # print(sql.version)
        return conn
    except Error as e:
        print(e)


def table_exists(conn):
    """check if devices table exists"""
    cur = conn.cursor()
    tables = cur.execute('SELECT COUNT(*) '
                         'FROM sqlite_master '
                         'WHERE type="table" AND name="devices"')

    if tables.fetchone()[0] == 1:
        return True
    else:
        return False


def create_table():
    """create devices table"""
    connection = get_db()
    cur = connection.cursor()
    if not table_exists(connection):
        try:
            cur.execute('create table devices(identifier TEXT,' +
                        'name TEXT,' +
                        'device_type TEXT,' +
                        'program TEXT,' +
                        'controller_gateway TEXT)')
            connection.commit()
        except Error as e:
            print(e)
        finally:
            connection.close()


@app.teardown_appcontext
def teardown_db(exception):
    # if conn is not None:
    #    conn.close()
    pass


@app.route("/update-device")
def update_page():
    """Serve GUI interface to interact with devices."""
    return render_template('update-device.html')


@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


class ColorList(Resource):
    def get(self):
        # TODO: Add create_table
        connection = get_db()
        cur = connection.cursor()
        color_list = cur.execute('SELECT * FROM colors').fetchall()
        connection.close()

        return {'message': 'Success', 'data': color_list}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True)
        parser.add_argument('r', required=True)
        parser.add_argument('g', required=True)
        parser.add_argument('b', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        # Parse arguments into a tuple for use with SQLite's *?* variable operator
        name = args['name']
        red = args['r']
        green = args['g']
        blue = args['b']
        new_record = (name, red, green, blue)

        # TODO: Fix this create_table()
        connection = get_db()
        cur = connection.cursor()
        cur.execute('INSERT INTO colors(name, r, g, b) ' +
                    'VALUES(?,?,?,?)', new_record)
        connection.commit()
        connection.close()

        return {'message': 'Device registered', 'data': args}, 201


class DeviceList(Resource):
    def get(self):
        # keys = ['identifier', 'name', 'device_type', 'controller_gateway']
        # Also responsible for checking existence of table.
        create_table()
        connection = get_db()
        cur = connection.cursor()
        dev_list = cur.execute('SELECT * FROM devices').fetchall()
        connection.close()

        return {'message': 'Success', 'data': dev_list}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('name', required=False)
        parser.add_argument('device_type', required=False)
        parser.add_argument('program', required=False)
        parser.add_argument('controller_gateway', required=False)

        # Parse the arguments into an object
        args = parser.parse_args()

        # Parse arguments into a tuple for use with SQLite's *?* variable operator
        id = args['identifier']
        name = args['name']
        device_type = args['device_type']
        program = args['program']
        controller_gateway = args['controller_gateway']
        new_record = (id, name, device_type, program, controller_gateway)

        create_table()
        connection = get_db()
        cur = connection.cursor()
        cur.execute('INSERT INTO devices(identifier, name, device_type, program, controller_gateway) ' +
                    'VALUES(?,?,?,?,?)', new_record)
        connection.commit()
        connection.close()

        return {'message': 'Device registered', 'data': args}, 201


class Device(Resource):
    def get(self, identifier):

        create_table()
        connection = get_db()
        cur = connection.cursor()
        exists_query = 'SELECT * FROM devices WHERE identifier="{identifier}"'.format(identifier=identifier)

        if cur.execute('SELECT EXISTS({sub_query})'.format(sub_query=exists_query)).fetchall()[0][0] == 1:
            device = cur.execute('SELECT * FROM devices WHERE identifier="{identifier}"'.format(
                identifier=identifier)).fetchall()
            connection.close()
            return {'message': 'Success', 'data': device}, 200
        else:
            print(cur.execute('SELECT EXISTS({sub_query})'.format(sub_query=exists_query)).fetchall())
            connection.close()
            return {'message': 'Device not found', 'data': {}}, 404

    def put(self, identifier):

        create_table()
        connection = get_db()
        cur = connection.cursor()
        exists_query = 'SELECT * FROM devices WHERE identifier="{identifier}"'.format(identifier=identifier)

        if not cur.execute('SELECT EXISTS({sub_query})'.format(sub_query=exists_query)).fetchall()[0][0] == 1:
            return {'message': 'Device not found.', 'data': {}}, 404

        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=False)
        parser.add_argument('name', required=False)
        parser.add_argument('device_type', required=False)
        parser.add_argument('program', required=False)
        parser.add_argument('controller_gateway', required=False)

        # Parse the arguments into an object
        args = parser.parse_args().items()

        # for field in args:
        #     if field[0] == 'program':
        #         wapi_main.set_program(field[1])

        for field in args:
            if field[1] is not None:
                cur.execute(f'UPDATE devices SET {field[0]}="{field[1]}" WHERE identifier="{identifier}"')
                connection.commit()
        connection.close()
        return {'message': 'Device successfully updated.', 'data': {}}, 200

    def delete(self, identifier):

        create_table()
        connection = get_db()
        cur = connection.cursor()
        exists_query = 'SELECT * FROM devices WHERE identifier="{identifier}"'.format(identifier=identifier)

        if cur.execute('SELECT EXISTS({sub_query})'.format(sub_query=exists_query)).fetchall()[0][0] == 1:
            cur.execute('DELETE FROM devices WHERE identifier="{identifier}"'.format(
                identifier=identifier))
            connection.commit()
            connection.close()
            return {'message': 'Item successfully deleted.', 'data': {}}, 200
        else:
            connection.close()
            return {'message': 'Device not found.', 'data': {}}, 404


api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/devices/<string:identifier>')
api.add_resource(ColorList, '/colors')
