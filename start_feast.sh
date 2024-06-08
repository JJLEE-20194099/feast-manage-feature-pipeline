cd feature_repo
tmux new-session -d -s feast_ui 'feast ui --host 127.0.0.1 --port 8889'
feast serve -p 8008