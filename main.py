import random
import subprocess
import json
import docker

class GameManager:
    def __init__(self, clear_threshold=8):
        """状態を初期化"""
        self.correct_count = 0
        self.solved_ids = []
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
        self.solved_ids.append(docker_id)
        print(self.solved_ids)
 
    def reset(self):
        """不正解時にスコアと保存済みIDをリセット"""
        self.correct_count = 0

def main():

    while True:
        gm = GameManager()
        start_or_end = choice_start_or_end()
        if start_or_end == 0:
            break

        print("ゲームスタート")
        num_of_collect = 0
        while True:
            docker_file_id = choice_docker_file()
            build_container(docker_file_id)
            exist_anomaly = boot_docker(docker_file_id)
            ans = gm.input_ans()

            if exist_anomaly == ans:
                num_of_collect += 1
                gm.save_dockerfile_id(docker_file_id)
            else:
                num_of_collect = 0
            
            if num_of_collect >= 8:
                print("clear")
                return
            
            while True:
                cin = input("continue?[y/n]")
                if cin == "y" or cin == "Y":
                    break
                elif cin == "n" or cin == "N":
                    return
                else:
                    print("もう一度入力してください")


def create_Dockerfile(script):
    with open("Dockerfile_orig", "r") as f:
        Dockerfile_text = f.read()
    
    with open("Dockerfile", "w") as f:
        f.write(Dockerfile_text.format("scripts/init.sh", "scripts/" + script))

def build_container(script):
    '''
    scriptのファイルを埋め込んだDockerファイルからイメージをビルドする
    ビルドしたimageの名前はmal8
    '''
    create_Dockerfile(script)
    cli = docker.from_env()
    images = cli.images.build(path="./", tag="mal8")
    # 中間コンテナ等を削除
    cli.containers.prune()
    cli.images.prune()

def choice_start_or_end():
    while True:
        soe = input("スタートしますか[y/N]")
        if soe == "" or soe == "n" or soe == "N":
            return 0
        elif soe == "y" or soe == "Y":
            return 1
        else:
            print("もう一度入力してください")

def choice_docker_file():
    """
    dockerfile のリストからランダムに選ぶ
    異変あり:異変なし = 7:3
    """
    with open("mal_shell.json", "r") as f:
        mal_dict = json.load(f)
    DOCKERFILES = []
    for file_name, mal in mal_dict.items():
        DOCKERFILES.append((file_name, mal))
    # 「異変あり」と「異変なし」でリストを分ける
    normal = [df for df in DOCKERFILES if df[1] == 0]
    anomaly = [df for df in DOCKERFILES if df[1] == 1]

    # 7:3 の割合でまずグループを選ぶ
    group = random.choices(
        population=[anomaly, normal],
        weights=[0.7, 0.3],
        k=1
    )[0]

    # 選んだグループからランダムに 1 つ選ぶ
    dockerfile_id, _ = random.choice(group)
    return dockerfile_id


def boot_docker(docker_id):
    """
    docker_id に応じてコンテナを起動する
    最大1時間で強制終了
    成功時 or タイムアウト時: docker_id の has_anomaly を返す
    エラー時のみ: None を返す
    """
    with open("mal_shell.json", "r") as f:
        mal_dict = json.load(f)
    DOCKERFILES = []
    for file_name, mal in mal_dict.items():
        DOCKERFILES.append((file_name, mal))
    # 「異変あり」と「異変なし」でリストを分ける
    normal = [df for df in DOCKERFILES if df[1] == 0]
    anomaly = [df for df in DOCKERFILES if df[1] == 1]

    try:
        subprocess.run(
            ["docker", "run", "-it", "--rm", "mal8"],
            check=True,
            timeout=3600   # 1時間でタイムアウト
        )
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] exceeded 1 hour, terminating...")
        # タイムアウトしても has_anomaly を返す
        for df_id, has_anomaly in DOCKERFILES:
            if df_id == docker_id:
                return has_anomaly
        return None
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Docker {docker_id} failed: {e}")
        return None

    # 正常終了した場合 → has_anomaly を返す
    for df_id, has_anomaly in DOCKERFILES:
        if df_id == docker_id:
            return has_anomaly

    return None


def input_ans():
    raise NotImplementedError


def save_dockerfile_id():
    raise NotImplementedError

if __name__ == "__main__":
    main()