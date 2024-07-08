tmux kill-session -t feast_ui
tmux kill-session -t feast_1
kill -9 $(lsof -t -i:8008)
kill -9 $(lsof -t -i:8886)
kill -9 $(lsof -t -i:8889)
kill -9 $(lsof -t -i:8890)



