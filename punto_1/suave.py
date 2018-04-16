# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 17:59:49 2018

@author: Usuario
"""
import matplotlib.pyplot as plt
import numpy as np

pi = np.pi

def fourier(X, N):
    n_filas = len(X)
    n_col = len(X[0])
    Re = np.zeros((n_filas,n_col))
    Im = np.zeros((n_filas,n_col))
    for i in range(N):
        for j in range(N):
            sumaRe = 0
            sumaIm = 0
            for k in range(n_filas):
                for m in range(n_col):
                    sumaRe += X[k,m]*np.cos(-2*pi*(k*i/n_filas + j*m/n_col))
                    sumaIm += X[k,m]*np.sin(-2*pi*(k*i/n_filas + j*m/n_col))
            #print(sumaRe)
            Re[i,j] = sumaRe
            Im[i,j] = sumaIm
    return Re, Im

def inv_fourier(Re,Im,N):
    X = Re +1j*Im
    n_filas = len(X)
    n_col = len(X[0])
    inv = np.zeros((n_filas,n_col))
    for i in range(n_filas):
        for j in range(n_col):
            suma = 0
            for k in range(N):
                for m in range(N):
                    suma += X[k,m]*np.exp(2*pi*1j*(k*i/n_filas + j*m/n_col))
            inv[i,j] = suma.real/(n_filas*n_col)
    return inv
    
        
def suave(imagen, n_pixeles_kernel):
    im = plt.imread(imagen)
    #plt.imshow(im)
    N = 20
    n_filas, n_col, n_3 = np.shape(im)
    print(n_filas, n_col)
    
    x = np.linspace(-2*n_pixeles_kernel, 2*n_pixeles_kernel, N)
    sigma = n_pixeles_kernel/2
    G_x = np.exp(-x**2/(2*sigma**2))
    G_x = G_x/np.trapz(G_x)
    
    k = G_x[:,np.newaxis]*G_x[np.newaxis,:]
    kernel = np.zeros((n_filas,n_col))
    kernel[:N,:N] = k

    ReK, ImK = fourier(kernel,N)
    new_image = np.zeros((n_filas,n_col,n_3))
    
    for i in range(n_3):
        im_slice = im[:,:,i]
        Re_im, Im_im = fourier(im_slice,N)
        #convolucion = (Re_im+1j*Im_im)*(ReK + 1j*ImK)
        convolucionRE = Re_im*ReK - Im_im*ImK
        convolucionIM = Im_im*ReK + ImK*Re_im
        new_image[:,:,i] = inv_fourier(convolucionRE,convolucionIM,N)
        print(new_image[:,:,i])
    plt.imshow(new_image/np.amax(new_image))
    plt.imsave('suave.png', new_image/np.amax(new_image))
    
        
        
        
        
    

    
