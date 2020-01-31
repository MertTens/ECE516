import cv2
import matplotlib.pyplot as plt




x_res = 500
y_res = 500

def MSE(original, reference, index):
    mse = 0
    for x in range(x_res):
        for y in range(y_res):
           mse += ((original[y][x][index]/255 - reference[y][x][index]/255)) ** 2 
           #mse += ((original[y][x][1]/255 - reference[y][x][1]/255)) ** 2 
           #mse += ((original[y][x][2]/255 - reference[y][x][2]/255)) ** 2 
    return mse

def single_correct(target, reference, gam, index):
    for x in range(x_res):
        for y in range(y_res):
            target[y][x][index] = ((reference[y][x][index] ** (1/gam)) * 2) ** gam
            if(((reference[y][x][index] ** (1/gam)) * 2) ** gam > 255):
                target[y][x][index] = 255; 
    return target

normal = cv2.imread('normal.jpg')
normal = cv2.resize(normal, (x_res, y_res)) 
#gray_normal = cv2.cvtColor(normal, cv2.COLOR_BGR2GRAY)

u_expose = cv2.imread('u_expose.jpg')
u_expose = cv2.resize(u_expose, (x_res, y_res)) 
#gray_u_expose = cv2.cvtColor(u_expose, cv2.COLOR_BGR2GRAY)

corrected = cv2.imread('u_expose.jpg')
corrected = cv2.resize(corrected, (x_res, y_res)) 

best_corrected = cv2.imread('u_expose.jpg')
best_corrected = cv2.resize(best_corrected, (x_res, y_res)) 

#gray_corrected = cv2.cvtColor(corrected, cv2.COLOR_BGR2GRAY)
#The best gamma_r was 0.8976000000000001
#The best gamma_g was 0.7664
#The best gamma_b was 0.5154



num_gammas = 1000
min_gamma_r = 0.5
min_gamma_g = 0.5
min_gamma_b = 0.3
max_gamma_r = 1
max_gamma_g = 1
max_gamma_b = 1
step_r = (max_gamma_r - min_gamma_r)/num_gammas
step_g = (max_gamma_g - min_gamma_g)/num_gammas
step_b = (max_gamma_b - min_gamma_b)/num_gammas
gammas_r = [None] * num_gammas
gammas_g = [None] * num_gammas
gammas_b = [None] * num_gammas

errors_r = [None] * num_gammas
errors_g = [None] * num_gammas
errors_b = [None] * num_gammas

for i in range(num_gammas):
    gammas_r[i] = min_gamma_r + step_r * i
    gammas_g[i] = min_gamma_g + step_g * i
    gammas_b[i] = min_gamma_b + step_b * i


#best_corrected = corrected
best_error_r = 100000000000
best_error_g = 100000000000
best_error_b = 100000000000
best_gamma_r = 0
best_gamma_g = 0
best_gamma_b = 0

#print(MSE(u_expose, normal))

for n in range(len(gammas_r)):
    print("using gamma", gammas_r[n])
    corrected = single_correct(corrected, u_expose, gammas_r[n], 0)
    corrected = single_correct(corrected, u_expose, gammas_g[n], 1)
    corrected = single_correct(corrected, u_expose, gammas_b[n], 2)
    print("calculating error for gamma", gammas_r[n])
    error_r = MSE(corrected, normal, 0)
    error_g = MSE(corrected, normal, 1)
    error_b = MSE(corrected, normal, 2)
    print("red error:",error_r, "blue error:", error_b, "green error:", error_g)

    
    if(error_r < best_error_r):
        best_error_r = error_r
        best_gamma_r = gammas_r[n]
    if(error_g < best_error_g):
        best_error_g = error_g
        best_gamma_g = gammas_g[n]
    if(error_b < best_error_b):
        best_error_b = error_b
        best_gamma_b = gammas_b[n]

    errors_r[n] = error_r
    errors_g[n] = error_g
    errors_b[n] = error_b
    print()
    print()


        #best_corrected = corrected
print("The best gamma_r was", best_gamma_r)
print("The best gamma_g was", best_gamma_g)
print("The best gamma_b was", best_gamma_b)
print("The best error_r was", best_error_r)
print("The best error_g was", best_error_g)
print("The best error_b was", best_error_b)
print()

gamma_new_r = best_gamma_r
gamma_new_g = best_gamma_g
gamma_new_b = best_gamma_b
for x in range(x_res):
    for y in range(y_res):
        best_corrected[y][x][0] = ((u_expose[y][x][0] ** (1/gamma_new_r)) * 2) ** gamma_new_r
        best_corrected[y][x][1] = ((u_expose[y][x][1] ** (1/gamma_new_g)) * 2) ** gamma_new_g
        best_corrected[y][x][2] = ((u_expose[y][x][2] ** (1/gamma_new_b)) * 2) ** gamma_new_b
        if(best_corrected[y][x][0] > 255):
            best_corrected[y][x][0] = 255; 
        if(best_corrected[y][x][1] > 255):
            best_corrected[y][x][1] = 255; 
        if(best_corrected[y][x][2] > 255):
            best_corrected[y][x][2] = 255; 


fig, axr = plt.subplots()
fig, axg = plt.subplots()
fig, axb = plt.subplots()
axr.plot(gammas_r, errors_r, label = "MSE of red gammas")
axg.plot(gammas_g, errors_g, label = "MSE of green gammas")
axb.plot(gammas_b, errors_b, label = "MSE of blue gammas")
plt.legend()
plt.show()

cv2.imshow('corrected', best_corrected)
cv2.imshow('under exposed', u_expose)
cv2.imshow('normal', normal)
cv2.waitKey(0)
