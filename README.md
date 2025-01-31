# RemoteDevServer (RDS)
## 專案簡介
RemoteDevServer (RDS) 是一個專為需要遠端開發的團隊設計的開源伺服器解決方案。它提供靈活的連接選項，允許使用者在啟動時選擇使用 Tailscale 或 WireGuard 作為 VPN，或僅使用預設的 Nginx 進行 TCP/HTTP 封包轉發。RDS 理論上支援任意的遠端協議，如 SSH、VNC、RDP，以及基於 HTTP 的 Jupyter Lab 和 Jupyter Notebook。

## 功能特性
- **多樣化的連接選項**：支援 Tailscale、WireGuard 或僅使用 Nginx 進行封包轉發。
- **廣泛的協議支援**：理論上支援所有遠端協議，包括但不限於：
  - SSH
  - VNC
  - RDP
  - 基於 HTTP 的應用（如 Jupyter Lab、Jupyter Notebook）
- **開源且可定制**：源代碼公開，允許根據團隊需求進行自定義和擴展。

## [UML 架構圖](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=RemoteDevServer.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1B6GDb5cnCX-GloY9904kPEiRbK9uuhUE%26export%3Ddownload)
### 組件圖(Component Diagram)
![組件圖](./UML/RDS-Component%20Diagram.drawio.png)
## 安裝與使用
### 先決條件
- OS: 推薦用 Ubuntu Server 22.04 或更高 , 大多數的 Linux 發行版皆可用
- Docker, Docker-Compose(Github 版本)

### 安裝步驟
1. 克隆儲存庫並授權啟動腳本
    ```bash
    git clone https://github.com/TsukiSama9292/RemoteDevServer.git
    cd ./RemoteDevServer
    chmod +x ./*.sh
    ```
2. 選擇啟動方式，Wireguard 和 Tailscale 可同時啟用
    - 以 Wireguard VPN 啟動 RDS 伺服器
        ```bash
        ./setup.sh --Wireguard true
        ```
    - 以 Tailscale 啟動 RDS 伺服器
        ```bash
        ./setup.sh --Tailscale true
        ```
    - 無 VPN 啟動 RDS 伺服器
        ```bash
        ./setup.sh
        ```

## 解除安裝
1. 執行解除安裝腳本
```bash
./remove.sh
```