# Flatpak Zed

## Issues
Please open issues under: https://github.com/flathub/dev.zed.Zed/issues

## Usage

Zed's current Flatpak integration exits the sandbox on startup and most functionalities work out of the box. Workflows that rely on Flatpak's sandboxing may not work as expected by default.

Please note that Zed's flatpak still runs in an isolated environment and some language toolchains might misbehave when executed from the host OS into the sandbox.  
To cope with it, Zed's flatpak defaults can be changed to: 
  - disable sandbox escape at startup
  - enable SDK extensions to get support for additional languages

### Environment variables

- `ZED_FLATPAK_NO_ESCAPE`: disable flatpak sandbox escape (default: set)
  ```shell
    $ flatpak override --user --unset-env=ZED_FLATPAK_NO_ESCAPE dev.zed.Zed
  ```

### Execute commands on the host system

When Zed's flatpak is running in the sandbox with no escape, it is not possible to execute commands on the host system.

To execute commands on the host system, run inside the sandbox:

```shell
$ flatpak-spawn --host <COMMAND>
```

or

```shell
$ host-spawn <COMMAND>
```

- Most users seem to report a better experience with `host-spawn`

### Use host shell in the integrated terminal.

Another option to execute commands is to use your host shell in the integrated terminal instead of the sandbox one.

For that, open Zed's settings via <kbd>Ctrl</kbd> + <kbd>,</kbd> and change Terminal > Environment > Shell from "System" to "Program", then replace the Program with `/app/libexec/host-sh/<YOUR SHELL>`. For example for Bash use `/app/libexec/host-sh/bash`.

This can also be configured directly in the `settings.json`:

```json
{
  "terminal": {
    "shell": {
      "program": "/app/libexec/host-sh/bash"
    }
  },
}
```

Shims are provided for many well-known shells. Alternatively, you can use your default shell by calling the `host-sh` wrapper directly:

```json
{
  "terminal": {
    "shell": {
      "program": "/app/bin/host-sh"
    }
  },
}
```

Note however that if your default shell is not POSIX-compliant, specifying `host-sh` directly is known to cause a "Failed to load environment variables" error. The shims are preferred if available.

More configuration settings for spawning commands can be found in [Zed's documentation](https://zed.dev/docs/reference/all-settings#terminal-shell).

### SDK extensions

This flatpak provides a standard development environment (gcc, python, etc).
To see what's available:

```shell
  $ flatpak run --command=sh dev.zed.Zed
  $ ls /usr/bin (shared runtime)
  $ ls /app/bin (bundled with this flatpak)
```
To get support for additional languages, you have to install SDK extensions, e.g.

```shell
  $ flatpak install flathub org.freedesktop.Sdk.Extension.dotnet
  $ flatpak install flathub org.freedesktop.Sdk.Extension.golang
```
To enable selected extensions, set `FLATPAK_ENABLE_SDK_EXT` environment variable
to a comma-separated list of extension names (name is ID portion after the last dot):

```shell
  $ FLATPAK_ENABLE_SDK_EXT=dotnet,golang flatpak run dev.zed.Zed
```
To make this persistent, set the variable via flatpak override:

```shell
  $ flatpak override --user dev.zed.Zed --env=FLATPAK_ENABLE_SDK_EXT="dotnet,golang"
```

You can use:
```shell
  $ flatpak search <TEXT>
```
to find others.

### Run flatpak Zed from host terminal

If you want to run `zed /path/to/file` from the host terminal just add this
to your shell's rc file:

```shell
  $ alias zed="flatpak run dev.zed.Zed"
```

then reload sources, now you could try:

```shell
  $ zed /path/to/
  # or
  $ FLATPAK_ENABLE_SDK_EXT=dotnet,golang zed /path/to/
```

## Related Documentation

- https://zed.dev/docs/
