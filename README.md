# Hetzner Management

Scripts that use the Hetzner API to run workloads on ephemeral servers


## Provisioning Nix on Hetzner

See https://github.com/elitak/nixos-infect?tab=readme-ov-file#hetzner-cloud

Provision your host and paste this into the cloud init box:

```
#cloud-config

runcmd:
  - curl https://raw.githubusercontent.com/elitak/nixos-infect/master/nixos-infect | PROVIDER=hetznercloud NIX_CHANNEL=nixos-22.11 bash 2>&1 | tee /tmp/infect.log
```

TODO - add this to be automatic

## Steps to use:

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
