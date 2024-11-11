from flask import Flask
from flask_restful import Api, Resource , reqparse , abort

# reqparser : helps send the needed data

app= Flask(__name__)
api = Api(app)      #wrap app in an api

names= {"tim":{"age":21 , "gen" :"male"}
        ,"jim":{"age":28 , "gen" :"male"}}

class HelloWorld(Resource):     #inheriting from resource  : class as a reaosurce

    # def get(self):
    #     return{"message":"helllow"}
    
    # def post(self):
    #     return{"message":"posted"}
    
    # def get(self,name,test):
    #     return{"name":name, "test" :test}
    
    def get(self,name):
        return names[name]   

    
# api.add_resource(HelloWorld,"/helloworld/<string:name>/<int:test>")      #registering it as a resource with endpoint helloworld
api.add_resource(HelloWorld,"/helloworld/<string:name>")

video_put_args= reqparse.RequestParser() #created reqparser obj

#automatically parse thru the req thats being sent and makes sure it fits the guidelines defined 
# and has the correct info in it
videos= {}
video_put_args.add_argument("name", type= str, help="Name odf video" , required= True)
video_put_args.add_argument("views", type= int, help="views odf video",required= True)
video_put_args.add_argument("likes", type= int, help="likes odf video",required= True)

#for error or hint to sender  : help

def if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message ="could not find the video")

def if_video_id_exists(video_id):
    if video_id in videos:
        abort(409, message ="video id exists already")

class Video(Resource):
    def get(self, video_id):
        if_video_id_doesnt_exist(video_id)      #to prevent crashing
        return videos[video_id]
    
    def put(self, video_id):
        if_video_id_exists(video_id)    
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201
    
    def delete(self, video_id):
        if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204
    
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == '__main__':
    app.run(debug= True, port = 8010)