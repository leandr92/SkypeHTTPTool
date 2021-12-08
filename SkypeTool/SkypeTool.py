from flask import Flask
from flask import request
from flask_restful import Api, Resource
import uuid
import os
import skype_manager as skype_manager

app = Flask(__name__)
api = Api(app)

appTokens = []

def findToken(token):
    
    for appToken in appTokens:
        if appToken["token"] == token:
            return appToken
        
    return None 

def resultDescription():
    return {"status": False, "errors":[]}

class Chats(Resource):
    
    def get(self, type="recent"):
        
        result = resultDescription()
        
        token = request.headers.get('token')
        
        authInfo = findToken(token)
        
        if authInfo == None:
            
            result["errors"]["Unauthorized"]
        
        else:
            
            skypeConnect = authInfo["skype"]    
                    
            if type == "recent":
                
                try:
                    conversitonsList = skypeConnect.conversationsList()
                
                    result["status"] = True
                    result["data"] = conversitonsList
                
                except Exception as e:
                    
                    result["errors"][str(e)]
            
            elif type == "reload":
            
                result["status"] = False
                result["error"]["Unsupported operation"]
                
            else:
                result["status"] = False
                result["error"]["Unsupported operation"]
            
        return result, 200

class ChatUsers(Resource):
    
    def get(self):
        
        result = resultDescription()
        
        data = request.get_json()
        
        chatId = data.get('chatId', '')
        
        if chatId=="":
            
            result["errors"]["Unsupported operation. Id not filled"]  
            
        else:
            
            token = request.headers.get('token')
        
            authInfo = findToken(token)
            
            if authInfo == None:
                
                result["errors"]["Unauthorized"]
            
            else:
                
                skypeConnect = authInfo["skype"]    
                try:        
                    
                    chatUsers = skypeConnect.chats[chatId].userIds
                    
                except Exception as e:
                    
                    result["errors"][str(e)]
                    
                result["status"] = True
                
                result["data"] = chatUsers
  
        
        return result, 200
    
    def post(self):
        
        result = resultDescription()
            
        token = request.headers.get('token')
    
        authInfo = findToken(token)
        
        if authInfo == None:
            
            result["errors"]["Unauthorized"]
        
        else:
            
            data = request.get_json()
        
            chatId      = data.get('chatId', '')
            userId      = data.get('userId', '')
            asAdmin     = data.get('AsAdmin', False)
            silentMode  = data.get('silentMode', False)
            
            if chatId == "":
                result["errors"]["chatId not filled"]
            
            if userId == "":
                result["errors"]["userId not filled"]
            
            if len(result["errors"]) == 0:
            
                skypeConnect = authInfo["skype"]    
                
                try:
                        
                    skypeConnect.addUser(chatId, userId, asAdmin, silentMode)
                
                    result["status"] = True
                
                except Exception as e:
                    
                    result["errors"][str(e)]
        
        return result, 200
    
    def delete(self):
        
        result = resultDescription()
            
        token = request.headers.get('token')
    
        authInfo = findToken(token)
        
        if authInfo == None:
            
            result["errors"]["Unauthorized"]
        
        else:
            
            data = request.get_json()
        
            chatId      = data.get('chatId', '')
            userId      = data.get('userId', '')
            silentMode  = data.get('silentMode', False)
            
            if chatId == "":
                result["errors"]["chatId not filled"]
            
            if userId == "":
                result["errors"]["userId not filled"]
            
            if len(result["errors"]) == 0:
            
                skypeConnect = authInfo["skype"]    
                
                try:
                        
                    skypeConnect.deleteUser(chatId, userId, silentMode)
                
                    result["status"] = True
                
                except Exception as e:
                    
                    result["errors"][str(e)]
        
        
        return result, 200

class Utils(Resource):
   
    def post(self, type):
    
        errors = []
    
        result = resultDescription()
    
        if type == "exit":
           
            try:
                self.shutdown_server()
                
                for appToken in appTokens:
                    
                    skypeConnect = appToken["skype"]
                    
                    if skypeConnect !=None:
                    
                        os.unlink(skypeConnect._tokenFile)
                
                result["status"] = True
                result["errors"] = errors
            
            except Exception as e:
                result["status"] = False
                result["errors"] = errors[str(e)]
            
        elif type == "auth":
           
            data = request.get_json()
           
            login = data.get('login', '')
            password = data.get('pass', '')
            
            token = uuid.uuid1().hex
            
            if login == "":
                errors.append("login not filled")
            if password == "":
                errors.append("password not filled")
                
            if len(errors) == 0:
               
                skype = skype_manager.SkypeManager()
                
                connected = skype.connect(login, password)
                
                if connected: 
                    appTokens.append({"token":token, "login":login, "pass":password, "skype":skype})
                    result["token"] = token
                    result["status"] = True
            
                result["connected"] = connected
            else:
                result["errors"] = errors
        elif type == "ping":
            result["status"] = True
            
        
        return result, 200
                      
    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        
        func()

api.add_resource(Chats, "/chats", "/chats/", "/chats/<string:type>")
api.add_resource(ChatUsers, "/chatUsers", "/chatUsers/")
api.add_resource(Utils, "/utils", "/utils/", "/utils/<string:type>")

if __name__ == '__main__':
    app.run()
