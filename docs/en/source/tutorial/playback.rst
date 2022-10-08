Playback System
##################

GoBigger's playback system supports three options, which can be selected through the environment's configuration file. The configuration items involved are as follows:

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

``playback_type`` can be one of ``['none', 'by_video', 'by_frame']``.

* ``none``: means no need to save playback
* ``by_video``: means to save the video directly, and the suffix of the saved file is ``.mp4``. Generally speaking, the video saved in the ``st_t4p3`` environment is about 80M.
* ``by_frame``: Represents the change amount of each frame saved, and the suffix of the saved file is ``.pb``. Generally speaking, the ``st_t4p3`` environment saves files around 25M.


Save video
----------------------------

If ``playback_type='by_video'`` is selected, the specific configuration items can be as follows:

.. code-block:: python

    env = create_env('st_t4p3', dict(
        playback_settings=dict(
            playback_type='by_video',
            by_video=dict(
                save_video=True,
                save_dir='.', # The directory location where the video needs to be saved
                save_name_prefix='test', # Save the prefix of the video name
            ),
        ),
    ))


Save the pb file
----------------------------

If ``playback_type='by_frame'`` is selected, the specific configuration items can be as follows:

.. code-block:: python

    env = create_env('st_t4p3', dict(
        playback_settings=dict(
            playback_type='by_frame',
            by_frame=dict(
                save_frame=True,
                save_dir='.', # The directory location where the video needs to be saved
                save_name_prefix='test', # The prefix of the name of the saving video
            )
        ),
    ))

After getting the saved ``.pb`` file, you need to view it through our given player. Execute the following command in the command line to open the player.

.. code-block:: python

    python -m gobigger.bin.replayer

After opening the player, you need to select the ``.pb`` file you want to view. Then you can start watching. The player supports double-speed playback, including 2x, 4x, and 8x (by clicking the button in the lower left corner). Also supports dragging the progress bar.
