import requests
for i in range(0,100):
    for j in range(0,200):
        # print('http://127.0.0.1:5000/paint?x='+str(i)+'&&y='+str(j)+'&&col=00ff00&&token=token1')
        print(requests.get('http://127.0.0.1:5000/paint?x='+str(i)+'&&y='+str(j)+'&&col=f00&&token=token1').content)