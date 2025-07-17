#!/usr/bin/env python3
import argparse
import json
import pathlib
import signal
import sys
from urllib.parse import urlparse

from utils.loader import get_plugins, load_plugin
from utils.paths import MAIN_DIR
from utils.request_module import requestTimeout
import utils.CDNEngine as CDNEngine  # чтобы подменить поведение find

def graceful_exit(sig, frame):
    sys.exit(0)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--target", required=True, type=str,
                   help="URL или домен для сканирования")
    p.add_argument("--output", required=True, type=str,
                   help="Путь к JSON-файлу для записи результатов")
    return p.parse_args()

def sanitize_url(hostname: str) -> str:
    c = urlparse(hostname)
    return hostname if c.scheme else "http://" + hostname

if __name__ == "__main__":
    args = parse_args()
    target: str = args.target
    output_path: pathlib.Path = MAIN_DIR / args.output

    # Подготовка: таймауты и прерывания
    signal.signal(signal.SIGALRM, requestTimeout)
    signal.signal(signal.SIGINT, graceful_exit)

    hostname = sanitize_url(target)
    found = []

    # Подменяем функцию поиска, чтобы накапливать результаты
    def record_find(data: str):
        for keyword, description in CDNEngine.CDN.items():
            if keyword.lower() in data:
                found.append(description)

    CDNEngine.find = record_find

    # Запускаем все плагины
    signal.alarm(5)
    for name in get_plugins():
        plugin = load_plugin(name)
        plugin.detect(hostname)

    # Отключаем сигнал
    signal.alarm(0)

    # Если ничего не нашли — помечаем
    if not found:
        found = ["No CDN found"]

    # Гарантируем, что директория существует
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Записываем в JSON
    with open(output_path, "w", encoding="utf-8") as jf:
        json.dump(found, jf, ensure_ascii=False, indent=2)

    print(f"Results saved to {output_path}")
