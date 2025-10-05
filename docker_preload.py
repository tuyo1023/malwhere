#!/usr/bin/env python3
"""
Docker イメージのプリロードスクリプト
ゲーム開始前にベースイメージをビルドして起動時間を短縮する
"""

import docker
import json
from docker_handle import build_container

def preload_all_containers():
    """
    すべての異常パターンのコンテナを事前ビルドする
    """
    # 設定ファイルを読み込み
    with open("mal_shell.json", "r") as f:
        mal_dict = json.load(f)
    
    # 各スクリプト用のコンテナを事前ビルド
    for script_name in mal_dict.keys():
        try:
            build_container(script_name)
        except Exception as e:
            pass

def cleanup_unused_images():
    """
    使用されていないDockerイメージをクリーンアップ
    """
    cli = docker.from_env()
    
    # 未使用イメージを削除
    cli.images.prune(filters={'dangling': True})
    
    # 未使用コンテナを削除
    cli.containers.prune()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        cleanup_unused_images()
    else:
        preload_all_containers()
