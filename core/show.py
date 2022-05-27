import pygame

cnt = 0

pygame.init()
screen=pygame.display.set_caption('preview')
screen=pygame.display.set_mode([800,600])
screen.fill([255,255,255])
pygame.display.flip()

f = open('./data/board_latest.txt','r')
while True:
    try:
        st = f.readline(9)
        if st == '':
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit(0)
            continue
        x = st[0]+st[1]+st[2]
        y = st[3]+st[4]+st[5]
        colr = st[6]
        colg = st[7]
        colb = st[8]

        # print(x,y,colr,colg,colb)
        x = int(x,16)
        y = int(y,16)
        colr = int(colr,16)
        colg = int(colg,16)
        colb = int(colb,16)
        # print(x,y,colr,colg,colb)
        screen.set_at([x,y],[colr*16,colg*16,colb*16])
        
        
            # print('flush')
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit(0)
        
            
    except Exception as e:
        pass

    