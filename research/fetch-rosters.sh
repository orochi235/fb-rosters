#!/bin/sh
# Stage 1: build the real 1994 player universe (MLB + NHL) -> artifacts/rosters-1994.json
# Lahman SQLite is ~63MB; NHL API rejects non-browser user agents, hence curl.
set -e
cd "$(dirname "$0")"
mkdir -p artifacts nhl_raw
[ -f lahman.sqlite ] || curl -sL --max-time 300 -o lahman.sqlite \
  https://raw.githubusercontent.com/WebucatorTraining/lahman-baseball-mysql/master/lahmansbaseballdb.sqlite
curl -s --max-time 25 https://api-web.nhle.com/v1/standings/1994-01-01 \
  | python3 -c "import sys,json;print('\n'.join(t['teamAbbrev']['default'] for t in json.load(sys.stdin)['standings']))" \
  > nhl_teams.txt
i=0; for t in $(cat nhl_teams.txt); do
  i=$((i+1)); echo "$i/26 $t"
  curl -s --max-time 25 -o "nhl_raw/$t.json" "https://api-web.nhle.com/v1/roster/$t/19931994"
done
echo "now run: python3 build-universe.py"
