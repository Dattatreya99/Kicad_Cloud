import os
import re

print("========================================")
print("  CanSat Footprint & Library Patcher")
print("========================================\n")

base_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(base_dir, "CanSat_Library.pretty")
sch_path = os.path.join(base_dir, "Cansat.kicad_sch")

# 1. Fix the SHT4x footprint comments
sht4x_path = os.path.join(lib_dir, "SHT4x_Breakout.kicad_mod")
if os.path.exists(sht4x_path):
    with open(sht4x_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strip any line that starts with ;;
    new_content = re.sub(r'^\s*;;.*$\n', '', content, flags=re.MULTILINE)
    
    if content != new_content:
        with open(sht4x_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("[+] Fixed SHT4x_Breakout.kicad_mod parser crash.")
    else:
        print("[ ] SHT4x footprint already clean.")
else:
    print("[-] Warning: SHT4x footprint not found.")

# 2. Generate 9 custom footprints
footprints = [
    {"name": "BNO085_Breakout", "pins": 4, "w": 25.6, "h": 22.7},
    {"name": "SGP41_Breakout", "pins": 4, "w": 25.4, "h": 17.8},
    {"name": "MAX17048_Breakout", "pins": 4, "w": 25.7, "h": 20.3},
    {"name": "BMP585_Breakout", "pins": 4, "w": 25.4, "h": 17.8},
    {"name": "INA260_Breakout", "pins": 10, "w": 22.9, "h": 22.8},
    {"name": "CC1101_Module", "pins": 8, "w": 31.0, "h": 18.0},
    {"name": "MicroSD_Breakout", "pins": 8, "w": 31.85, "h": 25.4},
    {"name": "5V_BEC_Pololu", "pins": 4, "w": 17.78, "h": 20.32},
    {"name": "ESC_HAKRC_20A", "pins": 8, "w": 27.0, "h": 31.0}
]

if not os.path.exists(lib_dir):
    os.makedirs(lib_dir)

for fp in footprints:
    w, h, pins, name = fp["w"], fp["h"], fp["pins"], fp["name"]
    pin_width = (pins - 1) * 2.54
    start_x = -pin_width / 2.0
    
    content = f"""(footprint "{name}" (version 20211014) (generator pcbnew)
  (layer "F.Cu")
  (attr through_hole)
  (fp_text reference "REF**" (at 0 -2.5) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))
  (fp_text value "{name}" (at 0 {h + 2}) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))
  (fp_rect (start {-w/2} -1.5) (end {w/2} {h-1.5}) (layer "F.SilkS") (width 0.12) (fill none))
  (fp_rect (start {-w/2 - 0.25} -1.75) (end {w/2 + 0.25} {h-1.5 + 0.25}) (layer "F.CrtYd") (width 0.05) (fill none))
"""
    for i in range(pins):
        x = start_x + (i * 2.54)
        shape = "rect" if i == 0 else "circle"
        content += f'  (pad "{i+1}" thru_hole {shape} (at {x} 0) (size 1.7 1.7) (drill 1.0) (layers *.Cu *.Mask))\n'
    content += ")\n"
    
    fp_path = os.path.join(lib_dir, f"{name}.kicad_mod")
    with open(fp_path, "w", encoding="utf-8") as f:
        f.write(content)

print("[+] Generated all 9 physical courtyard footprints.")

# 3. Assign footprints in Schematic
assignments = {
    "J3": "CanSat_Library:BNO085_Breakout",
    "J9": "CanSat_Library:SGP41_Breakout",
    "J11": "CanSat_Library:MAX17048_Breakout",
    "J2": "CanSat_Library:BMP585_Breakout",
    "U3": "CanSat_Library:INA260_Breakout",
    "J4": "CanSat_Library:CC1101_Module",
    "J10": "CanSat_Library:MicroSD_Breakout",
    "J7": "CanSat_Library:5V_BEC_Pololu",
    "J8": "CanSat_Library:ESC_HAKRC_20A"
}

if os.path.exists(sch_path):
    with open(sch_path, "r", encoding="utf-8") as f:
        data = f.read()

    def replace_footprint(content, ref, new_fp):
        idx = content.find(f'(property "Reference" "{ref}"')
        if idx == -1: return content
        block_start = content.rfind('(symbol', 0, idx)
        end_idx = content.find('(symbol', idx)
        if end_idx == -1: end_idx = len(content)
        block = content[block_start:end_idx]
        new_block = re.sub(r'\(property \"Footprint\" \"[^\"]*\"', f'(property "Footprint" "{new_fp}"', block)
        return content[:block_start] + new_block + content[end_idx:]

    for ref, new_fp in assignments.items():
        data = replace_footprint(data, ref, new_fp)

    with open(sch_path, "w", encoding="utf-8") as f:
        f.write(data)
    print("[+] Successfully mapped new footprints to the schematic.")
else:
    print("[-] Warning: Cansat.kicad_sch not found.")

print("\n========================================")
print(" Patch complete!")
print(" IMPORTANT: Close KiCad entirely, reopen")
print(" it, open your schematic, and press F8!")
print("========================================")
input("Press Enter to exit...")
