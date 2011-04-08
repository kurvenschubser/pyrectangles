from __future__ import print_function

import sys

import rectangles

R = rectangles.Rectangle


RECTS = (R(10, 10, 10, 10), R(5, 10, 5, 10), R(25, 10, 10, 10),
			R(10, 25, 10, 10),
			R(10, 40, 10, 5))


def test__get_new_ratio():
	baserect = RECTS[0].clone()
	tobeadded = RECTS[1].clone()
	
	ratio = rectangles.get_new_ratio(baserect, tobeadded)
	
	assert ratio == 15 / 10.0


def test__get_distance():
	p1 = 10, 20
	p2 = 35, 12
	dist = rectangles.get_distance(p1, p2)
	assert dist == (8 ** 2 + 25 ** 2) ** 0.5


def test__apply_rubberband():
	cx, cy = 20, 20
	leeway = R(10, 0, 30, 15)
	rect = R(0, 0, 10, 10)
	
	rubberbanded = rectangles.apply_rubberband((cx, cy), leeway, rect)
	assert rubberbanded == R(15, 5, 10, 10)
	
	leeway = R(18, 0, 30, 15)
	rubberbanded = rectangles.apply_rubberband((cx, cy), leeway, rect)
	assert rubberbanded == R(18, 5, 10, 10)
	
	leeway = R(22, 0, 30, 15)
	rubberbanded = rectangles.apply_rubberband((cx, cy), leeway, rect)
	assert rubberbanded == R(22, 5, 10, 10)
	
	leeway = R(-2, 0, 20, 18)
	rubberbanded = rectangles.apply_rubberband((cx, cy), leeway, rect)
	assert rubberbanded == R(8, 8, 10, 10)

	leeway = R(-2, 15, 20, 20)
	rubberbanded = rectangles.apply_rubberband((cx, cy), leeway, rect)
	assert rubberbanded == R(8, 15, 10, 10)


def test__apply_centering():
	stable = R(10, 10, 100, 100)
	tobecentered = R(0, 0, 20, 20)
	
	centered = rectangles.apply_centering(tobecentered, stable)
	assert centered == R(50, 50, 20, 20)