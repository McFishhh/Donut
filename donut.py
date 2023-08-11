import math 
import pygame

pygame.init()

widthScreen = 1920
heightScreen = 1080

xStart = 0
yStart = 0

widthPixel = 10
heightPixel = 15
widthScreenUnit = widthScreen // widthPixel
heightScreenUnit = heightScreen // heightPixel
screenSizeUnit = widthScreenUnit * heightScreenUnit
screen = pygame.display.set_mode((widthScreen, heightScreen))
textDisplay = pygame.display.set_mode((widthScreen, heightScreen))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18, bold=True )

illum = ".,-~:;=!*#$@"
theta_spacing = 0.07
phi_spacing = 0.02

R1 = 1
R2 = 2
K2 = 5
K1 = (widthPixel*3)/(8*(R1+R2))

A = 0
B = 0

changeRateA = 0.000010
changeRateB = 0.000005

running = True
while running:
    
    screen.fill((0, 0, 0)) # black background

    output = [' '] * screenSizeUnit
    zbuffer = [0] * screenSizeUnit

    if A == 2*math.pi:
        A = 0
    if B == 2*math.pi:
        B = 0
    
    sinA = math.sin(A)
    sinB = math.sin(B)
    cosA = math.cos(A)
    cosB = math.cos(B)

    theta = 0
    while (theta < 2*math.pi):
        theta += theta_spacing
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        phi = 0
        while (phi < 2*math.pi): # more precise imaging than range(0, 628, phi_spacing=2)
            phi += phi_spacing
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            circlex = R2+(R1*costheta)
            circley = R1*sintheta
            circlez = 0

            x = (circlex*(cosB*cosphi + sinA*sinB*sinphi)) - circley*cosA*sinB
            y = (circlex*(cosphi*sinB - cosB*sinA*sinphi)) + circley*cosA*cosB
            z = K2 + circlex*cosA*sinphi + circley*sinA
            zInv = 1/z

            xp = int((widthScreenUnit/2) + 25*K1*x*zInv)
            yp = int((heightScreenUnit/2) - 15*K1*y*zInv)

            L = float((costheta*cosphi*sinB) - (cosA*costheta*sinphi) - (sinA*sintheta) + cosB*(cosA*sintheta - costheta*sinA*sinphi))
            pos = int(xp + widthScreenUnit*yp)
            if zInv > zbuffer[pos]:
                zbuffer[pos] = zInv
                Lindex = int(L*8)
                output[pos] = illum[Lindex if Lindex > 0 else 0]
    
    if yStart == heightScreenUnit * heightPixel - heightPixel:
        yStart = 0
    
    for i in range(len(output)):
        A += changeRateA
        B += changeRateB
        text = font.render(output[i], True, (255, 255, 255))
        rect = text.get_rect(center=(xp, yp))
        if i == 0 or i % widthScreenUnit:
            textDisplay.blit(text, (xStart, yStart))
            xStart += widthPixel
        else:
            yStart += heightPixel
            xStart = 0
            textDisplay.blit(text, (xStart, yStart))
            xStart += widthPixel
            
    # arrow key input checker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN: 
            # dont use "or event.type == pygame.KEYUP" also or will register twice 
            if event.key == pygame.K_UP:
                changeRateA += 0.000005
            if event.key == pygame.K_DOWN:
                changeRateA -= 0.000005
            if event.key == pygame.K_LEFT:
                changeRateB -= 0.000005
            if event.key == pygame.K_RIGHT:
                changeRateB += 0.000005
        
    textA = font.render(f"ΔA = {changeRateA:.6f}", True, (255, 255, 255))
    textB = font.render(f"ΔB = {changeRateB:.6f}", True, (255, 255, 255))
    textRectA = textA. get_rect()
    textRectB = textB. get_rect()
    textDisplay.blit(textA, (0, 0))
    textDisplay.blit(textB, (0, 18))     
            
    pygame.display.update()
    clock.tick(40) # max tick rate for pygame is 40
    # print(pygame.time.get_ticks())
