# openwrt-packages

自用openwrt插件源（适用于官方源）

## 使用方法

```shell
cat <<- EOF >> feeds.conf.default
src-git lujiang0111 https://github.com/Lujiang0111/openwrt-packages.git
EOF
```

## 插件列表

| 软件名 | 说明 | 中文说明 |
| - | - | - |
| luci-app-uugamebooster | uu game booster | uu主机加速器 |
| luci-app-vlmcsd | LuCI support for KMS | KMS服务器 |
| luci-app-vsftpd | LuCI support for VSFTPD | FTP服务器 |
