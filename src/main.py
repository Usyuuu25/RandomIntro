import pygame
from mutagen.mp3 import MP3 as mp3
# flet用インポート
import flet as ft

from pathlib import Path    #filePath情報取得用
from state import State
import os
import random

# 画像を更新するためのインポート
from PIL import Image as image
import numpy as np
import base64
from io import BytesIO
from flet import Image

# state.py用
MusicInfo       = State()

# コンポーネント化するにはflet.UserControlクラスを継承し、buildメソッドでControlインスタンスを返す            
# 2列目
class IntroQuizParts_1(ft.UserControl):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.MusicPath                  = ft.Text()
        self.StartTime                  = ft.TextField(value=0.0,label="StartTime",width=125)
        self.EndTime                    = ft.TextField(value=1.0,label="EndTime",width=125)
        self.StartTime.on_change        = MusicInfo.set_StartMusicTimeInfo(self.StartTime.value)
        self.EndTime.on_change          = MusicInfo.set_EndMusicTimeInfo(self.EndTime.value)
        self.Alert                      = ft.AlertDialog( title=ft.Text("終了時間を開始時間より後にして下さい"),
                                                          on_dismiss=lambda e: print("Dialog dismissed!")
                                                        )

    # イントロ再生ボタンの機能関数
    def Start_Intro_Music_Button(self,e):
        # 選択中の音楽ファイルまでのPATH
        self.MusicPath                  = os.path.join(MusicInfo.get_MusicFilePath(),MusicInfo.get_MusicFileName())

        # 終了時間 <= 開始時間だった場合、アラート画面を表示
        if  float(self.EndTime.value) <= float(self.StartTime.value):
            self.dialog     = self.Alert
            self.Alert.open = True
            self.update()
        else:
            pygame.mixer.music.load(self.MusicPath)            # 音楽ファイルの読み込み
            pygame.mixer.music.set_volume(float(MusicInfo.get_MusicVolume() /100))
            # 指定した開始時間から再生
            pygame.mixer.music.play(start=float(self.StartTime.value))

            # 再生が終了するまで待機
            pygame.time.wait(int((float(self.EndTime.value) - float(self.StartTime.value))*1000))  # ミリ秒単位で待機

            # 再生停止
            pygame.mixer.music.stop()

    def build(self):
        return  ft.Row([ft.IconButton(icon=ft.icons.NOT_STARTED_OUTLINED,
                                      icon_size=50,
                                      on_click=self.Start_Intro_Music_Button,
                                      tooltip="START Intro Music"),
                        self.StartTime,
                        ft.Text(value="～"),
                        self.EndTime,
                        ],
                        width=600, height=100, spacing=50)  

