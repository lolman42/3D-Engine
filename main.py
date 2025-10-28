import pygame
import math
from readobj import readobj

pygame.init()
pygame.font.init()

FOV = 300
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('3D GAME')

class Camera:
    def __init__(self, x, y, z, yaw, pitch, roll, objects):
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.objects = objects

class Object3D:
    def __init__(self, vertexes, faces, speed):
        self.vertexes = vertexes
        self.faces = faces
        self.speed = speed

    def _projection(self, x, y, z):
        if z <= 0: return None
        projectedX = x * (FOV / z)
        projectedY = y * (FOV / z)
        screenX = int(projectedX + WIDTH / 2)
        screenY = int(-projectedY + HEIGHT / 2)
        return screenX, screenY
    
    def _rotateY(self, angle, x, y, z, px=0, py=0, pz=0):
        x -= px
        y -= py
        z -= pz
        cos = math.cos(angle)
        sin = math.sin(angle)
        x1 = x * cos - z * sin
        z1 = z * cos + x * sin
        x1 += px
        y1 = y + py
        z1 += pz
        return x1, y1, z1
    
    def _rotateX(self, angle, x, y, z, px=0, py=0, pz=0):
        x -= px
        y -= py
        z -= pz
        cos = math.cos(angle)
        sin = math.sin(angle)
        y1 = y * cos - z * sin
        z1 = z * cos + y * sin
        x1 = x + px
        y1 += py
        z1 += pz
        return x1, y1, z1

    def draw(self, screen, camera, color):
        for face in self.faces:
            for i in range(len(face)):
                try:
                    v1 = self.vertexes[int(face[i]) - 1]
                    v2 = self.vertexes[int(face[(i + 1) % len(face)]) - 1]
                    # rotate y
                    x1, y1, z1 = self._rotateY(-camera.yaw, v1.x, v1.y, v1.z, camera.x, camera.y, camera.z)
                    x2, y2, z2 = self._rotateY(-camera.yaw, v2.x, v2.y, v2.z, camera.x, camera.y, camera.z)
                    x1, y1, z1 = self._rotateX(-camera.pitch, x1, y1, z1, camera.x, camera.y, camera.z)
                    x2, y2, z2 = self._rotateX(-camera.pitch, x2, y2, z2, camera.x, camera.y, camera.z)
                    # move
                    x1, y1, z1 = x1 - camera.x, y1 - camera.y, z1 - camera.z
                    x2, y2, z2 = x2 - camera.x, y2 - camera.y, z2 - camera.z
                    start = self._projection(x1, y1, z1)
                    end = self._projection(x2, y2, z2)
                    if start and end: pygame.draw.line(screen, color, start, end, 1)
                except:
                    continue

cube_v, cube_f = readobj('cube/cube.obj')
cube = Object3D(cube_v, cube_f, 0.01)

camera = Camera(0, 0, 0, 0, 0, 0, [cube])

running = True
clock = pygame.time.Clock()
speed = cube.speed
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_w]:
        camera.x += speed * math.sin(-camera.yaw)
        camera.z += speed * math.cos(-camera.yaw)
    if keystate[pygame.K_s]:
        camera.x -= speed * math.sin(-camera.yaw)
        camera.z -= speed * math.cos(-camera.yaw)
    if keystate[pygame.K_a]:
        camera.x += speed * math.sin(-camera.yaw - math.pi/2)
        camera.z += speed * math.cos(-camera.yaw - math.pi/2)
    if keystate[pygame.K_d]:
        camera.x += speed * math.sin(-camera.yaw + math.pi/2)
        camera.z += speed * math.cos(-camera.yaw + math.pi/2)
    if keystate[pygame.K_SPACE]:
        camera.y += speed
    if keystate[pygame.K_LSHIFT]:
        camera.y -= speed
    
    if keystate[pygame.K_LEFT]:
        camera.yaw += speed
    if keystate[pygame.K_RIGHT]:
        camera.yaw -= speed
    if keystate[pygame.K_UP]:
        camera.pitch -= speed
    if keystate[pygame.K_DOWN]:
        camera.pitch += speed
    if camera.pitch < -math.pi/2: camera.pitch = -math.pi/2
    if camera.pitch > math.pi/2: camera.pitch = math.pi/2

    if keystate[pygame.K_q]:
        FOV += 10
    if keystate[pygame.K_e]:
        FOV -= 10
    if FOV >= 999: FOV = 999
    if FOV <= 300: FOV = 300

    SCREEN.fill((255,255,255))
    for object in camera.objects:
        object.draw(SCREEN, camera, (0,0,0))
    # FPS
    clock.tick(120)
    SCREEN.blit(pygame.font.SysFont("Arial", 24).render(
        f"FPS: {(int(clock.get_fps()))}   ",
        True, (0, 255, 0)), (10, 10))
    # POSITIONS
    SCREEN.blit(pygame.font.SysFont("Arial", 24).render(
        f"FOV: {FOV:.0f} " +
        f"Pos: ({camera.x:.2f}, {camera.y:.2f}, {camera.z:.2f}) " +
        f"Rot: ({camera.yaw:.2f}, {camera.pitch:.2f}, {camera.roll:.2f}) ",
        True, (0, 255, 0)), (100, 10))
    pygame.display.flip()
pygame.quit()