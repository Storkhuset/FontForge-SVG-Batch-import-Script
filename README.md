## 📝 README.md (FontForge Python Build Script)

# FontForge SVG Builder Script

## 🛠️ Project Overview

This Python script is designed to automate the process of converting a large number of individual SVG glyph files into unified, production-ready font files (`.ttf`, `.otf`, `.woff`, etc.) using **FontForge**.

As template for designing the font I recommend using the excellent template created by tomchen available on Github. 
https://github.com/tomchen/font-template


The script is highly customizable and ensures industry-standard practices are followed, including:

  * **Configurable Layout:** Easy switching between **Proportional** and **Monospace** spacing.
  * **Metric Consistency:** Sets the correct Ascender/Descender and EM size (1000 units).
  * **Conflict-Free Metadata:** Automatically generates unique IDs to prevent installation conflicts on user systems.
  * **Whitespace Integrity:** Ensures all critical whitespace and control characters (Space, Tab, En Space, etc.) are correctly created and sized.

-----

## ⚙️ Configuration

All user-configurable settings are located at the very top of the script (`generate_font.py`).

### 1\. File Path (Crucial Manual Step)

Due to limitations in some FontForge environments when using `Execute Script...`, the SVG input directory must be set manually:

```python
# --- File Path: MANUALLY SET THIS DIRECTORY ---
# Specify the path to your folder containing all the .svg glyph files.
svg_dir = Path('/Users/magnush/Documents/Font design/Pivemo Mouse Handwritten/Regular/')
```

### 2\. General Metadata

Customize your font's identifying information here:

```python
# --- Metadata ---
family_name = 'My Custom Font Family'
style_name = 'Regular'
base_name = 'MyCustomFont-Regular' # Technical Name (e.g., FontName-Style)
author_name = "Your Name"
# ... (Other metadata like version_number, copyright)
```

### 3\. Layout Toggle

Select your preferred spacing model:

```python
# --- Layout Configuration ---
# Set to True for proportional (variable width), False for monospace (fixed width)
proportional = True 
```

### 4\. Metrics and Spacing

These constants define how the script handles glyph placement:

| Constant | Value (Default) | Function |
| :--- | :--- | :--- |
| `LEFT_BUFFER`, `RIGHT_BUFFER` | 75 | Sidebearings (LSB/RSB) added to proportional glyphs (Separation 150). |
| `MIN_WIDTH` | 10 | Minimum total width for proportional glyphs. |
| `MONOSPACE_WIDTH` | 1000 | Fixed width used if `proportional = False`. |

-----

## ▶️ Execution

### Prerequisites

1.  **FontForge:** Must be installed on your system.
2.  **Python 3:** Required for the script.

### Steps to Run

1.  **Open** the `generate_font.py` file and **manually update** the `svg_dir` path (Section 0) to point to your SVG folder.
2.  Start **FontForge**.
3.  Go to **File -\> Execute Script...** (or `Shift + Cmd + /` on macOS).
4.  Select the **`generate_font.py`** file.
5.  Check the FontForge console for output messages confirming the import, metadata application, and file generation.

### Output Files

The following files will be generated and saved directly into the folder specified by `svg_dir`:

  * `.sfd` (FontForge Source File)
  * `.ttf` (TrueType Font)
  * `.otf` (OpenType Font)
  * `.woff` (Web Open Font Format)

### WOFF2 Generation

The WOFF2 format must be generated externally for maximal stability. Use the generated `.ttf` file as input:

```bash
woff2_compress [base_name].ttf
```

-----

## 🔑 Key Script Features (Technical)

The script handles several crucial aspects that are often forgotten in manual builds:

  * **Whitespace Integrity (Section 3):** Explicitly creates and sets the correct widths for `space`, `nonbreakingspace`, `enspace`, and control characters (`tab`, `linefeed`, `carriagereturn`). This prevents the common issue of seeing "missing glyph boxes" for whitespace.
  * **Unique ID Generation:** Uses `datetime.now()` to ensure the `UniqueID` field in the font metadata is unique every time the script is run, allowing for conflict-free re-installation and updates.
  * **Proportional Logic:** For proportional fonts, it sets the LSB/RSB first and then forces the `glyph.width` afterwards, correctly handling the zero-width issue for un-contoured characters like the `space`.

-----

## ©️ License

This script is provided under the MIT License. Feel free to use, modify, and distribute this script for any purpose.
