import random
import time
import _cgobigger

def test_obs():
    server = _cgobigger.Server(_cgobigger.DefaultServer())
    server.reset()
    player_names = server.get_player_names()
    for i in range(1000):
        actions = {player_name: [random.uniform(-1, 1), random.uniform(-1, 1), -1] for player_name in player_names}
        t1 = time.time()
        server.step(actions)
        t2 = time.time()
        o = server.obs()
        t3 = time.time()
        print("step={:.3f}, obs={:.3f}".format(t2-t1, t3-t2))

if __name__ == '__main__':
    test_obs()
