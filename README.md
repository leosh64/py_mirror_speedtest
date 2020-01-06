# py_mirror_speedtest
Tool to test and compare the speeds of different mirrors hosting the same files, for example for ubuntu package repositories.

## Configuration

### Mirror list
Provide a text file with a list of mirrors to be tested, one URL per line. The URLs should end with "/". Comment lines are allowed and start with "#", for example:

```
# File containing one mirror URL per line
# URLs should end with /
http://mirrors.aliyun.com/ubuntu/
http://ftp.sjtu.edu.cn/ubuntu/
http://mirrors.cn99.com/ubuntu/
```

### Files to be downloaded
The files to be downloaded (path after the mirror) are currently specified within the Python script. This will be changed in the future.

## Usage
The simplest way to run the speed test is to call the script with the filename of the mirror list as argument:
```
./mirror_speedtest.py mirrors-cn.txt
```

Call the script with the argument ```--help``` to see the help and a full list of available options.

## Example output
```
Mirror speed ranking:
  http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ at 2037.6 kB/s
  http://mirrors.yun-idc.com/ubuntu/ at 1726.4 kB/s
  http://mirrors.cqu.edu.cn/ubuntu/ at 1545.1 kB/s
  http://mirrors.aliyun.com/ubuntu/ at 1299.8 kB/s
  http://mirrors.cn99.com/ubuntu/ at 1261.2 kB/s
  http://mirrors.huaweicloud.com/repository/ubuntu/ at 886.9 kB/s
  http://ftp.sjtu.edu.cn/ubuntu/ at 837.2 kB/s
  http://mirrors.njupt.edu.cn/ubuntu/ at 775.3 kB/s
  http://mirrors.nju.edu.cn/ubuntu/ at 157.8 kB/s
  http://mirrors.dgut.edu.cn/ubuntu/ at 87.4 kB/s
  http://mirrors.sohu.com/ubuntu/ at 0.1 kB/s
  http://mirror.lzu.edu.cn/ubuntu/ at 0.0 kB/s
  http://mirrors.ustc.edu.cn/ubuntu/ at 0.0 kB/s
```