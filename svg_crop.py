#!/usr/bin/env python3
"""
SVG Padding Remover Script
This script removes extra padding from SVG files by calculating the actual bounding box
of the content and adjusting the viewBox accordingly.

Usage:
    python svg_crop.py input.svg [output.svg]
    python svg_crop.py --batch *.svg
    python svg_crop.py --batch input_folder/ output_folder/

Requirements:
    pip install svgpathtools
"""

import sys
import os
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from svgpathtools import svg2paths, wsvg
    SVGPATHTOOLS_AVAILABLE = True
except ImportError:
    SVGPATHTOOLS_AVAILABLE = False
    print("Warning: svgpathtools not installed. Install it with: pip install svgpathtools")


def calculate_bbox_with_svgpathtools(svg_file):
    """Calculate bounding box using svgpathtools library."""
    if not SVGPATHTOOLS_AVAILABLE:
        raise ImportError("svgpathtools is required. Install with: pip install svgpathtools")

    paths, attributes = svg2paths(svg_file)

    if not paths:
        return None

    # Calculate bounding box for all paths
    xmin, xmax, ymin, ymax = None, None, None, None

    for path in paths:
        try:
            bbox = path.bbox()
            if bbox:
                px_min, px_max, py_min, py_max = bbox

                if xmin is None:
                    xmin, xmax, ymin, ymax = px_min, px_max, py_min, py_max
                else:
                    xmin = min(xmin, px_min)
                    xmax = max(xmax, px_max)
                    ymin = min(ymin, py_min)
                    ymax = max(ymax, py_max)
        except Exception as e:
            print(f"Warning: Could not calculate bbox for a path: {e}")
            continue

    if xmin is None:
        return None

    width = xmax - xmin
    height = ymax - ymin

    return {
        'xmin': xmin,
        'ymin': ymin,
        'width': width,
        'height': height,
        'xmax': xmax,
        'ymax': ymax
    }


def parse_viewbox(viewbox_str):
    """Parse viewBox attribute string."""
    if not viewbox_str:
        return None
    parts = viewbox_str.strip().split()
    if len(parts) != 4:
        return None
    return {
        'x': float(parts[0]),
        'y': float(parts[1]),
        'width': float(parts[2]),
        'height': float(parts[3])
    }


def crop_svg(input_file, output_file=None, padding=0):
    """
    Remove extra padding from SVG file.

    Args:
        input_file: Path to input SVG file
        output_file: Path to output SVG file (if None, will add _cropped suffix)
        padding: Optional padding to keep around the content (in SVG units)

    Returns:
        Path to output file
    """
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.parent / f"{input_path.stem}_cropped{input_path.suffix}"

    print(f"Processing: {input_file}")

    # Calculate bounding box
    bbox = calculate_bbox_with_svgpathtools(input_file)

    if bbox is None:
        print(f"Error: Could not calculate bounding box for {input_file}")
        return None

    print(f"Calculated bounding box: x={bbox['xmin']:.2f}, y={bbox['ymin']:.2f}, "
          f"width={bbox['width']:.2f}, height={bbox['height']:.2f}")

    # Register SVG namespace to avoid prefixes
    ET.register_namespace('', 'http://www.w3.org/2000/svg')

    # Parse the SVG file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Get current viewBox
    current_viewbox = root.get('viewBox')
    if current_viewbox:
        old_vb = parse_viewbox(current_viewbox)
        print(f"Old viewBox: x={old_vb['x']}, y={old_vb['y']}, "
              f"width={old_vb['width']}, height={old_vb['height']}")

    # Create new viewBox with padding
    new_x = bbox['xmin'] - padding
    new_y = bbox['ymin'] - padding
    new_width = bbox['width'] + (2 * padding)
    new_height = bbox['height'] + (2 * padding)

    new_viewbox = f"{new_x} {new_y} {new_width} {new_height}"
    root.set('viewBox', new_viewbox)

    print(f"New viewBox: x={new_x:.2f}, y={new_y:.2f}, "
          f"width={new_width:.2f}, height={new_height:.2f}")

    # Remove width and height attributes to make it responsive
    if 'width' in root.attrib:
        del root.attrib['width']
    if 'height' in root.attrib:
        del root.attrib['height']

    # Save the modified SVG
    tree.write(output_file, encoding='unicode', xml_declaration=True)
    print(f"Saved cropped SVG to: {output_file}\n")

    return output_file


def process_batch(input_pattern, output_dir=None, padding=0):
    """
    Process multiple SVG files.

    Args:
        input_pattern: Glob pattern or directory path
        output_dir: Output directory (if None, will use same directory with _cropped suffix)
        padding: Optional padding to keep around the content
    """
    from glob import glob

    input_path = Path(input_pattern)

    # Handle directory input
    if input_path.is_dir():
        svg_files = list(input_path.glob('*.svg'))
    else:
        svg_files = [Path(f) for f in glob(str(input_pattern))]

    if not svg_files:
        print(f"No SVG files found matching: {input_pattern}")
        return

    print(f"Found {len(svg_files)} SVG files to process\n")

    # Create output directory if specified
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

    # Process each file
    for svg_file in svg_files:
        try:
            if output_dir:
                output_file = Path(output_dir) / svg_file.name
            else:
                output_file = None

            crop_svg(str(svg_file), str(output_file) if output_file else None, padding)
        except Exception as e:
            print(f"Error processing {svg_file}: {e}\n")
            continue


def main():
    parser = argparse.ArgumentParser(
        description='Remove extra padding from SVG files by cropping to content bounding box',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s icon.svg                          # Crop single file, output to icon_cropped.svg
  %(prog)s icon.svg output.svg               # Crop single file with custom output name
  %(prog)s icon.svg -p 10                    # Crop with 10 units of padding
  %(prog)s --batch *.svg                     # Crop all SVG files in current directory
  %(prog)s --batch icons/ output/            # Crop all SVGs from icons/ to output/
  %(prog)s --batch icons/ output/ -p 5       # Crop with 5 units padding
        """
    )

    parser.add_argument('input', help='Input SVG file or pattern')
    parser.add_argument('output', nargs='?', help='Output SVG file or directory (optional)')
    parser.add_argument('--batch', '-b', action='store_true',
                        help='Process multiple files (input can be glob pattern or directory)')
    parser.add_argument('--padding', '-p', type=float, default=0,
                        help='Padding to keep around content (default: 0)')

    args = parser.parse_args()

    if not SVGPATHTOOLS_AVAILABLE:
        print("\nError: This script requires svgpathtools library.")
        print("Install it with: pip install svgpathtools\n")
        sys.exit(1)

    if args.batch:
        process_batch(args.input, args.output, args.padding)
    else:
        crop_svg(args.input, args.output, args.padding)


if __name__ == '__main__':
    main()
