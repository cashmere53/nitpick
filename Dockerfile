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
COPY --chown=melon:melon pyproject.toml ./

# ユーザー切り替え
USER melon

# 依存関係のみ先にインストール
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir .

# 残りのファイルをコピー
COPY --chown=melon:melon . .

# 再インストール（既に依存関係は入っているので高速）
RUN python -m pip install --no-cache-dir .

CMD ["python", "-m", "nitpick"]
