import pygame
import random
import math
from copy import deepcopy
from boundary import Boundary
from utils import limit

class Bird:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        vx = random.uniform(-1, 1)
        vy = random.uniform(-1, 1)
        self.velocity = pygame.Vector2(vx, vy)
        self.velocity.normalize_ip()
        self.velocity *= random.uniform(1, 5)
        self.maxSpeed = 5
        self.acceleration = pygame.Vector2(0, 0)
        self.maxAcceleration = 1
        self.boundary = Boundary(0, 800, 0, 600)
        self.size = 2
        self.angle = 10
        self.color = (255, 255, 255)
        self.secondaryColor = (0, 0, 0)
        self.stroke = 3
        self.setRuleWeights()
        self.color = (255, 255, 255) if random.random() > 0.5 else (0, 255, 0)

    def computeAcceleration(self, group, predator=None):
        self.acceleration *= 0
        alignment = self.ruleAlignment(group)
        self.acceleration += alignment * self.alignmentWeight
        cohesion = self.ruleCohesion(group)
        self.acceleration += cohesion * self.cohesionWeight
        separation = self.ruleSeparation(group)
        self.acceleration += separation * self.separationWeight
        if predator:
            avoidance = self.ruleAvoidPredator(predator)
            self.acceleration += avoidance * self.avoidanceWeight

    def update(self, group, predator=None):
        self.computeAcceleration(group, predator)
        self.velocity += self.acceleration
        self.velocity = limit(self.velocity, self.maxSpeed)
        self.position += self.velocity
        self.boundary.periodicProject(self.position)
        self.angle = math.atan2(self.velocity.y, self.velocity.x) + math.pi / 2

    def setRuleWeights(self):
        self.maxSpeed = 3.5
        self.maxAcceleration = 1
        self.alignmentWeight = 0.25
        self.cohesionWeight = 0.5
        self.separationWeight = 0.6
        self.avoidanceWeight = 0.75
        self.alignmentRadius = 70
        self.cohesionRadius = 100
        self.separationRadius = 50
        self.avoidanceRadius = 100

    def ruleAlignment(self, group):
        acceleration = pygame.Vector2(0, 0)
        ct = 0
        for obj in group:
            if obj == self:
                continue
            displacement = self.boundary.periodicDisplacement(self.position, obj.position)
            distance = displacement.length()
            if distance <= self.alignmentRadius:
                acceleration += obj.velocity.normalize()
                ct += 1
        if ct == 0:
            return acceleration
        acceleration /= ct
        acceleration.normalize_ip()
        acceleration *= self.maxSpeed
        acceleration -= self.velocity
        return limit(acceleration, self.maxAcceleration)

    def ruleCohesion(self, group):
        acceleration = pygame.Vector2(0, 0)
        sum_pos = pygame.Vector2(0, 0)
        ct = 0
        for obj in group:
            if obj == self:
                continue
            displacement = self.boundary.periodicDisplacement(self.position, obj.position)
            distance = displacement.length()
            if distance <= self.cohesionRadius:
                sum_pos += obj.position
                ct += 1
        if ct == 0:
            return acceleration
        sum_pos /= ct
        acceleration = sum_pos - (self.position + self.velocity)
        acceleration.normalize_ip()
        acceleration *= self.maxSpeed
        acceleration -= self.velocity
        return limit(acceleration, self.maxAcceleration)

    def ruleSeparation(self, group):
        acceleration = pygame.Vector2(0, 0)
        ct = 0
        for obj in group:
            if obj == self:
                continue
            displacement = self.boundary.periodicDisplacement(self.position, obj.position)
            distance = displacement.length()
            if distance <= self.separationRadius:
                acceleration += displacement
                ct += 1
        if ct == 0:
            return acceleration
        acceleration /= ct
        acceleration.normalize_ip()
        acceleration *= self.maxSpeed
        acceleration -= self.velocity
        return limit(acceleration, self.maxAcceleration)

    def ruleAvoidPredator(self, predator):
        avoidance = pygame.Vector2(0, 0)
        displacement = self.position - predator.position
        distance = displacement.length()
        if distance <= self.avoidanceRadius:
            avoidance = displacement.normalize() * self.avoidanceWeight
        return avoidance

    def draw(self, screen, distance, scale):
        """
        Draws the bird on the screen.
        """
        ps = []
        points = [
            (0, -self.size),
            (math.sqrt(self.size), math.sqrt(self.size)),
            (-math.sqrt(self.size), math.sqrt(self.size))
        ]
        for point in points:
            rotation_matrix = [
                [math.cos(self.angle), -math.sin(self.angle)],
                [math.sin(self.angle), math.cos(self.angle)]
            ]
            rotated = (
                rotation_matrix[0][0] * point[0] + rotation_matrix[0][1] * point[1],
                rotation_matrix[1][0] * point[0] + rotation_matrix[1][1] * point[1]
            )
            x = int(rotated[0] * scale) + self.position.x
            y = int(rotated[1] * scale) + self.position.y
            ps.append((x, y))
        pygame.draw.polygon(screen, self.secondaryColor, ps)
        pygame.draw.polygon(screen, self.color, ps, self.stroke)
