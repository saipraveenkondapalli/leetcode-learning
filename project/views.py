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

"""
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
"""

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
        {'$sort': {'company_count': -1}},
        # Project the 'name', 'link', and 'company' fields into the output documents
        {'$project': {'name': 1, 'link': 1, 'level': 1, 'company': 1}}
    ]


    # Run the aggregation pipeline
    result = Problems.objects.aggregate(pipeline)

    return render_template('company_questions.html', name = company_name, problems=result)

# ----------------------------------------------------------- END OF COMPANY LIST ----------------------------------------------------------------------------------


@app.route('/problems', methods = ['GET', 'POST'])
def problems():
    level = request.args.get('level')
    category = request.args.get('category')
    print(f"level: {level}, category: {category}")
    if level == "All":
        level = None
    if level and category:
        problems = Problems.objects().filter(level = level, category__in=[category]).order_by('-total_companies').paginate(page=1,
                                                                                                            per_page=50)
    elif level and not category:
        problems = Problems.objects().filter(level = level).order_by('-total_companies').paginate(page=1, per_page=50)
    elif category and not level:
        problems = Problems.objects().filter(category__in=[category]).order_by('-total_companies').paginate(page=1,per_page=50)
    else:
        problems = Problems.objects().order_by('-total_companies').paginate(page=1, per_page=50)

    return render_template('problems.html', problems=problems.items, page= 1)




@app.route('/filter')
def test():
    level = request.args.get('level')
    category = request.args.get('category')
    page = request.args.get('page')

    if page is None:
        page = 1
    else:
        page = int(page)
    if level is None:
        level = 'All'

    if category is None or len(category) == 0:
        category = 'All'

    # print(f"level: {level}, category: {category}, page: {page}, type: {type(page)}")

    if level == 'All' and category == 'All':
        problems = Problems.objects().order_by('-total_companies').paginate(page=page, per_page=50)

    elif level == 'All' and category != 'All':
        problems = Problems.objects().filter(category__in=[category]).order_by('-total_companies').paginate(page=page,
                                                                                                            per_page=50)

    elif level != 'All' and category == 'All':
        problems = Problems.objects().filter(level=level).order_by('-total_companies').paginate(page=page, per_page=50)
    else:
        problems = Problems.objects().filter(level=level, category__in=[category]).order_by(
            '-total_companies').paginate(page=page, per_page=50)

    # print(*list(problems.items), sep='\n')
    return render_template('table_generate.html', problems=problems.items, page=page)


@app.route('/search', methods = ['GET', 'POST'])
def search():

    words = request.args.get('search')
    prob = Problems.objects().search_text(words).order_by('$text_score')
    return render_template('table_generate.html', problems=prob, page=1)


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
