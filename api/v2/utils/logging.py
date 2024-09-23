import logging

# ロガーの設定
logger = logging.getLogger("futarin-api")
logger.setLevel(logging.DEBUG)


# コンソール出力の設定
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# フォーマットの設定
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# ハンドラの設定
logger.addHandler(console_handler)


# 他のモジュールで使うための公開用ロガー
def get_logger():
    return logger
