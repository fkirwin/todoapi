import datetime
import json

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *

import config
import mock

DATABASE = SqliteDatabase('todo.sqlite')

class Todo(Model):
    name = CharField()
    completed = BooleanField()
    edited = BooleanField()

    class Meta:
        database = DATABASE

    @classmethod
    def write_new_todo(cls, name, completed=False, edited=False):
        try:
            with DATABASE.transaction():
                return cls.create(name=name,
                           completed=completed,
                           edited=edited)
        except IntegrityError:
            raise ValueError("Entry already exists")

    @classmethod
    def update_todo(cls, todo_id, name, completed, edited, **kwargs):
        if kwargs:
            try:
                todo_id = kwargs.pop('todo_id', None)
                exe = Todo.update(**kwargs).where((Todo.id==todo_id)).execute()
                return exe
            except (DataError, Exception) as e:
                print(e)
        else:
            try:
                todo = cls.get_specific_todo(todo_id)
                todo.name = name
                todo.completed = completed
                todo.edited = edited
                todo.save()
                return todo
            except (DataError, Exception) as e:
                print(e)

    @classmethod
    def get_all_todos(cls):
        return cls.select()

    @classmethod
    def get_specific_todo(cls, todo_id):
       return cls.select().where(Todo.id == todo_id).get()


def initialize():
    DATABASE.connect(reuse_if_open=True)
    DATABASE.create_tables([Todo], safe=True)
    with DATABASE.atomic():
        with open('mock/todos.json', 'r') as initial_data:
            for data_dict in json.loads(initial_data.read()):
                if not Todo.select().where(Todo.name==data_dict['name']):
                    data_dict['completed'] = False
                    data_dict['edited'] = False
                    Todo.create(**data_dict)
    DATABASE.close()
