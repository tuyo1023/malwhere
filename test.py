from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Header, Footer

# 1列あたりのボタンの最大数を定数として定義
BUTTONS_PER_COLUMN = 5

class DynamicLayoutApp(App):
    CSS_PATH = "hoge.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        # 列(Vertical)を横に並べるためのコンテナ
        yield Horizontal(id="columns-container")
        yield Footer()

    def on_mount(self) -> None:
        """アプリ起動時"""
        self.button_count = 0
        # 最初の列を作成する
        self.add_new_column()
        """ボタンが押されたときの処理"""
        self.button_count += 1
        
        # すべての列を取得し、最後の列を対象にする
        columns = self.query(".column")
        last_column = columns.last()

        # 最後の列のボタン数が上限に達しているかチェック
        if len(last_column.children) >= BUTTONS_PER_COLUMN:
            # 上限に達していたら新しい列を作成
            last_column = self.add_new_column()

        # 新しいボタンを作成
        new_button = Button(f"Button {self.button_count}")
        
        # 最後の列にボタンを追加
        last_column.mount(new_button)
        new_button.scroll_visible()

    def add_new_column(self) -> Vertical:
        """新しい列(Verticalコンテナ)を作成して追加する"""
        new_column = Vertical(classes="column")
        self.query_one("#columns-container").mount(new_column)
        return new_column

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """ボタンが押されたときの処理"""
        self.button_count += 1
        
        # すべての列を取得し、最後の列を対象にする
        columns = self.query(".column")
        last_column = columns.last()

        # 最後の列のボタン数が上限に達しているかチェック
        if len(last_column.children) >= BUTTONS_PER_COLUMN:
            # 上限に達していたら新しい列を作成
            last_column = self.add_new_column()

        # 新しいボタンを作成
        new_button = Button(f"Button {self.button_count}")
        
        # 最後の列にボタンを追加
        await last_column.mount(new_button)
        new_button.scroll_visible()


if __name__ == "__main__":
    app = DynamicLayoutApp()
    app.run()