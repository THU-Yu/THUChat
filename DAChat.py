import sys
import os
import copy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDockWidget, QListWidget
from PyQt5.QtGui import *
from Ui_Welcome import Ui_Dialog
from Ui_Main import Ui_MainWindow
from Ui_AddFriendDialog import Ui_AddFriendDialog
from Ui_GroupSendDialog import Ui_GroupSendDialog
from Ui_VoiceCall import Ui_VoiceCallDialog
from socket import *
from threading import Thread
import datetime
import json
import pyaudio


# 封装自己的数据报，以字典形式封装
def SetData(t,s,target,data):
     Data = {}
     Data['type'] = t
     Data['source'] = s
     Data['target'] = target
     Data['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
     Data['data'] = data
     return Data

# P2P模式下的服务器线程，TCP协议
class P2PServerTCP(QThread):
     ## 设置信号，根据收到的信息不同对应不同信号
     # addfriendrequest 代表收到交友邀请
     # Addfriendaccept 代表收到同意加好友信号
     # msgReceive 代表收到信息
     # fileReceive 代表收到文件
     # NoAccept 代表收到拒绝好友
     addfriendrequest = pyqtSignal(dict)
     Addfriendaccept = pyqtSignal(dict)
     msgReceive = pyqtSignal(dict)
     fileReceive = pyqtSignal(dict)
     group = pyqtSignal(dict)
     audio = pyqtSignal(dict)
     def __init__(self):
          super(P2PServerTCP, self).__init__()
          # 设置本机IP和端口号，绑定socket（TCP）
          self.P2PSeverName = gethostbyname(gethostname())
          self.P2PSeverPort = 8000
          self.P2PServerSocket = socket(AF_INET,SOCK_STREAM)
          self.P2PServerSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
          self.working = True
          self.audio.connect(self.Call)
     def stop(self):
          self.working = False
     def TCPLink(self,sock):
          ## 每个连接的处理函数
          # sock为该连接的socket（TCP）
          data = b''
          # 读取所有数据，直到长度小于1024
          while True:
               part = sock.recv(1024)
               data += part
               if len(part) < 1024:
                    break
          data = json.loads(data.decode('utf-8'))
          # 回复ACK
          sock.sendall(b'ACK')
          # 根据不同type的数据报决定处理方式
          if data['type'] == 'AddFriendRequest':
               self.addfriendrequest.emit(data)
          elif data['type'] == 'FriendAccept':
               self.Addfriendaccept.emit(data)
          elif data['type'] == 'Msg':
               self.msgReceive.emit(data)
          elif data['type'] == 'FILE':
               # 打开文件接收模式，将接收到的文件写入默认路径
               fileName = data['data'].split('/')[-1]
               Size = 0
               if not os.path.exists('./data/'+data['target']):
                    os.makedirs('./data/'+data['target'])
                    os.makedirs('./data/'+data['target']+'/recv_files')
               with open('./data/'+data['target']+'/recv_files/' + fileName, 'wb') as F:
                    part = sock.recv(20480)
                    Size += len(part)
                    while Size < data['FileSize']:
                         F.write(part)
                         part = sock.recv(20480)
                         Size += len(part)
                         if Size >= data['FileSize']:
                              break
                    F.write(part)
               self.fileReceive.emit(data)
          elif data['type'] == 'GROUP':
               self.group.emit(data)
          elif data['type'] == 'AUDIO':
               self.audio.emit(data)
          sock.close()
     def run(self):
          self.P2PServerSocket.bind((self.P2PSeverName,self.P2PSeverPort))
          # 开启监听，最大连接数设为5
          self.P2PServerSocket.listen(5)
          while self.working == True:
               client, addr = self.P2PServerSocket.accept()
               # 为新连接的客户开启处理线程
               t = Thread(target=self.TCPLink,args=(client,))
               t.start()
          self.P2PServerSocket.close()
     def Call(self, data):
          self.voicecall = VoiceCall(8003)
          self.voicecall.VoiceServer.start()
          self.voicecall.UserNameLabel.setText(data['source'])
          self.voicecall.P2PSeverPort = 8000
          self.voicecall.UserId_map[data['source']] = data['data']
          self.voicecall.AcceptButton.clicked.connect(self.voicecall.SendAccept)
          self.voicecall.RefuseButton.clicked.connect(self.voicecall.SendRefuse)
          self.voicecall.show()

# 为了方便处理文件传输另外写了一个文件传输下的P2P客户端
class P2PFileClient(QThread):
     ## 设置信号
     # finish代表传输完成
     # offline代表用户不在线
     finish = pyqtSignal()
     offline = pyqtSignal()
     def __init__(self, data):
          super(P2PFileClient,self).__init__()
          self.severName = '166.111.140.57'
          self.severPort = 8000
          self.P2PClientSocket = socket(AF_INET,SOCK_STREAM)
          self.Data = data
     def run(self):
          # 根据文件报文，打开对应文件并以二进制读取进行依次传输
          Filetarget = self.Data['target']
          self.Data['FileSize'] = os.path.getsize(self.Data['data'])
          self.P2PClientSocket.connect((self.severName,self.severPort))
          data = "q"+Filetarget
          self.P2PClientSocket.sendall(data.encode("utf-8"))
          modifiedData = self.P2PClientSocket.recv(1024).decode('utf-8')
          if modifiedData != "n":
               # 确认用户在线开始传输
               self.P2PClientSocket.close()
               self.P2PClientSocket = socket(AF_INET,SOCK_STREAM)
               self.P2PClientSocket.connect((modifiedData,int(Filetarget[5:])))
               # 先传文件报文
               self.P2PClientSocket.sendall(json.dumps(self.Data).encode('utf-8'))
               # 再传输文件内容
               with open(self.Data['data'], 'rb') as F:
                    while True:
                         chunk = F.read(20480)
                         if not chunk:
                              break                         
                         self.P2PClientSocket.sendall(chunk)
               self.finish.emit()
          else:
               self.offline.emit()

# P2P模式下，单一data的发送信息客户端线程
class P2PClientTCP(QThread):
     ## 设置信号
     # finish代表发送成功
     # fail代表超时或其他原因导致发送失败
     # offline代表目标用户不在线
     finish = pyqtSignal()
     fail = pyqtSignal(dict)
     offline = pyqtSignal(dict)
     def __init__(self, data, account):
          super(P2PClientTCP,self).__init__()
          self.severName = '166.111.140.57'
          self.severPort = 8000
          self.P2PClientName = gethostbyname(gethostname())
          self.P2PClientPort = 8001
          self.P2PClientSocket = socket(AF_INET,SOCK_STREAM)
          self.Data = json.dumps(data)
          self.Account= account
     def run(self):
          # 先向服务器询问目标用户是否在线
          self.P2PClientSocket.connect((self.severName,self.severPort))
          data = "q"+self.Account
          self.P2PClientSocket.sendall(data.encode("utf-8"))
          modifiedData = self.P2PClientSocket.recv(1024).decode('utf-8')
          if modifiedData != "n":
               # 目标用户在线，则正常发送数据
               self.P2PClientSocket.close()
               self.P2PClientSocket = socket(AF_INET,SOCK_STREAM)
               self.P2PClientSocket.connect((modifiedData,int(self.Account[5:])))
               self.P2PClientSocket.sendall(self.Data.encode('utf-8'))
               # 尝试接收ACK信号，确保传输成功
               try:
                    self.P2PClientSocket.settimeout(0.2)
                    receive = self.P2PClientSocket.recv(3)
               except timeout:
                    self.fail.emit(json.loads(self.Data))
               else:
                    if receive == b'ACK':
                         self.finish.emit()
                    else:
                         self.fail.emit(json.loads(self.Data))
          else:
               # 目标用户不在线
               self.P2PClientSocket.close()
               self.offline.emit(json.loads(self.Data))

# P2P模式下发送信息的线程（常开）
class SendMsgThread(QThread):
     offline = pyqtSignal(dict)
     fail = pyqtSignal(dict)
     def __init__(self):
          super(SendMsgThread,self).__init__()
          self.MsgWaitingList = []
          self.working = False
          self.Finish = True
          self.Filelen = 0
          self.Filetarget = ""
          self.p2pclient = P2PClientTCP(SetData('test',0,0,'test'),'')
     def run(self):
          self.working = True
          # working状态为True时，开启循环，尝试从信息列表中读取信息进行发送
          while self.working:
               if self.MsgWaitingList == []:
                    continue
               elif self.Finish:
                    # 如果前一次传输已经完成，继续发送下一个
                    self.Finish = False
                    data = self.MsgWaitingList[0]
                    account = data['target']
                    if data['type'] == 'FILE':
                         # 如果报文为文件模式，进入文件传输线程，开始传输文件
                         self.p2psendfile = P2PFileClient(data)
                         self.p2psendfile.start()
                         self.p2psendfile.finish.connect(self.KillFileThread)
                         self.p2psendfile.offline.connect(self.KillFileThread)
                         self.MsgWaitingList.remove(data)
                         continue
                    self.p2pclient.quit()
                    self.p2pclient = P2PClientTCP(data,account)
                    self.MsgWaitingList.remove(data)
                    self.p2pclient.finish.connect(self.DestroyClient)
                    self.p2pclient.offline.connect(self.UserOffline)
                    self.p2pclient.fail.connect(self.NetError)
                    self.p2pclient.start()
               else:
                    continue
     def DestroyClient(self):
          # 接收到finish信号后，将单次传输的client线程关闭，并更改Finish状态
          self.Finish = True
          self.p2pclient.quit()
          self.p2pclient.finish.disconnect(self.DestroyClient)
     def UserOffline(self,data):
          self.Finish = True
          self.p2pclient.quit()
          self.offline.emit(data)
          self.p2pclient.offline.disconnect(self.UserOffline)
          self.p2pclient.fail.disconnect(self.NetError)
     def NetError(self, data):
          # 发送失败的槽函数，提示可能因为网络问题导致发送失败
          self.Finish = True
          self.p2pclient.quit()
          # self.p2pclient.wait()
          self.fail.emit(data)
          self.p2pclient.offline.disconnect(self.UserOffline)
          self.p2pclient.fail.disconnect(self.NetError)
     def KillFileThread(self):
          # 文件传输线程退出的槽函数
          self.Finish = True
          self.p2psendfile.quit()
          # self.p2psendfile.wait()
          self.p2psendfile.finish.disconnect(self.KillFileThread)
          self.p2psendfile.offline.disconnect(self.KillFileThread)

class VoiceCallServer(QThread):
     ACK = pyqtSignal()
     NOT = pyqtSignal()
     END = pyqtSignal()
     def __init__(self,port):
          super(VoiceCallServer,self).__init__()
          # 设置本机IP和端口号，绑定socket（TCP）
          self.P2PSeverName = gethostbyname(gethostname())
          self.P2PSeverPort = port
          self.P2PServerSocket = socket(AF_INET,SOCK_STREAM)
          self.P2PServerSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
          self.working = True
     def stop(self):
          self.working = False
     def run(self):
          self.P2PServerSocket.bind((self.P2PSeverName,self.P2PSeverPort))
          self.P2PServerSocket.listen(1)
          client, addr = self.P2PServerSocket.accept()
          CHUNK = 10240
          FORMAT = pyaudio.paInt16
          CHANNELS = 1
          RATE = 44100
          p = pyaudio.PyAudio()
          stream=p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
          while self.working == True:
               receive = client.recv(10240)
               if receive == b'ACK':
                    self.ACK.emit()
               elif receive == b'NOT':
                    self.stop()
                    self.NOT.emit()
               elif receive[0:3] == b'END':
                    self.stop()
                    self.END.emit()
               else:
                    stream.write(receive)
          stream.stop_stream()            # 停止数据流
          stream.close()                        # 关闭数据流
          p.terminate()
          client.close()
          self.P2PServerSocket.close()

# 登入界面，采用CS模式
class mywindow(QtWidgets.QDialog, Ui_Dialog):
     sendaccount = pyqtSignal(str)
     def __init__(self):
         super(mywindow, self).__init__()
         self.setupUi(self)
         # 设置服务器IP和端口号
         self.severName = '166.111.140.57'
         self.severPort = 8000
     def Login(self):
          # 读取用户输入的账户和密码信息
          self.account = self.Username.text()
          self.password = self.Password.text()
          # 检查输入是否合法
          if self.account == "" or self.password == "":
               QMessageBox.warning(self, "Message", "请输入账户名和密码！",QMessageBox.Ok)
               return
          # 建立CS架构的客户端socket（TCP）
          clientSocket = socket(AF_INET,SOCK_STREAM)
          clientSocket.connect((self.severName,self.severPort))
          data = self.account + "_" + self.password
          clientSocket.sendall(data.encode('utf-8'))
          modifiedData = clientSocket.recv(1024).decode('utf-8')
          if modifiedData != "lol":
               QMessageBox.critical(self, "Message", "账户或密码错误！",QMessageBox.Ok)
          else:
               QMessageBox.information(self, "Message", "登入成功！",QMessageBox.Ok)
               self.sendaccount.emit(self.account)
          clientSocket.close()

# 好友邀请的窗口
class AddFriendDialog(QtWidgets.QDialog,Ui_AddFriendDialog):
     ## 设置信号
     # newfriend代表同意了交友申请，用以更新主界面的好友列表
     newfriend = pyqtSignal(str)
     def __init__(self):
          super(AddFriendDialog, self).__init__()
          self.setupUi(self)
          self.Account = ""
          self.RequestList = []
          self.SendMsg = SendMsgThread()
          self.SendMsg.start()
          self.AcceptButton.setEnabled(False)
          self.RefuseButton.setEnabled(False)
          self.listModel = QStringListModel()
          self.listModel.setStringList(self.RequestList)
          self.RequestListView.setModel(self.listModel)
          self.RequestListView.clicked.connect(self.ListViewItem)
          self.AcceptButton.clicked.connect(self.Accept)
          self.RefuseButton.clicked.connect(self.Refuse)
     def ResetUi(self):
          # 不同用户登入时需要更新Ui
          self.Account = ""
          self.RequestList = []
          self.SendMsg.quit()
          # self.SendMsg.wait()
          self.SendMsg = SendMsgThread()
          self.SendMsg.start()
          self.AcceptButton.setEnabled(False)
          self.RefuseButton.setEnabled(False)
          self.listModel = QStringListModel()
          self.listModel.setStringList(self.RequestList)
          self.RequestListView.setModel(self.listModel)
     def ListViewItem(self, index):
          # ListView选中的槽函数，用以读取当前选择的项目
          self.friend = self.RequestList[index.row()]
          self.AcceptButton.setEnabled(True)
          self.RefuseButton.setEnabled(True)
     def Accept(self):
          # 同意交友申请，删除申请并通知主界面修改好友列表
          self.newfriend.emit(self.friend)
          self.RequestList.remove(self.friend)
          self.listModel.setStringList(self.RequestList)
          self.AcceptButton.setEnabled(False)
          self.RefuseButton.setEnabled(False)
          self.RequestListView.setModel(self.listModel)
          # 发送同意信息给好友
          self.SendMsg.MsgWaitingList.append(SetData('FriendAccept',self.Account,self.friend,'Accept'))
          self.SendMsg.offline.connect(self.UserOffline)
          self.SendMsg.fail.connect(self.NetError)
     def Refuse(self):
          # 拒绝好友申请，并删除申请
          reply = QMessageBox.question(self, "DAChat", "确定要拒绝"+self.friend+"的交友邀请吗？",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
          if reply == QMessageBox.Yes:
               self.RequestList.remove(self.friend)
               self.listModel.setStringList(self.RequestList)
               self.RequestListView.setModel(self.listModel)
               self.AcceptButton.setEnabled(False)
               self.RefuseButton.setEnabled(False)
     def UserOffline(self,data):
          # 用户不在线的槽函数，通知目标用户不在线
          if data['type'] == 'Accept':
               QMessageBox.warning(self,"DAChat","该用户（"+self.Account+"）当前不在线，请稍后重试",QMessageBox.Ok)
               self.SendMsg.p2pclient.quit()
               # self.SendMsg.p2pclient.wait()
               self.SendMsg.offline.disconnect(self.UserOffline)
               self.SendMsg.fail.disconnect(self.NetError)
     def NetError(self, data):
          # 发送失败的槽函数，提示可能因为网络问题导致发送失败
          if data['type'] == 'Accept':
               QMessageBox.warning(self,"DAChat","网络出现问题，请稍后重试",QMessageBox.Ok)
               self.SendMsg.p2pclient.quit()
               # self.SendMsg.p2pclient.wait()
               self.SendMsg.fail.disconnect(self.NetError)
               self.SendMsg.offline.disconnect(self.UserOffline)
class GroupSendDialog(QtWidgets.QDialog,Ui_GroupSendDialog):
     choose = pyqtSignal(list)
     def __init__(self):
          super(GroupSendDialog,self).__init__()
          self.setupUi(self)
          self.FriendList = []
          self.listModel = QStringListModel()
          self.listModel.setStringList(self.FriendList)
          self.FriendListView.setModel(self.listModel)
          self.ChooseList = []
          self.listModel1 = QStringListModel()
          self.listModel1.setStringList(self.ChooseList)
          self.ChooseListView.setModel(self.listModel1)
          self.friend1 = ""
          self.friend2 = ""
          self.FriendListView.clicked.connect(self.ListViewItem1)
          self.ChooseListView.clicked.connect(self.ListViewItem2)
          self.AddButton.clicked.connect(self.AddFriendToChooseList)
          self.SubButton.clicked.connect(self.SubFriendToFriendList)
          self.pushButton.clicked.connect(self.Send)
     def ListViewItem1(self, index):
          # ListView选中的槽函数，用以读取当前选择的项目
          self.friend1 = self.FriendList[index.row()][0:10]
     def ListViewItem2(self, index):
          # ListView选中的槽函数，用以读取当前选择的项目
          self.friend2 = self.ChooseList[index.row()][0:10]
     def AddFriendToChooseList(self):
          if self.friend1 != "":
               self.ChooseList.append(self.friend1)
               self.FriendList.remove(self.friend1)
          self.listModel.setStringList(self.FriendList)
          self.FriendListView.setModel(self.listModel)
          self.listModel1.setStringList(self.ChooseList)
          self.ChooseListView.setModel(self.listModel1)
          self.friend1 = ""
     def SubFriendToFriendList(self):
          if self.friend2 != "":
               self.FriendList.append(self.friend2)
               self.ChooseList.remove(self.friend2)
          self.listModel.setStringList(self.FriendList)
          self.FriendListView.setModel(self.listModel)
          self.listModel1.setStringList(self.ChooseList)
          self.ChooseListView.setModel(self.listModel1)
          self.friend2 = ""
     def Send(self):
          self.choose.emit(self.ChooseList)
          self.close()

class VoiceCall(QtWidgets.QDialog, Ui_VoiceCallDialog):
     offline = pyqtSignal()
     def __init__(self,port):
          super(VoiceCall, self).__init__()
          self.setupUi(self)
          self.severName = '166.111.140.57'
          self.severPort = 8000
          self.P2PClientSocket = socket(AF_INET,SOCK_STREAM)
          self.Account = ""
          self.P2PSeverName = gethostbyname(gethostname())
          self.P2PSeverPort = 8000
          self.P2PServerSocket = socket(AF_INET,SOCK_STREAM)
          self.UserId_map = {}
          self.VoiceServer = VoiceCallServer(port)
          self.VoiceServer.ACK.connect(self.Accept)
          self.VoiceServer.NOT.connect(self.Refuse)
          self.VoiceServer.END.connect(self.End)
          self.offline.connect(self.UserOffline)
          self.calling = False
     def SendCallRequest(self, data):
          self.Data = json.dumps(data)
          self.Account = data['target']
          self.P2PClientSocket.connect((self.severName,self.severPort))
          data = "q"+self.Account
          self.P2PClientSocket.sendall(data.encode("utf-8"))
          modifiedData = self.P2PClientSocket.recv(1024).decode('utf-8')
          if modifiedData != "n":
               # 目标用户在线，则正常发送数据
               self.P2PClientSocket.close()
               self.P2PClientSocket = socket(AF_INET,SOCK_STREAM)
               self.P2PClientSocket.connect((modifiedData,int(self.Account[5:])))
               self.P2PClientSocket.sendall(self.Data.encode('utf-8'))
               self.UserId_map[self.Account] = modifiedData
               self.P2PClientSocket.close()
               self.P2PClientSocket = socket(AF_INET,SOCK_STREAM)
               self.P2PClientSocket.connect((modifiedData,self.P2PSeverPort))
          else:
               # 目标用户不在线
               self.P2PClientSocket.close()
               self.offline.emit()
     def SendAccept(self):
          self.P2PClientSocket = socket(AF_INET,SOCK_STREAM)
          self.P2PClientSocket.connect((self.UserId_map[self.UserNameLabel.text()],self.P2PSeverPort))
          self.P2PClientSocket.sendall(b'ACK')
          self.AcceptButton.setVisible(False)
          self.RefuseButton.setVisible(True)
          self.RefuseButton.setText("挂断")
          self.AcceptButton.clicked.disconnect(self.SendAccept)
          self.RefuseButton.clicked.disconnect(self.SendRefuse)
          self.RefuseButton.clicked.connect(self.EndCall)
          t = Thread(target=self.Calling)
          t.start()
     def SendRefuse(self):
          self.P2PClientSocket = socket(AF_INET,SOCK_STREAM)
          self.P2PClientSocket.connect((self.UserId_map[self.UserNameLabel.text()],self.P2PSeverPort))
          self.P2PClientSocket.sendall(b'NOT')
          self.VoiceServer.stop()
          self.AcceptButton.clicked.disconnect(self.SendAccept)
          self.RefuseButton.clicked.disconnect(self.SendRefuse)
          self.close()
     def EndCall(self):
          self.calling = False
     def End(self):
          if self.calling:
               self.calling = False
               self.close()
          else:
               self.close()
     def Accept(self):
          self.AcceptButton.setVisible(False)
          self.RefuseButton.setVisible(True)
          self.RefuseButton.setText("挂断")
          self.RefuseButton.clicked.connect(self.EndCall)
          t = Thread(target=self.Calling)
          t.start()
     def Refuse(self):
          QMessageBox.warning(self, 'DAChat', '对方拒绝接听！', QMessageBox.Ok)
          self.P2PClientSocket.close()
          self.close()
     def Calling(self):
          self.calling = True
          CHUNK = 10240
          FORMAT = pyaudio.paInt16
          CHANNELS = 1
          RATE = 44100
          p = pyaudio.PyAudio()
          stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
          while self.calling:
               data = stream.read(CHUNK)
               self.P2PClientSocket.sendall(data)
          self.P2PClientSocket.sendall(b'END')
          self.P2PClientSocket.close()
     def UserOffline(self):
          QMessageBox.warning(self, 'DAChat','对方不在线！',QMessageBox.Ok)
          self.close()

# 主界面
class MyMain(QtWidgets.QMainWindow, Ui_MainWindow):
     end = pyqtSignal()
     def __init__(self):
          super(MyMain, self).__init__()
          self.setupUi(self)
          self.severName = '166.111.140.57'
          self.severPort = 8000
          self.p2pserver = P2PServerTCP()
          self.logout = False
          self.SendMsg_thread = SendMsgThread()
          self.SendMsg_thread.start()
          self.MsgList = [[],]
          self.Account_dict = {}
          self.GroupMember_dict = {}
          self.listModel = QStringListModel()
          self.FriendList=[]
          self.friend = ""
          self.listModel.setStringList(self.FriendList)
          self.FriendListView.setModel(self.listModel)
          self.addfrienddialog = AddFriendDialog()
          self.SendMsgButton.setEnabled(False)
          self.SendFileButton.setEnabled(False)
          self.VideoButton.setEnabled(False)
          self.VoiceButton.setEnabled(False)
          self.FriendRequestButton.setIcon(QtGui.QIcon('resources/add.png'))
          self.SendMsgButton.setIcon(QtGui.QIcon('resources/send.png'))
          self.SendFileButton.setIcon(QtGui.QIcon('resources/file.png'))
          self.VideoButton.setIcon(QtGui.QIcon('resources/videotalk.png'))
          self.VoiceButton.setIcon(QtGui.QIcon('resources/voicetalk.png'))
          self.GroupChatButton.setIcon(QtGui.QIcon('resources/group.ico'))
          self.LogoutButton.setIcon(QtGui.QIcon('resources/logout.ico'))
          self.LogoutButton.clicked.connect(self.LogOut)
          self.FindFriendButton.clicked.connect(self.FindFriend)
          self.p2pserver.addfriendrequest.connect(self.FriendRequest)
          self.p2pserver.Addfriendaccept.connect(self.FriendAccept)
          self.FriendRequestButton.clicked.connect(self.addfrienddialog.show)
          self.addfrienddialog.newfriend.connect(self.NewFriend)
          self.FriendListView.clicked.connect(self.ListViewItem)
          self.SendMsgButton.clicked.connect(self.SendMsg)
          self.p2pserver.msgReceive.connect(self.MsgReceive)
          self.SendFileButton.clicked.connect(self.ChooseFile)
          self.GroupChatButton.clicked.connect(self.GroupDialogShow)
          self.VoiceButton.clicked.connect(self.VoiceCall)
     def ResetUi(self):
          # 更换用户时，需要刷新界面
          self.logout = False
          self.p2pserver.stop()
          self.p2pserver.quit()
          self.p2pserver = P2PServerTCP()
          self.SendMsg_thread.quit()
          self.SendMsg_thread = SendMsgThread()
          self.SendMsg_thread.start()
          self.MsgList = [[],]
          self.Account_dict = {}
          self.GroupMember_dict = {}
          self.FriendList=[]
          self.friend = ""
          self.listModel = QStringListModel()
          self.listModel.setStringList(self.FriendList)
          self.FriendListView.setModel(self.listModel)
          self.FindFriendBox.setText("")
          self.MsgInputBox.setText("")
          self.addfrienddialog.ResetUi()
          self.SendMsgButton.setEnabled(False)
          self.SendFileButton.setEnabled(False)
          self.VideoButton.setEnabled(False)
          self.VoiceButton.setEnabled(False)
          self.FriendRequestButton.setIcon(QtGui.QIcon('resources/add.png'))
          self.SendMsgButton.setIcon(QtGui.QIcon('resources/send.png'))
          self.SendFileButton.setIcon(QtGui.QIcon('resources/file.png'))
          self.VideoButton.setIcon(QtGui.QIcon('resources/videotalk.ico'))
          self.VoiceButton.setIcon(QtGui.QIcon('resources/voicetalk.png'))
          self.GroupChatButton.setIcon(QtGui.QIcon('resources/group.ico'))
          self.LogoutButton.setIcon(QtGui.QIcon('resources/logout.ico'))
          self.p2pserver.addfriendrequest.connect(self.FriendRequest)
          self.p2pserver.Addfriendaccept.connect(self.FriendAccept)
          self.p2pserver.msgReceive.connect(self.MsgReceive)
          self.p2pserver.fileReceive.connect(self.FileReceive)
          self.p2pserver.group.connect(self.GroupChatReceive)
     def closeEvent(self,event):
          # 重写关闭事件，确保每次关闭一定会登出
          if self.logout == False:
               reply = QMessageBox.question(self,'DAChat', "是否要退出程序？(退出时会自动登出)",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.No)
               if reply == QMessageBox.Yes:
                    # 向服务器发送下线指令
                    self.account = self.Account.text()[5:]
                    clientSocket = socket(AF_INET,SOCK_STREAM)
                    clientSocket.connect((self.severName,self.severPort))
                    data = "logout"+self.account
                    clientSocket.sendall(data.encode('utf-8'))
                    modifiedData = clientSocket.recv(1024).decode('utf-8')
                    if modifiedData == "loo":
                         QMessageBox.information(self, "Message", "成功登出！",QMessageBox.Ok)
                         clientSocket.close()
                         event.accept()
                         self.end.emit()
                    else:
                         QMessageBox.critical(self, "Message", "登出失败，请稍后再试！",QMessageBox.Ok)
                         clientSocket.close()
                         event.ignore()
               else:
                    event.ignore()
          else:
               event.accept()
               self.end.emit()
     def LogOut(self):
          # 主动向服务器发送下线指令
          self.account = self.Account.text()[5:]
          clientSocket = socket(AF_INET,SOCK_STREAM)
          clientSocket.connect((self.severName,self.severPort))
          data = "logout"+self.account
          clientSocket.sendall(data.encode('utf-8'))
          modifiedData = clientSocket.recv(1024).decode('utf-8')
          if modifiedData == "loo":
               QMessageBox.information(self, "Message", "成功登出！",QMessageBox.Ok)
               clientSocket.close()
               self.logout = True
               self.close()
          else:
               QMessageBox.critical(self, "Message", "登出失败，请稍后再试！",QMessageBox.Ok)
               clientSocket.close()
     def FindFriend(self):
          # 向服务器发送查询好友指令
          if self.FindFriendBox.text() == "":
               return
          self.account = self.Account.text()[5:]
          friend = self.FindFriendBox.text()
          self.FindFriendBox.setText("")
          clientSocket = socket(AF_INET,SOCK_STREAM)
          clientSocket.connect((self.severName,self.severPort))
          data = "q"+friend
          clientSocket.sendall(data.encode('utf-8'))
          modifiedData = clientSocket.recv(1024).decode('utf-8')
          if modifiedData == "n":
               QMessageBox.warning(self, "Warning", "该用户("+friend+")不在线，无法通信！\n请确认好友在线！",QMessageBox.Ok)
               clientSocket.close()
          else:
               if friend not in self.FriendList:
                    reply = QMessageBox.question(self,'DAChat', "该用户("+friend+")在线，是否添加为好友？",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.No)
                    if reply == QMessageBox.Yes:
                         # 向目标用户发送交友申请，采用P2P模式
                         addr = (modifiedData,int(friend[5:]))
                         clientSocket.close()
                         clientSocket = socket(AF_INET,SOCK_STREAM)
                         clientSocket.connect(addr)
                         data = SetData('AddFriendRequest',self.account,friend,'AddFriend')
                         data = json.dumps(data)
                         clientSocket.sendall(data.encode('utf-8'))
                    clientSocket.close()
               else:
                    QMessageBox.information(self,'DAChat', "该用户("+friend+")在线!",QMessageBox.Ok)
     def FriendRequest(self, data):
          # 收到交友申请的槽函数，用来更新交友申请界面的列表信息
          friend = data['source']
          if friend not in self.addfrienddialog.RequestList:
               self.addfrienddialog.RequestList.append(friend)
               self.addfrienddialog.listModel.setStringList(self.addfrienddialog.RequestList)
               self.addfrienddialog.RequestListView.setModel(self.addfrienddialog.listModel)
     def FriendAccept(self, data):
          # 好友接受申请的槽函数，用来更新主界面的好友列表
          self.Account_dict[data['source']] = len(self.FriendList)
          self.MsgList.append([])
          self.FriendList.append(data['source'])
          self.listModel.setStringList(self.FriendList)
          self.FriendListView.setModel(self.listModel)
     def NewFriend(self,s):
          # 同意交友申请的槽函数，用来更新主界面的好友列表
          if s not in self.FriendList:
               self.Account_dict[s] = len(self.FriendList)
               self.MsgList.append([])
               self.FriendList.append(s)
               self.listModel.setStringList(self.FriendList)
               self.FriendListView.setModel(self.listModel)
     def ListViewItem(self, index):
          # ListView选中的槽函数，用以读取当前选择的项目
          self.friend = self.FriendList[index.row()][0:10]
          if 'group' in self.friend:
               self.friend = self.FriendList[index.row()]
               if 'new' in self.friend:
                    self.friend = self.FriendList[index.row()][0:-5]
          self.FriendList[self.Account_dict[self.friend]] = self.friend          
          self.listModel.setStringList(self.FriendList)
          self.FriendListView.setModel(self.listModel)
          self.ChatLabel.setText(self.friend)
          if 'group' in self.friend:
               self.SendMsgButton.setEnabled(True)
               self.SendFileButton.setEnabled(False)
               self.VideoButton.setEnabled(False)
               self.VoiceButton.setEnabled(False)
          else:
               self.SendMsgButton.setEnabled(True)
               self.SendFileButton.setEnabled(True)
               self.VideoButton.setEnabled(True)
               self.VoiceButton.setEnabled(True)
               self.MsgShowBox.setText("")
          # 显示聊天记录，根据报文格式，选择不同的输出格式
          for data in self.MsgList[self.Account_dict[self.friend]]:
               if data['type'] == 'FILE':
                    if data['target'] == self.friend:
                         self.MsgShowBox.append("*****"+data['source']+"("+data['time']+"):\n发送了文件（"+data['data'].split('/')[-1]+'）\n')
                    elif data['source'] == self.friend:
                         self.MsgShowBox.append(data['source']+"("+data['time']+"):\n发送了文件（"+data['data'].split('/')[-1]+'）\n')
                    else:
                         continue
               elif data['type'] == 'Msg':
                    if data['target'] == self.friend:
                         self.MsgShowBox.append("*****"+data['source']+"("+data['time']+"):\n"+data['data']+'\n')
                    elif data['source'] == self.friend:
                         self.MsgShowBox.append(data['source']+"("+data['time']+"):\n"+data['data']+'\n')
                    else:
                         continue
               elif data['type'] == 'GROUP':
                    if data['source'] == self.account:
                         self.MsgShowBox.append("*****"+data['source']+"("+data['time']+"):\n"+data['data']+'\n')
                    else:
                         self.MsgShowBox.append(data['source']+"("+data['time']+"):\n"+data['data']+'\n')
     def SendMsg(self):
          if self.MsgInputBox.toPlainText() == "":
               QMessageBox.warning(self, "DAChat", "不能传送空字符！",QMessageBox.Ok)
          elif 'group' in self.friend:
               for user in self.GroupMember_dict[self.friend]:
                    if user == self.account:
                         continue
                    data = SetData('GROUP',self.account,user,self.MsgInputBox.toPlainText())
                    data['GROUPNAME'] = self.friend
                    self.SendMsg_thread.MsgWaitingList.append(data)
               self.MsgList[self.Account_dict[self.friend]].append(data)
               self.MsgShowBox.append("*****"+data['source']+"("+data['time']+"):\n"+data['data']+'\n')
               self.MsgInputBox.setText("")
               self.SendMsg_thread.offline.connect(self.UserOffline)
               self.SendMsg_thread.fail.connect(self.NetError)
          else:
               data = SetData('Msg', self.account, self.friend, self.MsgInputBox.toPlainText())
               self.MsgList[self.Account_dict[self.friend]].append(data)
               self.SendMsg_thread.MsgWaitingList.append(data)
               self.MsgShowBox.append("*****"+data['source']+"("+data['time']+"):\n"+data['data']+'\n')
               self.MsgInputBox.setText("")
               self.SendMsg_thread.offline.connect(self.UserOffline)
               self.SendMsg_thread.fail.connect(self.NetError)
     def MsgReceive(self, data):
          if data['source'] != data['target']:
               self.MsgList[self.Account_dict[data['source']]].append(data)
               if self.friend == data['source']:
                    self.MsgShowBox.append(data['source']+"("+data['time']+"):\n"+data['data']+'\n')
               else:
                    self.FriendList[self.Account_dict[data['source']]] = data['source'] + '(new)'         
                    self.listModel.setStringList(self.FriendList)
                    self.FriendListView.setModel(self.listModel)
     def ChooseFile(self):
          fileName_choose = QFileDialog.getOpenFileName(self,"选取文件",'./',"All Files (*)")
          if fileName_choose[0] != '':
               data = SetData('FILE',self.account,self.friend,fileName_choose[0])
               self.MsgList[self.Account_dict[self.friend]].append(data)
               self.SendMsg_thread.MsgWaitingList.append(data)
               self.MsgShowBox.append("*****"+data['source']+"("+data['time']+"):\n发送了文件（"+data['data'].split('/')[-1]+'）\n')
               self.SendMsg_thread.offline.connect(self.UserOffline)
               self.SendMsg_thread.fail.connect(self.NetError)
     def FileReceive(self, data):
          if data['source'] != data['target']:
               self.MsgList[self.Account_dict[data['source']]].append(data)
               if self.friend == data['source']:
                    self.MsgShowBox.append(data['source']+"("+data['time']+"):\n发送了文件（"+data['data'].split('/')[-1]+'）\n')
               else:
                    self.FriendList[self.Account_dict[data['source']]] = data['source'] + '(new)'         
                    self.listModel.setStringList(self.FriendList)
                    self.FriendListView.setModel(self.listModel)
     def GroupDialogShow(self):
          self.groupSendDialog = GroupSendDialog()
          self.groupSendDialog.FriendList = copy.deepcopy(self.FriendList)
          deleteList = [self.account,]
          for i,user in enumerate(self.groupSendDialog.FriendList):
               if 'new' in user:
                    self.groupSendDialog.FriendList[i] = user[0:-5]
                    user = user[0:-5]
               if 'group' in user:
                    deleteList.append(user)
          for user in deleteList:
               self.groupSendDialog.FriendList.remove(user)
          self.groupSendDialog.listModel.setStringList(self.groupSendDialog.FriendList)
          self.groupSendDialog.FriendListView.setModel(self.groupSendDialog.listModel)
          self.groupSendDialog.choose.connect(self.GroupCreate)
          self.groupSendDialog.show()
     def GroupCreate(self, chooselist):
          groupname = 'group('
          for user in chooselist:
               groupname = groupname + user + ','
          groupname += self.account
          groupname += ')'
          for user in chooselist:
               if user == self.account:
                    continue
               data = SetData('GROUP',self.account,user,'Group Create')
               data['GROUPNAME'] = groupname
               self.SendMsg_thread.MsgWaitingList.append(data)
               # self.MsgList[self.Account_dict[user]].append(data)
               # if user == self.friend:
               #      self.MsgShowBox.append("*****"+data['source']+"("+data['time']+"):\n"+data['data']+'\n')
          self.Account_dict[groupname] = len(self.FriendList)
          self.MsgList.append([])
          self.FriendList.append(groupname)
          self.listModel.setStringList(self.FriendList)
          self.FriendListView.setModel(self.listModel)
          self.GroupMember_dict[groupname] = chooselist
          self.groupSendDialog.choose.disconnect(self.GroupCreate)
     def GroupChatReceive(self,data):
          groupname = data['GROUPNAME']
          chooselist = groupname[6:-1].split(',')
          if data['data'] == 'Group Create':
               self.Account_dict[groupname] = len(self.FriendList)
               self.MsgList.append([])
               self.FriendList.append(groupname)
               self.listModel.setStringList(self.FriendList)
               self.FriendListView.setModel(self.listModel)
               self.GroupMember_dict[groupname] = chooselist
          else:
               self.MsgList[self.Account_dict[groupname]].append(data)
               if self.friend == groupname:
                    self.MsgShowBox.append(data['source']+"("+data['time']+"):\n"+data['data']+'\n')
               else:
                    self.FriendList[self.Account_dict[groupname]] = groupname + '(new)'         
                    self.listModel.setStringList(self.FriendList)
                    self.FriendListView.setModel(self.listModel)
     def VoiceCall(self):
          self.voicecall = VoiceCall(8000)
          self.voicecall.P2PSeverPort = 8003
          self.voicecall.VoiceServer.start()
          self.voicecall.RefuseButton.setVisible(False)
          self.voicecall.AcceptButton.setText("等待对方回应...")
          self.voicecall.AcceptButton.setEnabled(False)
          data = SetData('AUDIO',self.account,self.friend,gethostbyname(gethostname()))
          self.voicecall.UserNameLabel.setText(self.friend)
          self.voicecall.SendCallRequest(data)
          self.voicecall.show()
     def UserOffline(self,data):
          # 用户不在线的槽函数，通知目标用户不在线
          if data['type'] == 'Msg':
               QMessageBox.warning(self,"DAChat","该用户（"+self.account+"）当前不在线，请稍后重试",QMessageBox.Ok)
               self.SendMsg_thread.p2pclient.quit()
               # self.SendMsg_thread.p2pclient.wait()
               self.SendMsg_thread.offline.disconnect(self.UserOffline)
               self.SendMsg_thread.fail.disconnect(self.NetError)
     def NetError(self, data):
          # 发送失败的槽函数，提示可能因为网络问题导致发送失败
          if data['type'] == 'Msg':
               QMessageBox.warning(self,"DAChat","网络出现问题，请稍后重试",QMessageBox.Ok)
               self.SendMsg_thread.p2pclient.quit()
               # self.SendMsg_thread.p2pclient.wait()
               self.SendMsg_thread.offline.disconnect(self.UserOffline)
               self.SendMsg_thread.fail.disconnect(self.NetError)

def MainLogin(s):
     # 登入成功的槽函数，用来设置基本的界面（登入、主、交友申请界面）参数和显示主界面
     window.Username.setText("")
     window.Password.setText("")
     window.close()
     mainwindow.ResetUi()
     mainwindow.addfrienddialog.Account = s
     mainwindow.show()
     mainwindow.Account.setText("当前账号："+s)
     mainwindow.FriendList.append(s)
     mainwindow.listModel.setStringList(mainwindow.FriendList)
     mainwindow.FriendListView.setModel(mainwindow.listModel)
     mainwindow.Account_dict[s] = 0
     mainwindow.account = s
     mainwindow.p2pserver.P2PSeverPort = int(s[5:])
     mainwindow.p2pserver.start()

app = QtWidgets.QApplication(sys.argv)
window = mywindow()
mainwindow = MyMain()
window.sendaccount.connect(MainLogin)
mainwindow.end.connect(window.show)
window.show()
sys.exit(app.exec_())