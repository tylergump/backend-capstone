import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

# We can use this as a Python decorator for routing purposes
# first argument is blueprints name
# second argument is it's import_name
goals = Blueprint('goals', 'goals')

@goals.route('/', methods=["GET"])
def get_all_goals():
    ## find the goals and change each one to a dictionary into a new array
    try:
        goals = [model_to_dict(goal) for goal in models.Goal.select()]
        print(goals)
        return jsonify(data=goals, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting resources"})

@goals.route('/', methods=["POST"])
def create_dogs():
    # see request payload analogous to req.body in express
    payload = request.get_json()
    print(type(payload), 'payload')
    goal = models.Goal.create(**payload)
    # see the object
    print(goal.__dict__)
    # look at all the methods
    print(dir(goal))
    # change model to a dict
    goal_dict = model_to_dict(goal)
    return jsonify(data=goal_dict, status={"code": 201, "message": "Success"})

@goals.route('/<id>', methods=["GET"])
def get_one_goal(id):
    print(id, 'reserved word?')
    goal = models.Goal.get_by_id(id)
    print(goal.__dict__)
    return jsonify(
        data=model_to_dict(goal),
        status = 200,
        message = "Success"
    ), 200

@goals.route('/<id>', methods=["PUT"])
def update_goal(id):
    payload = request.get_json()
    query = models.Goal.update(**payload).where(models.Goal.id==id)
    query.execute()
    return jsonify(
        data=model_to_dict(models.Goal.get_by_id(id)),
        status=200,
        message= 'resource updated successfully'
    ), 200

@goals.route('/<id>', methods=["DELETE"])
def delete_goal(id):
    query = models.Goal.delete().where(models.Goal.id==id)
    query.execute()
    return jsonify(
        data='resource successfully deleted',
        message = 'resource deleted successfully',
        status=200
    ), 200