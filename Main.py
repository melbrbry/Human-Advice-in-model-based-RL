"""
Created on Tue May 15 11:33:06 2018
@author: Jose Jaramillo

Board with an agent with nails a key and a door.

"""

import pygame
import sys
import time
import random
import RMax
import HRI
import numpy as np
pygame.init()
pygame.font.init()
# init_game starts a board with squares of 50 pixels 
# height and width being the n*m squares. They are separated by 2pix
def startpage():
    global starting
    global boardSize
    boardSize=[20,15]
    font=pygame.font.SysFont("Century Gothic", 48)
    font1=pygame.font.SysFont("Century Gothic", 24)
    screen = pygame.display.set_mode(((52*boardSize[0])+2,(52*boardSize[1])+102))    
    screen.fill((96,96,96))
    text = font.render("E S C A P E !", True, (255, 255, 255))
    agentsize=4
    font2=pygame.font.SysFont("timesnewroman", 24)
    agent=drawagent(agentsize)
    screen.blit(agent,[(((boardSize[0]*51)/2)-(agentsize*25)),200])


    if starting ==0:
        
        pygame.draw.rect(screen,(235,235,235),(((boardSize[0]*51)/2)-250,((boardSize[1]*51)/2),500,130),0)
        pygame.draw.rect(screen,(0,0,0),(((boardSize[0]*51)/2)-250,((boardSize[1]*51)/2),500,130),5)
        
        text1 = font1.render("I need to escape from the room!", True, (0, 0, 0))
        text2 = font1.render("Can you help me?", True, (0, 0, 0))
        
        screen.blit(text,
            (((boardSize[0]*51)/2) - text.get_width() // 2, 150 - text.get_height() // 2))
        screen.blit(text1,
            (((boardSize[0]*51)/2) - text1.get_width() // 2, ((boardSize[1]*51)+80)/2 - text1.get_height() // 2))
        screen.blit(text2,
            (((boardSize[0]*51)/2) - text2.get_width() // 2, ((boardSize[1]*51)+160)/2 - text2.get_height() // 2))
        #Draw agent with "agentsize" multiplyer size
#        agent=drawagent(agentsize)
#        screen.blit(agent,[(((boardSize[0]*51)/2)-(agentsize*25)),200])
        
    #    text = font.render("Score:" + str(reward), True, (255, 255, 255))
        text3 = font2.render("Press any key to continue", True, (255, 255, 255))
        
    #    screen.blit(text,
    #        (((boardSize[0]*51)/2) - text.get_width() // 2, (((boardSize[1]*51)/2)-50) - text.get_height() // 2))
        screen.blit(text3,
            (100, ((boardSize[1]*51)+80) - text3.get_height() // 2))
    elif starting ==1:
        pygame.draw.rect(screen,(235,235,235),(((boardSize[0]*51)/2)-250,((boardSize[1]*51)/2),500,170),0)
        pygame.draw.rect(screen,(0,0,0),(((boardSize[0]*51)/2)-250,((boardSize[1]*51)/2),500,170),5)
        text1 = font1.render("Manual control (M)", True, (0, 0, 0))
        text2 = font1.render("I can give you some tips (T)", True, (0, 0, 0))
        text4 = font1.render("Learn it all by yourself (L)", True, (0, 0, 0))
        
        screen.blit(text,
            (((boardSize[0]*51)/2) - text.get_width() // 2, 150 - text.get_height() // 2))
        screen.blit(text1,
            (((boardSize[0]*51)/2) - text1.get_width() // 2, ((boardSize[1]*51)+80)/2 - text1.get_height() // 2))
        screen.blit(text2,
            (((boardSize[0]*51)/2) - text2.get_width() // 2, ((boardSize[1]*51)+160)/2 - text2.get_height() // 2))
        screen.blit(text4,
            (((boardSize[0]*51)/2) - text4.get_width() // 2, ((boardSize[1]*51)+240)/2 - text4.get_height() // 2))
        #Draw agent with "agentsize" multiplyer size

        text3 = font2.render("Press 'm', 't', 'l' or 'x' to exit", True, (255, 255, 255))
        
        screen.blit(text3,
            (100, ((boardSize[1]*51)+80) - text3.get_height() // 2))
    elif starting ==2:
        pygame.draw.rect(screen,(235,235,235),(((boardSize[0]*51)/2)-350,((boardSize[1]*51)/2),700,170),0)
        pygame.draw.rect(screen,(0,0,0),(((boardSize[0]*51)/2)-350,((boardSize[1]*51)/2),700,170),5)
        text1 = font1.render("You should avoid Nails (a)", True, (0, 0, 0))
        text2 = font1.render("You should go to the door after taking the key (b)", True, (0, 0, 0))
#        text4 = font1.render("-lie- you should collect the Nails (c)", True, (0, 0, 0))
        
        screen.blit(text,
            (((boardSize[0]*51)/2) - text.get_width() // 2, 150 - text.get_height() // 2))
        screen.blit(text1,
            (((boardSize[0]*51)/2) - text1.get_width() // 2, ((boardSize[1]*51)+80)/2 - text1.get_height() // 2))
        screen.blit(text2,
            (((boardSize[0]*51)/2) - text2.get_width() // 2, ((boardSize[1]*51)+160)/2 - text2.get_height() // 2))
#        screen.blit(text4,
#            (((boardSize[0]*51)/2) - text4.get_width() // 2, ((boardSize[1]*51)+240)/2 - text4.get_height() // 2))
        #Draw agent with "agentsize" multiplyer size

        text3 = font2.render("Press 'a', 'b' or 'x' to exit", True, (255, 255, 255))
        
        screen.blit(text3,
            (100, ((boardSize[1]*51)+80) - text3.get_height() // 2))
    pygame.display.update()
    return
def drawagent(agentsize):
    screen=pygame.Surface([50*agentsize,50*agentsize])
    screen.fill((0,0,255))
    screen.set_colorkey((0,0,255))
    pygame.draw.ellipse(screen,(255,255,255),(np.multiply((5,12,40,26),agentsize)))
    pygame.draw.ellipse(screen,(0,0,0),np.multiply((4,11,42,28),agentsize),2*agentsize)
    pygame.draw.circle(screen,(0,128,255),np.multiply((16,25),agentsize),4*agentsize)
    pygame.draw.circle(screen,(255,0,127),np.multiply((34,25),agentsize),4*agentsize)
    pygame.draw.circle(screen,(0,0,0),np.multiply((16,25),agentsize),1*agentsize)
    pygame.draw.circle(screen,(0,0,0),np.multiply((34,25),agentsize),1*agentsize)
    pygame.draw.line(screen,(0,0,0),np.multiply((22,30),agentsize),np.multiply((28,30),agentsize),2*agentsize)\
    
    return screen
def init_game(boardSize):
    global reward
    screen = pygame.display.set_mode(((52*boardSize[0])+2,(52*boardSize[1])+102))    
    screen.fill((96,96,96))
    for i in range (boardSize[0]):
        for ii in range (boardSize[1]):
            pygame.draw.rect(screen, (224,224,224),
                             (2+i*52,2+ii*52,50,50),0)
    font=pygame.font.SysFont("timesnewroman", 24)
    text = font.render("Score:" + str(reward), True, (255, 255, 255))
    text1 = font.render("Press X to exit or R to restart", True, (255, 255, 255))
    
    screen.blit(text,
        (150 - text.get_width() // 2, ((boardSize[1]*51)+50) - text.get_height() // 2))
    screen.blit(text1,
        (150 - text1.get_width() // 2, ((boardSize[1]*51)+80) - text1.get_height() // 2))
    pygame.display.update()
    return screen

# Agent draws the agent in the posX by posY possition

class Agent(pygame.sprite.Sprite):
    def __init__(self):
        global boardSize
        super().__init__()  #super calls the AGENT constructor
        # Set transparent background
        self.image= pygame.Surface([50,50])
        self.image.fill((0,0,255))
        self.image.set_colorkey((0,0,255))
        self.haveKey=False
        self.returnCurrentPos=(0,0)
        self.StartingPos=(0,0)
        self.returnLastAction="Stop"
        # Drawing
        #pygame.draw.rect(self.image,(150,255,100),(20,20,20,20))
        #pygame.draw.rect(self.image,(100,255,150),(0,0,20,20))
        pygame.draw.ellipse(self.image,(255,255,255),(5,12,40,26))
        pygame.draw.ellipse(self.image,(0,0,0),(4,11,42,28),2)
        pygame.draw.circle(self.image,(0,128,255),(16,25),4)
        pygame.draw.circle(self.image,(255,0,127),(34,25),4)
        pygame.draw.circle(self.image,(0,0,0),(16,25),1)
        pygame.draw.circle(self.image,(0,0,0),(34,25),1)
        pygame.draw.line(self.image,(0,0,0),(22,30),(28,30),2)
        
        # get rect will get all the objects in the rectangle as one
        self.rect = self.image.get_rect()
    def pos(self,posx,posy):
        self.rect.x=(2+(posx*52))
        self.rect.y=(2+(posy*52))
        self.returnCurrentPos=(posx,posy)
        
    def move(self,Action):
        if Action=="UP" and self.returnCurrentPos[1]>0:
            self.pos(self.returnCurrentPos[0],(self.returnCurrentPos[1]-1))
        elif Action=="DOWN" and self.returnCurrentPos[1]<(boardSize[1]-1):
            self.pos(self.returnCurrentPos[0],(self.returnCurrentPos[1]+1))
        elif Action=="LEFT" and self.returnCurrentPos[0]>0:
            self.pos(self.returnCurrentPos[0]-1,(self.returnCurrentPos[1]))
        elif Action=="RIGHT" and self.returnCurrentPos[0]<(boardSize[0]-1):
            self.pos(self.returnCurrentPos[0]+1,(self.returnCurrentPos[1]))
        else:
            print("Corrupt movement!")
        self.returnLastAction=Action

class nail(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  #super calls the AGENT constructor
        self.image= pygame.Surface([50,50])
        self.image.fill((0,0,255))
        self.image.set_colorkey((0,0,255))
        self.reward=-50
        
        pygame.draw.lines(self.image,(0,0,0),True,((10,10),(40,10),(37,15),
                                      (28,15),(28,35),(25,40),(22,35),(22,15),
                                      (20,15),(13,15)),3)

        self.rect = self.image.get_rect()
    def pos(self,posx,posy):
        self.rect.x=(2+(posx*52))
        self.rect.y=(2+(posy*52))
        self.returnCurrentPos=(posx,posy)

class key(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  #super calls the AGENT constructor
        self.image= pygame.Surface([50,50])
        self.image.fill((0,0,255))
        self.image.set_colorkey((0,0,255))
        self.reward=1000
        self.StartingPos=(0,0)
        
        pygame.draw.circle(self.image,(230,230,0),(25,13),10)
        pygame.draw.circle(self.image,(0,0,0),(25,13),10,2)
        pygame.draw.circle(self.image,(0,0,255),(25,13),5)
        pygame.draw.circle(self.image,(0,0,0),(25,12),5,1)
        pygame.draw.rect(self.image,(230,230,0),(22,21,6,22),0)
        pygame.draw.rect(self.image,(0,0,0),(22,21,6,22),2)
        pygame.draw.line(self.image,(0,0,0),(36,38),(28,38),4)
        pygame.draw.line(self.image,(0,0,0),(36,31),(28,31),4)
        self.rect = self.image.get_rect()
    def pos(self,posx,posy):
        self.rect.x=(2+(posx*52))
        self.rect.y=(2+(posy*52))
        self.returnCurrentPos=(posx,posy)
        
class door(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  #super calls the AGENT constructor
        self.image= pygame.Surface([50,50])
        self.image.fill((0,0,255))
        self.image.set_colorkey((0,0,255))
        self.reward=5000
        
#        pygame.draw.circle(self.image,(230,230,0),(25,13),10)
#        pygame.draw.circle(self.image,(0,0,0),(25,13),10,2)
#        pygame.draw.circle(self.image,(0,0,255),(25,13),5)

        pygame.draw.rect(self.image,(255,0,0),(13,8,24,34),0)
        pygame.draw.rect(self.image,(0,0,0),(13,8,24,34),2)
        pygame.draw.rect(self.image,(0,0,0),(18,12,14,10),1)
        pygame.draw.rect(self.image,(0,0,0),(18,28,14,10),1)
        pygame.draw.circle(self.image,(0,0,0),(32,25),2)
#        pygame.draw.rect(self.image,(0,0,0),(13,8,24,34),1)
        self.rect = self.image.get_rect()
    def pos(self,posx,posy):
        self.rect.x=(2+(posx*52))
        self.rect.y=(2+(posy*52))
        self.returnCurrentPos=(posx,posy)
class wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  #super calls the AGENT constructor
        self.image= pygame.Surface([50,50])
        self.image.fill((0,0,255))
        self.image.set_colorkey((0,0,255))
        self.reward=5000
        
#        pygame.draw.circle(self.image,(230,230,0),(25,13),10)
#        pygame.draw.circle(self.image,(0,0,0),(25,13),10,2)
#        pygame.draw.circle(self.image,(0,0,255),(25,13),5)

        pygame.draw.rect(self.image,(202,143,66),(0,0,50,50),0)
        pygame.draw.rect(self.image,(0,0,0),(0,0,50,50),2)
        pygame.draw.rect(self.image,(0,0,0),(0,0,25,10),1)
        pygame.draw.rect(self.image,(0,0,0),(25,0,25,10),1)
        pygame.draw.rect(self.image,(0,0,0),(0,20,25,10),1)
        pygame.draw.rect(self.image,(0,0,0),(25,20,25,10),1)
        pygame.draw.rect(self.image,(0,0,0),(0,40,25,10),1)
        pygame.draw.rect(self.image,(0,0,0),(25,40,25,10),1)
        
        pygame.draw.rect(self.image,(0,0,0),(0,10,12,10),1)
        pygame.draw.rect(self.image,(0,0,0),(12,10,25,10),1)
        pygame.draw.rect(self.image,(0,0,0),(37,10,12,10),1)
        pygame.draw.rect(self.image,(0,0,0),(0,30,12,10),1)
        pygame.draw.rect(self.image,(0,0,0),(12,30,25,10),1)
        pygame.draw.rect(self.image,(0,0,0),(37,30,12,10),1)
        #        pygame.draw.rect(self.image,(0,0,0),(13,8,24,34),1)
        self.rect = self.image.get_rect()
    def pos(self,posx,posy):
        self.rect.x=(2+(posx*52))
        self.rect.y=(2+(posy*52))
        self.returnCurrentPos=(posx,posy)
def updateReward():
    global reward
    global playing

#    global KepPos
    global boardSize
    #moving reward
    reward+=-1
    refresh()
    #Nail position? 
    for i in range(len(NailsPos)):
        if not((agent.returnCurrentPos-NailsPos[i]).any()):
            reward+=-10
            refresh()
    for i in range(len(WallPos)):
        if not((agent.returnCurrentPos-WallPos[i]).any()):
            print("Ouch!")
            if agent.returnLastAction=="UP":
                agent.move("DOWN")
            elif agent.returnLastAction=="DOWN":
                agent.move("UP")
            elif agent.returnLastAction=="LEFT":
                agent.move("RIGHT")
            elif agent.returnLastAction=="RIGHT":
                agent.move("LEFT")
            else:
                print("this should not happen! call Jose")
            refresh()
            
    if not((agent.returnCurrentPos-np.asarray(KEY.returnCurrentPos)).any()):
        reward+=1000
        agent.haveKey=True
        KEY.pos(boardSize[0]-1,boardSize[1])
        refresh()
        
    if (not((agent.returnCurrentPos-DoorPos).any()) and agent.haveKey):
        reward+=1000
        playing =False
        finishGame()
        
    return reward

def populateBoard():
    
    global boardSize
    global all_sprites_list
    all_sprites_list = pygame.sprite.Group()
    agent = Agent()
    agent.pos(random.randint(0,boardSize[0]-1),random.randint(0,boardSize[1]-1))
    all_sprites_list.add(agent)
    
    numbOnails=int(0.15*(boardSize[0]*boardSize[1]))
    numbOwalls=int(0.07*(boardSize[0]*boardSize[1]))
    keyPos=np.zeros(2)
    keyPos[0]=random.randint(0,boardSize[0]-1)
    keyPos[1]=random.randint(0,boardSize[1]-1)
    Key=key()
    Key.pos(keyPos[0],keyPos[1])
    all_sprites_list.add(Key)
    doorPos=np.zeros(2)
    doorPos[0]=random.randint(0,boardSize[0]-1)
    doorPos[1]=random.randint(0,boardSize[1]-1)
    Door=door()
    Door.pos(doorPos[0],doorPos[1])
    all_sprites_list.add(Door) 
    nailPos=np.zeros([numbOnails,2])
    
    for i in range(numbOnails):
        nailPos[i,0]=random.randint(0,boardSize[0]-1)
        nailPos[i,1]=random.randint(0,boardSize[1]-1)
        while not((nailPos[i]-Key.returnCurrentPos).any()):
            nailPos[i,0]=random.randint(0,boardSize[0]-1)
            nailPos[i,1]=random.randint(0,boardSize[1]-1)
        while not((nailPos[i]-Door.returnCurrentPos).any()):
            nailPos[i,0]=random.randint(0,boardSize[0]-1)
            nailPos[i,1]=random.randint(0,boardSize[1]-1)
        GenericNail=nail()
        GenericNail.pos(nailPos[i,0],nailPos[i,1])
        all_sprites_list.add(GenericNail) 
    
    wallPos=np.zeros([numbOwalls,2])
#    
    for i in range(numbOwalls):
        wallPos[i,0]=random.randint(0,boardSize[0]-1)
        wallPos[i,1]=random.randint(0,boardSize[1]-1)
        while not((wallPos[i]-Key.returnCurrentPos).any()):
            nailPos[i,0]=random.randint(0,boardSize[0]-1)
            nailPos[i,1]=random.randint(0,boardSize[1]-1)
        while not((wallPos[i]-Door.returnCurrentPos).any()):
            nailPos[i,0]=random.randint(0,boardSize[0]-1)
            nailPos[i,1]=random.randint(0,boardSize[1]-1)
        GenericWall=wall()
        GenericWall.pos(wallPos[i,0],wallPos[i,1])
        all_sprites_list.add(GenericWall) 
    return nailPos,doorPos,keyPos,Key,agent,wallPos
def finishGame():
#    global all_sprites_list
#    print(all_sprites_list)
#    global agent
#    del agent
    global boardSize
    if playing==True:
        boardSize[0]=random.randint(9,15)
        boardSize[1]=random.randint(9,12)
        init_game(boardSize)
        refresh()
        global reward,NailsPos,DoorPos,KeyPos,KEY,agent,WallPos
        
        reward=0
        NailsPos,DoorPos,KeyPos,KEY,agent,WallPos=populateBoard()  
    
    else:
        screen.fill((96,96,255))
        font=pygame.font.SysFont("timesnewroman", 34)
        text = font.render("Score:" + str(reward), True, (255, 255, 255))
        text1 = font.render("Press X to exit, R to restart, M jump to Main Menu", True, (255, 255, 255))
        if Rmax==True:
            text2 = font.render("Training score:" + str(comreward), True, (255, 255, 255))
            screen.blit(text2,
            (((boardSize[0]*51)/2) - text1.get_width() // 2, (((boardSize[1]*51)/2)+50) - text1.get_height() // 2))
        screen.blit(text,
            (((boardSize[0]*51)/2) - text.get_width() // 2, (((boardSize[1]*51)/2)-50) - text.get_height() // 2))
        screen.blit(text1,
            (((boardSize[0]*51)/2) - text1.get_width() // 2, ((boardSize[1]*51)/2) - text1.get_height() // 2))
        pygame.display.update()
    
    
    
    return True
def refresh():
    init_game(boardSize)
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    pygame.display.flip()

def getstate():
    finishGame()
    refresh()
    Board=np.zeros([boardSize[1]+2,boardSize[0]+2],dtype=str)
    Board[:,:]="."
    Board[:,[0,boardSize[0]+1]]='*'
    Board[[0,boardSize[1]+1],:]='*'
    for i in range (len(NailsPos)):
        Board[1+int(NailsPos[i,1]),1+int(NailsPos[i,0])]='N' 
    for i in range (len(WallPos)):
        Board[1+int(WallPos[i,1]),1+int(WallPos[i,0])]='*' 
    Board[1+int(KeyPos[1]),1+int(KeyPos[0])]='K'
    Board[1+int(DoorPos[1]),1+int(DoorPos[0])]='D'
    Board[1+int(agent.returnCurrentPos[1]),1+int(agent.returnCurrentPos[0])]='S'
    agent.StartingPos=agent.returnCurrentPos
    KEY.StartingPos=KEY.returnCurrentPos
    return Board
    
def rmaxplay():
    print("RMAX")
    global rmax
    rmax=True
    global comreward
    global reward
    STATE=getstate()
    learning,playingEstrategy=RMax.main(STATE)
    for i in range(len(learning)):
        if learning[i]=='L':
            agent.move("LEFT")
#                refresh()
            updateReward()
        elif learning[i]=='R':
            agent.move("RIGHT")
#                refresh()
            updateReward()
                
        elif learning[i]=='U':
            agent.move("UP")
#                refresh() 
            updateReward()
                
        elif learning[i]=='D':
            agent.move("DOWN")
#                refresh()
            updateReward()
        else:
            print("this should not happen! call Jose") 
        if not((agent.returnCurrentPos-DoorPos).any()) and agent.haveKey:
            agent.pos(agent.StartingPos[0],agent.StartingPos[1])
            KEY.pos(KEY.StartingPos[0],KEY.StartingPos[1])
            agent.haveKey=False
            refresh()
            print("Victory!")
        time.sleep(0.05)
    comreward=reward
    reward=0
    print("Playing phase")
    agent.pos(agent.StartingPos[0],agent.StartingPos[1])
    KEY.pos(KEY.StartingPos[0],KEY.StartingPos[1])
    refresh()
    for ii in range(len(playingEstrategy)):
        if playingEstrategy[ii]=='L':
            agent.move("LEFT")
#                refresh()
            updateReward()
        elif playingEstrategy[ii]=='R':
            agent.move("RIGHT")
#                refresh()
            updateReward()
                
        elif playingEstrategy[ii]=='U':
            agent.move("UP")
#                refresh() 
            updateReward()
                
        elif playingEstrategy[ii]=='D':
            agent.move("DOWN")
#                refresh()
            updateReward()
        else:
            print("this should not happen! call Jose") 
        time.sleep(0.5)
        global playing
        playing=False
    return learning,playingEstrategy,STATE
    
def adviseplay(advise):
    print("Advise")
    if advise== [0]:
        print("Key before door")
    elif advise==[1]:
        print("Avoid nails")
    global rmax
    rmax=True
    global comreward
    global reward
    STATE=getstate()
    learning,playingEstrategy=HRI.main(STATE,advise)
    for i in range(len(learning)):
        if learning[i]=='L':
            agent.move("LEFT")
#                refresh()
            updateReward()
        elif learning[i]=='R':
            agent.move("RIGHT")
#                refresh()
            updateReward()
                
        elif learning[i]=='U':
            agent.move("UP")
#                refresh() 
            updateReward()
                
        elif learning[i]=='D':
            agent.move("DOWN")
#                refresh()
            updateReward()
        else:
            print("this should not happen! call Jose") 
        if not((agent.returnCurrentPos-DoorPos).any()) and agent.haveKey:
            agent.pos(agent.StartingPos[0],agent.StartingPos[1])
            KEY.pos(KEY.StartingPos[0],KEY.StartingPos[1])
            agent.haveKey=False
            refresh()
            print("Victory!")
        time.sleep(0.05)
    comreward=reward
    reward=0
    print("Playing phase")
    agent.pos(agent.StartingPos[0],agent.StartingPos[1])
    KEY.pos(KEY.StartingPos[0],KEY.StartingPos[1])
    refresh()
    for ii in range(len(playingEstrategy)):
        if playingEstrategy[ii]=='L':
            agent.move("LEFT")
#                refresh()
            updateReward()
        elif playingEstrategy[ii]=='R':
            agent.move("RIGHT")
#                refresh()
            updateReward()
                
        elif playingEstrategy[ii]=='U':
            agent.move("UP")
#                refresh() 
            updateReward()
                
        elif playingEstrategy[ii]=='D':
            agent.move("DOWN")
#                refresh()
            updateReward()
        else:
            print("this should not happen! call Jose") 
        time.sleep(0.5)
        global playing
        playing=False
    return learning,playingEstrategy,STATE
reward=0
comreward=0
boardSize=[20,15]
screen=init_game(boardSize)
NailsPos,DoorPos,KeyPos,KEY,agent,WallPos=populateBoard()
STATE=[]
#refresh()
running = True
Rmax=False
playing =False
starting=0; #help me navigate through the starting menu
startpage()
#counter=0
clock=pygame.time.Clock()
font=pygame.font.SysFont("timesnewroman", 32)
while running:
    
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_x]:
            running = False
            pygame.display.quit()
            pygame.font.quit()
            pygame.quit()
            
            sys.exit()
        if playing==True:
            if keys[pygame.K_LEFT]:
                agent.move("LEFT")
#                refresh()
                updateReward()
                
            if keys[pygame.K_RIGHT]:
                agent.move("RIGHT")
#                refresh()
                updateReward()
                
            if keys[pygame.K_UP]:
                agent.move("UP")
#                refresh() 
                updateReward()
                
            if keys[pygame.K_DOWN]:
                agent.move("DOWN")
#                refresh()
                updateReward()
                
        if keys[pygame.K_r] and starting ==5:
            playing =True
            finishGame()
            refresh()
        if event.type == pygame.KEYDOWN and starting ==0:
            starting =1
            startpage()
        elif keys[pygame.K_m] and starting ==1 and playing ==False:
            finishGame()
            refresh()
            playing=True
            starting =5
        elif keys[pygame.K_t] and starting ==1:
            starting =2
            startpage()
        elif keys[pygame.K_a] and starting ==2:
            starting =3
            Rmax=True
            playing=True
            x,y,z=adviseplay([1])
            
            print("LEANING:")
            print(x)
            print("PLAYING:")
            print(y)
            print("on:")
            print(z)
        elif keys[pygame.K_b] and starting ==2:
            starting =3
            Rmax=True
            playing=True
            x,y,z=adviseplay([0])
            
            print("LEANING:")
            print(x)
            print("PLAYING:")
            print(y)
            print("on:")
            print(z)
        elif keys[pygame.K_l] and starting ==1:
            starting =3
            Rmax=True
            playing=True
            x,y,z=rmaxplay()
            
            print("LEANING:")
            print(x)
            print("PLAYING:")
            print(y)
            print("on:")
            print(z)
        elif keys[pygame.K_m] and starting ==5 and playing ==False:
            starting =0
            startpage()
        elif starting==3 and playing==False and keys[pygame.K_r]:
            playing=True    
            rmaxplay()
        elif starting==3 and playing==False and keys[pygame.K_m]:
                starting =0
                startpage()


    clock.tick(30)
    