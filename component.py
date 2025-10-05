from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header, Static
from textual.containers import Container
from textual.screen import Screen
from textual.message import Message


class AnomalyDesc(Static):

    class Selected(Message):
        def __init__(self, file_name: str) -> None:
            self.file_name = file_name
            super().__init__()

    def __init__(self, anomaly: str, *args, **kwargs):
        self.anomaly = anomaly
        self.description_name = "./descriptions/" + self.anomaly + ".txt"
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Button(self.anomaly, id=self.anomaly)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == self.anomaly:
            event.stop()
            self.post_message(self.Selected(file_name=self.description_name))