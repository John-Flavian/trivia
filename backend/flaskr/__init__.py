import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response



    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    
    #Route to get all categories
    @app.route("/categories")
    def get_categories():
        categories = Category.query.all()
        
        categories_list = {category.id:category.type for category in categories}
        if len(categories_list) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "categories": categories_list
        })

    

    
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """


    #Route to get all questions
    @app.route("/questions")
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.order_by(Category.id).all()
        formatted_categories={category.id:category.type for category in categories}
        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(selection),
            "categories": formatted_categories
        })
    

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    #Route to delete a question
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                "success": True,
                "deleted": question_id
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """


    #Route to add a question and also search for a question
    @app.route("/questions", methods=["POST"])
    def create_and_search_question():
        
        body = request.get_json()

        # if search term is present in the body
        if (body.get('searchTerm')):
            search_term = body.get('searchTerm')
            selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            # if no questions are found return 404
            if (len(selection) == 0):
                abort(404)

            # paginate the results
            paginated = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': paginated,
                'total_questions': len(Question.query.all())
            })
        else:
            # if no search term is present, add a new question
            body = request.get_json()
            new_question = body.get("question")
            new_answer = body.get("answer")
            new_category = body.get("category")
            new_difficulty = body.get("difficulty")
            try:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()
                return jsonify({
                    "success": True,
                    "created": question.id
                })
            except:
                abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    #Route to get questions based on category
    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        try:
            category = Category.query.get(category_id)
            questions = Question.query.filter(Question.category == category.id).all()
            current_questions = paginate_questions(request, questions)
            formatted_questions = [question.format() for question in questions]
            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "current_category": category.type
            })
        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    #Route to get questions to play the quiz
    @app.route("/quizzes", methods=["POST"])
    def get_quiz_questions():
        body = request.get_json()
        previous_questions = body.get("previous_questions")
        quiz_category = body.get("quiz_category")
        if quiz_category['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(Question.category == quiz_category['id']).all()
        quiz_questions = []
        for question in questions:
            if question.id not in previous_questions:
                quiz_questions.append(question)
        if len(quiz_questions) == 0:
            abort(422)
        random_question = random.choice(quiz_questions)
        return jsonify({
            "success": True,
            "question": random_question.format()
        })


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    return app

