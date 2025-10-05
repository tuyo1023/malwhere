FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    apache2 \
    openssh-server \
    vim \
    php \
    curl \
    cron \ 
    sl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# docker起動時のwarningを回避するための記述
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

COPY web/html_backup /var/www/html_backup
COPY web/index.php /var/www/html
# docker起動時にinit.shに記載されたシェルコマンドを実行
COPY scripts/init.sh /usr/local/bin/init.sh
COPY scripts/anomaly_0.sh /usr/local/bin/anomaly.sh
RUN chmod +x /usr/local/bin/init.sh /usr/local/bin/anomaly.sh
CMD ["/usr/local/bin/init.sh"]