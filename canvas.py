import pygame
import copy
from vector import Vec2, Vec4
from pixel import Pixel
from colors import *
from mymath import clamp, get_line_pixels


class Canvas:
    def __init__(self, x, y, width, height, zoom=1.00):
        self.pos = Vec2(x, y)
        self.size = Vec2(width, height)
        self.zoom = zoom
        self.scaled_size = Vec2(self.size.x * self.zoom, self.size.y * self.zoom)
        self.origin = Vec2(self.size.x / 2, self.size.y / 2)
        self.scaled_origin = Vec2(self.origin.x * self.zoom, self.origin.y * self.zoom)
        self.surface = pygame.Surface((self.size.x, self.size.y))
        self.current_surface = self.surface
        self.pixels = []
        self.changed_pixels = []
        self.buffer = []
        self.buffers = []
        self.pressed_count = 0
        self.released_count = 2  # Start at 2, because if it's 1 means it's released and 0 means that is pressed
        self.start_pos = Vec2(-1, -1)
        self.end_pos = Vec2(-1, -1)
        self.selected_color = BLACK.copy()

        self.init_pixels()
    
    def init_pixels(self, surface=None):
        self.pixels.clear()

        if surface is None:
            # Alocate memory for the pixels
            for y in range(self.size.y):
                self.pixels.append([])

                for x in range(self.size.x):
                    self.pixels[y].append(None)
            
            self.clear(WHITE)
        else:
            # Load image (for example .png)
            self.surface = surface.copy()
            self.size = Vec2(self.surface.get_width(), self.surface.get_height())
            self.scaled_size = Vec2(self.size.x * self.zoom, self.size.y * self.zoom)
            self.origin = Vec2(self.size.x / 2, self.size.y / 2)
            self.scaled_origin = Vec2(self.origin.x * self.zoom, self.origin.y * self.zoom)

            for y in range(self.size.x):
                self.pixels.append([])

                for x in range(self.size.y):
                    color = surface.get_at((x, y))
                    self.pixels[y].append(Pixel(
                        Vec2(x, y), color.copy()
                    ))
            
            self.update_pixels()
    
    def set_zoom(self, zoom):
        self.zoom = zoom
        self.scaled_origin.x = self.origin.x * self.zoom
        self.scaled_origin.y = self.origin.y * self.zoom
        self.scaled_size.x = self.size.x * self.zoom
        self.scaled_size.y = self.size.y * self.zoom
    
    def scale_zoom(self, percent):
        self.zoom *= percent
        self.scaled_origin.x = self.origin.x * self.zoom
        self.scaled_origin.y = self.origin.y * self.zoom
        self.scaled_size.x = self.size.x * self.zoom
        self.scaled_size.y = self.size.y * self.zoom
    
    def is_mouse_inside(self, x, y):
        if (x >= self.pos.x - self.scaled_origin.x and x <= self.pos.x - self.scaled_origin.x + self.scaled_size.x) and \
            (y >= self.pos.y - self.scaled_origin.y and y <= self.pos.y - self.scaled_origin.y + self.scaled_size.y):
            return True
        
        return False
    
    def fill_pixel(self, pixel):
        self.pixels[pixel.pos.y][pixel.pos.x] = pixel.copy()
        self.changed_pixels.append(pixel.copy())
    
    def fill_line(self, start_pos: Vec2, end_pos: Vec2, color: Vec4):
        line_pixels = get_line_pixels(start_pos, end_pos)
        for vec in line_pixels:
            self.fill_pixel(Pixel(
                Vec2(vec.x, vec.y), color.copy()
            ))
    
    def get_inside_mouse_pos(self, x, y):
        relative_pos = Vec2(
            x - (self.pos.x - self.scaled_origin.x), 
            y - (self.pos.y - self.scaled_origin.y)
        )
        converted_pos = Vec2(
            clamp(int(relative_pos.x / self.zoom), 0, self.size.x - 1),
            clamp(int(relative_pos.y / self.zoom), 0, self.size.y - 1)
        )

        return converted_pos
    
    def clear(self, color: Vec4):
        for y in range(self.size.y):
            for x in range(self.size.x):
                self.pixels[y][x] = Pixel(Vec2(x, y), color.copy())
        
        self.surface.fill(color.as_tuple())
        self.changed_pixels.clear()
    
    def update_pixels(self):
        for y in range(self.size.y):
            for x in range(self.size.x):
                pixel = self.pixels[y][x]
                pygame.draw.rect(self.surface, pixel.as_tuple(), (x, y, 1, 1))

        self.changed_pixels.clear()
    
    def update_changes(self):
        for pixel in self.changed_pixels:
            pygame.draw.rect(self.surface, pixel.color.as_tuple(), (pixel.pos.x, pixel.pos.y, 1, 1))
        
        self.changed_pixels.clear()

    def undo(self):
        # TODO:
        # Get the correct color
        self.clear(WHITE)
        self.changed_pixels.clear()

        for buffer in self.buffers[:-1]:
            for sub_buffer in buffer:
                for pixel in sub_buffer:
                    self.fill_pixel(pixel)

        if len(self.buffers) >= 1:
            self.buffers.pop(-1)
            self.update_changes()
        
    def update(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = Vec2(*pygame.mouse.get_pos())

        if mouse_buttons[0]:
            self.released_count = 0

            if self.is_mouse_inside(mouse_pos.x, mouse_pos.y):
                self.released_count = 0

                if self.pressed_count == 0:
                    self.start_pos = self.get_inside_mouse_pos(mouse_pos.x, mouse_pos.y)
                    self.end_pos = self.get_inside_mouse_pos(mouse_pos.x, mouse_pos.y)
                else:
                    # Create something to now have duplicate pixels in the same buffer
                    self.start_pos = self.end_pos.copy()
                    self.end_pos = self.get_inside_mouse_pos(mouse_pos.x, mouse_pos.y)
                    self.fill_line(self.start_pos, self.end_pos, self.selected_color)
                    
                    self.buffer.append(copy.deepcopy(self.changed_pixels))
                    self.update_changes()
                    
                self.pressed_count += 1
        else:
            self.pressed_count = 0
            if self.released_count == 1:
                self.buffers.append(copy.deepcopy(self.buffer))
                # Show that it's adding to buffer repeated pixels
                print(len(self.buffer))
                self.buffer.clear()
            
            self.released_count += 1
        
    def draw(self, win):
        # If zoom has not be changed no need to resize
        if self.scaled_size.x != self.size.x or self.scaled_size.y != self.size.y:
            self.current_surface = pygame.transform.scale(self.surface, (round(self.scaled_size.x), round(self.scaled_size.y)))

        win.blit(self.current_surface, (self.pos.x - self.scaled_origin.x, self.pos.y - self.scaled_origin.y))
