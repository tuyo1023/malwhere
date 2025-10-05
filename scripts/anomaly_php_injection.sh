#!/bin/bash
echo "Hello anomaly_php_injection"

PHP_FILE="/var/www/html/index.php"
SCRIPT="/var/www/html/anomaly.sh"

cat <<'EOS' > "$SCRIPT"
#!/bin/bash
colors=(31 32 33 34 35 36 37)

for i in $(seq 1 300); do
    color=${colors[$RANDOM % ${#colors[@]}]}
    echo -ne "\e[${color}mAnomaly\e[m"
done
EOS

chmod +x "$SCRIPT"

cat <<EOF > "$PHP_FILE"
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>anomaly</title>
</head>
<body>
    <p>
    <?php
        \$output = shell_exec("$SCRIPT 2>&1");
        echo "\$output";
    ?>
    </p>
</body>
</html>exit
EOF

chown www-data:www-data "$PHP_FILE"
chmod 644 "$PHP_FILE"


