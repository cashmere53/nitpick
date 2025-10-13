FROM python:3.13-slim

# Pythonのバッファリング無効化（ログの即時出力）
ENV PYTHONUNBUFFERED=1

# システムパッケージの更新とインストール
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ユーザー作成
RUN adduser --disabled-password --gecos '' melon
ENV HOME=/home/melon
WORKDIR ${HOME}

# まず依存関係定義ファイルのみコピー（キャッシュ効率化）
COPY --chown=melon:melon pyproject.toml README.md ./

# ユーザー切り替え
USER melon

# 依存関係のみ先にインストール（editable installを避けて依存関係のみ）
RUN python -m pip install --no-cache-dir --upgrade pip

# 残りのファイルをコピー
COPY --chown=melon:melon . .

# パッケージをインストール
RUN python -m pip install --no-cache-dir .

CMD ["python", "-m", "nitpick"]
