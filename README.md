# CatBot-V1.1

猫之城自动钓鱼调查使用说明

## 下载

[雷电模拟器9 64位-9.0.23版本](https://www.ldmnq.com/other/version-history-and-release-notes.html)

[CatBot](https://github.com/Lorpaves/CatCity-AutoFishing/releases)

### 使用教程

[使用教程视频](https://www.bilibili.com/video/BV1EV4y1T7iq/?spm_id_from=333.999.0.0&vd_source=823ee27acf1c9478547aa057f9d54e6c)

### 版本更新说明

- 新增涂鸦功能

- 以管理员身份运行软件

- 先进游戏，把所有活动提示关掉

- 有活动的钓鱼点需要手动点进去把票先领了

### 软件开启前的调整

- 先启动模拟器，进入游戏，再使用软件，否则软件打不开！！！！！

- 模拟器名称改为ld

- 模拟器分辨率：1280x720

- 桌面分辨率：1920x1080 / 2560x1440

- 桌面文本缩放：100%

- 修改按键设置，向下滑动为space键，灵敏度设置为3

### 问题解答

- 软件打不开可能因为没按照以上步骤来，下载最新版本CatBot，把CatBot放到C盘，以管理员身份运行

- 软件打开后没用，可能是因为模拟器和桌面的分辨率有问题，如果是两个显示器，把分辨率为1920x1080的设为主显示器

- 如果钓鱼不能自动购买渔具，把游戏分辨率调高，可能是因为OCR不能识别出来

- 如果以上解决方法仍无效，B站私信我，最好能发图片给我看

- 测试过2560x1440分辨率，27寸的显示器，也可以用

### 关于使用GPU版本

**GPU版本的CatBot对CPU的使用率会低些。**

**这只是一个测试。如果运行失败建议使用原版本，因为需要自己编译Opencv CUDA版本，比较折腾。**

1. 环境要求：

   - python3.x

   - opencv gpu版本

2. 下载[gpu_version](https://github.com/Lorpaves/CatCity-AutoFishing/blob/master/gpu_version.py)

3. 下载[requirements.txt](https://github.com/Lorpaves/CatCity-AutoFishing/blob/master/requirements.txt)

4. 下载环境所需要的模块

    ```shell
    pip install -r requirements.txt
    ```

5. 在gpu_version文件所在的文件夹下

```shell
python gui_version.py
```
