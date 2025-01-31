# RemoteDevServer (RDS)
## 說明
專門為需要遠端開發的團隊設計  
支援 SSH/VNC/RDP...etc 遠端協議  
針對 VPN 需求可選啟動方法
## [UML 架構圖](https://drive.google.com/file/d/1B6GDb5cnCX-GloY9904kPEiRbK9uuhUE/view?usp=sharing)
## 操作
### 授權啟動腳本
```bash
chmod +x ./*.sh
```
### 以 Wireguard VPN 啟動 RDS 伺服器
```bash
./setup.sh --Wireguard true
```
### 以 Tailscale 啟動 RDS 伺服器
```bash
./setup.sh --Tailscale true
```
### 無 VPN 啟動 RDS 伺服器
```bash
./setup.sh
```
### 移除 RDS 伺服器
```bash
./remove.sh
```