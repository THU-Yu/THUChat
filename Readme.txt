Platform: Window10
Version: 1.0.0
Author: Chen YuHong
********************************************************************
Section I: Project introduction

This is a chatting app using CS tech and P2P tech. It is a homework of computure network in Tsinghua University.
This project need a TCP server to deal with users requests(inculding login, logout, find friend). This server is provided by the teacher assistant of the class. If you want to use this project, you need to use Tsinghua WiFi and make sure the TCP server is open. 

*********************************************************************
Section II: Dependency

Python3.7 is needed.
Install necessary modules using pip:

$pip3 install pyqt5
$pip3 install pyaudio
$pip3 install json

If something wrong when installing pyaudio, go to https://www.lfd.uci.edu/~gohlke/pythonlibs/ 
and download the .whl file. Move to the path that include the whl file, and input the following command:

$ pip3 install yourpath\whlfilename.whl

Then you can import pyaudio successfully.

*********************************************************************
Section III: Introdution of folders and files

1.Introduction of each python scripts:
	(1)Python scripts for testing pyaudio modules
	----pyaudiotest.py: running this script can test whether your microphone is ok.(This script is copied from https://www.jianshu.com/p/ba82e90ce706)
	----pyaudioplay.py: running this script can test whether your loudspeaker or earphone is ok.(This script is copied from https://www.jb51.net/article/163992.htm)
	(2)Python scripts for UI(In folder Ui File):
	----Ui_Welcome.py: this ui is for login.
	----Ui_Main.py: this is main window for DAChat.
	----Ui_AddFriendDialog.py: when you want to answer friend request, you will see this dialog.
	----Ui_GroupSendDialog.py: when you want to create a group chat, you will see this dialog.
	----Ui_VoiceCall.py: this dialog show when you are calling your friend only with audio.
	(3)Python scripts for DAChat:
	----DAChat.py: if you have install all module needed, run this script and you can use DAChat to chat with your friend.
2.Introduction of folder:
	----folder data: "Don't" delete this folder, all file you received will save in this folder. If you delete it, there will be bugs when you running DAChat.
	----folder resources: "Don't" delete this folder, this folder save all icon used on UI.
	----folder Ui File: All Ui file is placed in this folder.
3.Introduction of *.ui:
All *.ui files are made by Qt designer. You can check the details of each UI in Qt designer.

*********************************************************************
Section IV: How to use

If you install all necessary modules, click DAChat.py to use DAChat.

What you can do in DAChat?
1.Login and Logout.
2.Confirm friends are online, and add friends: input friend's account and click the right button(“查询好友”), then the server will inform you whether he/she is online.
3.Answer friend requests: click the button with icon(Add Friend) at the left bottom side, then you can answer the friend request.
4.Chat with your friend: choose who you want to chat with in your friend list, then input what you want to send in the right bottom textbox and click the button with icon(Send Msg).
5.Send files to your friend: choose who you want to send to in your friend list, then click the button with icon(File) and choose what file yo want to send.
6.Group chat: click the button with icon(Group) at the left bottom side, then you can choose who you want to add to the group. Choose the group in your friend list, then you can send Msg to all group members.
7.Voice call: choose who you want to call to in your friend list and click the button with icon(Voice Call). After your friend accept your voice call request, you can chat with your friend by voice call.

*********************************************************************
中文版Readme：
第一部分：项目介绍

这是一个基于CS架构和P2P架构设计的聊天程序，是清华大学计算机网络课程的作业。
这个项目需要一个TCP服务器协助进行用户登入、登出和查找朋友的功能，而这个服务器由课程助教提供并维护，如果想要使用此程序，需要确保使用的是Tsinghua WiFi且服务器是开启的。

*********************************************************************
第二部分：依赖项

程序运行环境为Python3.7，除此之外还需要安装相应的模块，可以使用pip命令安装：

$pip3 install pyqt5
$pip3 install pyaudio
$pip3 install json

在安装pyaudio模块时，如果发生错误，可以到https://www.lfd.uci.edu/~gohlke/pythonlibs/ 下载whl文件。下载后移动到相应目录，并输入以下命令进行安装：

$ pip3 install 你的目录\whl文件名.whl

安装完成后就可以正常使用pyaudio模块了。

*********************************************************************
第三部分：文件夹和文件的介绍

1.Python脚本介绍：
	（1）测试pyaudio模块的脚本
	----pyaudiotest.py：执行此脚本可以测试电脑麦克风是否可以正常使用。（这部分代码截取自https://www.jianshu.com/p/ba82e90ce706）
	----pyaduioplay.py：执行此脚本可以测试电脑耳机或喇叭是否可以正常使用。(这部分代码截取自https://www.jb51.net/article/163992.htm)
	（2）UI界面脚本（在Ui File文件夹中）：
	----Ui_Welcome.py：登入界面的脚本。
	---Ui_Main.py：主界面的脚本。
	----Ui_AddFriendDialog.py：确认好友申请的界面。
	----Ui_GroupSendDialog.py：创建群组的界面。
	----Ui_VoiceCall.py：语音聊天的界面。
	（3）DAChat的脚本：
	----DAChat.py：如果你安装了所有的依赖模块，运行此脚本就可以使用DAChat和其他人聊天了。
2.文件夹介绍：
	----data文件夹：请不要删除此文件夹，所有你收到的文件将保存在此文件夹中。如果删除了此文件夹，程序将会出现问题。
	----resources文件夹：请不要删除此文件夹，这个资料夹里保存了界面所需要的icon文件。
	----Ui File文件夹：所有的Ui文件都放在这个资料夹中。
3.ui文件介绍：
所有的ui文件都是由Qt designer设计而成，可以使用Qt designer查看各个ui界面的设计。

*********************************************************************
第四部分：如何使用

如果你已经安装了所有需要的模块，点击DAChat.py可以运行DAChat。

你可以使用DAChat干什么？
1.登入和登出。
2.确认好友是否在线，并加好友：输入好友账户并点击“查询好友”的按钮，服务器会通知你好友的在线情况。
3.回复好友申请：点击加好友图标的按钮（左下角），可以打开确认好友申请界面进行回复。
4.和好友聊天：在好友列表中选择想要聊天的对象，在输入框输入想发送的信息，点击传送信息图标的按钮发送信息。
5.传送文件给好友：在好友列表选择想要发送的对象，点击文件图标的按钮选择文件以发送。
6.群聊：点击左下角发起群聊图标的按钮，可以选择要邀请群聊的好友。在好友列表中选择群组，输入想要发送的信息，点击传送信息图标的按钮发送信息。
7.语音通话：在好友列表选择想要通话的对象，点击语音图标的按钮。当对方同意后，你们就可以开始进行语音通话了。