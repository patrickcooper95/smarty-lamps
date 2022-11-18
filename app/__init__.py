# Import the framework
import logging
import os
import sqlite3 as sql
from sqlite3 import Error

from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
from flask_swagger_ui import get_swaggerui_blueprint
import markdown
from yaml import Loader, load

import config
from add_ons.nyct import nyct
import wapi.configs as configs
import wapi.led_utils as utils

# Logging
LOGGER = config.logging_config(__name__)

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

SWAGGER_URL = '/swagger'
swagger_yml = load(open(os.path.join(configs.base_path, "swagger.yml"), 'r'), Loader=Loader)
blueprint = get_swaggerui_blueprint(SWAGGER_URL, swagger_yml, config={'spec': swagger_yml})
app.register_blueprint(blueprint, url_prefix=SWAGGER_URL)


def get_db():
    """create a database connection to a SQLite database"""
    try:
        conn = sql.connect(os.path.join(configs.db_path))
        # print(sql.version)
        return conn
    except Error as e:
        LOGGER.error(e)


def table_exists(conn):
    """check if devices table exists"""
    cur = conn.cursor()
    query = 'SELECT COUNT(*) FROM sqlite_master WHERE type="table" AND name="devices"'
    tables = cur.execute(query)
    LOGGER.info(f"Running query: {query}")

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
            LOGGER.info("Creating devices table.")
            cur.execute('create table devices(identifier TEXT,' +
                        'name TEXT,' +
                        'device_type TEXT,' +
                        'program TEXT,' +
                        'controller_gateway TEXT)')
            connection.commit()
        except Error as e:
            LOGGER.error(e)
        finally:
            connection.close()


def record_exists(table, id, cursor):
    if table == "devices":
        query = 'SELECT * FROM devices WHERE identifier="{identifier}"'.format(identifier=id)
    elif table == "colors":
        query = 'SELECT * FROM colors WHERE name="{identifier}"'.format(identifier=id)
    elif table == "times":
        query = 'SELECT * FROM times WHERE id="{identifier}"'.format(identifier=id)
    else:
        return False

    LOGGER.info(f"Running query: {query}")
    if cursor.execute('SELECT EXISTS({sub_query})'.format(sub_query=query)).fetchall()[0][0] == 1:
        return True
    else:
        return False


@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


class TimesList(Resource):

    def get(self):
        connection = get_db()
        cur = connection.cursor()
        time_list = cur.execute('SELECT * FROM times WHERE id="alarm"').fetchall()
        connection.close()

        LOGGER.info("Get all programs successful.")

        return {'message': 'Success', 'data': time_list}, 200


class AlarmTime(Resource):

    def put(self, id):
        id = id.lower()
        conn = get_db()
        cur = conn.cursor()
        time_exists = record_exists("times", id, cur)

        if not time_exists:
            LOGGER.info("Time entry: %s not found.", id)
            return {'message': 'Time entry not found.', 'data': {}}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('time', required=True)

        # Parse the arguments into an object
        args = parser.parse_args().items()

        for field in args:
            if field[1] is not None:
                new_time = field[1].lower()
                LOGGER.info(new_time)

                cur.execute(f'UPDATE times SET {field[0]}="{new_time}" WHERE id="{id}"')
                conn.commit()
                LOGGER.info("Time set to %s", field[1])

        conn.close()
        return {'message': 'Successful.', 'data': {}}, 200


class Effects(Resource):
    def put(self, identifier):

        identifier = identifier.lower()
        create_table()
        connection = get_db()
        cur = connection.cursor()
        device_exists = record_exists("devices", identifier, cur)

        if not device_exists:
            LOGGER.info("Device %s not found.", identifier)
            return {'message': 'Device not found.', 'data': {}}, 404

        parser = reqparse.RequestParser()

        parser.add_argument('program', required=False)

        # Parse the arguments into an object
        args = parser.parse_args().items()

        for field in args:
            if field[1] is not None:
                new_color = field[1].lower()
                
                program_exists = record_exists("colors", new_color, cur)
                if program_exists:
                    cur.execute(f'UPDATE devices SET {field[0]}="{new_color}" WHERE identifier="{identifier}"')
                    connection.commit()
                    LOGGER.info("Updating device to %s", field[1])
                else:
                    LOGGER.info("Program %s not found.", field[1])
                    return {'message': 'Program not found.', 'data': {}}, 404

        connection.close()
        return {'message': 'Lighting effects successfully updated.', 'data': {}}, 200


