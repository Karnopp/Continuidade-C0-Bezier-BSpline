import numpy as np
from scipy.special import comb
from matplotlib import pyplot as plt

def bezier(pontos_controle, nr_pontos_curva):
    n=len(pontos_controle)-1 #n eh o grau, ou seja, nr de pontos de controle - 1
    x_ponto_controle = [p[0] for p in pontos_controle]
    y_ponto_controle = [p[1] for p in pontos_controle]
    t = np.linspace(0, 1, nr_pontos_curva)
    x_final=[0]*nr_pontos_curva
    y_final=[0]*nr_pontos_curva
    for k in range(0,len(t)):
        for i in range(0,len(pontos_controle)):
            aux = binomio(i,n)*((1-t[k])**(n-i))*(t[k]**i)
            x_final[k]=x_final[k] + x_ponto_controle[i] * aux
            y_final[k]=y_final[k] + y_ponto_controle[i] * aux
    return x_final,y_final

def binomio(i,n):
    return fatorial(n)/(fatorial(i)*fatorial(n-i))

def fatorial(n):
    n_fat=1
    for i in range(2,n+1):
        n_fat = n_fat * i
    return n_fat



def bspline(pontos_controle, nr_pontos_curva):
    n=len(pontos_controle)-1
    k=len(pontos_controle) #ordem 6, grau = ordem - 1
    x_ponto_controle = [p[0] for p in pontos_controle]
    y_ponto_controle = [p[1] for p in pontos_controle]
    knots=[0,0,0,0,0,0,1,1,1,1,1,1]
    t = np.linspace(0, 1, nr_pontos_curva)
    x_final=[0]*nr_pontos_curva
    y_final=[0]*nr_pontos_curva
    for j in range(0,len(t)):
        for i in range(0,len(pontos_controle)):
            aux=Boor(i,k,t[j],knots)
            x_final[j]=x_final[j] + (x_ponto_controle[i] * aux)
            y_final[j]=y_final[j] + (y_ponto_controle[i] * aux)
    return x_final,y_final
def Boor(i, k, t, knots):
    if k == 1:
        if(knots[i] <= t and t <= knots[i+1]):
            return 1.0
        else:
            return 0.0
    else:
        if(knots[i+k-1]-knots[i] == 0):
            aux1=0
        else:
            aux1=((t-knots[i])/(knots[i+k-1]-knots[i])) * Boor(i,k-1,t,knots)
        if(knots[i+k]-knots[i+1] == 0 ):
            aux2=0
        else:
            aux2=((knots[i+k]-t)/(knots[i+k]-knots[i+1])) * Boor(i+1,k-1,t,knots)
        return  aux1+aux2



if __name__ == "__main__":
    grau=5
    numero_pontos_controle = grau +1
    print("Gostaria de usar os pontos de controle predeterminados ou gera-los aleatoriamente")
    print("1 - predeterminado, 2 - gerar aleatoriamente")
    op=int(input())
    pontos_controle=[[0 for x in range(2)] for y in range(grau)]
    if(op==1):
        pontos_controle_bezier= [[31, 21],
                                 [14, 5],
                                 [ 8, 41],
                                 [12, 47],
                                 [34, 31],
                                 [34, 38]]

        pontos_controle_spline= [[40, 45],
                                 [99, 18],
                                 [88, 76],
                                 [72, 88],
                                 [98, 31]]
        pontos_controle=np.concatenate((pontos_controle_bezier,pontos_controle_spline),axis=0)
        pontos_controle_spline=np.concatenate(([pontos_controle_bezier[grau]],pontos_controle_spline),axis=0)
        #print(len(pontos_controle))
    else:
        print("Gerando pontos de controle aleatoriamente")
        pontos_controle_bezier = np.random.rand(grau+1,2)*50
        pontos_controle_spline = np.random.rand(grau,2)*100
        pontos_controle=np.concatenate((pontos_controle_bezier,pontos_controle_spline),axis=0)
        pontos_controle_spline=np.concatenate(([pontos_controle_bezier[grau]],pontos_controle_spline),axis=0)
        print(pontos_controle_bezier)
        print(pontos_controle_spline)
        #print(len(pontos_controle))

    print("Gerando a curva...")

    x_ponto_controle = [p[0] for p in pontos_controle]
    y_ponto_controle = [p[1] for p in pontos_controle]
    x_bezier_c0,y_bezier_c0=bezier(pontos_controle_bezier, 1000)
    x_spline_c0, y_spline_c0 = bspline(pontos_controle_spline, 1000)
    #plt.plot(x_ponto_controle, y_ponto_controle)
    for i in range(0,len(pontos_controle)):
        if(i<grau):
            plt.plot(x_ponto_controle[i], y_ponto_controle[i], "o", color='C1')
        if(i==grau):
            plt.plot(x_ponto_controle[i], y_ponto_controle[i], "ro", label='C0')
        if(i>grau):
            plt.plot(x_ponto_controle[i], y_ponto_controle[i], "o", color='C10')
        plt.annotate(u'P'+str(i), xy=(x_ponto_controle[i], y_ponto_controle[i]))
    plt.plot(x_bezier_c0,y_bezier_c0, 'C1', label='Bézier')
    plt.plot(x_spline_c0, y_spline_c0, 'C10', label='B-Spline')
    plt.legend()
    plt.ylabel('Eixo Y')
    plt.xlabel('Eixo X')
    plt.title(u'Bézier e B-Spline de grau '+str(grau)+' com continuidade C0')
    plt.show()
