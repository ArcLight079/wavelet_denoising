import numpy as np
import pandas as pd
import os
import random
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pywt

from PIL import Image
from keras.utils import img_to_array
from keras.utils import load_img
from keras.utils import np_utils
from scipy import stats
from scipy import signal

def add_gauss_noise(path,noise_value):  #returns noised img,add gauss noise to image
    img = cv2.imread(str(path), 0)
    gauss_noise = np.zeros(img.shape, dtype=np.uint8)
    cv2.randn(gauss_noise, 0, noise_value)
    gauss_noise = (gauss_noise).astype(np.uint8)
    noised_img = cv2.add(img, gauss_noise)
    return(noised_img)

def add_sp_noise(image,prob):     #returns noised img,add salt and pepper noise to image
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    noised_img = output
    return (noised_img)

def coeffs(image,level,wavelet): #get coeffs
    coeffs = pywt.wavedec2(image, wavelet, level=level)
    arr, coeff_slices = pywt.coeffs_to_array(coeffs)
    return(arr,coeff_slices)

def unique_coeffs(image,level,wavelet): #get unique coeffs
    coeffs = pywt.wavedec2(image, wavelet, level=level)
    arr, coeff_slices = pywt.coeffs_to_array(coeffs)
    x = []
    for i in arr:
        x.append(list(set(list(i))))
    res = []
    # traversing in till the length of the input list of lists
    for m in range(len(x)):
        for n in range(len(x[m])):
            res.append(x[m][n])

    try:
        for i in range(len(res)):
            res[i] = abs(res[i])
    except:
        print('bad dtype at pos'+i)

    unique = list(set(res))
    unique.sort()
    return(unique) #returns sorted in ascendind order for purpose of thresholding

def MSE(img1, img2): #get MSE of 2 images
    squared_diff = (img1 - img2) ** 2
    summed = np.sum(squared_diff)
    num_pix = img1.shape[0] * img1.shape[1]
    err = summed / num_pix
    return err

path="Schloss_Neuschwanstein_2013.jpg"
img=add_gauss_noise(path,200)
final_noised_img=add_sp_noise(img,0.005)
unique_coeffs(final_noised_img,1,'db6')
M=len(coeffs)
prev_max=-1000 #first initialisation, doesnt matter
new_max=len(coeffs)
for i in range(len(coeffs)):
  M=M-1
  iter=coeffs[:M]
  I=len(iter)
  cumsum_res=np.cumsum(iter)
  threshold=iter[-1]*cumsum_res
  #check for max:
  for i in range(I):
    eps=M/I
    smiwc=(1/M)*(pow(iter,2))
    func=eps*(smiwc)
    if func>prev_max:
      new_max=M
  if new_max=len(coeffs):
      print('Thresholding failed, check math')
unique=(final_noised_img,1,'db6')
cA,(cD1,cD2,cD3)=coeffs
threshold=unique[new_max]

for coeff in (cA,cD1,cD2,cD3):
    for i in range(len(coeff)):
        for j in range (len(coeff[i])):
            if abs(coeff[i][j])>abs(threshold):
             coeff[i][j]=0


coeffs=cA,(cD1,cD2,cD3)
rev=pywt.waverec2(coeffs,'db6')
plt.imshow(rev,cmap='gray')
print(MSE(final_noised_img,rev))