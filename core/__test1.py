import requests
for i in range(100,300):
    for j in range(100,200):
        # print('http://127.0.0.1:5000/paint?x='+str(i)+'&&y='+str(j)+'&&col=00ff00&&token=token1')
        requests.get('http://127.0.0.1:5000/paint?x='+str(i)+'&&y='+str(j)+'&&col=00f&&token=token1')