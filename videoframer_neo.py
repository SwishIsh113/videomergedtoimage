import cv2
import argparse
import os

def extractImages(pathIn, pathOut):
    count = 0

    vidcap = cv2.VideoCapture(pathIn)
    success, image = vidcap.read()
    success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
        success, image = vidcap.read()
        if success:
            print('Read a new frame:', success)
            filename = os.path.join(pathOut, "frame%d.jpg" % count)
            cv2.imwrite(filename, image)
            count += 1
        else:
            print('Error reading frame:', success)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    output_folder = "frames"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_folder = "video"
    video_files = [f for f in os.listdir(video_folder) if os.path.isfile(os.path.join(video_folder, f))]
    video_files = [f for f in video_files if f.lower().endswith(('.mp4', '.avi', '.mov'))]

    for video_file in video_files:
        pathIn = os.path.join(video_folder, video_file)
        video_name = os.path.splitext(video_file)[0]
        output_subfolder = os.path.join(output_folder, video_name)
        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)
        extractImages(pathIn, output_subfolder)
