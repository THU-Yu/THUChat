# 引入模块
from pyaudio import *
import wave

def play():
    # 用文本文件记录wave模块解码每一帧所产生的内容。注意这里不是保存为二进制文件
    
    chunk=1                                       # 指定WAV文件的大小
    wf=wave.open(r"output.wav",'rb')              # 打开WAV文件
    p=PyAudio()                                   # 初始化PyAudio模块
    print(wf.getnchannels())
    # 打开一个数据流对象，解码而成的帧将直接通过它播放出来，我们就能听到声音啦
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=1, rate=wf.getframerate(), output=True)
 
    data = wf.readframes(chunk)      # 读取第一帧数据
    print(wf.getnchannels())# 以文本形式打印出第一帧数据，实际上是转义之后的十六进制字符串
    # 播放音频，并使用while循环继续读取并播放后面的帧数
    # 结束的标志为wave模块读到了空的帧
    while data != b'':   
        stream.write(data)                # 将帧写入数据流对象中，以此播放之
        data = wf.readframes(chunk)            # 继续读取后面的帧
        
    stream.stop_stream()            # 停止数据流
    stream.close()                        # 关闭数据流
    p.terminate()                          # 关闭 PyAudio
    print('play函数结束！')

play()