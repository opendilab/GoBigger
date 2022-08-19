回放系统
##############

GoBigger的回放系统支持三种选择，可以通过环境的配置文件来进行选择。涉及到的配置项如下：

.. code-block:: python

    config = dict(
        ...
        playback_settings=dict(
            playback_type='none', # ['none', 'by_video', 'by_frame']
            by_video=dict(
                save_video=False,
                save_fps=10,
                save_resolution=552,
                save_all=True,
                save_partial=False,
                save_dir='.',
                save_name_prefix='test',
            ),
            by_frame=dict(
                save_frame=False,
                save_all=True,
                save_partial=False,
                save_dir='.',
                save_name_prefix='test',
            ),
            by_action=dict(
                save_action=False,
                save_dir='.',
                save_name_prefix='test',
            ),
        ),
        ...
    )

``playback_type`` 可以是 ``['none', 'by_video', 'by_frame']`` 中的其中一种。其中，

* ``none``: 代表不需要存回放
* ``by_video``: 代表直接保存录像，保存文件后缀是 ``.mp4``。一般来说，``st_t4p3`` 环境存下来的录像在 80M 左右。
* ``by_frame``: 代表存每一帧的变化量，保存文件后缀是 ``.pb``。一般来说，``st_t4p3`` 环境存下来文件在 25M 左右。


直接保存录像
--------------

如果选择 ``playback_type='by_video'``，具体的配置项可以像下面这样：

.. code-block:: python

    env = create_env('st_t4p3', dict(
        playback_settings=dict(
            playback_type='by_video',
            by_video=dict(
                save_video=True,
                save_dir='.', # 需要保存录像的目录位置
                save_name_prefix='test', # 保存录像名字的前缀
            ),
        ),
    ))


直接保存pb文件
--------------

如果选择 ``playback_type='by_frame'``，具体的配置项可以像下面这样：

.. code-block:: python

    env = create_env('st_t4p3', dict(
        playback_settings=dict(
            playback_type='by_frame',
            by_frame=dict(
                save_frame=True,
                save_dir='.', # 需要保存录像的目录位置
                save_name_prefix='test', # 保存录像名字的前缀
            )
        ),
    ))

得到保存后的 ``.pb`` 文件之后，需要通过我们给定的播放器来查看。在命令行中执行下面的命令来打开播放器。

.. code-block:: python

    python -m gobigger.bin.replayer

打开播放器之后，需要选择你想要查看的 ``.pb`` 文件。然后就可以开始看了。播放器支持倍速播放，包括2倍，4倍，8倍（通过点击左下角的按钮）。同时支持拖动进度条。
