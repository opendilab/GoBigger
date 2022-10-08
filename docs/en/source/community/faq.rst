FAQ
##############


Q1: How to save video in a game?
***********************************

:A1:

Set ``playback_settings`` when you create the environment. After finishing a game, ``test.pb`` will be saved at ``save_dir``, which can be shown by the GoBigger replayer.

.. code-block::
    
    env = create_env('st_t3p2', dict(
        playback_settings=dict(
            playback_type='by_frame',
            by_frame=dict(
                save_frame=True,
                save_dir='.',
                save_name_prefix='test',
            ),
        ),
    ))



Q2: What are the winning conditions at the end of the game?
**********************************************************************

:A2:

Sort by calculating the sum of the scores of all players under each team at the end of the game.


Q3: Is there a limit to the size of the partial field of view?
**********************************************************************

:A3:

The size of the player's partial field of view is determined by the relative position of the player's doppelganger. We set the player’s minimum field of view to be a matrix of 36*36. With the dispersion of the doppelganger, the player's maximum field of vision can reach the global level.