class ProgramList(Resource):
    def get(self):
        # TODO: Add create_table
        connection = get_db()
        cur = connection.cursor()
        color_list = cur.execute('SELECT * FROM colors').fetchall()
        connection.close()

        LOGGER.info("Get all programs successful.")

        return {'message': 'Success', 'data': color_list}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True)
        parser.add_argument('r', required=False)
        parser.add_argument('g', required=False)
        parser.add_argument('b', required=False)
        parser.add_argument('dynamic', required=True)
        parser.add_argument('callable_path', required=False)

        # Parse the arguments into an object
        args = parser.parse_args()

        # Parse arguments into a tuple for use with SQLite's *?* variable operator
        name = args["name"]
        red = args.get('r', 0)
        green = args.get("g", 0)
        blue = args.get("b", 0)
        dynamic= args["dynamic"]
        callable = args.get("callable_path", "")
        new_record = (name, red, green, blue, dynamic, callable)

        connection = get_db()
        cur = connection.cursor()
        cur.execute('INSERT INTO colors(name, r, g, b, dynamic, callable_path) ' +
                    'VALUES(?,?,?,?,?,?)', new_record)
        connection.commit()
        connection.close()

        # Re-index programs package for new dynamic programs
        utils.index()

        LOGGER.info("Added program %s successfully.", name)

        return {'message': 'Program added.', 'data': args}, 201


class Program(Resource):
    def delete(self, name):
        
        name = name.lower()
        create_table()
        connection = get_db()
        cur = connection.cursor()
        exists_query = 'SELECT * FROM colors WHERE name="{name}"'.format(name=name)

        if cur.execute('SELECT EXISTS({sub_query})'.format(sub_query=exists_query)).fetchall()[0][0] == 1:
            cur.execute('DELETE FROM colors WHERE name="{name}"'.format(name=name))
            connection.commit()
            connection.close()

            LOGGER.info("Program %s successfully deleted.", name)
            return {'message': 'Program successfully deleted.', 'data': {}}, 200
        else:
            connection.close()

            LOGGER.info("Program %s not found.", name)
            return {'message': 'Program not found.', 'data': {}}, 404

    def put(self, name):

        name = name.lower()
        create_table()
        connection = get_db()
        cur = connection.cursor()
        exists_query = f'SELECT * FROM colors WHERE name="{name}"'

        if not cur.execute('SELECT EXISTS({sub_query})'.format(sub_query=exists_query)).fetchall()[0][0] == 1:
            return {'message': 'Program not found.', 'data': {}}, 404

        parser = reqparse.RequestParser()

        parser.add_argument('name', required=False)
        parser.add_argument('r', required=False)
        parser.add_argument('g', required=False)
        parser.add_argument('b', required=False)
        parser.add_argument('dynamic', required=False)
        parser.add_argument('callable_path', required=False)

        # Parse the arguments into an object
        args = parser.parse_args().items()

        for field in args:
            if field[1] is not None:
                new_value = field[1].lower()
                cur.execute(f'UPDATE colors SET {field[0]}="{new_value}" WHERE name="{name}"')
                connection.commit()
        connection.close()
        return {'message': 'Program successfully updated.', 'data': {}}, 200


class DeviceList(Resource):
    def get(self):
        # Also responsible for checking existence of table.
        create_table()
        connection = get_db()
        cur = connection.cursor()
        dev_list = cur.execute('SELECT * FROM devices').fetchall()
        connection.close()

        LOGGER.info("Program list returned successfully.")

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

        LOGGER.info("Device %s added successfully.", id)

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

            LOGGER.info("Devices returned successfully.")
            return {'message': 'Success', 'data': device}, 200
        else:
            print(cur.execute('SELECT EXISTS({sub_query})'.format(sub_query=exists_query)).fetchall())
            connection.close()

            LOGGER.info("Device %s not found.", identifier)
            return {'message': 'Device not found', 'data': {}}, 404

    def put(self, identifier):

        identifier = identifier.lower()
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
                new_value = field[1].lower()
                cur.execute(f'UPDATE devices SET {field[0]}="{new_value}" WHERE identifier="{identifier}"')
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


class Subway(Resource):
    def get(self, service, segment):
        return {"message": "Success", "data": nyct.get_trains(service, segment)}, 200


api.add_resource(TimesList, '/times')
api.add_resource(AlarmTime, '/times/<string:id>')
api.add_resource(Effects, '/effects/<string:identifier>')
api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/devices/<string:identifier>')
api.add_resource(ProgramList, '/program')
api.add_resource(Program, '/program/<string:name>')
api.add_resource(Subway, '/subway')
