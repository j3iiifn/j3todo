#!/usr/bin/env bash

if [ $# -ne 2 ]; then
  echo "Usage: $(basename $0) j3todo.txt report.txt" 1>&2
  exit 1
fi

cd "$(dirname $0)"

TODO="$1"
REPORT="$2"
today="$(date +%Y%m%d)"

dir_backup="$(dirname ${TODO})/backup"
[[ -d ${dir_backup} ]] || mkdir -pv ${dir_backup}

todo_backup="${dir_backup}/todo_${today}.txt"
cp "${TODO}" "${todo_backup}"

tmp_report="${dir_backup}/report_${today}.txt"

./daily_report.py "${todo_backup}" "${tmp_report}" "${TODO}"

echo "" >> "${REPORT}"
echo "# $(date +"%Y-%m-%d (%a)")" >> "${REPORT}"
cat "${tmp_report}" >> "${REPORT}"

rm ${tmp_report}
