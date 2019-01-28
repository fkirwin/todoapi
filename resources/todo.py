from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse,
                               inputs, fields, marshal,
                               marshal_with, url_for)

import models

todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'completed': fields.Boolean,
    'edited': fields.Boolean
}


def todo_or_404(todo_id):
    try:
        todo = models.Todo.get(models.Todo.id == todo_id)
    except models.Todo.DoesNotExist:
        abort(404)
    else:
        return todo


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name was provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'completed',
            required=False,
            help='Has this items been completed or not?',
            location=['form', 'json'],
            type=inputs.boolean
        )
        self.reqparse.add_argument(
            'edited',
            required=False,
            help='Has this items been completed or not?',
            location=['form', 'json'],
            type=inputs.boolean
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self):
        courses = [each for each in models.Todo.get_all_todos()]
        return courses

    @marshal_with(todo_fields)
    def post(self):
        kwargs = self.reqparse.parse_args()
        todo = models.Todo.write_new_todo(**kwargs)
        return (todo, 201, {
            'Location': url_for('resources.todo.todos')
        })

class Todo(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name was provided.',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'completed',
            required=False,
            help='Has this items been completed or not?',
            location=['form', 'json'],
            type=inputs.boolean
        )
        self.reqparse.add_argument(
            'edited',
            required=False,
            help='Has this items been completed or not?',
            location=['form', 'json'],
            type=inputs.boolean
        )
        super().__init__()



todo_api = Blueprint('resources.todo', __name__)
api = Api(todo_api)
api.add_resource(
    TodoList,
    '/api/v1/todos',
    endpoint='todos'
)
'''
api.add_resource(
    Todo,
    '/api/v1/courses/<int:id>',
    endpoint='todo'
)
'''