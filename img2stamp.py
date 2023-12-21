#!/usr/bin/env python
"""A small tool to make stamp stl files from black on white background images."""

import argparse

from PIL import Image
import numpy as np
from stl import mesh

def img2stl(fn, output):
		"read the file in fn and produces an stl to save to output"
		im = Image.open(fn)
		im = im.convert('L')

		width, height = im.size

		heightmap = np.array(im)
		heightmap = 10.0 * (heightmap) / 255.0

		triangles = []

		def p(x, y):
				return x, y, heightmap[y][x]

		def add_quad(triangles, p1, p2, p3, p4):
				triangles.append([p1, p2, p3])
				triangles.append([p3, p2, p4])

		def add_quad2(triangles, p1, p2, p3, p4):
				triangles.append([p1, p2, p3])
				triangles.append([p3, p2, p4])
				print([p1, p2, p3])
				print([p3, p2, p4])

		for y in range(height-1):
				for x in range(width-1):
						# We draw the quad at x,y -> x+1, y+1
						a = p(x,y) # x, y, heightmap[y][x]
						b = p(x+1, y) # x+1, y, heightmap[y][x+1]
						c = p(x, y+1) # x, y+1, heightmap[y+1][x]
						d = p(x+1, y+1) # x+1, y+1, heightmap[y+1][x+1]

						add_quad(triangles, a, b, c, d)

		depth = -10

		ta = p(0, 0)
		tb = p(width-1, 0)
		tc = p(width-1, height-1)
		td = p(0, height-1)

		ba = [0, 0, depth]
		bb = [width-1, 0, depth]
		bc = [width-1, height-1, depth]
		bd = [0, height-1, depth]

		# Add the bottom
		add_quad2(triangles, ba, bd, bb, bc)

		# Front
		for x in range(width-1):
				triangles.append([p(x+1, 0), p(x, 0), ba])
		# Front ta - tb - ba - bb
		triangles.append([tb, ba, bb])

		# Right
		for y in range(height-1):
				triangles.append([p(width-1, y+1), p(width-1, y), bb])
		# Right tb - tc - bb - bc
		triangles.append([tc, bb, bc])

		# Back
		for x in range(width-1):
				triangles.append([p(x, height-1), p(x+1, height-1), bc])
		# # # Back tc - td - bc - bd
		triangles.append([td, bc, bd])

		# Left
		for y in range(height-1):
				triangles.append([p(0, y), p(0, y+1), bd])
		# # # Left td - ta - bd - ba
		triangles.append([ta, bd, ba])

		#print(f"ta = {ta}")
		#print(f"tb = {tb}")
		#print(f"tc = {tc}")
		#print(f"td = {td}")
		#print(f"ba = {ba}")
		#print(f"bb = {bb}")
		#print(f"bc = {bc}")
		#print(f"bd = {bd}")

		cube = mesh.Mesh(np.zeros(len(triangles), dtype=mesh.Mesh.dtype))
		for i, t in enumerate(triangles):
				for j in range(3):
						cube.vectors[i][j] = list(t[j])

		cube.save(output)

parser = argparse.ArgumentParser(
	prog='img2stamp_stl',
	description='Take a black and white image and produce a 3d printable stamp out of it.')

parser.add_argument('filename')           # positional argument
parser.add_argument('out_filename')           # positional argument

args = parser.parse_args()

img2stl(args.filename, args.out_filename)
