# Hetzner Management

Scripts that use the Hetzner API to run workloads on ephemeral servers

Steps to use:

Create a new hetzner cloud project
Get an API key for that cloud project

```
nix-shell #if you dont have direnv
export HETZNER_API_TOKEN=XXXXXXXXXXXXXXXXXXXXX
./menu.py
```

![Example in use](img/example.gif)

Tim Sutton
Feb 2024
