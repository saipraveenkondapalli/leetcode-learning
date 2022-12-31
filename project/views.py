import time
from flask import request, render_template, redirect, url_for, make_response, jsonify
from project.models import User, Problems
from project import app, oauth, bcrypt
from mongoengine.errors import NotUniqueError as MongoNotUniqueError
from flask_login import login_required, login_user, logout_user, current_user
import boto3
import random
from bson.son import SON


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/privacy')
def privacy():
    return render_template("privacy.html")




"""

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user.name)
"""

"""
@app.route('/problems')
def problems():
    return render_template('table.html', problems=Problems.objects.limit(50))
"""

# -------------------------------------------------------------------------Companies---------------------------------------------------------------------------------------------


@app.route('/chart_data')
def chart_data():
    # Load the data from your database or other source

    pipeline = [
        {"$unwind": "$company"},  # unpack the "company" array field
        {"$group": {"_id": "$company.name", "count": {"$sum": 1}}},
        # group by company name and calculate the count of problems
        {"$sort": SON([("count", -1)])},  # sort by count in descending order
        {"$limit": 10}  # limit the results to the top 10
    ]

    result = Problems.objects.aggregate(pipeline)
    company_name = []
    company_count = []
    for doc in result:
        company_name.append(doc['_id'])
        company_count.append(doc['count'])
    pipeline = [
        {"$group": {
            "_id": None,
            "easy_count": {"$sum": {"$cond": [{"$eq": ["$level", "Easy"]}, 1, 0]}},
            "medium_count": {"$sum": {"$cond": [{"$eq": ["$level", "Medium"]}, 1, 0]}},
            "hard_count": {"$sum": {"$cond": [{"$eq": ["$level", "Hard"]}, 1, 0]}}
        }}
    ]

    counts = Problems.objects.aggregate(pipeline)
    for count in counts:
        easy = count['easy_count']
        medium = count['medium_count']
        hard = count['hard_count']
        total = easy + medium + hard


    return jsonify({'company_name': company_name, 'company_count': company_count, "easy": easy, "medium": medium, "hard": hard, "total": total})


@app.route('/companies')

def companies():
    pipeline = [
        {"$unwind": "$company"},  # unpack the "company" array field
        {"$group": {"_id": "$company.name", "count": {"$sum": 1}}},
        # group by company name and calculate the count of problems
        {"$sort": {'_id':1}},  # sort by count in descending order
    ]

    result = Problems.objects.aggregate(pipeline)

    return render_template('companies.html', company=result)


@app.route('/company/<company_name>')
def company(company_name):
    # Define the pipeline stages
    if company_name.__contains__('%20'):
        company_name = company_name.replace('%20', ' ')

    pipeline = [
        # Find all documents where the 'company.name' field is equal to 'company_name'
        {'$match': {'company.name': company_name}},
        # Unwind the 'company' array to create a separate document for each element in the array
        {'$unwind': '$company'},
        # Match the 'company.name' field again to filter out any documents that do not have a 'company.name' field equal to 'company_name'
        {'$match': {'company.name': company_name}},
        {'$sort': {'company.freq': -1}},
        # Project the 'name', 'link', and 'company' fields into the output documents
        {'$project': {'name': 1, 'link': 1, 'level': 1, 'company': 1}}
    ]


    # Run the aggregation pipeline
    result = Problems.objects.aggregate(pipeline)

    return render_template('company_questions.html', name = company_name, problems=result)

# ----------------------------------------------------------- END OF COMPANY LIST ----------------------------------------------------------------------------------






"""
@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # generate a random file name using random module
        
        file.filename = str(random.randint(100000, 9999999999)) +'.'+ file.filename.split('.')[-1] # 1234567.jpg
        s3 = boto3.resource('s3', aws_access_key_id='73234ac2e5a5a497e7249fc13ab802e4',
                            aws_secret_access_key='e671453794d1b58b01d7c05bfa8f1345f28ad01d372b0685a6414b8c1a6acfc2',
                            endpoint_url='https://4e3989f550197dead69bd70821c5fc3f.r2.cloudflarestorage.com')

        bucket = s3.Bucket('leetcode-problems')
        bucket.upload_fileobj(file, file.filename)

        return "File uploaded Successfully"
    return render_template('upload.html')
    
"""
