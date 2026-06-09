color_map = {
    "Warm": [
        "earthy tones (olive, mustard, terracotta)",
        "warm reds and corals",
        "golden yellow, peach, cream",
        "gold jewelry"
    ],
    "Cool": [
        "jewel tones (emerald, sapphire, ruby)",
        "blues, purples, and pinks",
        "cool grays and pure white",
        "silver jewelry"
    ],
    "Neutral": [
        "soft neutrals (taupe, beige, off-white)",
        "muted versions of most colors",
        "both gold and silver jewelry"
    ]
}

shape_map = {
    "Inverted Triangle": [
        "A-line skirts and dresses to add volume at the hips",
        "wide-leg or flared bottoms",
        "softer, less structured shoulders",
        "V-necks to balance the upper body"
    ],
    "Pear / Triangle": [
        "structured or embellished tops to draw the eye up",
        "boat necks and wider necklines",
        "darker bottoms, brighter tops",
        "fit-and-flare dresses"
    ],
    "Rectangle": [
        "belted styles to define the waist",
        "peplum tops and wrap dresses",
        "layering to create curves",
        "ruffles and details at bust or hips"
    ]
}
makeup_map = {
    "Warm": {
        "lipstick": ["coral", "warm peach", "brick red", "terracotta nude"],
        "blush": ["peach", "warm apricot", "golden coral"],
        "eyeshadow": ["bronze", "warm gold", "copper", "olive"],
    },
    "Cool": {
        "lipstick": ["berry", "rose pink", "blue-red", "plum"],
        "blush": ["cool pink", "soft rose", "mauve"],
        "eyeshadow": ["taupe", "cool plum", "silver-grey", "navy"],
    },
    "Neutral": {
        "lipstick": ["rosy nude", "soft mauve", "dusty rose", "muted berry"],
        "blush": ["soft peach-pink", "natural rose", "muted coral"],
        "eyeshadow": ["soft brown", "champagne", "warm taupe", "rose-gold"],
    },
}


def recommend(undertone, body_shape):
    """Returns (colors, cuts, makeup) for the given undertone and shape."""
    colors = color_map.get(undertone, [])
    cuts = shape_map.get(body_shape, [])
    makeup = makeup_map.get(undertone, {})
    return colors, cuts, makeup