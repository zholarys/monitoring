#!/usr/bin/env bash
set -Eeuo pipefail
export PATH=/usr/local/bin:/usr/bin:/bin
umask 077

cd /home/kara/devops-lab
backup_dir="$PWD/backups/auto"
mkdir -p "$backup_dir"

# Не допускаем два одновременных запуска.
exec 9>"$backup_dir/.backup.lock"
flock -n 9 || {
    echo "ERROR: другой процесс резервирования уже работает" >&2
    exit 1
}

partial=""
cleanup() {
    if [[ -n "$partial" ]]; then
        rm -f -- "$partial"
    fi
}
trap cleanup EXIT
trap 'echo "ERROR: резервирование прервано, строка $LINENO" >&2' ERR

partial=$(mktemp "$backup_dir/.dump.XXXXXXXX.partial")
backup_file="$backup_dir/backup_practice_$(date +%Y%m%d_%H%M%S)_$$.sql.gz"

echo "START: резервирование backup_practice"

docker compose exec -T db sh -c '
    export MYSQL_PWD="$MYSQL_ROOT_PASSWORD"
    exec mysqldump -u root \
        --single-transaction \
        --no-tablespaces \
        --set-gtid-purged=OFF \
        backup_practice
' | gzip > "$partial"

gzip -t "$partial"
mv -- "$partial" "$backup_file"
partial=""

date --iso-8601=seconds > "$backup_dir/.last_success.tmp"
mv "$backup_dir/.last_success.tmp" "$backup_dir/last_success.txt"

echo "SUCCESS: $backup_file"
