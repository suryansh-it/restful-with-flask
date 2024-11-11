from flask import Flask
from flask_restful import Api, Resource , reqparse , abort , marshal_with , fields
from flask_sqlalchemy import SQLAlchemy 

# reqparser : helps send the needed data

app= Flask(__name__)
api = Api(app)      #wrap app in an api

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'  #tmp/database : if we store in temp folder in the project folder
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id =  db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable= False)
    views = db.Column(db.Integer, nullable= False)
    likes = db.Column(db.Integer, nullable= False)

    def __repr__(self):
        return f'Video(name= {self.name}, views={self.views}, likes={self.likes})'  # to represent object in this form

# Create tables if they don't exist
with app.app_context():
    db.create_all()


# names= {"tim":{"age":21 , "gen" :"male"}
#         ,"jim":{"age":28 , "gen" :"male"}}

# class HelloWorld(Resource):     #inheriting from resource  : class as a reaosurce

    # def get(self):
    #     return{"message":"helllow"}
    
    # def post(self):
    #     return{"message":"posted"}
    
    # def get(self,name,test):
    #     return{"name":name, "test" :test}
    
    # def get(self,name):
    #     return names[name]   

    
# api.add_resource(HelloWorld,"/helloworld/<string:name>/<int:test>")      #registering it as a resource with endpoint helloworld
# api.add_resource(HelloWorld,"/helloworld/<string:name>")

video_put_args= reqparse.RequestParser() #created reqparser obj

#automatically parse thru the req thats being sent and makes sure it fits the guidelines defined 
# and has the correct info in it
# videos= {}
video_put_args.add_argument("name", type= str, help="Name odf video" , required= True)
video_put_args.add_argument("views", type= int, help="views odf video",required= True)
video_put_args.add_argument("likes", type= int, help="likes odf video",required= True)

video_update_args= reqparse.RequestParser()
video_update_args.add_argument("name", type= str, help="Name odf video" , )
video_update_args.add_argument("views", type= int, help="views odf video",)
video_update_args.add_argument("likes", type= int, help="likes odf video",)
#for error or hint to sender  : help

# def if_video_id_doesnt_exist(video_id):
#     if video_id not in videos:
#         abort(404, message ="could not find the video")

# def if_video_id_exists(video_id):
#     if video_id in videos:
#         abort(409, message ="video id exists already")

resource_field={            #deines hoe an object should be serialized
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer,
}

class Video(Resource):
    @marshal_with(resource_field)       #decorator serialises the obj(ex; result) using the fiels in resorce field
    def get(self, video_id):
        # if_video_id_doesnt_exist(video_id)      #to prevent crashing
        result  = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            
            abort(404, message='couldnt find video ')
        return result
    
    @marshal_with(resource_field) 
    def put(self, video_id):
        # if_video_id_exists(video_id)    
        args = video_put_args.parse_args()
        result= VideoModel.query.filter_by(id=video_id).first()
        if  result:
            abort(409, message='video id already taken')
        video= VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        
        # videos[video_id] = args
        return video, 201

    @marshal_with(resource_field)
    def patch(self,video_id):
        args = video_update_args.parse_args()
        result= VideoModel.query.filter_by(id=video_id).first()
        if not result:
            
            abort(404, message='couldnt find video ')
        if  args ['name'] :
            result.name = args['name']                  #using result. ; as we modify only this instance not the whole db
    
        if args ['views']:
            result.name = args['views']

        if args ['likes']:
            result.name = args['likes']

        
        db.session.commit()

        return result

    # def delete(self, video_id):
    #     if_video_id_doesnt_exist(video_id)
    #     del videos[video_id]
    #     return '', 204
    
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == '__main__':
    app.run(debug= True, port = 8010)