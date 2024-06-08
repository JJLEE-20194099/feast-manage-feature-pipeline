tmux kill-session -t feast_ui
kill $(lsof -t -i:8008)

