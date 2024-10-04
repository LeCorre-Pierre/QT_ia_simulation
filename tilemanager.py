from PyQt5.QtGui import QImage, QPixmap


class TileManager:
    def __init__(self):
        # Dictionnaires pour stocker les tiles de personnages et de la carte
        self.char_tiles = {}
        self.map_tiles = {}

    def load_tileset(self, file_name, tile_width, tile_height, spacing=1, col_num=54, row_num=12):
        """ Charge et découpe un tileset générique """
        tileset_image = QImage(file_name)
        if tileset_image.isNull():
            print(f"Erreur : Impossible de charger l'image {file_name}")
            return []

        tiles = []
        for row in range(row_num):
            for col in range(col_num):
                x = col * (tile_width + spacing)
                y = row * (tile_height + spacing)
                tile = tileset_image.copy(x, y, tile_width, tile_height)
                tiles.append(QPixmap.fromImage(tile))
        return tiles

    def load_character_tiles(self, file_name="mnt/data/roguelikeChar_transparent.png", tile_width=16, tile_height=16,
                             spacing=1, col_num=54, row_num=12):
        """ Charge et découpe les tiles de personnages """
        self.char_tiles = self.load_tileset(file_name, tile_width, tile_height, spacing, col_num, row_num)

    def load_map_tiles(self, file_name="mnt/data/roguelikeMap_transparent.png", tile_width=16, tile_height=16,
                       spacing=1, col_num=54, row_num=12):
        """ Charge et découpe les tiles de la carte """
        self.map_tiles = self.load_tileset(file_name, tile_width, tile_height, spacing, col_num, row_num)

    def get_character_tile(self, index):
        """ Récupère une tile de personnage spécifique par son index """
        if 0 <= index < len(self.char_tiles):
            return self.char_tiles[index]
        else:
            print(f"Erreur : Index {index} en dehors des limites pour les tiles de personnages.")
            return None

    def get_map_tile(self, index):
        """ Récupère une tile de carte spécifique par son index """
        if 0 <= index < len(self.map_tiles):
            return self.map_tiles[index]
        else:
            print(f"Erreur : Index {index} en dehors des limites pour les tiles de la carte.")
            return None



