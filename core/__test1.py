import requests
for i in range(0,100):
    for j in range(0,200):
        # print('http://127.0.0.1:5000/paint?x='+str(i)+'&&y='+str(j)+'&&col=00ff00&&token=token1')
        cont = requests.get('https://127.0.0.1:5000/paint?x='+str(i)+'&&y='+str(j)+'&&col=f00&&token=token1')
        print(cont)
        # print(requests.get('https://5000-rickyxrc-pixelboard-lj25edabenq.ws-us46.gitpod.io/paint?x='+str(i)+'&&y='+str(j)+'&&col=f00&&token=token1').content)