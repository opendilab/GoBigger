.. gobigger documentation master file, created by
   sphinx-quickstart on Fri Aug 27 11:46:57 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

欢迎查阅 GoBigger 中文文档!
=========================================

总览
------------

多智能体对抗作为决策AI中重要的部分，也是强化学习领域的难题之一。为丰富多智能体对抗环境， OpenDILab 开源了一款多智能体对抗竞技游戏环境——Go-Bigger。同时，Go-Bigger 还可作为强化学习环境协助多智能体决策 AI 研究。
与风靡全球的 `Agar <https://agar.io/>`_ 等游戏类似，在 Go-Bigger 中，玩家（AI）控制地图中的一个或多个圆形球，通过吃食物球和其他比玩家球小的单位来尽可能获得更多重量，并需避免被更大的球吃掉。每个玩家开始仅有一个球，当球达到足够大时，玩家可使其分裂、吐孢子或融合，和同伴完美配合来输出博弈策略，并通过AI技术来操控智能体由小到大地进化，凭借对团队中多智能体的策略控制来吃掉尽可能多的敌人，从而让己方变得更强大并获得最终胜利。

GoBigger 提供了多种接口供用户方便快捷地与游戏环境进行交互。如果想快速了解游戏，可以通过实时人机对战接口在本地快速地开启一局游戏。同时 GoBigger 还提供了方便的标准 gym.Env 的接口以供研究人员学习他们的策略。用户也可以自定义游戏的初始环境，来进行更多样化的游戏对局。


索引
=====================

.. toctree::
   :maxdepth: 2

   installation/index

.. toctree::
   :maxdepth: 2

   tutorial/index
