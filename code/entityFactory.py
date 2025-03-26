from code.background import Background
from code.const import WIN_WIDTH


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position = (0, 0)):
        match entity_name:
            case 'BgLevel':
                list_bg = []
                for i in range(1,4):
                    list_bg.append(Background(f'BgLevel{i}', (0,0)))
                    list_bg.append(Background(f'BgLevel{i}', (WIN_WIDTH, 0)))
                return list_bg

