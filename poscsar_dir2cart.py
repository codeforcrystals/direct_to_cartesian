#!/usr/bin/env python3

import numpy as np

def read_poscar(file_path):
    """Reads a POSCAR file and extracts its contents."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # System name
    system_name = lines[0].strip()

    # Scaling factor
    scaling_factor = float(lines[1].strip())

    # Lattice vectors
    lattice_vectors = np.array([list(map(float, line.split())) for line in lines[2:5]])

    # Atom types and numbers
    atom_types = lines[5].split()
    atom_counts = list(map(int, lines[6].split()))

    # Check if coordinates are direct
    coord_type = lines[7].strip().lower()
    if coord_type not in ["direct", "d"]:
        raise ValueError("The POSCAR file is not in direct coordinates.")

    # Atomic positions in direct coordinates
    atomic_positions = np.array([list(map(float, line.split()[:3])) for line in lines[8:8 + sum(atom_counts)]])

    return system_name, scaling_factor, lattice_vectors, atom_types, atom_counts, atomic_positions

def convert_to_cartesian(scaling_factor, lattice_vectors, direct_coords):
    """Converts direct coordinates to Cartesian coordinates."""
    lattice_matrix = scaling_factor * lattice_vectors
    cartesian_coords = np.dot(direct_coords, lattice_matrix)
    return cartesian_coords

def write_poscar(file_path, system_name, scaling_factor, lattice_vectors, atom_types, atom_counts, cartesian_coords):
    """Writes the Cartesian coordinates to a new POSCAR file."""
    with open(file_path, 'w') as file:
        file.write(f"{system_name}\n")
        file.write(f"{scaling_factor}\n")
        for vector in lattice_vectors:
            file.write(" ".join(f"{x:.16f}" for x in vector) + "\n")
        file.write(" ".join(atom_types) + "\n")
        file.write(" ".join(map(str, atom_counts)) + "\n")
        file.write("Cartesian\n")
        for coord in cartesian_coords:
            file.write(" ".join(f"{x:.16f}" for x in coord) + "\n")

def write_xyz(file_path, atom_types, atom_counts, cartesian_coords):
    """Writes the Cartesian coordinates to an XYZ file."""
    with open(file_path, 'w') as file:
        total_atoms = sum(atom_counts)
        file.write(f"{total_atoms}\n")
        file.write("Generated from POSCAR\n")
        atom_index = 0
        for atom_type, count in zip(atom_types, atom_counts):
            for _ in range(count):
                coord = cartesian_coords[atom_index]
                file.write(f"{atom_type} {coord[0]:.8f} {coord[1]:.8f} {coord[2]:.8f}\n")
                atom_index += 1

def main():
    input_file = "POSCAR"  # Input file in direct coordinates
    poscar_output_file = "POSCAR_cartesian"  # Output file in Cartesian coordinates
    xyz_output_file = "POSCAR.xyz"  # Output file in XYZ format

    # Read the POSCAR file
    system_name, scaling_factor, lattice_vectors, atom_types, atom_counts, atomic_positions = read_poscar(input_file)

    # Convert to Cartesian coordinates
    cartesian_coords = convert_to_cartesian(scaling_factor, lattice_vectors, atomic_positions)

    # Write the new POSCAR file
    write_poscar(poscar_output_file, system_name, scaling_factor, lattice_vectors, atom_types, atom_counts, cartesian_coords)

    # Write the XYZ file
    write_xyz(xyz_output_file, atom_types, atom_counts, cartesian_coords)

    print(f"Converted POSCAR file written to {poscar_output_file}")
    print(f"XYZ file written to {xyz_output_file}")

if __name__ == "__main__":
    main()
