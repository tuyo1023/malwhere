class GameManager:
    def __init__(self, clear_threshold=8):
        """状態を初期化"""
        self.correct_count = 0
        self.solved_ids = set()
        self.clear_threshold = clear_threshold
 
    def input_ans(self) -> int:
        """プレイヤーから回答の入力を受け付ける
        あると答えた場合は1、ないと答えた場合は0
        """
        while True:
            ans = input("異変がある？ (y/n): ").lower()
            if ans == 'y':
                return 1
            elif ans == 'n':
                return 0
            else:
                print("yかnで入力してください")
 
    def save_dockerfile_id(self, docker_id: str):
        """正解したときにIDを保存"""
        self.correct_count += 1
        self.solved_ids.add(docker_id)
 
    def reset(self):
        """不正解時にスコアと保存済みIDをリセット"""
        self.correct_count = 0