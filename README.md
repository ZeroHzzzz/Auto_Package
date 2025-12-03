# Auto Packaging

[![Release](https://img.shields.io/github/v/release/zerohzzzz/Auto_Package?style=flat-square)](https://github.com/zerohzzzz/Auto_Package/releases)
[![Build Status](https://img.shields.io/github/actions/workflow/status/zerohzzzz/Auto_Package/release.yml?branch=main&label=build&style=flat-square)](https://github.com/zerohzzzz/Auto_Package/actions/workflows/release.yml)

本项目用于自动打包：通过 GitHub Actions 在你推送符合 vX.Y.Z 格式的 tag 时，自动构建 Windows、macOS 和 Linux 三平台的可执行文件，并把构建产物发布到项目的 [Releases](https://github.com/zerohzzzz/Auto_Package/releases) 页面。

---

## 🚀 快速使用

1. 把你的 `.spec` 文件、`requirements.txt` 和代码上传到仓库根目录（.spec 文件用于 PyInstaller）。
2. 打标签并推送到远程，例如：

```bash
git tag v1.0.4
git push origin v1.0.4
```

3. 等待 GitHub Actions 完成构建（工作流会在矩阵上同时构建三个平台），完成后到 [Releases 页面](https://github.com/zerohzzzz/Auto_Package/releases) 下载对应平台的二进制：

   - `myapp-windows.exe`（Windows）
   - `myapp-macos`（macOS，可执行文件）
   - `myapp-linux`（Linux，可执行文件）

注意事项：

- Windows runner 在构建时使用 PowerShell；生成的 Windows 可执行通常以 `.exe` 结尾。  
- macOS 上首次打开可能需要右键 → “打开” 来绕过 Gatekeeper 策略。  
- 如果构建失败，可在 Actions 日志中查看对应平台的详细输出。