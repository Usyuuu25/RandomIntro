from pathlib import Path    #filePath情報取得用
from typing import TypeVar, Generic, Union, Callable
import time
import os

T = TypeVar('T')

#状態管理クラス。bind()で状態変更時に呼び出したい処理を登録できる。
class State(Generic[T]):

    def __init__(self):
        self._MusicTitle                = "Random Intro Quiz"        #選択中の音楽ファイル名
        self._MusicVolume               = int(60)                    #音楽Volume
        self._VolumeIconInfo            = "ft.icons.VOLUME_UP"
        self._PauseFlag                 = 0
        self._StartTime                 = 0                          #再生開始時間
        self._EndTime                   = 0                          #再生終了時間
        self._observers: list[Callable] = []
        self._MusicFilePath             = Path.cwd() / '..' / 'IntroMusic'    #音楽ファイルのPATH情報
        self._MusicFileName             = None
        self._ImageFileName             = Path.cwd() / '..' / 'IntroMusic' /'Before_Quiz.png'
        self._SoundEffectPath           = Path.cwd() / '..' / 'Soundeffects'
        self._SoundEffectPath_OK        = '' 
        self._SoundEffectPath_NG        = ''         
        
    #   情報取得群
    def get_MusicTitle(self):
        return self._MusicTitle
    
    def get_MusicVolume(self):
        return self._MusicVolume
    
    def get_VolumeIconName(self, MusicVolume: T):
        if MusicVolume >50:
            self._VolumeIconInfo    = 'ft.icons.VOLUME_UP'
        elif 0< MusicVolume <= 50:
            self._VolumeIconInfo    = 'ft.icons.VOLUME_DOWN'
        else:
            self._VolumeIconInfo    = 'ft.icons.VOLUME_OFF'
        return self._VolumeIconInfo
    
    def get_PauseFlag(self):
        return self._PauseFlag
    
    def get_MusicFilePath(self):
        return self._MusicFilePath
    
    def get_MusicFileName(self):
        return self._MusicFileName
    
    def get_ImageFileName(self):
        return self._ImageFileName
    
    def get_InitialImageFileName(self):
        return (Path.cwd() / '..' / 'IntroMusic' /'Before_Quiz.png')
    
    # 開始時間を取得
    def get_Music_StartTime_Info(self):
        if self._StartTime == '':
            return 0  # もしくは適切なデフォルト値を返す
        else:
            return self._StartTime

    # 終了時間を取得
    def get_Music_EndTime_Info(self):
        if self._EndTime == '':
            return 0  # もしくは適切なデフォルト値を返す
        else:
            return self._EndTime     

    def get_SoundEffectPath(self):
        return self._SoundEffectPath

    def get_SoundEffectPath_OK(self):
        self._SounfEffectName_OK = [i for i in os.listdir(self._SoundEffectPath) if 'OK' in i]
        self._SoundEffectPath_OK = os.path.join(self._SoundEffectPath,self._SounfEffectName_OK[0])
        return self._SoundEffectPath_OK

    def get_SoundEffectPath_NG(self):
        self._SounfEffectName_NG = [i for i in os.listdir(self._SoundEffectPath) if 'NG' in i]
        self._SoundEffectPath_NG = os.path.join(self._SoundEffectPath,self._SounfEffectName_NG[0])
        return self._SoundEffectPath_NG

    #   情報設定群
    def set_MusicTitle(self, new_Title: T):
        if self._MusicTitle != new_Title:
            self._MusicTitle = new_Title
            for observer in self._observers: observer() #変更時に各observerに通知する

    def set_MusicVolume(self, new_Volume : T):
        if self._MusicVolume != new_Volume:
            self._MusicVolume = new_Volume
            for observer in self._observers: observer() #変更時に各observerに通知する

    def set_PauseFlag(self, new_Flag : T):
        if self._PauseFlag != new_Flag:
            self._PauseFlag = new_Flag
            for observer in self._observers: observer() #変更時に各observerに通知する
    
    def set_MusicFilePath(self, new_FilePath : T):
        if self._MusicFilePath != new_FilePath:
            self._MusicFilePath = new_FilePath
            for observer in self._observers: observer() #変更時に各observerに通知する

    def set_MusicFileName(self, new_FileName : T):
        if self._MusicFileName != new_FileName:
            self._MusicFileName = new_FileName
            for observer in self._observers: observer() #変更時に各observerに通知する

    def set_ImageFileName(self, new_ImageName : T):
        if self._ImageFileName != new_ImageName:
            self._ImageFileName = new_ImageName
            for observer in self._observers: observer() #変更時に各observerに通知する

    def set_StartMusicTimeInfo(self, new_StartTime : T):
        if self._StartTime != new_StartTime:
            self._StartTime = new_StartTime
            for observer in self._observers: observer() #変更時に各observerに通知する

    def set_EndMusicTimeInfo(self, new_EndTime : T):
        if self._EndTime != new_EndTime:
            self._EndTime = new_EndTime
            for observer in self._observers: observer() #変更時に各observerに通知する 

    def bind(self, observer):
        self._observers.append(observer)# 変更時に呼び出す為のリストに登録