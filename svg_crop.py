#!/usr/bin/env python3
"""
SVG Padding Remover - Correct Version
Removes ALL padding from all sides and creates a perfectly centered, square output
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from svgpathtools import svg2paths
except ImportError:
    print("Error: svgpathtools not installed")
    sys.exit(1)


def calculate_bbox(svg_file):
    """Calculate bounding box using svgpathtools library."""
    try:
        paths, attributes = svg2paths(svg_file)
    except Exception as e:
        return None

    if not paths:
        return None

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
        except Exception:
            continue

    if xmin is None:
        return None

    return {
        'xmin': xmin,
        'ymin': ymin,
        'xmax': xmax,
        'ymax': ymax,
        'width': xmax - xmin,
        'height': ymax - ymin
    }


def crop_svg_correctly(input_file, output_file, padding=0):
    """
    Remove ALL padding from SVG and create perfectly centered, square output.

    Args:
        input_file: Path to input SVG
        output_file: Path to output SVG
        padding: Optional padding to keep (default: 0)
    """
    # Calculate bounding box
    bbox = calculate_bbox(input_file)
    if bbox is None:
        print(f"❌ Error: Could not calculate bounding box for {input_file}")
        return False

    # Register SVG namespace
    ET.register_namespace('', 'http://www.w3.org/2000/svg')

    # Parse SVG
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Calculate content dimensions with padding
    content_width = bbox['width'] + (2 * padding)
    content_height = bbox['height'] + (2 * padding)

    # Make it square - use the larger dimension
    square_size = max(content_width, content_height)

    # Center the content perfectly in the square
    center_x = bbox['xmin'] + bbox['width'] / 2
    center_y = bbox['ymin'] + bbox['height'] / 2

    # Calculate new viewBox to center content
    new_x = center_x - square_size / 2
    new_y = center_y - square_size / 2

    # Set new viewBox
    new_viewbox = f"{new_x} {new_y} {square_size} {square_size}"
    root.set('viewBox', new_viewbox)

    # Remove fixed width/height
    if 'width' in root.attrib:
        del root.attrib['width']
    if 'height' in root.attrib:
        del root.attrib['height']

    # Save
    tree.write(output_file, encoding='unicode', xml_declaration=True)

    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Crop SVG correctly - remove all padding')
    parser.add_argument('input', help='Input SVG file or directory')
    parser.add_argument('output', help='Output SVG file or directory')
    parser.add_argument('--padding', '-p', type=float, default=0,
                        help='Padding to keep (default: 0)')
    parser.add_argument('--batch', '-b', action='store_true',
                        help='Process directory')

    args = parser.parse_args()

    if args.batch:
        input_dir = Path(args.input)
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        svg_files = sorted(input_dir.glob('*.svg'))
        print(f"Processing {len(svg_files)} icons...\n")

        success_count = 0
        for svg_file in svg_files:
            output_file = output_dir / svg_file.name
            print(f"Processing: {svg_file.name}...", end=' ')

            if crop_svg_correctly(str(svg_file), str(output_file), args.padding):
                print("✓")
                success_count += 1
            else:
                print("✗")

        print(f"\n✅ Successfully processed {success_count}/{len(svg_files)} icons")
    else:
        if crop_svg_correctly(args.input, args.output, args.padding):
            print(f"✅ Saved: {args.output}")
        else:
            print(f"❌ Failed to process {args.input}")


if __name__ == '__main__':
    main()
