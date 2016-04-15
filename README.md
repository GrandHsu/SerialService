# SerialService

### 串口服务程序

用于电源项目和磁场项目的通信部分

由于使用 LabView 编写串口服务较为繁琐，效率貌似不怎么高。所以考虑用 python 来运行串口驱动，并提供接口给 LabView 调用，同时将通信与界面显示分开，简化 LabView 界面程序编写过程。

目前想通过 Socket 与 LabView 进行同步通信。

先开启串口服务，再运行 LabView，同步之后，进行界面操作。

### 运行环境

Windows 10, python 2.7, (LabView 2015)

### 依赖

* python 2.7
* pyserial
* __msvcrt__ 

### 目前状态

- [x]   通信协议		`CommunicationProtocol.py`
- [x]   串口服务		`SerialService.py`
- [ ]   Socket服务	`SocketService.py`

### 我

E-mail: mr.iridescent.rsy@hotmail.com
