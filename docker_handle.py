import os
import json
import random
import subprocess
import docker

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
    
    # ビルドキャッシュを活用し、--no-cacheを使わない
    images = cli.images.build(
        path="./", 
        tag="mal8",
        quiet=True,  # ビルドログを非表示
        forcerm=True,  # 中間コンテナを自動削除
        pull=False     # ベースイメージを毎回プルしない
    )
    
    # プルーニングは頻繁に行わない（リソース消費を減らすため）
    # cli.containers.prune()
    # cli.images.prune()

def boot_docker(docker_id):
    """
    docker_id に応じてコンテナを起動する
    最大30分で強制終了（1時間は長すぎる）
    成功時 or タイムアウト時: docker_id の has_anomaly を返す
    エラー時のみ: None を返す
    """
    with open("mal_shell.json", "r") as f:
        mal_dict = json.load(f)
    
    try:
        # タイムアウトを30分に短縮
        subprocess.run(
            ["docker", "run", "-it", "--rm", "mal8"],
            check=True,
            timeout=1800   # 30分でタイムアウト
        )
    except subprocess.TimeoutExpired:
        # タイムアウトしても has_anomaly を返す
        return mal_dict.get(docker_id, None)
    except subprocess.CalledProcessError as e:
        return None
    except KeyboardInterrupt:
        return mal_dict.get(docker_id, None)

    # 正常終了した場合 → has_anomaly を返す
    return mal_dict.get(docker_id, None)