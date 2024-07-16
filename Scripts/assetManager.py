import pygame

class AssetManager:
    def __init__(self):
        self.assets = {}

    def load_asset(self, name, path):
        image = pygame.image.load(path).convert_alpha()
        self.assets[name] = image

    def get_asset(self, name):
        return self.assets[name]

    def resize_asset(self, name, new_size):
        image = self.assets[name]
        scaled_image = pygame.transform.smoothscale(image, new_size)
        self.assets[name] = scaled_image

    def load_sprite_sheet(self, name, path, frame_dimensions):
        sprite_sheet = pygame.image.load(path).convert_alpha()
        self.assets[name] = []
        sheet_width, sheet_height = sprite_sheet.get_size()
        frame_width, frame_height = frame_dimensions

        # print(f"Sprite sheet size: {sheet_width}x{sheet_height}")
        # print(f"Expected frames per row: {sheet_width // frame_width}")

        for y in range(0, sheet_height, frame_height):
            for x in range(0, sheet_width, frame_width):
                if x + frame_width <= sheet_width:
                    frame = sprite_sheet.subsurface((x, y, frame_width, frame_height))
                    self.assets[name].append(frame)
                #     print(f"Loaded frame at ({x}, {y}) with dimensions ({frame_width}, {frame_height})")
                # else:
                #     print(f"Skipped frame at ({x}, {y}) as it exceeds sprite sheet width")

    def get_frame(self, name, frame_index):
        """
        Retrieve a specific frame from a loaded sprite sheet.
        """
        return self.assets[name][frame_index]
