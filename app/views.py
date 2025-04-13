"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import make_response, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from app.models import Movie
from app.forms import MovieForm
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm()

    if form.validate_on_submit():
        filename = secure_filename(form.poster.data.filename)
        form.poster.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        added_movie = Movie(
            title= form.title.data,
            description=form.description.data,
            poster=filename
        )
        db.session.add(added_movie)
        db.session.commit()

        response = {
            "message": "Movie Successfully added",
            "title": added_movie.title,
            "poster": added_movie.poster,
            "description": added_movie.description
        }
        return jsonify(response), 201
    else:
        return jsonify({"errors": form_errors(form)}), 400
    
@app.route('/api/v1/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movie_list = []
    for m in movies:
        movie_data={
            'id': m.id,
            'title': m.title,
            'description': m.description,
            'poster': m.poster
        }
        movie_list.append(movie_data)
    return jsonify({'movies':movie_list})

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    csrf_token = generate_csrf()
    return jsonify({'csrf_token': csrf_token})

@app.route('/api/v1/posters/<filename>')
def get_poster(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page."""
    return make_response(jsonify({'error':'Not Found'}), 404)
