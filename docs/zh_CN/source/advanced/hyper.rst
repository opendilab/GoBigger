衍生环境和动作空间
################

总览
======================

在 GoBigger 环境的基础上，考虑到大环境训练的复杂度以及针对特定任务的算法验证，我们提供了部分特定条件下的小环境，以及高级序列化动作来方便
大家进行训练和算法设计。


小环境
======================

我们通过提供config的方式来提供小环境的初始化方式。


* 分身合球，分身持球（2f2s）

    这个小环境中只有两只队伍，每支队伍中有两个玩家。地图中同时还会存在相同比例的食物求和荆棘球。在本地图中，蓝色A球
    只需要向右边进行分裂，同时蓝色B球需要吃掉蓝色A球分裂出来的小球并向下移动，通过分裂（或移动）的方式吃掉黄色A球。

    .. only:: html

        .. figure:: images/2f2s.png
          :width: 300
          :align: center


* 测涨（2f2s_v2）

    这个小环境是2f2s的v2版本。在本地图中，蓝色A球只需要向右边进行分裂，同时蓝色B球保持不动即可吃掉黄色A球。

    .. only:: html

        .. figure:: images/2f2s_v2.png
          :width: 300
          :align: center


* 测涨（2f2s_v3）

    这个小环境是2f2s的v3版本。在本地图中，蓝色A球需要向黄色球和蓝色B球之间进行分裂并向中心吐孢子，同时蓝色B球
    向下移动即可吃掉黄色A球。

    .. only:: html

        .. figure:: images/2f2s_v3.png
          :width: 300
          :align: center


高级序列化动作
======================

请查看 ``gobigger/hyper/tests`` 目录下的测试文件来使用高级序列化动作。


* 直线合球

    .. only:: html

        .. figure:: images/straight_merge.gif
          :width: 362
          :align: center


* 四分合球

    .. only:: html

        .. figure:: images/quarter_merge.gif
          :width: 362
          :align: center


* 八分合球

    .. only:: html

        .. figure:: images/eighth_merge.gif
          :width: 338
          :align: center
