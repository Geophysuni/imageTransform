# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 16:55:12 2023

@author: Sergey Zhuravlev
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 16:43:09 2023

@author: Sergey Zhuravlev
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

# # Load the image
# before = cv2.imread('../files/beforeCity.png')
# after = cv2.imread('../files/afterCity.png')

def calculate_image_attributes(ini_image):    
    
    image = np.copy(ini_image)
    
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    saturation = hsv_image[:,:,1]
    avg_saturation = saturation.mean()
    hue = hsv_image[:,:,0].mean()
    color_balance = image.mean(axis=(0, 1))
    white_balance = cv2.xphoto.createSimpleWB()
    # white_balance.setP(0.5)  # Adjust the parameter as needed
    balanced_image = white_balance.balanceWhite(image)
    gamma = 1.5  # Adjust the gamma value as needed
    gamma_corrected_image = np.power(balanced_image / 255.0, gamma) * 255.0
    exposure = image.mean()
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    vignette = 1 - gray_image / gray_image.mean()
    contrast = np.std(gray_image)
    brightness = int(gray_image.mean())    
    return {
        
        "Brightness": brightness,
        "Contrast": contrast,
        "Saturation": avg_saturation,
        "Hue": hue,
        "Color Balance": color_balance,
        "Exposure": exposure
    }

def adjust_brightness(ini_image, brightness_factor):
    
    image = np.copy(ini_image)
    
    adjusted_image = cv2.convertScaleAbs(image, alpha=brightness_factor, beta=0)
    return adjusted_image

def adjust_contrast(ini_image, contrast_factor):
    
    image = np.copy(ini_image)
    
    image_float = image.astype(float)
    adjusted_image = image_float * contrast_factor
    adjusted_image = np.clip(adjusted_image, 0, 255)
    adjusted_image = adjusted_image.astype('uint8')
    return adjusted_image

def adjust_saturation(ini_image, saturation_factor):
    
    image = np.copy(ini_image)
    
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    current_saturation = hsv_image[:, :, 1].mean()
    # saturation_factor = target_saturation / current_saturation
    # saturation_factor = np.clip(saturation_factor, 0.1, 10.0)
    hsv_image[:, :, 1] = np.uint8(hsv_image[:, :, 1] * saturation_factor)
    adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return adjusted_image

def adjust_hue(ini_image, target_hue):
    
    image = np.copy(ini_image)
    
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    current_hue = hsv_image[:, :, 0].mean()
    hue_difference = target_hue - current_hue
    hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue_difference) % 180
    adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return adjusted_image

def adjust_color_balance(ini_image, blue_factor, red_factor, green_factor):
    
    # image = np.copy(ini_image)
    
    # total_balance = red_balance + green_balance + blue_balance
    # red_factor = red_balance / total_balance
    # green_factor = green_balance / total_balance
    # blue_factor = blue_balance / total_balance
    adjusted_image = ini_image.copy()
    adjusted_image[:, :, 0] = np.uint8(adjusted_image[:, :, 0] * blue_factor)
    adjusted_image[:, :, 1] = np.uint8(adjusted_image[:, :, 1] * green_factor)
    adjusted_image[:, :, 2] = np.uint8(adjusted_image[:, :, 2] * red_factor)    
    return adjusted_image

def adjust_exposure(ini_image, exposure_factor):
    
    image = np.copy(ini_image)
    
    current_exposure = image.mean()
    # exposure_factor = target_exposure / current_exposure
    adjusted_image = np.clip(image * exposure_factor, 0, 255).astype(np.uint8)
    return adjusted_image
        

def editImage(ini_image, b_coef, c_coef, s_coef, e_coef, bl_coef, gr_coef, red_coef):
# def editImage(ini_image, a, b, c):
    image = np.copy(ini_image)
    
    image = adjust_brightness(image, b_coef)
    image = adjust_contrast(image, c_coef)    
    image = adjust_saturation(image, s_coef)
    image = adjust_exposure(image, e_coef)
    
    image = adjust_color_balance(ini_image, bl_coef, gr_coef, red_coef)
    
    return image
    

def resFunc(iniCoef, ini_image, tar_image):
    
    image = editImage(ini_image, iniCoef[0], iniCoef[1], iniCoef[2], 
                      iniCoef[3],iniCoef[4] ,iniCoef[5] ,iniCoef[6])
    
    iniAttr = calculate_image_attributes(image)
    tarAttr = calculate_image_attributes(tar_image)
    
    vec = np.array([iniAttr['Brightness']-tarAttr['Brightness'],
           iniAttr['Contrast']-tarAttr['Contrast'], 
           iniAttr['Saturation']-tarAttr['Saturation'], 
           iniAttr['Exposure']-tarAttr['Exposure']])
    
    dist = np.mean(abs(vec))
    
    # plt.figure()
    # plt.plot([iniAttr['Brightness'], iniAttr['Contrast'], iniAttr['Saturation'], 
    #           iniAttr['Exposure']], linestyle = '--', color = 'blue')
    # plt.plot([tarAttr['Brightness'], tarAttr['Contrast'], tarAttr['Saturation'], 
    #           tarAttr['Exposure']], color = 'blue')
    
    return dist

def edit(iniPath, tarPath):
    before = cv2.imread(iniPath)
    after = cv2.imread(tarPath)
    result = minimize(resFunc, x0=[1,1,1,1,1,1,1], method='Nelder-Mead', args=(before, after))
    
    resIm = cv2.cvtColor(editImage(before, result.x[0], result.x[1], result.x[2], result.x[3], result.x[4], result.x[5], result.x[6]), cv2.COLOR_BGR2RGB) 
    
    return resIm
    # ax[2].imshow(cv2.cvtColor(after, cv2.COLOR_BGR2RGB))