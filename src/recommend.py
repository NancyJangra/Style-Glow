# --- Recommendation logic ---
# Inputs (later these come from the analysis steps)
undertone = "Warm"          # from skin_tone.py
body_shape = "Inverted Triangle"  # from body_detection.py

# Color suggestions based on undertone
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

# Silhouette suggestions based on body shape
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


# Build the recommendation
print("=" * 45)
print("        YOUR STYLE RECOMMENDATIONS")
print("=" * 45)
print(f"\nDetected undertone : {undertone}")
print(f"Detected body shape: {body_shape}")

print(f"\n--- Colors that suit you ({undertone}) ---")
for item in color_map.get(undertone, []):
    print(f"  • {item}")

print(f"\n--- Cuts & silhouettes for you ({body_shape}) ---")
for item in shape_map.get(body_shape, []):
    print(f"  • {item}")

print("\n" + "=" * 45)