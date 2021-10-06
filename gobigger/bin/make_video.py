import os
import sys
import cv2
import time

def save_mp4(player_name, fps=1):
    video_file = '{}.mp4'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
    out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'MP4V'), fps, (300, 300))
    
    for file_name in sorted(list(os.listdir('.'))):
        if file_name.startswith(player_name):
            img = cv2.imread(file_name)
            out.write(img)
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # save_mp4(player_name='e59630ba-0710-11ec-b006-8c85904b27f6')
    save_mp4(player_name='e5965114-0710-11ec-9a6d-8c85904b27f6')
    