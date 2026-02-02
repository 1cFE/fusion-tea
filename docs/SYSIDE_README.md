# SysIDE Setup Guide

This project uses [Sensmetry SysIDE](https://sensmetry.com/) for SysML v2 modeling. We're on the **Solo** plan.

## Prerequisites

- A valid Syside Modeler license (obtained from [Sensmetry.com](https://sensmetry.com/) or contact syside@sensmetry.com)
- Linux (this guide assumes Linux; see official docs for Windows/macOS)

## CLI Installation

**Documentation**: https://docs.sensmetry.com/modeler/cli.html

### 1. Download and Extract

Download the Linux release, then extract to your local directory:

```bash
mkdir -p ~/.local
tar -xJf syside-<version>-x86_64-linux-glibc.tar.xz --directory ~/.local
```

### 2. Add to PATH

Add this line to your `~/.bashrc`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload:

```bash
source ~/.bashrc
```

### 3. Verify Installation

```bash
syside --version
```

Should output something like: `0.8.1 (4bb41581f62d5fe422a57c1c381aa42cb41203b3)`

### Key CLI Commands

| Command | Description |
|---------|-------------|
| `syside check <file>` | Validate model for semantic errors |
| `syside format <file>` | Format code to consistent style |

**Note**: In this project, always run via `uv`:
```bash
uv run syside check models/path/to/file.sysml
```

## VSCode Plugin Installation

**Documentation**: https://docs.sensmetry.com/modeler/install.html

### Option A: Marketplace (Recommended)

1. Open VSCode
2. Open Extensions view (`Ctrl+Shift+X`)
3. Search for "Syside Modeler"
4. Install the extension by Sensmetry

Or install directly from: https://marketplace.visualstudio.com/items?itemName=sensmetry.syside-modeler

### Option B: Manual VSIX Installation

1. Download the `.vsix` file for Linux x64
2. In VSCode, open Extensions (`Ctrl+Shift+X`)
3. Either:
   - Drag and drop the `.vsix` file into the Extensions panel, or
   - Open Command Palette (`Ctrl+Shift+P`) → "Extensions: Install from VSIX…"

**Note**: VSIX installations don't receive automatic updates.

## License Activation

When you first open a `.sysml` file, you'll be prompted to enter your license key.

Alternatively:
1. Open Command Palette (`Ctrl+Shift+P`)
2. Run "Syside Modeler: Add Syside license key to keyring"
3. Enter your license key when prompted

A confirmation message appears on successful activation.

## Installing Syside Tools

After activating your license, VSCode will prompt you to install Syside Tools. Accept this prompt to enable full functionality including visualization.

You can also trigger this manually:
1. Open Command Palette (`Ctrl+Shift+P`)
2. Run "Syside Modeler: Install Syside Tools"

## Additional Resources

- [Full Documentation](https://docs.sensmetry.com/)
- [Troubleshooting](https://docs.sensmetry.com/modeler/troubleshooting.html)
- [SysML v2 Standard Library](https://docs.sensmetry.com/modeler/stdlib.html)
