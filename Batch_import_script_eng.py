import fontforge
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 0. CONFIGURATION AND METADATA
# ==============================================================================

# --- File and Naming Configuration ---
# Directory where the script is located and SVGs are stored
svg_dir = Path('/Users/magnush/Documents/Font design/Pivemo Mouse Handwritten/Regular/')

# --- Metadata ---
family_name = 'Pivemo Mouse Handwritten'
style_name = 'Regular'
base_name = f"{family_name.replace(' ', '')}-Regular" # Technical Name: FamilyName-StyleName
version_number = "1.000"
version = "Version " + version_number
italic_angle = 0
author_name = "Magnus Hållberg Pivemo AB"
copyright = "Copyright (c) 2025 {author_name}, all rights reserved."

# --- Layout Configuration ---
# Set to True for proportional (variable width), False for monospace (fixed width)
proportional = True 

# --- Automatic Unique ID (CRITICAL for conflict-free installation) ---
# Generates a unique ID string based on date/time to ensure the OS installs 
# new versions correctly without conflict.
version_str = datetime.now().strftime(version_number + ";%Y%m%d.%H%M")
unique_id = f"{version_str};{author_name};{base_name}"

# --- Metrics and Width Constants ---
# Constants used when 'proportional' is True
LEFT_BUFFER = 75     # Left Sidebearing (LSB)
RIGHT_BUFFER = 75    # Right Sidebearing (RSB)
MIN_WIDTH = 10       # Minimum allowed glyph width (to prevent zero-width for tiny marks)

# Constant used when 'proportional' is False
MONOSPACE_WIDTH = 1000 # Fixed width per character

# ==============================================================================
# 1. INITIALIZATION AND FONT CORE METRICS
# ==============================================================================

svgFilePaths = list(svg_dir.glob('**/*.svg'))
font = fontforge.font()

# Vertical Metrics (EM-Size = 1000 Units Per EM)
font.ascent = 800  # Distance from baseline upwards
font.descent = 200 # Distance from baseline downwards
font.em = 1000     # Total height of the font (UPM)

# ==============================================================================
# 2. IMPORT GLYPHS AND SET WIDTH
# ==============================================================================

print("2. Importing glyphs and setting width...")

for p in svgFilePaths:
    try:
        # Extract the numerical Unicode value from the filename (e.g., "65" in "65 A")
        dec = p.stem.split(" ", 1)[0]
        unicode_val = int(dec)
        
        # Create a unique internal glyph name based on the filename
        glyph_name = p.stem.replace(" ", "_").replace(".", "_") 
        
        if glyph_name not in font:
            # Create a new glyph
            font.createChar(-1, glyph_name) 
            
        glyph = font[glyph_name]
        
        # Map the uniquely named glyph to the correct Unicode code point
        glyph.unicode = unicode_val
        glyph.clear()
        
        # Import the SVG outlines
        glyph.importOutlines(str(p))

        # --- Width Handling ---
        if proportional:
            # Set sidebearings (LSB/RSB) for proportional spacing
            glyph.left_side_bearing = LEFT_BUFFER
            glyph.right_side_bearing = RIGHT_BUFFER
            
            # Handle minimum width requirement
            if glyph.width < MIN_WIDTH:
                glyph.width = MIN_WIDTH
        else:
            # Monospace: Force all glyphs to a fixed width
            glyph.width = MONOSPACE_WIDTH
        
    except ValueError:
        print(f"Skipped file {p.name}: Not a valid numerical Unicode value.")
        continue


# ==============================================================================
# 3. CRITICAL GLYPH ADJUSTMENTS (WHITESPACE AND CONTROL CHARACTERS)
# ==============================================================================

print("3. Creating and adjusting critical whitespace characters...")

