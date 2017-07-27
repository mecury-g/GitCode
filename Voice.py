#coding=utf-8
#导入模块
import sys
import json
import time
import base64
import urllib
import urllib2
import requests
import os
import pyaudio
import wave

class Voice():
	def __init__(self,cuid,api_key,api_secret):
		self.cuid = cuid
		self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
		self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
		self.upvoice_url = 'http://vop.baidu.com/server_api'
		self.get_token(api_key,api_secret)
	def get_token(self,api_key,api_secret):
		token_url = self.token_url%(api_key,api_secret)
		r_str = urllib2.urlopen(token_url).read()
		token_data = json.loads(r_str)
		self.token_str = token_data['access_token']
	#语音合成
	def text2audio(self,text,filename):
		get_url=self.getvoice_url%(urllib2.quote(text),self.cuid,self.token_str)
		voice_data=urllib2.urlopen(get_url).read()
		voice_f=open(filename,'wb+')
		voice_f.write(voice_data)
		voice_f.close()
	#语音识别
	def audio2text(self,filename):
		#参数设置
		data = {}
		data['format'] = 'wav'
		data['rate'] = 8000
		data['channel'] = 1
		data['cuid'] = self.cu_id
		data['token'] = self.token_str
		#转换格式
		os.system('ffmpeg -i '+filename+' -ac 1 -ar 8000 -vn '+filename)
		#读取文件
		wav_fp = open(filename,'rb')
		voice_data = wav_fp.read()
		data['len'] = len(voice_data)
		#data['speech'] = base64.b64encode(voice_data).decode('utf-8')
		data['speech'] = base64.b64encode(voice_data).replace('\n', '')
		#post_data = json.dumps(data)
		result = requests.post('http://vop.baidu.com/server_api', json=data, headers={'Content-Type': 'application/json'})
		data_result = result.json()
		return data_result['result'][0]
	def audioRecode(self,filename,time=5):
		#设置相关参数
		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 1
		RATE = 8000
		RECORD_SECONDS = time
		WAVE_OUTPUT_FILENAME = filename
		#创建对象
		p = pyaudio.PyAudio()
		#打开数据流开始录音
		stream = p.open(format=FORMAT,
		                channels=CHANNELS,
		                rate=RATE,
		                input=True,
		                frames_per_buffer=CHUNK)

		print("* recording")
		#把音频数据写入list
		frames = []
		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		    data = stream.read(CHUNK)
		    frames.append(data)

		#录制完毕
		print("* done recording")
		#关闭stream
		stream.stop_stream()
		stream.close()
		p.terminate()
		#list内容写入文件
		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()


