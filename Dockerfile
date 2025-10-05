FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# パッケージリストを更新し、必要なパッケージを一括インストール
# キャッシュレイヤーを効率化
RUN apt-get update && apt-get install -y \
    apache2 \
    openssh-server \
    vim \
    php \
    curl \
    cron \
    sl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "ServerName localhost" >> /etc/apache2/apache2.conf

# ファイルコピーを最後に行い、キャッシュ効率を向上
COPY web/html_backup /var/www/html_backup
COPY web/index.php /var/www/html

# スクリプトファイルを最後にコピー（変更が最も頻繁な部分）
COPY scripts/init.sh /usr/local/bin/init.sh
COPY scripts/anomaly_sl.sh /usr/local/bin/anomaly.sh
RUN chmod +x /usr/local/bin/init.sh /usr/local/bin/anomaly.sh

CMD ["/usr/local/bin/init.sh"]