# List of all critical whitespace/control characters (Unicode, Glyph Name, Fixed Width)
CRITICAL_GLYPHS = [
    (32, 'space', 0),                 # U+0020: Standard Space
    (160, 'nonbreakingspace', 0),      # U+00A0: No-break Space
    # Fixed-width spaces (defined by OpenType standard)
    (8194, 'enspace', 500),           # U+2002: En Space (1/2 EM)
    (8195, 'emspace', 1000),          # U+2003: Em Space (1 EM)
    (8201, 'thinspace', 250),         # U+2009: Thin Space (approx 1/4 EM)
    (8202, 'hairspace', 100),         # U+200A: Hair Space (approx 1/10 EM)
    # Control characters (Zero width)
    (9, 'tab', 0),                     # U+0009: Character Tabulation (Tab)
    (10, 'linefeed', 0),              # U+000A: Line Feed (LF)
    (13, 'carriagereturn', 0),        # U+000D: Carriage Return (CR)
]

for unicode_val, name, fixed_width in CRITICAL_GLYPHS:
    if name not in font:
        font.createChar(unicode_val, name)

    glyph = font[name]
    glyph.clear() # Ensure there are no accidental outlines

    if name in ['space', 'nonbreakingspace']:
        # Handle U+0020 and U+00A0 based on proportional/monospace setting
        if proportional:
            desired_width = 250
        else:
            desired_width = MONOSPACE_WIDTH
        
        # Set LSB/RSB to 0 (correct for pure whitespace)
        glyph.left_side_bearing = 0
        glyph.right_side_bearing = 0
        
        # Force the width to the desired value (overrides calculated width=0)
        glyph.width = desired_width 
        
    elif name in ['enspace', 'emspace', 'thinspace', 'hairspace']:
        # Fixed spaces: Set width to the standardized fixed width
        glyph.left_side_bearing = 0
        glyph.right_side_bearing = 0
        glyph.width = fixed_width
        
    elif name in ['tab', 'linefeed', 'carriagereturn']:
        # Control characters: Zero width
        glyph.left_side_bearing = 0
        glyph.right_side_bearing = 0
        glyph.width = 0

# ==============================================================================
# 4. CORRECTION ACTIONS
# ==============================================================================

font.reencode('unicode') 
print("4. Font successfully re-encoded to Unicode (BMP).")

# ==============================================================================
# 5. FONT INFO (METADATA APPLICATION)
# ==============================================================================

print("5. Applying Font Info (Metadata)...")

# --- PS Names (PostScript Names - For legacy systems) ---
font.fontname = base_name         
font.familyname = family_name     
font.fullname = f"{family_name} {style_name}"
font.weight = style_name          

# --- General ---
font.version = version   
font.italicangle = italic_angle              
font.copyright = copyright.format(author_name=author_name) # Ensure variable is used

# --- CRITICAL PARAMETERS (TTF/OpenType Names) ---
# Uses numerical IDs for maximum compatibility in FontForge Python
font.sfnt_names = (
    ('English (US)', 3, unique_id),         # ID 3: UniqueID (Critical for installation)
    ('English (US)', 16, family_name),      # ID 16: Preferred Family
    ('English (US)', 17, style_name)        # ID 17: Preferred Subfamily
)

# ==============================================================================
# 6. SAVE AND GENERATE FILES
# ==============================================================================

print("6. Saving and generating files...")

# Save the FontForge source file (SFD)
sfd_output_path = svg_dir / f'{base_name}.sfd'
font.save(str(sfd_output_path))
print(f"   Source file (SFD) saved.")

# --- Generation ---
# Generate TrueType Font (TTF)
ttf_output_path = svg_dir / f'{base_name}.ttf'
font.generate(str(ttf_output_path), flags=('opentype', 'round'))
print(f"   Generated: {ttf_output_path.name}")

# Generate OpenType Font (OTF)
otf_output_path = svg_dir / f'{base_name}.otf'
font.generate(str(otf_output_path), flags=('opentype'))
print(f"   Generated: {otf_output_path.name}")

# Generate Web Open Font Format (WOFF)
font.generate(str(svg_dir / f'{base_name}.woff'))
print(f"   Generated: {base_name}.woff")

# --- WOFF2 Instruction ---
print(f"\n** WOFF2 Instruction **")
print(f"To create WOFF2, use the external command in your terminal:")
print(f"    woff2_compress {base_name}.ttf")

print("\nScript finished successfully.")