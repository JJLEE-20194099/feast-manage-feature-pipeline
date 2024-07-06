tmux kill-session -t feast_ui
tmux kill-session -t feast_1
kill $(lsof -t -i:8008)
kill $(lsof -t -i:8886)


