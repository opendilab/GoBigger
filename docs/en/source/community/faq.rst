FAQ
##############


Q1: How to save video in a game?
***********************************

:A1:

Set ``save_video=True`` in the ``cfg`` of ``server``. By default, we will save the video in the current directory where the command is executed. If you want to set the save path, you can specify it by setting ``save_path``. While saving the video, we will also save all player perspectives.


Q2: What are the winning conditions at the end of the game?
**********************************************************************

:A2:

Sort by calculating the sum of the scores of all players under each team at the end of the game.


Q3: Is there a limit to the size of the partial field of view?
**********************************************************************

:A3:

The size of the player's partial field of view is determined by the relative position of the player's doppelganger. We set the player’s minimum field of view to be a matrix of 300*300. With the dispersion of the doppelganger, the player's maximum field of vision can reach the global level.