# 3列目
class IntroQuizParts_2(ft.UserControl):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.MusicVolume_Stock  = 0
        self.MusicPath          = ft.Text()
        self.VolumeIconButton   = ft.IconButton(icon=ft.icons.VOLUME_UP,
                                                selected_icon=ft.icons.VOLUME_OFF,
                                                selected=False,
                                                icon_size=50,
                                                on_click=self.Volume_Icon)
        self.FullMusic_Button   = ft.IconButton(icon=ft.icons.START,icon_size=50,
                                               selected_icon=ft.icons.PAUSE_CIRCLE_OUTLINED,
                                               on_click=self.Start_FullMusic_Button,
                                               selected=False,
                                               tooltip="START/PAUSE Full Music")
        self.row =   ft.Row([self.FullMusic_Button,
                            # STOP Music   
                             ft.IconButton(icon=ft.icons.STOP_CIRCLE_OUTLINED,
                                           icon_size=50,
                                           on_click=self.STOP_Music_Button,
                                           tooltip="Stop Music"),
                            ft.Slider(min=0,
                                    max=100,
                                    divisions=100,
                                    label="{value}",
                                    value=MusicInfo.get_MusicVolume(),
                                    width=300,
                                    on_change=self.Edit_Music_Volume,
                                    ),
                            self.VolumeIconButton
                            ],
                            width=600, height=100, spacing=10)

    def Start_FullMusic_Button(self,e):
        # 選択中の音楽ファイルまでのPATH
        self.MusicPath          = os.path.join(MusicInfo.get_MusicFilePath(),MusicInfo.get_MusicFileName())
        self.PauseFlag          = MusicInfo.get_PauseFlag()

        if e.control.selected == False:
            if self.PauseFlag   == 0:
                MusicInfo.set_PauseFlag(1)                      # pause flag
                pygame.mixer.music.load(self.MusicPath)         # 音楽ファイルの読み込み
                pygame.mixer.music.set_volume(float(MusicInfo.get_MusicVolume() /100))
                pygame.mixer.music.play(1)                      # 音楽の再生回数(1回)
            else:
                pygame.mixer.music.set_volume(float(MusicInfo.get_MusicVolume() /100))
                pygame.mixer.music.unpause()

        else:
            pygame.mixer.music.pause()

        e.control.selected = not e.control.selected
        e.control.update()

    def STOP_Music_Button(self,e):
        MusicInfo.set_PauseFlag(0)
        pygame.mixer.music.stop()
        self.FullMusic_Button.selected   =False                 # StopしたらFull Musicボタンを再生前に戻す
        self.update()

    def Edit_Music_Volume(self,e):
        # ボリューム取得
        self.MusicVolume            = int(e.control.value)
        MusicInfo.set_MusicVolume(self.MusicVolume)
        pygame.mixer.music.set_volume(float(self.MusicVolume / 100))
        self.update()

    def Volume_Icon(self,e):
        if(MusicInfo.get_MusicVolume() != 0):
            self.MusicVolume_Stock  = MusicInfo.get_MusicVolume()
            MusicInfo.set_MusicVolume(0)
            pygame.mixer.music.set_volume(0)
        else:
            MusicInfo.set_MusicVolume(self.MusicVolume_Stock)
            pygame.mixer.music.set_volume(float(self.MusicVolume_Stock/100))
        e.control.selected         = not e.control.selected
        self.update()


    def build(self):
        return  self.row

# 4列目
class IntroQuizParts_3(ft.UserControl):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.SounfEffectName_OK = [i for i in os.listdir(MusicInfo.get_SoundEffectPath()) if 'OK' in i]
        self.SounfEffectPath_OK = os.path.join(MusicInfo.get_SoundEffectPath(),self.SounfEffectName_OK[0])
        self.SounfEffectName_NG = [i for i in os.listdir(MusicInfo.get_SoundEffectPath()) if 'NG' in i]
        self.SounfEffectPath_NG = os.path.join(MusicInfo.get_SoundEffectPath(),self.SounfEffectName_NG[0])

    def Start_OKSE_Button(self,e):
        pygame.mixer.music.load(self.SounfEffectPath_OK)
        pygame.mixer.music.play(1)                                 # 音楽の再生回数(1回)

    def Start_NGSE_Button(self,e):
        pygame.mixer.music.load(self.SounfEffectPath_NG)
        pygame.mixer.music.play(1)                                  # 音楽の再生回数(1回)

    def build(self):
        return  ft.Row([ft.FilledTonalButton("正解SE",on_click=self.Start_OKSE_Button,width=120, height=40),
                        ft.FilledTonalButton("不正解SE",on_click=self.Start_NGSE_Button,width=120, height=40)],
                        width=600, height=100, spacing=90)
   

# ----------------メイン処理--------------------
def main(page: ft.Page):
    # ---------ページレイアウト--------------
    page.title              = MusicInfo.get_MusicTitle()
    page.window_width       = 600
    page.window_height      = 900
    page.padding            = 20

    # ---------音楽関係--------------
    pygame.mixer.init()
    # 音楽ファイル群
    Musicfiles              = []
    # 音楽ファイルまでのフルPATH
    MusicPath               = ft.Text()
    # 選択中のファイル名
    MusicName               = ft.Text()
    mp3_length              = 0
    EndTime                 = ft.TextField()
    
    # ---------画像関係--------------
    image_path              = MusicInfo.get_InitialImageFileName()
    pil_photo               = image.open(image_path) # Pillow Opens the Image
    arr                     = np.asarray(pil_photo) # Numpy transforms it into an array

    pil_img                 = image.fromarray(arr) # Then you convert it in an image again
    buff                    = BytesIO() # Buffer
    pil_img.save(buff, format="png") # Save it


    AnswerText              = ft.Text(MusicInfo.get_MusicFileName(),size=50)
    image_string            = base64.b64encode(buff.getvalue()).decode('utf-8')
    Answer_Image            = Image(src_base64=image_string)
    
