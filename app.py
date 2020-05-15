import os
from flask import Flask, jsonify, request, abort
from models import setup_db, Actor, Movie
from flask_cors import CORS
from auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # --------------------------------------#
    # CONTROLLERS
    # --------------------------------------#

    # ---------------------------------------#
    # GET
    # ---------------------------------------#

    @app.route('/actors')
    @requires_auth('view:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        formatted_actors = [actor.get_actor_description() for actor in actors]
        return jsonify({
            'success': True,
            'actors': formatted_actors
        })

    @app.route('/movies')
    @requires_auth('view:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        formatted_movies = [movie.get_movie_description() for movie in movies]
        return jsonify({
            'success': True,
            'movies': formatted_movies
        })

    @app.route('/actors/<int:actor_id>')
    @requires_auth('view:actors')
    def get_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        return jsonify({
            'success': True,
            'actor': actor.get_actor_description()
        })

    @app.route('/movies/<int:movie_id>')
    @requires_auth('view:movies')
    def get_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        return jsonify({
            'success': True,
            'movie': movie.get_movie_description()
        })

    # --------------------------------------#
    # DELETE
    # --------------------------------------#

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor.id
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': movie.id
        })

    # --------------------------------------#
    # POST
    # --------------------------------------#

    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movies')
    def add_movie(payload):
        req = request.get_json()
        movie = Movie()
        if 'title' not in req:
            abort(400)
        if 'release_year' not in req:
            abort(400)
        movie.title = req['title']
        movie.release_year = req['release_year']
        movie.insert()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actors')
    def add_actor(payload):
        req = request.get_json()
        actor = Actor()
        if 'name' not in req:
            abort(400)
        if 'age' not in req:
            abort(400)
        if 'gender' not in req:
            abort(400)
        actor.name = req['name']
        actor.age = req['age']
        actor.gender = req['gender']
        actor.insert()
        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    # --------------------------------------#
    # PATCH
    # --------------------------------------#

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('modify:actors')
    def update_actor(payload, actor_id):
        req = request.get_json()
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        if 'name' in req:
            actor.name = req['name']
        if 'age' in req:
            actor.age = req['age']
        if 'gender' in req:
            actor.gender = req['gender']
        actor.update()
        return jsonify({
            'success': True,
            'actor': Actor.query.get(actor_id).format()
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('modify:movies')
    def update_movie(payload, movie_id):
        req = request.get_json()
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        if 'release_year' in req:
            movie.release_year = req['release_year']
        if 'title' in req:
            movie.title = req['title']
        movie.update()
        return jsonify({
            'success': True,
            'movie': Movie.query.get(movie_id).format()
        })

    # ---------------------------------------#
    # ACTOR-MOVIE ASSOCIATION
    # ---------------------------------------#

    @app.route('/cast', methods=['POST'])
    @requires_auth('add:movies')
    def add_association(payload):
        req = request.get_json()
        if 'actor_id' not in req:
            abort(400)
        if 'movie_id' not in req:
            abort(400)
        actor = Actor.query.get(req['actor_id'])
        if actor is None:
            abort(404)
        movie = Movie.query.get(req['movie_id'])
        if movie is None:
            abort(404)
        movie.actors.append(actor)
        movie.update()
        return jsonify({
            'success': True,
            'actor': actor.name,
            'movie': movie.title
        })

    # --------------------------------------#
    # ERROR HANDLERS
    # --------------------------------------#

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'Unprocessable'
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": 'Resource Not Found'
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()

# --------------------------------------#
# LAUNCH
# --------------------------------------#

if __name__ == '__main__':
    app.run(debug=True)
