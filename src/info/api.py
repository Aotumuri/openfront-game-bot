import os


def get_bot_name() -> str:
    name = os.getenv("OPENFRONT_BOT_NAME")
    if not name:
        raise RuntimeError("OPENFRONT_BOT_NAME is not set")
    return name


def get_bot_author() -> str:
    author = os.getenv("OPENFRONT_BOT_AUTHOR")
    if not author:
        raise RuntimeError("OPENFRONT_BOT_AUTHOR is not set")
    return author


def get_git_url() -> str:
    url = os.getenv("OPENFRONT_BOT_GIT_URL")
    if not url:
        raise RuntimeError("OPENFRONT_BOT_GIT_URL is not set")
    return url
