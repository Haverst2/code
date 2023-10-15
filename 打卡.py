import cv2 as cv
import numpy as np

cap = cv.VideoCapture('D:\\USE_NOW\\code\\MyCode\\a.mp4')

if not cap.isOpened():
    print("Cannot open camera")
    exit()
FPS = int(cap.get(cv.CAP_PROP_FPS))
print(FPS)
total_frame = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
print(total_frame)

out_file = '打卡_'
second = 16
total_frame_per_file = FPS * second

file_number = 0
frame_number = 0
fourcc = cv.VideoWriter_fourcc('M','P','4','V')

output_width , output_height = int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
print(output_width, output_height)

while frame_number < total_frame:

    out_filename = out_file + str(file_number) + '.mp4'
    out = cv.VideoWriter(out_filename, fourcc, FPS, (output_width, output_height))

    for _ in range(total_frame_per_file):
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        frame_number += 1
    
    out.release()
    file_number += 1

cap.release()