# ------------出題ボタンの挙動--------------
    # mp3とwavのみをリストアップする
    def list_wav_mp3_files(directory):
        wav_mp3_files = []
        for filename in os.listdir(directory):
            if filename.endswith(".wav") or filename.endswith(".mp3"):
                wav_mp3_files.append(filename)
        return wav_mp3_files
    
    # 指定名の画像ファイルを探索
    def find_matching_image(filename):
        matching_images = []
        for file in os.listdir(MusicInfo.get_MusicFilePath()):
            if file.lower().replace(".png", "").replace(".jpg", "").replace(".jpeg", "") == filename.lower():
                if file.lower().endswith('.png') or file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
                    matching_images.append(os.path.join(MusicInfo.get_MusicFilePath(), file))
        return matching_images

    # 出題ボタン押下時の挙動
    def Set_Question(e):
        # 音楽ファイル群とPATH取得
        MusicPath.value        = MusicInfo.get_MusicFilePath()
        Musicfiles             = list_wav_mp3_files(MusicPath.value)  # フォルダ内のファイル一覧を取得
        # 音楽ファイルがある場合
        if Musicfiles:
            # 前回取得したファイル名は除外
            # 除外したリスト
            Musicfiles = [item for item in Musicfiles if item != MusicName.value]
            # ランダムに音楽ファイルを取得
            MusicName.value    = random.choice(Musicfiles)  # ファイル一覧からランダムに1つ選択
            MusicName.size     = 30
            # ファイルPATHを取得
            MusicPath.value    = os.path.join(MusicPath.value,MusicName.value)
            # 音楽ファイルの長さを取得
            mp3_length         = mp3(MusicPath.value).info.length  # 音源の長さ取得
            # 音楽ファイルの長さをGUIに反映
            EndTime.value      = mp3_length

            # 音楽再生処理
            pygame.mixer.music.load(MusicPath.value)

            # 答えの初期化
            AnswerText.value    = ""
            Update_Image(MusicInfo.get_InitialImageFileName())

            # 音楽情報をState.pyに反映
            MusicInfo.set_MusicFileName(MusicName.value)
            MusicInfo.set_EndMusicTimeInfo(mp3_length)
            MusicInfo.set_ImageFileName(find_matching_image(MusicInfo.get_MusicFileName().replace(".wav", "").replace(".mp3", "")))
        # 更新情報反映
        page.update()

    # 答えの画像更新
    def Update_Image(ImageFilePath):
        pil_photo                   = image.open(ImageFilePath)
        pil_photo.thumbnail((300,300))                                  # Resize

        arr                         = np.asarray(pil_photo)
        pil_img                     = image.fromarray(arr)
        buff                        = BytesIO()
        pil_img.save(buff, format=pil_photo.format)

        newstring                   = base64.b64encode(buff.getvalue()).decode("utf-8")
        Answer_Image.src_base64     = newstring

    # ------------出題ボタン押下時の挙動--------------
    def Show_Answer(e):
        # 答えの名前更新
        AnswerText.value            = MusicName.value.replace(".wav", "").replace(".mp3", "")

        # 答えの画像更新
        Update_Image(MusicInfo.get_ImageFileName()[0])

        page.update()

    # ページビューを追加 
    page.add(
        ft.Row([ft.FilledButton("出題", on_click=Set_Question, icon="QUESTION_MARK"),
                MusicName
                ],
                width=600, height=100, spacing=50),
        IntroQuizParts_1(),
        IntroQuizParts_2(),
        # 境界
        ft.Divider(height=12, thickness=5),
        ft.Row([ft.FilledTonalButton("答え",on_click=Show_Answer, width=120, height=40),
                IntroQuizParts_3(),
                ],
                width=600, height=100, spacing=90),
        # 境界
        ft.Divider(height=12, thickness=5),
        # 答え
        ft.Column([ AnswerText,
                    Answer_Image],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    width=600,height = 300
                )
        )

if __name__ == "__main__":
    try:
        ft.app(target=main)

    # 強制終了した時の処理
    finally:
        pygame.mixer.music.stop()