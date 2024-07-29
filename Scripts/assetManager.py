import pygame

class AssetManager:
    def __init__(self):
        self.assets = {}

    def load_asset(self, name, path):
        if name in self.assets:
            print(f"Asset '{name}' is already loaded.")
            return
        try:
            image = pygame.image.load(path).convert_alpha()
            self.assets[name] = image
            print(f"Loaded asset '{name}' from {path}")
        except pygame.error as e:
            print(f"Failed to load asset '{name}' from {path}: {str(e)}")

    def get_asset(self, name):
        return self.assets[name]

    def resize_asset(self, name, new_size):
        """
        Resize an asset image stored in the assets dictionary with the given name to the specified new size.

        Parameters:
            name (str): The name of the asset.
            new_size (tuple): The new size of the asset image in pixels.

        Returns:
            None
        """
        image = self.assets[name]
        scaled_image = pygame.transform.smoothscale(image, new_size)
        self.assets[name] = scaled_image

    def load_sprite_sheet(self, name, path, frame_dimensions):
        """
        Load a sprite sheet from the given path and store it in the assets dictionary with the given name.
        The sprite sheet is divided into frames of specified dimensions, which are loaded into the assets dictionary.
        
        Args:
            name (str): The name of the sprite sheet.
            path (str): The path to the sprite sheet image file.
            frame_dimensions (tuple): The dimensions of each frame in the sprite sheet.
        
        Returns:
            None
        
        """
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
    
    def load_tiles(self, path, tile_properties):
        """
        Load tiles from a tileset image file and store them in the `tiles` attribute of the `AssetManager` object.
        
        Parameters:
            path (str): The path to the tileset image file.
            tile_properties (dict): A dictionary containing tile properties for each tile in the tileset. The keys are tuples representing the x and y coordinates of the tile in the tileset, and the values are dictionaries containing the properties of the tile.
        
        Returns:
            None
        
        """
        tileset = pygame.image.load(path).convert_alpha()
        tile_width, tile_height = self.tile_size
        for y in range(0, tileset.get_height(), tile_height):
            for x in range(0, tileset.get_width(), tile_width):
                tile = tileset.subsurface((x, y, tile_width, tile_height))
                properties = tile_properties.get((x // tile_width, y // tile_height), {})
                self.tiles.append((tile, properties))

    def check_collision(self, player_rect):
        """
        Check collision between the player and solid tiles.
        Returns True if there is a collision.
        """
        for tile, properties in self.tiles:
            if properties.get('solid', False):
                tile_rect = pygame.Rect(tile.get_rect())
                if tile_rect.colliderect(player_rect):
                    return True
        return False
