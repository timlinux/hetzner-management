with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
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
    # Needed for vscode autocompletion...
    pythonPackages.pygobject-stubs
    pkgs.vscode
    # Those are dependencies that we would like to use from nixpkgs, which will
    # add them to PYTHONPATH and thus make them accessible from within the venv.
  ];

  # Run this command, only after creating the virtual environment
  postVenvCreation = ''
     unset SOURCE_DATE_EPOCH
     pip install -r requirements.txt
  '';

  shellHook = ''
     export DIRENV_LOG_FORMAT=
     echo "-----------------------"
     echo "🌈 Your Hetzner Dev Environment is prepared."
     echo "Run ./menu.py to start the gui"
     echo ""
     echo "🪛 Installing VSCode Extensions:"
     echo "--------------------------------"
     code --extensions-dir=".vscode-extensions" --install-extension donjayamanne.python-environment-manager
     code --extensions-dir=".vscode-extensions" --install-extension donjayamanne.python-extension-pack
     code --extensions-dir=".vscode-extensions" --install-extension hbenl.vscode-test-explorer
     code --extensions-dir=".vscode-extensions" --install-extension jamesqquick.python-class-generator
     code --extensions-dir=".vscode-extensions" --install-extension KevinRose.vsc-python-indent
     code --extensions-dir=".vscode-extensions" --install-extension littlefoxteam.vscode-python-test-adapter
     code --extensions-dir=".vscode-extensions" --install-extension maziac.asm-code-lens
     code --extensions-dir=".vscode-extensions" --install-extension ms-python.debugpy
     code --extensions-dir=".vscode-extensions" --install-extension ms-python.python
     code --extensions-dir=".vscode-extensions" --install-extension ms-python.vscode-pylance
     code --extensions-dir=".vscode-extensions" --install-extension ms-vscode.test-adapter-converter
     code --extensions-dir=".vscode-extensions" --install-extension njpwerner.autodocstring
     code --extensions-dir=".vscode-extensions" --install-extension VisualStudioExptTeam.intellicode-api-usage-examples
     code --extensions-dir=".vscode-extensions" --install-extension VisualStudioExptTeam.vscodeintellicode
     echo ""
     echo "📒 Note:"
     echo "-----------------------"
     echo "start vscode like this:"
     echo ""
     echo "code --extensions-dir=\".vscode-extensions\" ."
     echo "-----------------------"
  '';

  # Now we can execute any commands within the virtual environment.
  # This is optional and can be left out to run pip manually.
  postShellHook = ''
    # allow pip to install wheels
    unset SOURCE_DATE_EPOCH
  '';

}
