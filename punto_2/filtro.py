# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 11:01:36 2018

@author: Usuario
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as ms
pi = np.pi

def fourier(X):
    n_filas = len(X)
    n_col = len(X[0])
    Re = np.zeros((n_filas,n_col))
    Im = np.zeros((n_filas,n_col))
    for i in range(n_filas):
        for j in range(n_col):
            sumaRe = 0
            sumaIm = 0
            for k in range(n_filas):
                for m in range(n_col):
                    sumaRe += X[k,m]*np.cos(-2*pi*(k*i/n_filas + j*m/n_col))
                    sumaIm += X[k,m]*np.sin(-2*pi*(k*i/n_filas + j*m/n_col))
            Re[i,j] = sumaRe
            Im[i,j] = sumaIm
        print(i)
    return Re, Im

def flt(freq, cutoff, w, tipo):
    if(tipo == 'bajo'):
        if(freq < cutoff - w):
            return 1
        elif(freq > cutoff + w):
            return 0
        else:
            return 0.5*(1-np.sin(pi*(freq - cutoff)/(2*w)))
    elif(tipo == 'alto'):
        if(freq < cutoff - w):
            return 0
        elif(freq > cutoff + w):
            return 1
        else:
            return 0.5*(1+np.sin(pi*(freq - cutoff)/(2*w)))

def inv_fourier(Re,Im):
    X = Re +1j*Im
    n_filas = len(X)
    n_col = len(X[0])
    inv = np.zeros((n_filas,n_col))
    for i in range(n_filas):
        for j in range(n_col):
            suma = 0
            for k in range(n_filas):
                for m in range(n_col):
                    suma += X[k,m]*np.exp(2*pi*1j*(k*i/n_filas + j*m/n_col))
            inv[i,j] = suma.real/(n_filas*n_col)
    return inv

def filtro(imagen, tipo):
    if(tipo == 'alto'):
        nombre = 'altas.png'
    else:
        nombre = 'bajas.png'
        
    im = ms.imread(imagen, flatten = True)
    n_fila, n_col = np.shape(im)
    
    #RE, IM = fourier(im)
    I = np.absolute(np.fft.fft2(im))
    RE = np.fft.fft2(im).real
    IM = np.fft.fft2(im).imag
    Imax = np.amax(I)
    
    I_norm = I / Imax
    
    i_cut = 0
    for i in range(n_fila):
        I_i = I_norm[i,0]
        I_prev = I_norm[i-1,0]
        if(I_prev > 1/np.sqrt(2) and I_i < 1/np.sqrt(2)):
            i_cut = i           
                
    cutoff = i_cut
    w = i_cut*15
    Re_filtrado = np.zeros((n_fila,n_col))
    Im_filtrado = np.zeros((n_fila,n_col))
    for i in range(n_fila):
        for j in range(n_col):
                freq = (i**2 + j**2)**0.5
                Re_filtrado[i,j] = RE[i,j]*flt(freq,cutoff,w,tipo)
                Im_filtrado[i,j] = IM[i,j]*flt(freq,cutoff,w,tipo)

    new_image = np.fft.fft2(Re_filtrado+1j*Im_filtrado)
    plt.imsave(nombre,new_image.real, cmap = 'gray')
                
    
            
    
    

    