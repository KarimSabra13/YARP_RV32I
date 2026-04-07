"""
Generate all images for the YARP RV32I Guide.
Run: python generate_images.py
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, ArrowStyle, Polygon
import matplotlib.patheffects as pe
import numpy as np
import os

OUT = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(OUT, exist_ok=True)

# ── color palette ──────────────────────────────────────────────
C = {
    'bg':       '#FAFCFF',
    'dark':     '#1A2744',
    'accent':   '#3B7DD8',
    'light':    '#E6F0FA',
    'gold':     '#D4A017',
    'green':    '#2E7D32',
    'red':      '#C62828',
    'purple':   '#6A1B9A',
    'teal':     '#00796B',
    'orange':   '#EF6C00',
    'salmon':   '#EF9A9A',
    'lime':     '#7CB342',
    'pink':     '#AD1457',
    'cyan':     '#0097A7',
    'white':    '#FFFFFF',
    'gray':     '#757575',
    'lgray':    '#EEEEEE',
}

# ── shared styling helpers ─────────────────────────────────────
SHADOW = [pe.withStroke(linewidth=3, foreground='#00000015')]
TITLE_PROPS = dict(fontsize=18, fontweight='bold', color=C['dark'],
                   fontfamily='sans-serif')

def save(fig, name, dpi=220):
    fig.savefig(os.path.join(OUT, name), dpi=dpi, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none', pad_inches=0.15)
    plt.close(fig)
    print(f"  ✓ {name}")

def _sbox(ax, x, y, w, h, fc, label, fs=11, ec=C['dark'], lw=2, sublabel=None,
          alpha=1.0, text_color=None, style='round,pad=0.12'):
    """Draw a rounded box with optional sub-label."""
    r = FancyBboxPatch((x, y), w, h, boxstyle=style,
                       facecolor=fc, edgecolor=ec, linewidth=lw, alpha=alpha,
                       zorder=2)
    ax.add_patch(r)
    tc = text_color or C['dark']
    dy = 0.15 if sublabel else 0
    ax.text(x + w/2, y + h/2 + dy, label, ha='center', va='center',
            fontsize=fs, fontweight='bold', color=tc, zorder=3,
            fontfamily='sans-serif')
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.25, sublabel, ha='center', va='center',
                fontsize=max(7, fs - 3), color=ec, style='italic', zorder=3,
                fontfamily='sans-serif')
    return r

def _arrow(ax, x1, y1, x2, y2, color=None, lw=2, style='->', rad=0, zorder=4):
    """Simple arrow helper."""
    color = color or C['accent']
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                connectionstyle=f'arc3,rad={rad}'),
                zorder=zorder)

def _mux(ax, cx, cy, w=0.5, h=1.0, color='#4FC3F7', label='', orientation='right'):
    """Draw a trapezoidal MUX shape."""
    if orientation == 'right':
        pts = [(cx - w/2, cy + h/2), (cx + w/2, cy + h*0.35),
               (cx + w/2, cy - h*0.35), (cx - w/2, cy - h/2)]
    elif orientation == 'down':
        pts = [(cx - h/2, cy + w/2), (cx + h/2, cy + w/2),
               (cx + h*0.35, cy - w/2), (cx - h*0.35, cy - w/2)]
    else:  # left
        pts = [(cx + w/2, cy + h/2), (cx - w/2, cy + h*0.35),
               (cx - w/2, cy - h*0.35), (cx + w/2, cy - h/2)]
    poly = Polygon(pts, closed=True, facecolor=color, edgecolor=C['dark'],
                   linewidth=1.5, zorder=3)
    ax.add_patch(poly)
    if label:
        ax.text(cx, cy, label, ha='center', va='center', fontsize=7,
                fontweight='bold', color=C['dark'], zorder=4, fontfamily='sans-serif')


# ════════════════════════════════════════════════════════════════
# 1. Von Neumann Architecture
# ════════════════════════════════════════════════════════════════
def gen_von_neumann():
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.set_facecolor(C['bg'])
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-1, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Von Neumann Architecture', pad=18, **TITLE_PROPS)

    # CPU boundary
    r = FancyBboxPatch((0.3, 0.8), 4.4, 4.4, boxstyle="round,pad=0.25",
                       facecolor='#E8F5E9', edgecolor=C['green'], linewidth=2.5,
                       zorder=1, alpha=0.5)
    ax.add_patch(r)
    ax.text(2.5, 5.0, 'CPU', ha='center', fontsize=15, fontweight='bold',
            color=C['green'], fontfamily='sans-serif', zorder=3)

    _sbox(ax, 0.7, 3.2, 3.6, 1.5, '#C8E6C9', 'Control Unit', fs=13, ec=C['green'],
          sublabel='Sequencing & Decode')
    _sbox(ax, 0.7, 1.2, 3.6, 1.5, '#A5D6A7', 'ALU', fs=14, ec=C['green'],
          sublabel='Arithmetic & Logic')

    # Single shared memory
    _sbox(ax, 6.0, 2.5, 2.5, 2.5, '#BBDEFB', 'Memory', fs=14, ec=C['accent'],
          sublabel='Instructions & Data')

    # I/O
    _sbox(ax, 6.0, 0.0, 2.5, 1.8, '#FFE0B2', 'I/O Devices', fs=12, ec=C['orange'])

    # System bus (vertical bar on right)
    _sbox(ax, 9.3, 0.5, 1.2, 4.2, '#F3E5F5', 'System\nBus', fs=11, ec=C['purple'])

    # Bus connections
    _arrow(ax, 8.5, 3.75, 9.3, 3.75, C['purple'], lw=2.5, style='<->')
    _arrow(ax, 8.5, 0.9, 9.3, 0.9, C['purple'], lw=2.5, style='<->')
    _arrow(ax, 4.7, 3.0, 9.3, 2.5, C['purple'], lw=2.5, style='<->')

    # CPU ↔ Memory
    _arrow(ax, 4.7, 4.0, 6.0, 4.0, C['accent'], lw=2.2, style='->')
    _arrow(ax, 6.0, 3.2, 4.7, 3.2, C['accent'], lw=2.2, style='->')

    # CPU ↔ I/O
    _arrow(ax, 4.7, 1.5, 6.0, 0.9, C['orange'], lw=2, style='<->', rad=-0.15)

    # Bottleneck note
    ax.text(5.2, -0.75, 'Single shared bus for instructions and data → Von Neumann bottleneck',
            ha='center', va='center', fontsize=10, color=C['red'], style='italic',
            fontfamily='sans-serif',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#FFEBEE',
                      edgecolor=C['red'], alpha=0.9, linewidth=1.5))

    save(fig, 'von_neumann.png')


# ════════════════════════════════════════════════════════════════
# 2. Harvard Architecture
# ════════════════════════════════════════════════════════════════
def gen_harvard():
    fig, ax = plt.subplots(figsize=(12, 6.5))
    fig.set_facecolor(C['bg'])
    ax.set_xlim(-0.5, 12)
    ax.set_ylim(-1, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Harvard Architecture', pad=18, **TITLE_PROPS)

    # CPU boundary
    r = FancyBboxPatch((3.3, 1.0), 4.0, 4.2, boxstyle="round,pad=0.25",
                       facecolor='#E8F5E9', edgecolor=C['green'], linewidth=2.5,
                       alpha=0.5, zorder=1)
    ax.add_patch(r)
    ax.text(5.3, 5.0, 'CPU', ha='center', fontsize=15, fontweight='bold',
            color=C['green'], fontfamily='sans-serif', zorder=3)

    _sbox(ax, 3.7, 3.4, 3.2, 1.3, '#C8E6C9', 'Control Unit', fs=12, ec=C['green'])
    _sbox(ax, 3.7, 1.5, 3.2, 1.3, '#A5D6A7', 'ALU', fs=13, ec=C['green'])

    # Instruction Memory (upper left)
    _sbox(ax, 0.0, 3.8, 2.6, 1.8, '#E3F2FD', 'Instruction\nMemory', fs=11, ec='#1565C0')
    # Data Memory (lower left)
    _sbox(ax, 0.0, 0.8, 2.6, 1.8, '#BBDEFB', 'Data\nMemory', fs=11, ec=C['accent'])

    # I/O (right)
    _sbox(ax, 8.2, 1.8, 2.5, 2.2, '#FFE0B2', 'I/O\nDevices', fs=12, ec=C['orange'])

    # Instruction Bus label + arrow
    _arrow(ax, 2.6, 4.7, 3.3, 4.1, '#1565C0', lw=2.5, style='<->')
    ax.text(2.95, 5.3, 'Instruction Bus', ha='center', fontsize=9,
            fontweight='bold', color='#1565C0', fontfamily='sans-serif',
            bbox=dict(boxstyle='round,pad=0.25', fc='#E3F2FD', ec='#1565C0', lw=1.2))

    # Data Bus label + arrow
    _arrow(ax, 2.6, 1.7, 3.3, 2.1, C['purple'], lw=2.5, style='<->')
    ax.text(2.95, 0.35, 'Data Bus', ha='center', fontsize=9,
            fontweight='bold', color=C['purple'], fontfamily='sans-serif',
            bbox=dict(boxstyle='round,pad=0.25', fc='#F3E5F5', ec=C['purple'], lw=1.2))

    # CPU ↔ I/O
    _arrow(ax, 7.3, 2.9, 8.2, 2.9, C['orange'], lw=2.5, style='<->')

    # Advantage note
    ax.text(5.8, -0.6, 'Separate memories → simultaneous fetch & data access → higher throughput',
            ha='center', va='center', fontsize=10, color=C['green'], style='italic',
            fontfamily='sans-serif',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#E8F5E9',
                      edgecolor=C['green'], alpha=0.9, linewidth=1.5))

    save(fig, 'harvard.png')


# ════════════════════════════════════════════════════════════════
# 3. YARP CPU Core — Schematic Block Diagram
# ════════════════════════════════════════════════════════════════
def gen_cpu_block():
    fig, ax = plt.subplots(figsize=(14, 8.5))
    fig.set_facecolor('#FFFDF7')
    ax.set_xlim(-1, 15)
    ax.set_ylim(-1.5, 8.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # ── outer processor boundary (dashed) ─────────────────
    outer = FancyBboxPatch((-0.5, -0.8), 15, 9, boxstyle="round,pad=0.3",
                           facecolor='#FEFEFE', edgecolor=C['dark'],
                           linewidth=2, linestyle='--', zorder=0, alpha=0.3)
    ax.add_patch(outer)
    ax.text(14, 8.0, 'YARP', ha='right', fontsize=20, fontweight='bold',
            color=C['dark'], fontfamily='sans-serif', style='italic', zorder=5)

    # ── CONTROL (top, spans most width) ───────────────────
    _sbox(ax, 1.5, 7.0, 8.5, 1.0, '#FFE0B2', 'CONTROL', fs=13, ec=C['orange'], lw=2.5)

    # ── BRANCH CONTROL (top right) ────────────────────────
    _sbox(ax, 10.5, 7.0, 2.5, 1.0, '#FFE0B2', 'BRANCH\nCONTROL', fs=10, ec=C['orange'], lw=2.5)

    # Control signals going down (vertical lines)
    ctrl_xs = [2.5, 4.0, 5.5, 7.0, 8.5]
    for cx in ctrl_xs:
        ax.plot([cx, cx], [7.0, 6.0], color=C['orange'], lw=1.2, ls='--',
                alpha=0.5, zorder=1)

    # ── Main datapath row (y ≈ 3.5–6) ────────────────────
    # IMEM
    _sbox(ax, 0, 3.8, 2.0, 2.2, '#FFCDD2', 'IMEM', fs=14, ec=C['red'], lw=2.5)

    # Decode
    _sbox(ax, 2.6, 3.8, 1.8, 2.2, '#FFCDD2', 'Decode', fs=12, ec=C['red'], lw=2.5)

    # Register File
    _sbox(ax, 5.0, 3.5, 2.2, 2.8, '#FFCDD2', 'REG\nFILE', fs=13, ec=C['red'], lw=2.5)

    # MUX before ALU (selects rs2 or pc_q)
    _mux(ax, 7.8, 5.5, w=0.5, h=1.0, color='#4FC3F7', label='')
    _mux(ax, 7.8, 4.2, w=0.5, h=1.0, color='#4FC3F7', label='')

    # ALU
    # Draw ALU as a trapezoidal shape (wider at top, narrower at bottom)
    alu_pts = [(8.6, 6.2), (10.0, 5.5), (10.0, 3.8), (8.6, 3.1),
               (8.6, 4.2), (9.0, 4.65), (8.6, 5.1)]
    alu = Polygon(alu_pts, closed=True, facecolor='#C8E6C9', edgecolor=C['green'],
                  linewidth=2.5, zorder=3)
    ax.add_patch(alu)
    ax.text(9.15, 4.65, 'ALU', ha='center', va='center', fontsize=14,
            fontweight='bold', color=C['green'], zorder=4, fontfamily='sans-serif')

    # MUX after ALU
    _mux(ax, 10.5, 4.65, w=0.5, h=1.0, color='#4FC3F7', label='')

    # DMEM
    _sbox(ax, 11.3, 3.5, 2.2, 2.8, '#FFCDD2', 'DMEM', fs=14, ec=C['red'], lw=2.5)

    # ── Bottom: PC_REG + Adder ────────────────────────────
    _sbox(ax, 0, 0.5, 1.8, 1.2, '#FFCDD2', 'PC_REG', fs=11, ec=C['red'], lw=2.5)

    # Adder circle
    circle = plt.Circle((3.2, 1.1), 0.45, facecolor='#FFCDD2',
                         edgecolor=C['red'], linewidth=2, zorder=3)
    ax.add_patch(circle)
    ax.text(3.2, 1.1, '+', ha='center', va='center', fontsize=18,
            fontweight='bold', color=C['red'], zorder=4)

    # 32'h4 label
    ax.text(3.2, 0.3, "32'h4", ha='center', fontsize=9, fontweight='bold',
            color=C['dark'], fontfamily='monospace', zorder=4,
            bbox=dict(boxstyle='round,pad=0.15', fc='#FFF9C4', ec=C['gold'], lw=1))

    # PC MUX (selects between PC+4 and branch target)
    _mux(ax, 5.5, 1.1, w=0.5, h=1.2, color='#4FC3F7', label='')

    # ── Wiring / Data flow ────────────────────────────────
    # PC_REG → IMEM (pc_q going up)
    ax.plot([0.9, 0.9], [1.7, 3.8], color=C['dark'], lw=2, zorder=2)
    ax.annotate('', xy=(0.9, 3.8), xytext=(0.9, 1.7),
                arrowprops=dict(arrowstyle='->', color=C['dark'], lw=2), zorder=4)

    # pc_q label
    ax.text(0.5, 2.8, 'pc_q', fontsize=8, color=C['accent'], fontweight='bold',
            fontfamily='monospace', rotation=90, ha='center', zorder=4)

    # PC_REG → Adder
    _arrow(ax, 1.8, 1.1, 2.75, 1.1, C['dark'], lw=2)

    # Adder → PC MUX
    _arrow(ax, 3.65, 1.1, 5.25, 1.1, C['dark'], lw=2)

    # PC MUX → PC_REG (loop back underneath)
    ax.plot([5.75, 6.2, 6.2, -0.4, -0.4, 0], [1.1, 1.1, 0.0, 0.0, 1.1, 1.1],
            color=C['dark'], lw=2, zorder=2)
    ax.annotate('', xy=(0, 1.1), xytext=(-0.4, 1.1),
                arrowprops=dict(arrowstyle='->', color=C['dark'], lw=2), zorder=4)

    # pc_q → ALU MUX (top)
    ax.plot([0.9, 0.9], [2.8, 6.8], color=C['accent'], lw=1.5, ls=':', zorder=1)
    ax.plot([0.9, 7.55], [6.8, 6.8], color=C['accent'], lw=1.5, ls=':', zorder=1)
    ax.plot([7.55, 7.55], [6.8, 5.8], color=C['accent'], lw=1.5, zorder=1)
    ax.annotate('', xy=(7.55, 5.8), xytext=(7.55, 6.2),
                arrowprops=dict(arrowstyle='->', color=C['accent'], lw=1.5), zorder=4)
    ax.text(4.5, 6.95, 'pc_q', fontsize=8, color=C['accent'], fontweight='bold',
            fontfamily='monospace', ha='center', zorder=4)

    # IMEM → Decode
    _arrow(ax, 2.0, 4.9, 2.6, 4.9, C['dark'], lw=2)

    # Decode → Reg File
    _arrow(ax, 4.4, 4.9, 5.0, 4.9, C['dark'], lw=2)

    # Reg File → MUX (top) rs1
    _arrow(ax, 7.2, 5.5, 7.55, 5.5, C['dark'], lw=2)

    # Reg File → MUX (bot) rs2
    _arrow(ax, 7.2, 4.2, 7.55, 4.2, C['dark'], lw=2)

    # MUX top → ALU top
    _arrow(ax, 8.05, 5.5, 8.6, 5.5, C['dark'], lw=2)

    # MUX bot → ALU bot
    _arrow(ax, 8.05, 4.2, 8.6, 4.2, C['dark'], lw=2)

    # ALU → MUX after ALU
    _arrow(ax, 10.0, 4.65, 10.25, 4.65, C['dark'], lw=2)

    # MUX after ALU → DMEM
    _arrow(ax, 10.75, 4.65, 11.3, 4.65, C['dark'], lw=2)

    # Branch result → PC MUX (from ALU/branch control down)
    ax.plot([11.75, 11.75], [7.0, 6.8], color=C['orange'], lw=1.5, zorder=2)
    ax.plot([11.75, 7.0, 7.0], [6.8, 6.8, 1.5], color=C['orange'], lw=1.5, ls='--', zorder=1)
    ax.annotate('', xy=(5.75, 1.3), xytext=(7.0, 1.3),
                arrowprops=dict(arrowstyle='->', color=C['orange'], lw=1.5), zorder=4)

    # DMEM output → goes back (write-back path)
    ax.plot([13.5, 13.8, 13.8], [4.65, 4.65, 2.5], color=C['purple'], lw=1.8, zorder=2)
    ax.plot([13.8, 5.5, 5.5], [2.5, 2.5, 3.5], color=C['purple'], lw=1.8, zorder=2)
    ax.annotate('', xy=(5.5, 3.5), xytext=(5.5, 2.7),
                arrowprops=dict(arrowstyle='->', color=C['purple'], lw=1.8), zorder=4)
    ax.text(12.0, 2.2, 'Write-back', fontsize=8, color=C['purple'],
            fontweight='bold', fontfamily='sans-serif', zorder=4)

    # Control → IMEM, Decode, RegFile, ALU, DMEM (dashed arrows down)
    tgt_xs = [1.0, 3.5, 6.1, 9.3, 12.4]
    tgt_ys = [6.0, 6.0, 6.3, 6.5, 6.3]
    for tx, ty in zip(tgt_xs, tgt_ys):
        ax.annotate('', xy=(tx, ty), xytext=(tx, 7.0),
                    arrowprops=dict(arrowstyle='->', color=C['orange'],
                                    lw=1.2, ls='--'), zorder=2)

    # Branch control → PC MUX (dashed)
    ax.text(11.75, 6.65, 'branch\ntarget', fontsize=7, color=C['orange'],
            fontweight='bold', fontfamily='monospace', ha='center', va='top', zorder=4)

    # Signal labels on datapath
    ax.text(2.3, 5.25, 'instr', fontsize=7.5, color=C['gray'], fontweight='bold',
            fontfamily='monospace', ha='center', zorder=4)
    ax.text(4.7, 5.25, 'rs1/rs2\nrd', fontsize=7, color=C['gray'], fontweight='bold',
            fontfamily='monospace', ha='center', zorder=4)

    save(fig, 'cpu_block.png', dpi=220)


# ════════════════════════════════════════════════════════════════
# 4. RV32I Register File (Programmer's Model)
# ════════════════════════════════════════════════════════════════
def gen_register_file():
    fig, ax = plt.subplots(figsize=(9, 13))
    fig.set_facecolor(C['bg'])
    ax.set_xlim(-1.5, 9.5)
    ax.set_ylim(-1.5, 34)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("RV32I Programmer's Model — 32 Registers (x0–x31)",
                 fontsize=15, fontweight='bold', color=C['dark'],
                 fontfamily='sans-serif', pad=18)

    reg_names = [
        ('x0',  'zero', 'Hard-wired zero'),
        ('x1',  'ra',   'Return address'),
        ('x2',  'sp',   'Stack pointer'),
        ('x3',  'gp',   'Global pointer'),
        ('x4',  'tp',   'Thread pointer'),
        ('x5',  't0',   'Temp / alt link'),
        ('x6',  't1',   'Temporary'),
        ('x7',  't2',   'Temporary'),
        ('x8',  's0/fp','Saved / frame ptr'),
        ('x9',  's1',   'Saved register'),
        ('x10', 'a0',   'Arg / return val'),
        ('x11', 'a1',   'Arg / return val'),
        ('x12', 'a2',   'Argument'),
        ('x13', 'a3',   'Argument'),
        ('x14', 'a4',   'Argument'),
        ('x15', 'a5',   'Argument'),
        ('x16', 'a6',   'Argument'),
        ('x17', 'a7',   'Argument'),
        ('x18', 's2',   'Saved register'),
        ('x19', 's3',   'Saved register'),
        ('x20', 's4',   'Saved register'),
        ('x21', 's5',   'Saved register'),
        ('x22', 's6',   'Saved register'),
        ('x23', 's7',   'Saved register'),
        ('x24', 's8',   'Saved register'),
        ('x25', 's9',   'Saved register'),
        ('x26', 's10',  'Saved register'),
        ('x27', 's11',  'Saved register'),
        ('x28', 't3',   'Temporary'),
        ('x29', 't4',   'Temporary'),
        ('x30', 't5',   'Temporary'),
        ('x31', 't6',   'Temporary'),
    ]

    def get_color(i):
        if i == 0: return '#BDBDBD'
        if i == 1: return '#EF9A9A'
        if i == 2: return '#F48FB1'
        if i in (3, 4): return '#CE93D8'
        if i in (5, 6, 7, 28, 29, 30, 31): return '#90CAF9'
        if i in (8, 9, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27): return '#A5D6A7'
        if 10 <= i <= 17: return '#FFCC80'
        return C['light']

    bw, bh = 5.5, 0.88
    x0 = 1.5
    for i, (reg, abi, desc) in enumerate(reg_names):
        y = 32 - i
        fc = get_color(i)
        r = FancyBboxPatch((x0, y), bw, bh, boxstyle="round,pad=0.06",
                           facecolor=fc, edgecolor=C['dark'], linewidth=1.3,
                           zorder=2)
        ax.add_patch(r)
        ax.text(x0 - 0.2, y + bh/2, reg, ha='right', va='center',
                fontsize=9, fontweight='bold', color=C['dark'],
                family='monospace', zorder=3)
        ax.text(x0 + 0.75, y + bh/2, abi, ha='center', va='center',
                fontsize=9, fontweight='bold', color=C['purple'],
                family='monospace', zorder=3)
        ax.text(x0 + bw/2 + 0.5, y + bh/2, desc, ha='center', va='center',
                fontsize=9, color=C['dark'], fontfamily='sans-serif', zorder=3)
        if i == 0:
            ax.annotate('', xy=(x0 + bw, y + bh + 0.18), xytext=(x0, y + bh + 0.18),
                        arrowprops=dict(arrowstyle='<->', color=C['accent'], lw=1.5))
            ax.text(x0 + bw/2, y + bh + 0.4, '32 bits', ha='center', fontsize=9,
                    fontweight='bold', color=C['accent'], fontfamily='sans-serif')

    # PC
    y_pc = -0.5
    r = FancyBboxPatch((x0, y_pc), bw, bh, boxstyle="round,pad=0.06",
                       facecolor='#FFF9C4', edgecolor=C['gold'], linewidth=2.5,
                       zorder=2)
    ax.add_patch(r)
    ax.text(x0 - 0.2, y_pc + bh/2, 'PC', ha='right', va='center',
            fontsize=9, fontweight='bold', color=C['gold'],
            family='monospace', zorder=3)
    ax.text(x0 + bw/2 + 0.5, y_pc + bh/2, 'Program Counter (32 bits)',
            ha='center', va='center', fontsize=10, fontweight='bold',
            color=C['gold'], fontfamily='sans-serif', zorder=3)

    # Legend
    legend_items = [
        ('#BDBDBD', 'Zero (x0)'),
        ('#EF9A9A', 'Return Address'),
        ('#F48FB1', 'Stack Pointer'),
        ('#CE93D8', 'Global/Thread Ptr'),
        ('#90CAF9', 'Temporaries'),
        ('#A5D6A7', 'Saved Registers'),
        ('#FFCC80', 'Arguments'),
        ('#FFF9C4', 'Program Counter'),
    ]
    for j, (col, lbl) in enumerate(legend_items):
        lx = 7.8
        ly = 32.5 - j * 1.05
        r = FancyBboxPatch((lx, ly), 0.55, 0.55, boxstyle="round,pad=0.03",
                           facecolor=col, edgecolor=C['dark'], linewidth=0.8,
                           zorder=2)
        ax.add_patch(r)
        ax.text(lx + 0.7, ly + 0.27, lbl, ha='left', va='center',
                fontsize=7.5, color=C['dark'], fontfamily='sans-serif',
                zorder=3)

    save(fig, 'register_file.png', dpi=200)


# ════════════════════════════════════════════════════════════════
# 5. RV32I Instruction Formats (R, I, S, B, U, J)
# ════════════════════════════════════════════════════════════════
def gen_instruction_formats():
    fig, axes = plt.subplots(6, 1, figsize=(14, 17))
    fig.set_facecolor(C['bg'])
    fig.suptitle('RV32I Base Instruction Formats', fontsize=20,
                 fontweight='bold', color=C['dark'], y=0.985,
                 fontfamily='sans-serif')

    formats = [
        {
            'name': 'R-Type  (Register-Register)',
            'fields': [
                (25, 31, 'funct7',  7, '#EF9A9A'),
                (20, 24, 'rs2',     5, '#A5D6A7'),
                (15, 19, 'rs1',     5, '#90CAF9'),
                (12, 14, 'funct3',  3, '#FFCC80'),
                (7,  11, 'rd',      5, '#CE93D8'),
                (0,   6, 'opcode',  7, '#81D4FA'),
            ],
            'color': '#C62828',
        },
        {
            'name': 'I-Type  (Immediate)',
            'fields': [
                (20, 31, 'imm[11:0]', 12, '#EF9A9A'),
                (15, 19, 'rs1',       5,  '#90CAF9'),
                (12, 14, 'funct3',    3,  '#FFCC80'),
                (7,  11, 'rd',        5,  '#CE93D8'),
                (0,   6, 'opcode',    7,  '#81D4FA'),
            ],
            'color': '#1565C0',
        },
        {
            'name': 'S-Type  (Store)',
            'fields': [
                (25, 31, 'imm[11:5]', 7, '#EF9A9A'),
                (20, 24, 'rs2',       5, '#A5D6A7'),
                (15, 19, 'rs1',       5, '#90CAF9'),
                (12, 14, 'funct3',    3, '#FFCC80'),
                (7,  11, 'imm[4:0]',  5, '#EF9A9A'),
                (0,   6, 'opcode',    7, '#81D4FA'),
            ],
            'color': '#2E7D32',
        },
        {
            'name': 'B-Type  (Branch)',
            'fields': [
                (31, 31, '[12]',    1, '#EF9A9A'),
                (25, 30, '[10:5]',  6, '#EF9A9A'),
                (20, 24, 'rs2',     5, '#A5D6A7'),
                (15, 19, 'rs1',     5, '#90CAF9'),
                (12, 14, 'funct3',  3, '#FFCC80'),
                (8,  11, '[4:1]',   4, '#EF9A9A'),
                (7,   7, '[11]',    1, '#EF9A9A'),
                (0,   6, 'opcode',  7, '#81D4FA'),
            ],
            'color': '#E65100',
        },
        {
            'name': 'U-Type  (Upper Immediate)',
            'fields': [
                (12, 31, 'imm[31:12]', 20, '#EF9A9A'),
                (7,  11, 'rd',          5, '#CE93D8'),
                (0,   6, 'opcode',      7, '#81D4FA'),
            ],
            'color': '#6A1B9A',
        },
        {
            'name': 'J-Type  (Jump)',
            'fields': [
                (31, 31, '[20]',     1, '#EF9A9A'),
                (21, 30, '[10:1]',  10, '#EF9A9A'),
                (20, 20, '[11]',     1, '#EF9A9A'),
                (12, 19, '[19:12]',  8, '#EF9A9A'),
                (7,  11, 'rd',       5, '#CE93D8'),
                (0,   6, 'opcode',   7, '#81D4FA'),
            ],
            'color': '#00695C',
        },
    ]

    for idx, (ax, fmt) in enumerate(zip(axes, formats)):
        ax.set_xlim(-1, 33)
        ax.set_ylim(-0.9, 2.4)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor(C['bg'])

        ax.text(-0.5, 1.9, fmt['name'], fontsize=14, fontweight='bold',
                color=fmt['color'], fontfamily='sans-serif')

        h = 1.0
        y0 = 0.2

        for lo, hi, label, width, fc in fmt['fields']:
            x = lo
            w = hi - lo + 1
            r = FancyBboxPatch((x, y0), w, h, boxstyle="round,pad=0.04",
                               facecolor=fc, edgecolor=C['dark'], linewidth=1.5,
                               zorder=2)
            ax.add_patch(r)
            fs = 9.5 if w >= 4 else (8 if w >= 2 else 7)
            ax.text(x + w/2, y0 + h/2, label, ha='center', va='center',
                    fontsize=fs, fontweight='bold', color=C['dark'],
                    fontfamily='sans-serif', zorder=3)
            if w > 1:
                ax.text(x + 0.15, y0 - 0.22, str(lo), ha='center',
                        fontsize=6.5, color=C['gray'], fontfamily='monospace')
                ax.text(x + w - 0.15, y0 - 0.22, str(hi), ha='center',
                        fontsize=6.5, color=C['gray'], fontfamily='monospace')
            else:
                ax.text(x + 0.5, y0 - 0.22, str(lo), ha='center',
                        fontsize=6.5, color=C['gray'], fontfamily='monospace')

        ax.text(0, y0 + h + 0.18, '0', ha='center', fontsize=7,
                color=C['accent'], fontfamily='monospace')
        ax.text(31.5, y0 + h + 0.18, '31', ha='center', fontsize=7,
                color=C['accent'], fontfamily='monospace')

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    save(fig, 'instruction_formats.png', dpi=200)


# ════════════════════════════════════════════════════════════════
# 6. Instruction type overview (conceptual)
# ════════════════════════════════════════════════════════════════
def gen_type_overview():
    fig, ax = plt.subplots(figsize=(13, 7.5))
    fig.set_facecolor(C['bg'])
    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(-0.5, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('RV32I Instruction Types — Overview', pad=18, **TITLE_PROPS)

    types = [
        ('R-Type', 'Register ↔ Register\nADD, SUB, AND, OR,\nXOR, SLL, SLT, ...', '#EF9A9A', '#C62828'),
        ('I-Type', 'Immediate Operations\nADDI, LW, JALR,\nSLTI, XORI, ...', '#90CAF9', '#1565C0'),
        ('S-Type', 'Store to Memory\nSW, SH, SB', '#A5D6A7', '#2E7D32'),
        ('B-Type', 'Conditional Branch\nBEQ, BNE, BLT,\nBGE, BLTU, BGEU', '#FFCC80', '#E65100'),
        ('U-Type', 'Upper Immediate\nLUI, AUIPC', '#CE93D8', '#6A1B9A'),
        ('J-Type', 'Jump\nJAL', '#80CBC4', '#00695C'),
    ]

    cols = 3
    for i, (tname, desc, fc, ec) in enumerate(types):
        col = i % cols
        row = i // cols
        x = col * 4.0 + 0.3
        y = 5.2 - row * 3.5
        w, h = 3.4, 2.8

        r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.18",
                           facecolor=fc, edgecolor=ec, linewidth=2.5, zorder=2)
        ax.add_patch(r)
        ax.text(x + w/2, y + h - 0.4, tname, ha='center', va='center',
                fontsize=16, fontweight='bold', color=ec,
                fontfamily='sans-serif', zorder=3)
        ax.text(x + w/2, y + h/2 - 0.25, desc, ha='center', va='center',
                fontsize=9.5, color=C['dark'], linespacing=1.4,
                fontfamily='sans-serif', zorder=3)

    save(fig, 'type_overview.png')


# ════════════════════════════════════════════════════════════════
# 7. ISA Map / Opcode Map (simplified visual)
# ════════════════════════════════════════════════════════════════
def gen_isa_map():
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.set_facecolor(C['bg'])
    ax.set_xlim(-0.2, 16.5)
    ax.set_ylim(-0.5, 10)
    ax.axis('off')
    ax.set_title('RV32I Base Integer Instruction Set — Complete Listing',
                 pad=14, **TITLE_PROPS)

    groups = [
        ('R-Type\n(opcode 0110011)', '#EF9A9A', '#C62828', [
            'ADD    rd, rs1, rs2',
            'SUB    rd, rs1, rs2',
            'SLL    rd, rs1, rs2',
            'SLT    rd, rs1, rs2',
            'SLTU   rd, rs1, rs2',
            'XOR    rd, rs1, rs2',
            'SRL    rd, rs1, rs2',
            'SRA    rd, rs1, rs2',
            'OR     rd, rs1, rs2',
            'AND    rd, rs1, rs2',
        ]),
        ('I-Type Arithmetic\n(opcode 0010011)', '#90CAF9', '#1565C0', [
            'ADDI   rd, rs1, imm',
            'SLTI   rd, rs1, imm',
            'SLTIU  rd, rs1, imm',
            'XORI   rd, rs1, imm',
            'ORI    rd, rs1, imm',
            'ANDI   rd, rs1, imm',
            'SLLI   rd, rs1, shamt',
            'SRLI   rd, rs1, shamt',
            'SRAI   rd, rs1, shamt',
        ]),
        ('I-Type Loads\n(opcode 0000011)', '#C8E6C9', '#2E7D32', [
            'LB     rd, imm(rs1)',
            'LH     rd, imm(rs1)',
            'LW     rd, imm(rs1)',
            'LBU    rd, imm(rs1)',
            'LHU    rd, imm(rs1)',
        ]),
        ('S-Type Stores\n(opcode 0100011)', '#A5D6A7', '#388E3C', [
            'SB     rs2, imm(rs1)',
            'SH     rs2, imm(rs1)',
            'SW     rs2, imm(rs1)',
        ]),
        ('B-Type Branches\n(opcode 1100011)', '#FFCC80', '#E65100', [
            'BEQ    rs1, rs2, offset',
            'BNE    rs1, rs2, offset',
            'BLT    rs1, rs2, offset',
            'BGE    rs1, rs2, offset',
            'BLTU   rs1, rs2, offset',
            'BGEU   rs1, rs2, offset',
        ]),
        ('U-Type\n(opcodes 0110111\n / 0010111)', '#CE93D8', '#6A1B9A', [
            'LUI    rd, imm',
            'AUIPC  rd, imm',
        ]),
        ('J-Type / I-Type Jumps\n(opcodes 1101111\n / 1100111)', '#80CBC4', '#00695C', [
            'JAL    rd, offset',
            'JALR   rd, rs1, offset',
        ]),
        ('System\n(opcode 1110011)', '#FFF9C4', '#F57F17', [
            'ECALL',
            'EBREAK',
        ]),
    ]

    x_positions = [0, 4.1, 8.2, 12.3]
    y_start = 9.2
    col = 0
    y = y_start

    for gname, fc, ec, instrs in groups:
        if y - (len(instrs) * 0.33 + 1.3) < -0.3:
            col += 1
            y = y_start
        x = x_positions[col]
        gh = len(instrs) * 0.33 + 1.1

        r = FancyBboxPatch((x, y - gh), 3.7, gh, boxstyle="round,pad=0.12",
                           facecolor=fc, edgecolor=ec, linewidth=2, zorder=2)
        ax.add_patch(r)
        ax.text(x + 1.85, y - 0.28, gname, ha='center', va='top',
                fontsize=8.5, fontweight='bold', color=ec, linespacing=1.2,
                fontfamily='sans-serif', zorder=3)

        nlines = gname.count('\n') + 1
        text_y = y - 0.28 - nlines * 0.3 - 0.1
        for j, instr in enumerate(instrs):
            ax.text(x + 0.3, text_y - j * 0.33, instr,
                    fontsize=8, color=C['dark'], family='monospace',
                    va='top', zorder=3)

        y -= gh + 0.35

    save(fig, 'isa_map.png', dpi=200)


# ════════════════════════════════════════════════════════════════
# 8. Memory layout / addressing
# ════════════════════════════════════════════════════════════════
def gen_memory_layout():
    fig, ax = plt.subplots(figsize=(7.5, 9.5))
    fig.set_facecolor(C['bg'])
    ax.set_xlim(-1, 7.5)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('RV32I Memory Address Space (32-bit)', pad=14, **TITLE_PROPS)

    regions = [
        (8.5, 1.2, '0xFFFFFFFF', '0xF0000000', 'I/O & Peripherals', '#FFCC80', C['orange']),
        (7.0, 1.3, '0xEFFFFFFF', '0x80000000', 'Stack (grows ↓)', '#CE93D8', C['purple']),
        (5.0, 1.8, '0x7FFFFFFF', '0x10000000', 'Heap (grows ↑)\n& Data Segment', '#A5D6A7', C['green']),
        (3.4, 1.4, '0x0FFFFFFF', '0x00001000', 'Text (Instructions)', '#90CAF9', C['accent']),
        (2.4, 0.8, '0x00000FFF', '0x00000000', 'Reserved', '#BDBDBD', C['gray']),
    ]

    bw = 4.5
    x0 = 1.2
    for y, h, addr_hi, addr_lo, label, fc, ec in regions:
        r = FancyBboxPatch((x0, y), bw, h, boxstyle="round,pad=0.1",
                           facecolor=fc, edgecolor=ec, linewidth=2.2, zorder=2)
        ax.add_patch(r)
        ax.text(x0 + bw/2, y + h/2, label, ha='center', va='center',
                fontsize=10.5, fontweight='bold', color=C['dark'],
                fontfamily='sans-serif', zorder=3)
        ax.text(x0 - 0.2, y + h, addr_hi, ha='right', va='bottom',
                fontsize=7, color=ec, family='monospace', fontweight='bold', zorder=3)
        ax.text(x0 - 0.2, y, addr_lo, ha='right', va='bottom',
                fontsize=7, color=ec, family='monospace', fontweight='bold', zorder=3)

    ax.annotate('', xy=(x0 + bw + 0.35, 2.4), xytext=(x0 + bw + 0.35, 9.7),
                arrowprops=dict(arrowstyle='<->', color=C['dark'], lw=1.5))
    ax.text(x0 + bw + 0.6, 6.0, '4 GiB\nAddress\nSpace', ha='left',
            va='center', fontsize=9.5, fontweight='bold', color=C['dark'],
            fontfamily='sans-serif')

    save(fig, 'memory_layout.png')


# ════════════════════════════════════════════════════════════════
# 9. YARP fetch interface
# ════════════════════════════════════════════════════════════════
def gen_fetch_interface():
    fig, ax = plt.subplots(figsize=(12.5, 7))
    fig.set_facecolor('#FFFDF7')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('YARP Fetch Interface', pad=16, **TITLE_PROPS)

    block = FancyBboxPatch((4.2, 1.8), 4.4, 4.8, boxstyle="round,pad=0.18",
               facecolor='#506A96', edgecolor=C['dark'],
               linewidth=2.5, zorder=2)
    ax.add_patch(block)
    ax.text(6.4, 4.2, 'FETCH', ha='center', va='center', fontsize=24,
        fontweight='bold', color=C['white'], fontfamily='sans-serif',
        zorder=3)

    _arrow(ax, 0.9, 4.2, 4.2, 4.2, C['gold'], lw=2.8, style='->')
    ax.text(0.15, 4.65, 'instr_mem_pc_i', ha='left', va='center', fontsize=11,
        fontweight='bold', color=C['dark'], fontfamily='sans-serif')
    ax.text(2.45, 4.48, '32', ha='center', va='bottom', fontsize=11,
        fontweight='bold', color=C['gold'], fontfamily='sans-serif')

    _arrow(ax, 8.6, 5.2, 11.5, 5.2, C['orange'], lw=2.6, style='->')
    ax.text(11.7, 5.55, 'instr_mem_req_o', ha='left', va='center', fontsize=11,
        fontweight='bold', color=C['dark'], fontfamily='sans-serif')
    ax.text(10.1, 5.45, '1', ha='center', va='bottom', fontsize=10.5,
        fontweight='bold', color=C['orange'], fontfamily='sans-serif')

    _arrow(ax, 8.6, 4.0, 11.5, 4.0, C['accent'], lw=2.6, style='->')
    ax.text(11.7, 4.35, 'instr_mem_addr_o', ha='left', va='center', fontsize=11,
        fontweight='bold', color=C['dark'], fontfamily='sans-serif')
    ax.text(10.1, 4.25, '32', ha='center', va='bottom', fontsize=10.5,
        fontweight='bold', color=C['accent'], fontfamily='sans-serif')

    _arrow(ax, 11.5, 2.8, 8.6, 2.8, C['green'], lw=2.6, style='->')
    ax.text(11.7, 3.15, 'mem_rd_data_i', ha='left', va='center', fontsize=11,
        fontweight='bold', color=C['dark'], fontfamily='sans-serif')
    ax.text(10.1, 3.05, '32', ha='center', va='bottom', fontsize=10.5,
        fontweight='bold', color=C['green'], fontfamily='sans-serif')

    _arrow(ax, 6.4, 1.8, 6.4, 0.45, C['purple'], lw=2.8, style='->')
    ax.text(6.4, 0.18, 'instr_mem_instr_o', ha='center', va='center',
        fontsize=11, fontweight='bold', color=C['dark'],
        fontfamily='sans-serif')
    ax.text(6.75, 1.0, '32', ha='left', va='center', fontsize=10.5,
        fontweight='bold', color=C['purple'], fontfamily='sans-serif')

    ax.text(6.4, 7.3, 'Single-cycle memory model', ha='center', va='center',
        fontsize=12, fontweight='bold', color=C['dark'],
        fontfamily='sans-serif')
    ax.text(6.4, 6.9,
        'PC drives the address, memory returns the instruction in the same cycle.',
        ha='center', va='center', fontsize=10.5, color=C['dark'],
        fontfamily='sans-serif',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#F5F7FB',
              edgecolor=C['accent'], linewidth=1.3))

    save(fig, 'fetch_interface.png')


# ════════════════════════════════════════════════════════════════
# 10. YARP fetch timing
# ════════════════════════════════════════════════════════════════
def gen_fetch_timing():
    fig, ax = plt.subplots(figsize=(13.5, 6.8))
    fig.set_facecolor(C['bg'])
    ax.set_xlim(0, 10.8)
    ax.set_ylim(0, 8.8)
    ax.axis('off')
    ax.set_title('YARP Fetch Timing (Conceptual)', pad=16, **TITLE_PROPS)

    x0 = 2.2
    step = 1.9
    y0 = 7.1
    lane_gap = 1.0

    for i in range(5):
        x = x0 + i * step
        ax.plot([x, x], [0.9, 7.8], color='#CFD8DC', lw=1, ls='--', zorder=1)
        if i < 4:
            ax.text(x + step / 2, 8.05, f'cycle {i}', ha='center', va='bottom',
                    fontsize=10, fontweight='bold', color=C['dark'],
                    fontfamily='sans-serif')

    def draw_digital(lane_idx, values, color, label):
        y = y0 - lane_idx * lane_gap
        high = y + 0.24
        low = y - 0.24
        xs = []
        ys = []
        for i, value in enumerate(values):
            x_left = x0 + i * step
            x_right = x_left + step
            level = high if value else low
            if i == 0:
                xs.extend([x_left, x_right])
                ys.extend([level, level])
            else:
                prev_level = high if values[i - 1] else low
                xs.extend([x_left, x_left, x_right])
                ys.extend([prev_level, level, level])
        ax.plot(xs, ys, color=color, lw=2.5, zorder=3)
        ax.text(0.25, y, label, ha='left', va='center', fontsize=10.5,
                fontweight='bold', color=C['dark'], family='monospace')

    def draw_bus(lane_idx, values, color, label):
        y = y0 - lane_idx * lane_gap
        ax.text(0.25, y, label, ha='left', va='center', fontsize=10.5,
                fontweight='bold', color=C['dark'], family='monospace')
        for i, value in enumerate(values):
            x_left = x0 + i * step + 0.07
            r = FancyBboxPatch((x_left, y - 0.26), step - 0.14, 0.52,
                               boxstyle="round,pad=0.02", facecolor=color,
                               edgecolor=color, linewidth=1.5, alpha=0.18,
                               zorder=2)
            ax.add_patch(r)
            ax.text(x_left + (step - 0.14) / 2, y, value, ha='center',
                    va='center', fontsize=9.5, color=C['dark'],
                    family='monospace', zorder=3)

    draw_digital(0, [0, 1, 1, 1], C['red'], 'reset_n')
    draw_digital(1, [0, 1, 1, 1], C['orange'], 'instr_mem_req_o')
    draw_bus(2, ['PC0', 'PC4', 'PC8', 'PC12'], C['accent'], 'instr_mem_pc_i')
    draw_bus(3, ['PC0', 'PC4', 'PC8', 'PC12'], C['accent'], 'instr_mem_addr_o')
    draw_bus(4, ['--', 'INST0', 'INST1', 'INST2'], C['green'], 'mem_rd_data_i')
    draw_bus(5, ['--', 'INST0', 'INST1', 'INST2'], C['purple'], 'instr_mem_instr_o')

    ax.text(6.0, 0.35,
            'After reset, request stays high. Address follows the PC, and returned data is forwarded to decode in the same cycle.',
            ha='center', va='center', fontsize=10, color=C['dark'],
            fontfamily='sans-serif',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#F5F7FB',
                      edgecolor=C['accent'], linewidth=1.2))

    save(fig, 'fetch_timing.png')


# ════════════════════════════════════════════════════════════════
# Run all generators
# ════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating images...")
    gen_von_neumann()
    gen_harvard()
    gen_cpu_block()
    gen_register_file()
    gen_instruction_formats()
    gen_type_overview()
    gen_isa_map()
    gen_memory_layout()
    gen_fetch_interface()
    gen_fetch_timing()
    print("All images generated!")
