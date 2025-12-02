#!/usr/bin/env python3
import numpy as np

def read_contcar(filename="POSCAR"):
    with open(filename, "r") as f:
        lines = f.readlines()

    scale = float(lines[1].split()[0])
    
    # Read lattice vectors
    lattice = np.array([
        list(map(float, lines[2].split())),
        list(map(float, lines[3].split())),
        list(map(float, lines[4].split()))
    ]) * scale

    # Element names & counts
    elements = lines[5].split()
    counts = list(map(int, lines[6].split()))
    
    # Format line
    coord_type = lines[7].strip().lower()
    start = 8

    # Total number of atoms
    total_atoms = sum(counts)

    # Read coordinates
    coords = []
    for i in range(total_atoms):
        coords.append(list(map(float, lines[start + i].split()[:3])))
    coords = np.array(coords)

    return elements, counts, coord_type, lattice, coords

def convert_to_cartesian(lattice, coords):
    return np.dot(coords, lattice)

def write_cartesian(filename, elements, counts, lattice, cart_coords):
    with open(filename, "w") as f:
        f.write("Converted to Cartesian from Direct\n")
        f.write(" 1.0\n")
        for vec in lattice:
            f.write(f" {vec[0]:.16f} {vec[1]:.16f} {vec[2]:.16f}\n")
        f.write(" " + " ".join(elements) + "\n")
        f.write(" " + " ".join(map(str, counts)) + "\n")
        f.write("Cartesian\n")
        for c in cart_coords:
            f.write(f" {c[0]:.16f} {c[1]:.16f} {c[2]:.16f}\n")

if __name__ == "__main__":
    elements, counts, ctype, lattice, coords = read_contcar()
    
    if "direct" in ctype:
        cart_coords = convert_to_cartesian(lattice, coords)
        write_cartesian("CONTCAR7_cartesian", elements, counts, lattice, cart_coords)
        print("Conversion complete! Output saved in: CONTCAR7_cartesian")
    else:
        print("Coordinates are already Cartesian!")
