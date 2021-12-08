from skpy import Skype
import time
from skpy import SkypeAuthException
from skpy import SkypeApiException
import skpy
import tempfile

class SkypeManager(Skype):

    _user = ""
    _tokenFile = ""

    def connect(self, _user, password):

        self._user = _user
        self._tokenFile = tempfile.NamedTemporaryFile().name
        self.conn.setTokenFile(self._tokenFile)

        try:
            self.conn.readToken()
        except SkypeAuthException:
            print("пытаюсь подключиться")
            if not self.conn.connected: 
                
                self.conn.setUserPwd(self._user, password)
                tryCount = 3
                i = 0
                while not self.conn.connected and i < tryCount:
                    
                    try:
                        self.conn.getSkypeToken()
                    except:     
                        time.sleep(10)
                        pass
                    finally:        
                        i += 1 

        try:
            self.conn
            print("подключено")
            
        except SkypeAuthException as authEx:
            skype_auth_error = authEx.args[0]
            print(skype_auth_error)
            
        return self.conn.connected

    def checkAuth(self):
        
        return self.conn.connected

    def conversationsList(self):

        groupChats = []

        chats = self.chats.recent()
        
        if len(chats) > 0:
            for item in chats: 
                if isinstance(chats[item], skpy.SkypeGroupChat):
                    groupChats.append({"topic":chats[item].topic, "id":chats[item].id})
        return groupChats


    def moveChat(self, admins, chatId, newChatName, moderate=False):

        chat = self.chats[chatId]
        members = chat.userIds
        result = False

        try:
            newChat = self.chats.create(members, admins)

            newChat.setTopic(newChatName)
            newChat.setIsModerateThread(self, moderate)

            result = True
        except:
            pass

        return result

    # Сделать группу модерируемой 
    def setIsModerateThread(self, chatId, moderate=True):

        result = False

        try:
            chat = self.chats[chatId]
            chat.setModerated(moderate)

            result = True
            print("Модерирование установлено в " + moderate + " для чата id: " + chatId + " name: " + chat.Topic)

        except:
            pass

        return result
    
    def setUserRole(self, chatId, userId, admin=False, silentMode = False):
        chat = self.chats[chatId]
        
        if  userId in chat.userIds:
        
            chat.addMember(userId, admin)
            role = "user"
            
            if admin:
                role = "admin"
            
            print("Пользователь " + userId + " изменил роль в чате : " + chat.topic + " " + chat.id + " на " + role)
            
            if silentMode:
                msgs = chat.getMsgs()

                for message in msgs:
                    if isinstance(message, 
                                (skpy.msg.SkypeChangeMemberMsg, 
                                skpy.msg.SkypeRemoveMemberMsg, skpy.msg.SkypeAddMemberMsg)) and not message.deleted:
                        
                        message.delete()
                        print("Сообщение удалено")
                        break
            
        else: 
            print("Пользователь " + userId + " не состоит в чате ")
        
    def addUser(self, chatId, userId, admin=False, silentMode = False):
        
        chat = self.chats[chatId]
        
        chat.addMember(userId, admin)
        role = "user"
        
        if admin:
            role = "admin"
        
        print("Пользователь " + userId + " добавлен в чат : " + chat.topic + " " + chat.id)
        
        if silentMode:
            msgs = chat.getMsgs()

            for message in msgs:
                if isinstance(message, 
                            (skpy.msg.SkypeChangeMemberMsg, 
                            skpy.msg.SkypeRemoveMemberMsg, skpy.msg.SkypeAddMemberMsg)) and not message.deleted:
                    
                    message.delete()
                    print("Сообщение удалено")
                    break
            
    def deleteUser(self, chatId, userId, silentMode = False):
       
        chat = self.chats[chatId]
        
        if  userId in chat.userIds:
        
            chat.removeMember(userId)
            
            print("Пользователь " + userId + " удален из чата " + chat.topic)
            
            if silentMode:
                msgs = chat.getMsgs()

                for message in msgs:
                    if isinstance(message, 
                                (skpy.msg.SkypeChangeMemberMsg, 
                                skpy.msg.SkypeRemoveMemberMsg, skpy.msg.SkypeAddMemberMsg)) and not message.deleted:
                        
                        message.delete()
                        print("Сообщение удалено")
                        break
        else: 
            print("Пользователь " + userId + " не состоит в чате ")

        
        
