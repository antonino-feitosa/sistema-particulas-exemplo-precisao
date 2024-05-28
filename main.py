
#Teoria: https://ravnik.eu/collision-of-spheres-in-2d/

import pygame, random, sys, argparse
from pygame.locals import QUIT

WIDTH = 400
HEIGHT = 400
NUM_PARTICLES = 15
VELOCITY_RATE = 0.8
RESTITUTION = 1.0

particles:list['Particle'] = []
total_energy = 0

class Vector:
    def __init__(self, x:float, y:float):
        self.x:float = x
        self.y:float = y

    def distance(self, other:'Vector') -> float:
        dist = ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
        return dist

    def add(self, other:'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)
    
    def sub(self, other:'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y)

    def mul_scalar(self, scalar:float) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar)

    def mul_dot(self, other:'Vector') -> float:
        return self.x * other.x + self.y * other.y
    
    def normal(self) -> 'Vector':
        return self.mul_scalar(1.0/self.mag())

    def mag(self) -> float:
        return ((self.x**2 + self.y**2)**0.5)

    def clone(self):
        return Vector(self.x, self.y)

    def __repr__(self) -> str:
        return f"({self.x:.2f},{self.y:.2f})"

class Particle:
    def __init__(self:'Particle'):
        self.size:float = 10.0 + 10.0 * random.random()
        self.mass:float = 1.0 + 2.0 * random.random()

        self.position = Vector(self.size + random.randrange(WIDTH - 2*int(self.size)),self.size + random.randrange(HEIGHT - 2*int(self.size)))
        self.velocity = Vector(VELOCITY_RATE*random.random(), VELOCITY_RATE*random.random())

        c1 = min(255, int(self.velocity.mag() * 255))
        c2 = min(255, int(self.size * 255/20.0))
        c3 = min(255, int(self.mass * 255/3.0))
        self.color = (c1, c2, c3)

    def update(self:'Particle'):
        c1 = min(255, int(self.velocity.mag() * 255))
        c2 = min(255, int(self.size * 255/20.0))
        c3 = min(255, int(self.mass * 255/3.0))
        self.color = (c1, c2, c3)

        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        if self.position.x > WIDTH - self.size or self.position.x < self.size:
            self.velocity.x = -self.velocity.x
        if self.position.y > HEIGHT - self.size or self.position.y < self.size:
            self.velocity.y = -self.velocity.y

    def draw(self, screen:pygame.Surface):
        (x,y) = int(self.position.x), int(self.position.y)
        pygame.draw.circle(screen, self.color, (x,y), self.size + 1)


    def check(self, particle:'Particle'):
        distance = self.position.distance(particle.position)
        return distance < 2 + self.size + particle.size

    def resolve(self, particle:'Particle'):
        direction = self.position.sub(particle.position).normal()

        a = self.velocity
        b = particle.velocity
        tangent = Vector(-direction.y, direction.x)

        a_normal = a.mul_dot(direction)
        b_normal = b.mul_dot(direction)
        a_tangent = a.mul_dot(tangent)
        b_tangent = b.mul_dot(tangent)

        a_mass = self.mass
        b_mass = particle.mass
        sum = a_mass + b_mass
        
        a_vel_normal = (1 + RESTITUTION) * b_normal
        a_vel_normal += (a_mass/b_mass - RESTITUTION) * a_normal
        a_vel_normal *= b_mass/sum

        b_vel_normal = (1 + RESTITUTION) * a_normal
        b_vel_normal += (b_mass/a_mass - RESTITUTION) * b_normal
        b_vel_normal *= a_mass/sum

        a_velocity = direction.mul_scalar(a_vel_normal).add( tangent.mul_scalar(a_tangent) )
        b_velocity = direction.mul_scalar(b_vel_normal).add( tangent.mul_scalar(b_tangent) )

        self.velocity = a_velocity
        particle.velocity = b_velocity
        

    def __repr__(self) -> str:
        return '{' + str(self.position) + ' ' + str(self.velocity) + '}'



def update():
    for particle in particles:
        particle.update()

    for i in range(0, len(particles)):
        for j in range(i+1, len(particles)):
            a = particles[i]
            b = particles[j]
            if(a.check(b)):
                a.resolve(b)
    
    global total_energy
    total_energy = 0
    for particle in particles:
        total_energy += 0.5 * particle.mass + particle.velocity.mag()**2


def draw(screen:pygame.Surface, font:pygame.font.Font):
    screen.fill((0,0,0))
    for particle in particles:
        particle.draw(screen)
    for particle in particles:
        (x,y) = int(particle.position.x), int(particle.position.y)
        next_position = particle.position.add(particle.velocity.normal().mul_scalar(particle.size + 10))
        (fx, fy) = int(next_position.x), int(next_position.y)
        pygame.draw.line(screen, (255,0,0), (x, y), (fx, fy))

    surface = font.render(f'Energia Total: {total_energy:.3f}', True, (255, 255,255), (0,0,0))
    screen.blit(surface, (20, HEIGHT - 40))



def example1():
    global particles
    a = Particle()
    a.velocity = Vector(1,0)
    a.position = Vector(100, 100)

    b = Particle()
    b.velocity = Vector(-1,0)
    b.position = Vector(250, 100)
    particles = [a, b]

def example0():
    global particles
    a = Particle()
    a.velocity = Vector(1,0.1)
    a.position = Vector(100, 100)
    particles = [a]


def restart():
    tries = 10
    while len(particles) < NUM_PARTICLES and tries:
        particle = Particle()
        collide = False
        for p in particles:
            if p.check(particle):
                collide = True
                break
        if not collide:
            particles.append(particle)
            tries = 10
        else:
            tries -= 1



def main():
    running = True
    paused = False
    clock = pygame.time.Clock()
    pygame.init()
    text_font = pygame.font.Font(None,36)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Particle System')
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    restart()
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            update()
        draw(screen, text_font)

        pygame.display.update()
        clock.tick(100)

pygame.quit()




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Particle System Simulator.')
    parser.add_argument("--seed", type=int, help="Seed for the pseudorand generator", default=0)
    parser.add_argument("--size", type=int, help="Number of particles", default=10)
    parser.add_argument("--example", type=int, help="Run the specified example", default=0)
    args = parser.parse_args()

    NUM_PARTICLES = args.size
    random.seed(args.seed)
    
    restart()
    if args.example == 1:
        example0()
    if args.example == 2:
        example1()
    
    main()









