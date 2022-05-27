import pygame

cnt = 0

x=0
y=0
cntt=0

pygame.init()
screen=pygame.display.set_caption('preview')
screen=pygame.display.set_mode([800,600])
screen.fill([255,255,255])
pygame.display.flip()

f = open('./data/board_rendered.txt','r')
while True:
    try:
        st = f.readline(3)
        if st == '':
            break
        x = cntt%800
        y = int(cntt/800)
        colr = st[0]
        colg = st[1]
        colb = st[2]

        # print(x,y,colr,colg,colb,st)
        colr = int(colr,16)
        colg = int(colg,16)
        colb = int(colb,16)
        # print(x,y,colr,colg,colb)
        # print(x,y,colr,colg,colb)
        screen.set_at([x,y],[colr*16,colg*16,colb*16])
        # pygame.display.flip()
        
        cntt = cntt+1
        
            
    except Exception as e:
        pass

print("done")

while True:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit(0)