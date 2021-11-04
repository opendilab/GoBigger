Collision Detection Algorithm
=============================

Overview
--------

| In order to detect the collision of the sphere in each frame of the
  game so that the server can update the state of the sphere, we need to
  design an efficient collision detection algorithm.
| We have designed four collision detection algorithms and encapsulated
  them into the following four classes.


Algorithm efficiency analysis
-----------------------------

The theoretical time complexity of the above four algorithms is as
follows:

**ExhaustiveCollisionDetection:**

:math:`O(n*m)`

where n denotes the total number of balls and m denotes the number of balls to be asked.

**PrecisionCollisionDetection:**

:math:`O(n*log(n)+\Sigma{r}*logn+p)`

where n denotes the total number of balls, m denotes the number of balls to be asked, k denotes the presicion we set and p denotes number of spheres that actually collided.

**RebuildQuadTreeCollisionDetection:**

:math:`O(n*log(n) + m*log(n)+p)`

where n denotes the total number of balls, m denotes the number of balls to be asked and p denotes number of spheres that actually collided.

**RemoveQuadTreeCollisionDetection:**

:math:`O(r*log(n)+m*log(n)+p)`

where n denotes the total number of balls, m denotes the number of balls to be asked, r denotes the number of spheres whose position status has changed and p denotes number of spheres that actually collided.

In order to test the efficiency of these algorithms, we modify the
parameters including the total number of balls, the number of queries,
the number of changed balls, and the iteration rounds to set the test
scenario. The data in the following table comes from the most
representative scenarios

* `T: the number of all balls in the map`
* `Q: the number of query balls, which usually means the moving balls in the map`
* `C: the number of changing balls, which means the number of collisions`

+----------+------------+-----------+------------------+-----------------+
|          | Exhaustive | Precision | Rebuild QuadTree | Remove QuadTree |
+==========+============+===========+==================+=================+
| T=3000   | 688ms      | 14ms      | 47ms             | 48ms            |
|          |            |           |                  |                 |
| Q=300    |            |           |                  |                 |
|          |            |           |                  |                 |
| C=600    |            |           |                  |                 |
+----------+------------+-----------+------------------+-----------------+
| T=3000   | 1067ms     | 16ms      | 50ms             | 178ms           | 
|          |            |           |                  |                 |
| Q=300    |            |           |                  |                 |
|          |            |           |                  |                 |
| C=1500   |            |           |                  |                 |
+----------+------------+-----------+------------------+-----------------+
| T=10000  | 8384ms     | 61ms      | 339ms            | 497ms           |
|          |            |           |                  |                 |
| Q=1000   |            |           |                  |                 |
|          |            |           |                  |                 |
| C=2000   |            |           |                  |                 |
+----------+------------+-----------+------------------+-----------------+
| T=10000  | 12426ms    | 86ms      | 586ms            | 2460ms          |
|          |            |           |                  |                 |
| Q=2000   |            |           |                  |                 |
|          |            |           |                  |                 |
| C=5000   |            |           |                  |                 |
+----------+------------+-----------+------------------+-----------------+
| T=30000  | 127000ms   | 403ms     | 5691ms           | 8419ms          |
|          |            |           |                  |                 |
| Q=6000   |            |           |                  |                 |
|          |            |           |                  |                 |
| C=3000   |            |           |                  |                 |
+----------+------------+-----------+------------------+-----------------+

In order to see the pros and cons of each algorithm more intuitively, we
integrated test data and drew diagrams of four algorithms and various
parameters as follows:

.. only:: html

    .. figure:: images/changed_num_3000.png
      :width: 600
      :align: center

.. only:: html

    .. figure:: images/query_num_3000.png
      :width: 600
      :align: center

.. only:: html

    .. figure:: images/iters_num_3000.png
      :width: 600
      :align: center

According to the results, we can think that the **PrecisionCollisionDetection**  algorithm is far better than the other algorithms in terms of efficiency and stability.
