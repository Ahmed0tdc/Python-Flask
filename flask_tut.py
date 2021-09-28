from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy  


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"video(name = {name}, views = {views}, likes = {likes})"

# db.create_all() # should be run only once


video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help='Name of the video', required=True)
video_put_args.add_argument('views', type=int, help='Views of the video',required=True)
video_put_args.add_argument('likes', type=int, help='Likes on the video',required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument('name', type=str, help='Name of the video')
video_update_args.add_argument('views', type=int, help='Views of the video')
video_update_args.add_argument('likes', type=int, help='Likes on the video')


resource_fields = {
	'id' : fields.Integer,
	'name' : fields.String,
	'views' : fields.Integer,
	'likes' : fields.Integer,
}



# videos = {}

# def abort_if_video_id_not_exist(video_id):
# 	if video_id not in videos:
# 		abort(404, message= 'this video id does not exist')

# def abort_if_video_exists(video_id):
# 	if video_id in videos:
# 		abort(409, message = 'this video already exists with that ID')

class Video(Resource):

	@marshal_with(resource_fields)
	def get(self, video_id):
		# abort_if_video_id_not_exist(video_id)
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(409, message='no is like this')
		return result          #videos[video_id]

	@marshal_with(resource_fields)
	def put(self, video_id):
		args = video_put_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if result:
			abort(409, message='vdieo id is taked')
		video = VideoModel(id=video_id, name=args['name'],views=args['views'],likes=args['likes'])
		db.session.add(video)
		db.session.commit()
		# abort_if_video_exists(video_id)
		# args = video_put_args.parse_args()
		# videos[video_id] = args
		# return videos[video_id], 201
		return video, 201

	def delete(self, video_id):
		abort_if_video_id_not_exist(video_id)
		del videos[video_id]
		return '' , 204

	@marshal_with(resource_fields)
	def patch(self, video_id):
		args = video_update_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message='vid not exsit, cant update')
		if 'name' in args and args['name'] != None:
			result.name = args['name']
		if 'likes' in args and args['likes'] != None:
			result.likes = args['likes']
		if 'views' in args and args['views'] != None:
			result.views = args['views']
		
		db.session.commit()
		return result


api.add_resource(Video, '/video/<int:video_id>')           # here we give the name of the route, and the resource it's controlling (get, post...)
if __name__ == '__main__':
	app.run(debug = True)
 