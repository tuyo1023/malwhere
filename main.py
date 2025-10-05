import random
import subprocess
import json
import docker
import os

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header, Static
from textual.containers import Container
from textual.screen import Screen
from textual.message import Message

from Gamemanager import GameManager
from screen import *
from docker_handle import boot_docker

anomaly_list = set(["anomaly_0", "anomaly_1"])


class MalWhere(App[None]):
    CSS_PATH = "style.tcss"
    def __init__(self, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        self.game_manager = GameManager()
        self.first = True
        self.has_anomaly = False
        super().__init__(driver_class, css_path, watch_css, ansi_color)
    
    def compose(self) -> ComposeResult:
        yield Header()
        # yield Static(f"現在の正解数: {self.game_manager.correct_count}")
        yield Button("ゲームスタート", id="game_start")
        yield Button("異変の説明を見る", id="description")
        yield Button("終了", id="quit")
        yield Footer()

    @on(Button.Pressed, "#game_start")
    def game_start(self) -> None:
        if self.first:
            self.docker_file_id = "anomary_0.sh"
            self.first = False
        else:
            self.docker_file_id = choice_docker_file()
            build_container(self.docker_file_id)

        with self.suspend(): 
            os.system("clear")
            self.has_anomaly = boot_docker(self.docker_file_id)
        
        self.push_screen(AnswerScreen())
    
    @on(Button.Pressed, "#description")
    def switch_description(self) -> None:
        self.push_screen(DescriptionScreen(src="title", anomaly_list=self.game_manager.solved_ids))

    @on(Button.Pressed, "#quit")
    def quit(self) -> None:
        self.exit()

    def on_detail_screen_selected(self) -> None:
        self.pop_screen()
    
    def on_anomaly_desc_selected(self, message: AnomalyDesc.Selected) -> None:
        file_name = message.file_name
        with open(file_name, "r") as f:
            file_data = f.read()
        self.push_screen(DetailScreen(file_data))
    
    def on_description_screen_selected(self, message: DescriptionScreen.Selected) -> None:
        if message.src == "count":
            self.pop_screen()
        self.pop_screen()
    
    def on_title_screen_selected(self, message: TitleScreen.Selected) -> None:
        with self.suspend(): 
            os.system("clear")
            self.docker_file_id = message.docker_file_id
            self.has_anomaly = boot_docker(self.docker_file_id)
        
        self.push_screen(AnswerScreen())
    
    def on_answer_screen_selected(self, message: AnswerScreen.Selected) -> None:
        ans = message.ans
        if ans == "yes":
            ans_num = 1
        else:
            ans_num = 0
        
        if self.has_anomaly == ans_num:
            self.game_manager.save_dockerfile_id(self.docker_file_id)
        else:
            self.game_manager.reset()
    
        
        self.push_screen(CountScreen(self.game_manager.correct_count))
    
    def on_count_screen_selected(self, message: CountScreen.Selected) -> None:
        data = message.data
        if data == "next":
            self.pop_screen()
            self.pop_screen()
        elif data == "description":
            self.push_screen(DescriptionScreen(src="count", anomaly_list=self.game_manager.solved_ids))
        else:
            self.exit()

if __name__ == "__main__":
    print("ベース環境をビルドします")
    build_container("anomaly_0.sh")
    app = MalWhere()
    app.run()