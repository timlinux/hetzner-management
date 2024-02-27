let
  pinnedHash = "933d7dc155096e7575d207be6fb7792bc9f34f6d"; 
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/${pinnedHash}.tar.gz") { };
  pythonPackages = pkgs.python3Packages;
in pkgs.mkShell rec {
  name = "impurePythonEnv";
  venvDir = "./.venv";
  buildInputs = [
    # A Python interpreter including the 'venv' module is required to bootstrap
    # the environment.
    pythonPackages.python

    # This executes some shell code to initialize a venv in $venvDir before
    # dropping into the shell
    pythonPackages.venvShellHook
    pythonPackages.prompt-toolkit
    pythonPackages.hetzner
    pythonPackages.hcloud
    pythonPackages.paramiko
    pythonPackages.pygobject3
    pythonPackages.keyring
    # Needed to prevent application does not support app id errors
    pkgs.gobject-introspection # for Gio typelib
    pkgs.gnome3.gnome-shell
    # Needed for vscode autocompletion...
    pythonPackages.pygobject-stubs
    pkgs.libadwaita
    pkgs.vscode
    pkgs.hcloud

    # Those are dependencies that we would like to use from nixpkgs, which will
    # add them to PYTHONPATH and thus make them accessible from within the venv.
  ];

  # Run this command, only after creating the virtual environment
  postVenvCreation = ''
     export DIRENV_LOG_FORMAT=
     unset SOURCE_DATE_EPOCH
     pip install -r requirements.txt
     echo "-----------------------"
     echo "🌈 Your Hetzner Dev Environment is prepared."
     echo "Run ./menu.py to start the gui"
     echo ""
     echo "📒 Note:"
     echo "-----------------------"
     echo "start vscode like this:"
     echo ""
     echo "./vscode.sh"
     echo "-----------------------"
  '';

  # Now we can execute any commands within the virtual environment.
  # This is optional and can be left out to run pip manually.
  postShellHook = ''
    # allow pip to install wheels
    unset SOURCE_DATE_EPOCH
  '';

}
