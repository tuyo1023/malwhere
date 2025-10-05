from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header, Static
from textual.containers import Container
from textual.screen import Screen
from textual.message import Message

from component import AnomalyDesc
from docker_handle import choice_docker_file, boot_docker, build_container

class DescriptionScreen(Screen):
    class Selected(Message):
        def __init__(self, src: str):
            self.src = src
            super().__init__()

    def __init__(self, src, anomaly_list, name = None, id = None, classes = None):
        self.src = src
        self.anomaly_list = anomaly_list
        super().__init__(name, id, classes)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(id="Descriptions")
        yield Button("戻る", id="back_title")
        yield Footer()

    def on_mount(self) -> None:
        for a in self.anomaly_list:
            new_button = AnomalyDesc(a[:-3])
            self.query_one("#Descriptions").mount(new_button)
    
    @on(Button.Pressed, "#back_title")
    def back_title(self) -> None:
        self.post_message(self.Selected(src=self.src))

class TitleScreen(Screen):

    class Selected(Message):
        def __init__(self, docker_file_id: str):
            self.docker_file_id = docker_file_id
            super().__init__()
    
    def __init__(self, name = None, id = None, classes = None):
        super().__init__(name, id, classes)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(f"現在の正解数: {0}")
        yield Button("ゲームスタート", id="game_start")
        yield Button("異変の説明を見る", id="description")
        yield Button("終了", id="quit")
        yield Footer()
    
    @on(Button.Pressed, "#game_start")
    def game_start(self) -> None:
        docker_file_id = choice_docker_file()
        build_container(docker_file_id)
        self.post_message(self.Selected(docker_file_id=docker_file_id))
    

class DetailScreen(Screen):

    class Selected(Message):
        def __init__(self) -> None:
            super().__init__()

    def __init__(self, anomaly: str, *args, **kwargs):
        self.anomaly = anomaly
        self.description_name = "./descriptions/" + self.anomaly + ".txt"
        super().__init__(*args, **kwargs)
    
    def __init__(self, data, name = None, id = None, classes = None):
        self.data = data
        super().__init__(name, id, classes)
    
    def compose(self):
        yield Header()
        yield Static(self.data)
        yield Button("戻る", id="description_back")
        yield Footer()
    
    @on(Button.Pressed, "#description_back")
    def back_description(self) -> None:
        self.post_message(self.Selected())
    

class AnswerScreen(Screen):
    class Selected(Message):
        def __init__(self, ans: str):
            self.ans = ans
            super().__init__()
    
    def compose(self):
        yield Header()
        yield Static("異変はある？")
        yield Button("ある", id="yes")
        yield Button("ない", id="no")
        yield Footer()
    
    @on(Button.Pressed, "#no")
    def answer_no(self) -> None:
        self.post_message(self.Selected(ans="no"))
    
    @on(Button.Pressed, "#yes")
    def answer_yes(self) -> None:
        self.post_message(self.Selected(ans="yes"))


class CountScreen(Screen):
    class Selected(Message):
        def __init__(self, data: str):
            self.data = data
            super().__init__()
    
    def __init__(self, num_of_count: int, name = None, id = None, classes = None):
        self.num_of_count = num_of_count
        super().__init__(name, id, classes)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(f"現在の正解数: {self.num_of_count}")
        if self.num_of_count >= 8:
            yield Static("クリア！")
            yield Button("異変の説明を見る", id="description")
            yield Button("終了", id="quit")
        else:
            yield Button("次へ", id="next")
        yield Footer()
    
    @on(Button.Pressed, "#next")
    def back_title(self) -> None:
        self.post_message(self.Selected(data="next"))
    
    @on(Button.Pressed, "#quit")
    def quit(self) -> None:
        self.post_message(self.Selected(data="quit"))

    @on(Button.Pressed, "#description")
    def description(self) -> None:
        self.post_message(self.Selected(data="description"))

class YesScreen(Screen):
    def __init__(self, hoge: str, name = None, id = None, classes = None):
        self.hoge = hoge
        super().__init__(name, id, classes)
    
    def compose(self):
        yield Header()
        yield Static(f"{self.hoge}")
        yield Footer()

class BaseScreen(Screen):
    def compose(self):
        return super().compose()
    