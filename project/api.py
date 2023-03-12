from flask import make_response, jsonify
from project.models import Problems
from project import app


@app.route('/api/problems/<string:problem>', methods=['GET'])
def get_problem(problem):
    problem = Problems.objects(link_name=problem).first()
    if problem:
        return (jsonify({'message': 'Problem found', 'problem':problem.to_json()}), 200)
    else:
        return (jsonify({'message': 'Problem not found'}), 404)

