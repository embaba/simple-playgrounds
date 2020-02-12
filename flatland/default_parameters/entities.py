import math

"""
Different standard parameters for entities
"""

# Edibles


edible_texture =  {
    'type': 'centered_random_tiles',
    'min': [40, 120, 150],
    'max': [80, 150, 190],
    'size_tiles' : 10
    }

edible_default = {
    'physical_shape': 'circle',
    'radius': 15,
    'mass': 10,
    'texture': edible_texture.copy(),
    'movable': False,

    'entity_type':'edible',
    'interaction_range': 10,
    'shrink_when_eaten': 0.9,
    'min_reward': 5,

    'initial_reward': 30
}

# Basic entities

basic_texture =  {
    'type': 'color',
    'color': (125, 100, 150)
    }

basic_default = {
    'entity_type': 'basic',
    'physical_shape': 'circle',
    'radius': 10,
    'mass': 10,
    'texture': basic_texture.copy(),
    'movable': False
}

# Absorbables

absorbable_texture =  {
    'type': 'color',
    'color': (200, 100, 50)
    }

absorbable_default = {
    'physical_shape': 'triangle',
    'radius': 5,
    'mass': 5,
    'texture': absorbable_texture.copy(),
    'movable': True,
    'entity_type' : 'absorbable',
    'reward' : 15

}

# Dispenser
dispenser_texture =  {
    'type': 'centered_random_tiles',
    'min': [200, 80, 180],
    'max': [240, 120, 220],
    'size_tiles' : 10
    }


dispenser_default = {
    'entity_type':'dispenser',
    'physical_shape': 'circle',
    'radius': 15,
    'mass': 10,
    'texture': dispenser_texture.copy(),
    'movable': False,

    'interaction_range': 10,

    'object_produced': absorbable_default.copy(),
    'area_shape': 'rectangle',
    'limit': 15

}

# Yielder

yielder_default = {

    'entity_type':'yielder',
    'object_produced': absorbable_default.copy(),
    'area_shape': 'rectangle',
    'limit': 10,
    'probability': 0.1

}

###


# Zones
zone_default = {
    'physical_shape': 'circle',
    'radius': 10,
    'movable': False

}

end_zone_texture =  {
    'type': 'centered_random_tiles',
    'min': [0, 225, 0],
    'max': [0, 255, 0],
    'size_tiles' : 3
    }

end_zone_default = {

    'texture': end_zone_texture.copy(),
    'entity_type':'end_zone',
    'reward': 200
}

healing_zone_texture =  {
    'type': 'color',
    'color': (0, 0, 250)
    }

healing_zone_default = {

    'texture': healing_zone_texture.copy(),
    'entity_type':'reward_zone',
    'reward': 2,
    'total_reward': 200
}

damaging_zone_texture =  {
    'type': 'color',
    'color': (250, 0, 0)
    }

damaging_zone_default = {

    'texture': damaging_zone_texture.copy(),
    'entity_type':'reward_zone',
    'reward': -2,
    'total_reward': -200
}

contact_endzone_default = {

    'physical_shape': 'circle',
    'radius': 10,
    'movable': False,


    'texture': end_zone_texture.copy(),
    'entity_type': 'contact_endzone',
    'reward': 200
}


# Basic entities

door_texture =  {
    'type': 'random_tiles',
    'min': [110, 110, 110],
    'max': [130, 130, 130],
    'size_tiles' : 10
    }

door_default = {
    'entity_type': 'basic',
    'physical_shape': 'rectangle',
    'shape_rectangle': [10, 100],
    'texture': door_texture.copy(),
    'movable': False
}

button_door_openclose_texture =  {
    'type': 'color',
    'color': (50, 100, 150)
    }

button_door_openclose_default = {
    'entity_type': 'button_door_openclose',
    'door': door_default.copy(),
    'physical_shape': 'square',
    'radius': 10,
    'texture': button_door_openclose_texture.copy(),
    'movable': False,
    'interaction_range': 10,
}

button_door_opentimer_texture =  {
    'type': 'color',
    'color': (50, 100, 150)
    }

button_door_opentimer_default = {
    'entity_type': 'button_door_opentimer',
    'door': door_default.copy(),
    'physical_shape': 'square',
    'radius': 10,
    'texture': button_door_opentimer_texture.copy(),
    'movable': False,
    'interaction_range': 10,
    'time_open': 50
}


lock_key_door_texture =  {
    'type': 'color',
    'color': (50, 100, 150)
    }

lock_key_door_default = {
    'entity_type': 'lock_key_door',
    'door': door_default.copy(),
    'physical_shape': 'square',
    'radius': 10,
    'texture': lock_key_door_texture.copy(),
    'movable': False,
    'interaction_range': 10,

    'key':
        {
            'entity_type': 'gem',
            'physical_shape': 'circle',
            'radius': 5,
            'mass': 10,
            'texture': lock_key_door_texture.copy(),
            'movable': True,
            'graspable': True,
            'interaction_range': 10,
        }


}

#######
fireball_texture =  {
    'type': 'centered_random_tiles',
    'min': [200, 0, 0],
    'max': [255, 100, 0],
    'size_tiles' : 4
    }

fireball_default = {

    'texture': fireball_texture.copy(),
    'entity_type':'fireball',
    'interaction_range': 10,
    'reward': -2,
    'total_reward': -200,

    'physical_shape': 'circle',
    'radius': 10,
    'mass': 10,
    'movable': True
}

fairy_texture =  {
    'type': 'centered_random_tiles',
    'min': [0, 150, 200],
    'max': [0, 200, 250],
    'size_tiles' : 3
    }

fairy_default = {

    'texture': fairy_texture.copy(),
    'entity_type':'fairy',
    'interaction_range': 10,
    'reward': 2,
    'total_reward': 200,

    'physical_shape': 'circle',
    'radius': 10,
    'mass': 10,
    'movable': True
}


key_chest_texture =  {
    'type': 'color',
    'color': (50, 100, 150)
    }


key_chest_default = {
            'entity_type': 'gem',
            'physical_shape': 'square',
            'radius': 10,
            'mass': 20,
            'texture': key_chest_texture.copy(),
            'movable': True,
            'graspable': True,
            'interaction_range': 10,
        }

chest_texture =  {
    'type': 'color',
    'color': (70, 180, 200)
    }


chest_default = {

    'physical_shape': 'square',
    'radius': 20,
    'movable': False,
    'interaction_range': 10,

    'texture': chest_texture.copy(),
    'entity_type': 'chest',
    'reward': 50,

    'key_pod': key_chest_default.copy()
}