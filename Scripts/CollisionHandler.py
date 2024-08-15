class CollisionHandler:
    @staticmethod
    def resolve_collisions(character, others, allowed_overlap):
        for other in others:
            if other != character and CollisionHandler.check_collision(character, other):
                CollisionHandler.adjust_position(character, other, allowed_overlap)

    @staticmethod
    def check_collision(character, other):
        offset_x = other.rect.x - character.rect.x
        offset_y = other.rect.y - character.rect.y
        return character.mask.overlap(other.mask, (offset_x, offset_y))

    @staticmethod
    def adjust_position(character, other, allowed_overlap):
        if character.rect.centerx < other.rect.centerx:
            overlap = character.rect.right - other.rect.left
            if overlap > allowed_overlap:
                adjust_distance = (overlap - allowed_overlap) // 2
                character.rect.x -= adjust_distance
                other.rect.x += adjust_distance
        else:
            overlap = other.rect.right - character.rect.left
            if overlap > allowed_overlap:
                adjust_distance = (overlap - allowed_overlap) // 2
                character.rect.x += adjust_distance
                other.rect.x -= adjust_distance

        character.pos = [character.rect.x, character.rect.y]
        other.pos = [other.rect.x, other.rect.y]
        # Update masks as the position changes
        character.update_mask()
        other.update_mask()
