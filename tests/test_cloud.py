from __future__ import print_function

import sys
import math
import random

from rectangles import Rectangle as R, RectangleCloud, INF


RECTS = (R(10, 10, 10, 10), R(5, 10, 5, 10), R(25, 10, 10, 10),
			R(10, 25, 10, 10),
			R(10, 40, 10, 5))


CLOUDS = dict(
	checkers = RectangleCloud([
		R(5, 5, 10, 10), R(20, 5, 10, 10), R(35, 5, 10, 10), 
		R(5, 20, 10, 10), R(20, 20, 10, 10), R(35, 20, 10, 10),
		R(5, 35, 10, 10), R(20, 35, 10, 10), R(35, 35, 10, 10)
	]),
	cross = RectangleCloud([
		R(0, 10, 10, 20), R(10, 0, 10, 40), R(20, 10, 10, 20)
	]),
	slash = RectangleCloud([
		R(5, 5, 10, 10), R(20, 20, 10, 10), R(35, 35, 10, 10)
	]),
	back_slash = RectangleCloud([
		R(5, 35, 10, 10), R(20, 20, 10, 10), R(35, 5, 10, 10)
	]),
	x = RectangleCloud([
		R(5, 5, 10, 10),                   R(35, 5, 10, 10),
		                 R(20, 20, 10, 10), 
		R(5,35, 10, 10),                   R(35, 35, 10, 10), 
	]),
	c = RectangleCloud([
		R(5, 5, 10, 10), R(20, 5, 10, 10), R(35, 5, 10, 10),
		R(5, 20, 10, 10),
		R(5,35, 10, 10), R(20, 35, 10, 10), R(35, 35, 10, 10)
	]),
	mortar_left = RectangleCloud([
		R(5, 5, 10, 10), R(20, 5, 10, 10), R(35, 5, 10, 10),
											R(35, 20, 10, 10),
		R(5,35, 10, 10), R(20, 35, 10, 10), R(35, 35, 10, 10)
	]),
	ring = RectangleCloud([
		R(5, 5, 10, 10), R(20, 5, 10, 10), R(35, 5, 10, 10), 
		R(5, 20, 10, 10),                  R(35, 20, 10, 10),
		R(5, 35, 10, 10), R(20, 35, 10, 10), R(35, 35, 10, 10)
	]),
	percent = RectangleCloud([
		R(5, 5, 10, 10),                                                       R(5, 65, 10, 10),
		                 R(20, 20, 10, 10),
		                                   R(35, 35, 10, 10),
		                                                     R(50, 50, 10, 10),
		R(5, 65, 10, 10),									                   R(65, 65, 10, 10)
	]),
	explode = RectangleCloud([
		R(5, 5, 10, 10),                     R(35, 5, 10, 10), 

		R(5, 35, 10, 10),                    R(35, 35, 10, 10)
	]),
	eight = RectangleCloud([
		R(5, 5, 10, 10), R(20, 5, 10, 10), R(35, 5, 10, 10), 
		R(5, 20, 10, 10),                  R(35, 20, 10, 10),
		R(5, 35, 10, 10), R(20, 35, 10, 10), R(35, 35, 10, 10),
		R(5, 50, 10, 10),                    R(35, 50, 10, 10),
		R(5, 65, 10, 10), R(20, 65, 10, 10), R(35, 65, 10, 10)
	]),
	wheel = RectangleCloud([
		R(5, 5, 10, 10), R(20, 5, 10, 10), R(35, 5, 10, 10), R(50, 5, 10, 10), R(65, 5, 10, 10),
		R(5, 20, 10, 10),                                                      R(65, 20, 10, 10),
		R(5, 35, 10, 10),                    R(35, 35, 10, 10),                R(65, 35, 10, 10),
		R(5, 50, 10, 10),                                                      R(65, 50, 10, 10),
		R(5, 65, 10, 10), R(20, 65, 10, 10), R(35, 65, 10, 10), R(50, 65, 10, 10), R(65, 65, 10, 10)
	]),
)


def test_arrange():
	rects = r1, r2 = R(0, 0, 10, 30), R(10, 0, 20, 10)
	cloud = RectangleCloud(rects)
	cloud.arrange()

	assert r1.x == 20 and r2.x == 0 or r1.x == 0 and r2.x == 10
	assert r1.y == 0 and r2.y == 10
	assert r1.w == 10
	assert r1.h == 30

	assert r2.w == 20
	assert r2.h == 10


def test_ratio():
	cloud = RectangleCloud()
	cloud.add_rect(RECTS[0].clone())


def test_add_rect():
	rects = r1, r2 = R(0, 0, 10, 30), R(10, 10, 20, 10)
	cloud = RectangleCloud(rects)

	# add a rect
	r = R(0, 0, 20, 10)
	cloud.add_rect(r)
	assert r == R(10, 20, 10, 0)


def test_add_rect_successive():

	cloud = RectangleCloud()

	# add a rect
	r1 = RECTS[0].clone()

	cloud.add_rect(r)
	assert r1 == R(0,0,10,10)

	# add next rect
	r2 = RECTS[1].clone()

	cloud.add_rect(r2)

	assert r1 == R(0,0,10,10)
	assert r2 == R(10,0,5,10)


def test_get_sorted_left():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)

	assert cloud._rects == rects
	assert (
		cloud.get_sorted_left()
		== [rects[1], rects[0], rects[3], rects[4], rects[2]]
	)


def test_get_sorted_lower():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)
	assert (
		cloud.get_sorted_lower()
		== [rects[0], rects[1], rects[2], rects[3], rects[4]]
	)


def test_get_sorted_right():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)
	assert (
		cloud.get_sorted_right()
		== [rects[1], rects[0], rects[3], rects[4], rects[2]]
	)


def test_get_sorted_upper():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)
	assert (
		cloud.get_sorted_upper()
		== [rects[0], rects[1], rects[2], rects[3], rects[4]]
	)


def test_get_occupied_rect():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)
	assert (
		cloud.get_occupied_rect()
		== R(5, 10, 30, 35)
	)


def test_get_sector_rect():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)

	# x > 0, y > 0
	assert (
		cloud.get_sector_rect(1, 1)
		== R(5 + 30 / 2.0, 10 + 35 / 2.0, 30 / 2.0, 35 / 2.0)
	)
	# x < 0, y > 0
	assert (
		cloud.get_sector_rect(0, 1)
		== R(5, 10 + 35 / 2.0, 30 / 2.0, 35 / 2.0)
	)
	# x < 0, y < 0
	assert (
		cloud.get_sector_rect(0, 0)
		== R(5, 10, 30 / 2.0, 35/ 2.0)
	)
	# x > 0, y < 0
	assert (
		cloud.get_sector_rect(1, 0)
		== R(5 + 30 / 2.0, 10, 30 / 2.0, 35 / 2.0)
	)


def test_get_selection_by_rect():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)

	selrect = cloud.get_sector_rect(1, 1)
	assert (
		set(cloud.get_selection_by_rect(selrect))
		== set()
	)

	selrect = cloud.get_sector_rect(0, 1)
	assert (
		set(cloud.get_selection_by_rect(selrect))
		== set([rects[3], rects[4]])
	)

	selrect = cloud.get_sector_rect(0, 0)
	assert (
		set(cloud.get_selection_by_rect(selrect))
		== set([rects[0], rects[1], rects[3]])
	)

	selrect = cloud.get_sector_rect(1, 0)
	assert (
		set(cloud.get_selection_by_rect(selrect))
		== set([rects[2]])
	)


def test_make_candidates_data():
	r1 = R(5, 5, 10, 30)
	cloud = RectangleCloud([r1])

	## Make a spot facing down to infinity, i.e. without intersection
	occ = cloud.get_occupied_rect()
	spot = R(occ.x - INF, occ.y - INF, occ.w + 2 * INF, INF)
	intsec = occ.get_intersection(spot)
	assert not intsec

	rect = R(0, 0, 10, 10)
	data = cloud.make_candidates_data(spot, rect, occ)

	cand = R(5, -5, 10, 10)
	assert data == [(cand, intsec, spot)]

	## test intersecting spot
	r2 = R(15, 20, 10, 10)
	cloud._rects.append(r2)
	cloud._invalidate()
	occ = cloud.get_occupied_rect()
	spot = R(r1.x + r1.w, r2.y + r2.h, occ.x + occ.w - (r2.x + r2.w) + INF, \
										occ.y + occ.h - (r2.y + r2.h) + INF)
	intsec = occ.get_intersection(spot)
	assert intsec

	data = cloud.make_candidates_data(spot, rect, occ)

	cand = R(spot.x, spot.y, rect.w, rect.h)
	assert data == [(cand, intsec, spot)]


def test_rate_candidates():
	# r1, r2, r3 = R(0, 10, 10, 10), R(10, 0, 10, 30), R(20, 10, 10, 10)
	# cloud = RectangleCloud([r1, r2, r3], steps=12)
	# occ = cloud.get_occupied_rect()
	tobefit = R(0, 0, 20, 20)
	# spots = cloud.get_spots_for_rectangle(tobefit)

	# candidates_data = set()
	# for sp in spots:
		# data = cloud.make_candidates_data(sp, tobefit, occ)
		# candidates_data.update(data)

	# candidates_data = list(candidates_data)
	# rated = cloud.rate_candidates(candidates_data, occ)

	# expected_candidates = [
			# R(r2.x + r2.w, r3.y + r3.h, tobefit.w, tobefit.h),
			# R(r2.x - tobefit.w, r1.y + r1.h, tobefit.w, tobefit.h),
			# R(r2.x - tobefit.w, r1.y - tobefit.h, tobefit.w, tobefit.h),
			# R(r2.x + r2.w, r3.y - tobefit.h, tobefit.w, tobefit.h)
		# ]

	# assert (sorted([n[1] for n in sorted(rated, key=lambda t:t[0])][-4:], key=tuple)
		# == sorted(expected_candidates, key=tuple))


	## Try again with different coordinates.
	r1, r2, r3 = R(0, 15, 15, 10), R(15, 0, 10, 30), R(25, 10, 5, 10)
	cloud = RectangleCloud([r1, r2, r3])
	occ = cloud.get_occupied_rect()

	spots = cloud.get_spots_for_rectangle(tobefit)

	print("\n\n>>>>>>>>>>>>>>>>>>>>candidates_data>>>>>>>>>>>>>>>>>>>")
	print("spots", spots)
	
	candidates_data = set()
	for sp in spots:
		data = cloud.make_candidates_data(sp, tobefit, occ)
		print("sp", sp)
		print("data", data)
		candidates_data.update(data)

	candidates_data = list(candidates_data)
	
	print(candidates_data)
	print("<<<<<<<<<<<<<<<<<<<<<candidates_data<<<<<<<<<<<<<<<<<<<")
	
	rated = cloud.rate_candidates(candidates_data, occ)

	for i, (ratio, c) in enumerate(rated):
		print(i, ratio, c)
		print(c.debuginfo)
		print()
	print([n for n in sorted(rated, key=lambda t:t[0])])

	expected_candidates = [
			R(r2.x + r2.w, r3.y + r3.h, tobefit.w, tobefit.h),
			R(r2.x - tobefit.w, r1.y + r1.h, tobefit.w, tobefit.h),
			R(r2.x - tobefit.w, r1.y - tobefit.h, tobefit.w, tobefit.h),
			R(r2.x + r2.w, r3.y - tobefit.h, tobefit.w, tobefit.h)
		]

	print("\n", "spots", spots)
	print("expected_candidates", expected_candidates, len(expected_candidates))
	print("actual candidates", rated, len(rated))
	print()

	assert (sorted([n[1] for n in sorted(rated, key=lambda t:t[0])][-4:], key=tuple)
		== sorted(expected_candidates, key=tuple))


def test_get_spot_for_rectangle():
	r1, r2, r3 = R(0, 10, 10, 10), R(10, 0, 10, 30), R(20, 10, 10, 10)
	cloud = RectangleCloud([r1, r2, r3])
	occ = cloud.get_occupied_rect()
	
	tobefit = R(0, 0, 20, 20)
	
	spots = cloud.get_spots_for_rectangle(tobefit)
	
	expected_spots = [
		## inner spots
		R(r2.x + r2.w, r3.y + r3.h, 
			occ.x + occ.w - (r2.x + r2.w) + INF,
			occ.y + occ.h - (r3.y + r3.h) + INF),
		R(r2.x + r2.w, occ.y - INF, 
			occ.x + occ.w - (r2.x + r2.w) + INF,
			r3.y - occ.y + INF),
		R(occ.x - INF, occ.y - INF,
			r2.x - occ.x + INF,
			r1.y - occ.y + INF),
		R(occ.x - INF, r1.y + r1.h,
			r2.x - occ.x + INF,
			occ.y + occ.h - (r1.y + r1.h) + INF),
		## outer spots
		R(occ.x + occ.w, occ.y - INF,
			INF,
			occ.h + 2 * INF),
		R(occ.x - INF, occ.y + occ.h,
			occ.w + 2 * INF,
			INF),
		R(occ.x - INF, occ.y - INF,
			INF,
			occ.h + 2 * INF),
		R(occ.x - INF, occ.y - INF,
			occ.w + 2 * INF,
			INF)
	]
	
	print(len(spots), len(expected_spots))
	print(sorted(spots, key=tuple))
	print(sorted(expected_spots, key=tuple))

	assert sorted(spots, key=tuple) == sorted(expected_spots, key=tuple)


##! complete tested sectors
##? put inside class
def test_get_cut_point():
	######################
	## Test sector 1, 1 ##
	######################

	r1, r2 = R(10, 10, 10, 10), R(20.5, 21, 9.5, 9)
	cloud = RectangleCloud([r1, r2])

	rect = r2
	occ = cloud.get_occupied_rect()
	cx, cy = occ.get_center()
	step = 3	# ~= deg 45

	tan = math.tan(2 * math.pi / cloud._steps * step)

	sector_x, sector_y = 1, 1

	## inner horizontal
	outer, vertical = False, False

	cut_x, cut_y = cloud._get_cut_point(rect, cx, cy, tan, sector_x, sector_y,
															outer, vertical)

	assert cut_y == r2.y
	assert cut_x == 21

	## outer vertical
	outer, vertical = True, True

	cut_x, cut_y = cloud._get_cut_point(rect, cx, cy, tan, sector_x, sector_y,
															outer, vertical)

	assert cut_x == r2.x + r2.w
	assert cut_y == r2.y + r2.h

	## outer horizontal
	step = 4	# ~= deg 60
	tan = math.tan(2 * math.pi / cloud._steps * step)
	outer, vertical = True, False

	cut_x, cut_y = cloud._get_cut_point(rect, cx, cy, tan, sector_x, sector_y,
															outer, vertical)

	print(cut_x, cut_y)
	assert r2.x <= cut_x <= r2.x + r2.w
	assert cut_y == r2.x + r2.w

	## inner vertical
	step = 5
	tan = math.tan(2 * math.pi / cloud._steps * step)
	outer, vertical = False, True

	cut_x, cut_y = cloud._get_cut_point(rect, cx, cy, tan, sector_x, sector_y,
															outer, vertical)

	print(cut_x, cut_y)
	assert r2.y <= cut_y <= r2.y + r2.h
	assert cut_x == r2.x

	######################
	## Test sector 0, 0 ##
	######################

	r1, r2 = R(10, 10, 9.5, 9), R(20, 20, 10, 10)
	cloud = RectangleCloud([r1,r2])

	rect = r1
	occ = cloud.get_occupied_rect()
	cx, cy = occ.get_center()
	step = 14	# ~= deg 225

	tan = math.tan(2 * (math.pi / cloud._steps) * step)

	sector_x, sector_y = 0, 0

	## inner horizontal
	outer, vertical = False, False
	cut_x, cut_y = cloud._get_cut_point(rect, cx, cy, tan, sector_x, sector_y,
															outer, vertical)
	assert cut_y == r1.y + r1.h
	assert r1.x <= cut_x <= r1.x + r1.w

	## outer vertical
	outer, vertical = True, True
	cut_x, cut_y = cloud._get_cut_point(rect, cx, cy, tan, sector_x, sector_y,
															outer, vertical)
	assert cut_x == r1.x
	assert r1.y <= cut_y <= r1.y + r1.h

	## outer horizontal
	step = 17
	tan = math.tan(2 * (math.pi / cloud._steps) * step)

	outer, vertical = True, False
	cut_x, cut_y = cloud._get_cut_point(rect, cx, cy, tan, sector_x, sector_y,
															outer, vertical)
	assert cut_y == r1.y
	assert r1.x <= cut_x <= r1.x + r1.w

	## inner vertical
	outer, vertical = False, True
	cut_x, cut_y = cloud._get_cut_point(rect, cx, cy, tan, sector_x, sector_y,
															outer, vertical)
	assert cut_x == r1.x + r1.w
	assert r1.y <= cut_y <= r1.y + r1.h

	## there is no inner horizontal cutting point
	outer, vertical = False, False
	p = cloud._get_cut_point(rect, cx, cy, tan, sector_x, sector_y,
												outer, vertical)
	assert not p


##? put inside class
def test_get_selector():
	r1, r2, r3, r4, r5 = (R(0,0,10,10), R(10,10,10,10), R(20,20,10,10),
							R(0,20,10,10), R(20,0,10,10))
	cloud = RectangleCloud([r1,r2,r3,r4,r5])
	
	sector_x, sector_y = 1,1
	occ= cloud.get_occupied_rect()
	restriction = 1

	## outer vertical
	cut_x, cut_y = 30, 21
	outer, vertical = True, True	

	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )

	assert (sel == R(cut_x, occ.y, occ.x + occ.w - cut_x, occ.h))
	
	## inner vertical ##
	cut_x, cut_y = 20, 21
	outer, vertical = False, True
	
	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )
	
	assert (sel == R(occ.x, occ.y, cut_x - occ.x, occ.h))
	assert (sel == R(0, 0, 20, 30))
	
	## outer horizontal ##
	cut_x, cut_y = 25, 30
	outer, vertical = True, False
	
	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )
	
	assert (sel == R(occ.x, cut_y, occ.w, occ.y + occ.h - cut_y))
	assert (sel == R(0, 30, 30, 0))
	
	## inner horizontal ##
	cut_x, cut_y = 25, 20
	outer, vertical = False, False
	
	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )
	
	assert (sel == R(occ.x, occ.y, occ.w, cut_y - occ.y))
	assert (sel == R(0, 0, 30, 20))
	
	## Sector (0, 0)
	sector_x, sector_y = 0,0

	## outer vertical
	cut_x, cut_y = 0, 2
	outer, vertical = True, True	

	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )

	assert (sel == R(occ.x, occ.y, cut_x - occ.x, occ.h))
	
	## inner vertical ##
	cut_x, cut_y = 10, 3
	outer, vertical = False, True
	
	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )
	
	assert (sel == R(cut_x, occ.y, occ.x + occ.w - cut_x, occ.h))
	assert (sel == R(10, 0, 20, 30))
	
	## outer horizontal ##
	cut_x, cut_y = 4, 0
	outer, vertical = True, False
	
	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )
	
	assert (sel == R(occ.x, occ.y, occ.w, cut_y - occ.y))
	assert (sel == R(0, 0, 30, 0))
	
	## inner horizontal ##
	cut_x, cut_y = 5, 10
	outer, vertical = False, False
	
	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )
	
	assert (sel == R(occ.x, cut_y - occ.y, occ.w, occ.y + occ.h - cut_y))
	assert (sel == R(0, 10, 30, 20))
	
	## sector 0, 1
	sector_x, sector_y = 0,1

	## outer vertical
	cut_x, cut_y = 0, 21
	outer, vertical = True, True	

	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )

	assert (sel == R(cut_x, occ.y, cut_x - occ.x, occ.h))
	
	## inner vertical ##
	cut_x, cut_y = 10, 21
	outer, vertical = False, True
	
	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )
	
	assert (sel == R(cut_x, occ.y, occ.x + occ.w - cut_x, occ.h))
	assert (sel == R(10, 0, 20, 30))
	
	## outer horizontal ##
	cut_x, cut_y = 5, 30
	outer, vertical = True, False
	
	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )
	
	assert (sel == R(occ.x, cut_y, occ.w, occ.y + occ.h - cut_y))
	assert (sel == R(0, 30, 30, 0))
	
	## inner horizontal ##
	cut_x, cut_y = 5, 20
	outer, vertical = False, False
	
	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )
	
	assert (sel == R(occ.x, occ.y, occ.w, cut_y - occ.y))
	assert (sel == R(0, 0, 30, 20))

	## sector 1,0
	sector_x, sector_y = 1,0

	## outer vertical
	cut_x, cut_y = 30, 3
	outer, vertical = True, True	

	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )

	assert (sel == R(cut_x, occ.y, occ.x + occ.w - cut_x, occ.h))
	
	## inner vertical ##
	cut_x, cut_y = 20, 3
	outer, vertical = False, True
	
	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )
	
	assert (sel == R(occ.x, occ.y, cut_x - occ.x, occ.h))
	assert (sel == R(0, 0, 20, 30))
	
	## outer horizontal ##
	cut_x, cut_y = 25, 0
	outer, vertical = True, False
	
	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )
	
	assert (sel == R(occ.x, cut_y, occ.w, cut_y - occ.y))
	assert (sel == R(0, 0, 30, 0))
	
	## inner horizontal ##
	cut_x, cut_y = 25, 10
	outer, vertical = False, False
	
	sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
									outer, vertical, )
	
	assert (sel == R(occ.x, cut_y, occ.w, occ.w + occ.y - cut_y))
	assert (sel == R(0, 10, 30, 20))


class TestGetSpotNoIntersect:
	"""Find spots not intersecting with global occupied rect.
	There is no such thing as an inner non-intersecting spot,
	so do not test for that.
	"""

	def test_outer_vertical(self):
		r1 = R(5, 5, 10, 10)
		cloud = RectangleCloud([r1])
		rectangle = R(0,0,10,10)
		
		occ = cloud.get_occupied_rect()
		outer, vertical = True, True
		
		#################
		## sector 1, 1 ##
		#################

		sector_x, sector_y = 1,1
		cut_x, cut_y = 15, 12
		
		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)
		assert (spot == R(occ.x + occ.w, occ.y - INF, INF, occ.h + 2 * INF))
		
		#################
		## sector 1, 0 ##
		#################

		sector_x, sector_y = 1, 0
		cut_x, cut_y = 15, 8

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)
		assert (spot == R(occ.x + occ.w, occ.y - INF, INF, occ.h + 2 * INF))
		
		#################
		## sector 0, 1 ##
		#################

		sector_x, sector_y = 0, 1
		cut_x, cut_y = 5, 12

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)
		assert (spot == R(occ.x - INF, occ.y - INF, INF, occ.h + 2 * INF))
		
		#################
		## sector 0, 0 ##
		#################

		sector_x, sector_y = 0, 0
		cut_x, cut_y = 5, 8
		
		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)
		assert (spot == R(occ.x - INF, occ.y - INF, INF, occ.h + 2 * INF))


	def test_outer_horizontal(self):
		r1 = R(5, 5, 10, 10)
		cloud = RectangleCloud([r1])
		rectangle = R(0,0,10,10)
		
		occ = cloud.get_occupied_rect()
		outer, vertical = True, False
		
		#################
		## sector 1, 1 ##
		#################

		sector_x, sector_y = 1,1
		cut_x, cut_y = 12, 15

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)	
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)
		assert (spot == R(occ.x - INF, occ.y + occ.h, occ.w + 2 * INF, INF))

		#################
		## sector 1, 0 ##
		#################

		sector_x, sector_y = 1,0
		cut_x, cut_y = 12, 5

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)
		assert (spot == R(occ.x - INF, occ.y - INF, occ.w + 2 * INF, INF))

		#################
		## sector 0, 1 ##
		#################

		sector_x, sector_y = 0, 1
		cut_x, cut_y = 8, 15
		
		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)
		assert (spot == R(occ.x - INF, occ.y + occ.h, occ.w + 2 * INF, INF))

		#################
		## sector 0, 0 ##
		#################

		sector_x, sector_y = 0, 0
		cut_x, cut_y = 8, 5
		
		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)
		assert (spot == R(occ.x - INF, occ.y - INF, occ.w + 2 * INF, INF))

	def test_inner_vertical(self):
		"""There is no such thing as an inner non-intersecting spot."""
	
	def test_inner_horizontal(self):
		"""There is no such thing as an inner non-intersecting spot."""


class TestGetSpotCornerIntersects:
	"""Get spots that have a corner inside occupied rect.
	"""

	def test_outer_vertical(self):
		cloud = CLOUDS["cross"]
		r1, r2, r3 = cloud.get_rects()
		rectangle = R(0, 0, 20, 20)
		occ = cloud.get_occupied_rect()

		###################
		##  sector 1, 1  ##
		###################

		sector_x, sector_y = 1, 1
		outer, vertical = True, True
		cut_x, cut_y = 20, 35

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(r2.x + r2.w, r3.y + r3.h, 
						occ.x + occ.w - (r2.x + r2.w) + INF, 
						occ.y + occ.h - (r3.y + r3.h) + INF)


		####################
		##   sector 1, 0  ##
		####################

		sector_x, sector_y = 1, 0

		outer, vertical = True, True
		cut_x, cut_y = 20, 5

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(r2.x + r2.w, occ.y - INF, 
						occ.x + occ.w - (r2.x + r2.w) + INF, 
						r3.y - occ.y + INF)


		####################
		##   sector 0, 1  ##
		####################

		sector_x, sector_y = 0, 1

		outer, vertical = True, True
		cut_x, cut_y = 10, 35

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(occ.x - INF, r1.y + r1.h, 
						r2.x - occ.x + INF,
						occ.y + occ.h - (r1.y + r1.h) + INF)


		####################
		##   sector 0, 0  ##
		####################

		sector_x, sector_y = 0, 0

		outer, vertical = True, True
		cut_x, cut_y = 10, 5

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(occ.x - INF, occ.y - INF, 
						r2.x - occ.x + INF,
						r1.y - occ.y + INF)


	def test_outer_horizontal(self):
		cloud = CLOUDS["cross"]
		r1, r2, r3 = cloud.get_rects()
		rectangle = R(0, 0, 20, 20)
		occ = cloud.get_occupied_rect()

		###################
		##  sector 1, 1  ##
		###################

		sector_x, sector_y = 1, 1
		outer, vertical = True, False
		cut_x, cut_y = 25, 30

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(r2.x + r2.w, r3.y + r3.h, 
						occ.x + occ.w - (r2.x + r2.w) + INF, 
						occ.y + occ.h - (r3.y + r3.h) + INF)

		####################
		##   sector 1, 0  ##
		####################

		sector_x, sector_y = 1, 0

		outer, vertical = True, False
		cut_x, cut_y = 25, 10

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(r2.x + r2.w, occ.y - INF, 
						occ.x + occ.w - (r2.x + r2.w) + INF, 
						r3.y - occ.y + INF)


		####################
		##   sector 0, 1  ##
		####################

		sector_x, sector_y = 0, 1

		outer, vertical = True, False
		cut_x, cut_y = 5, 30

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(occ.x - INF, r1.y + r1.h, 
						r2.x - occ.x + INF,
						occ.y + occ.h - (r1.y + r1.h) + INF)


		####################
		##   sector 0, 0  ##
		####################

		sector_x, sector_y = 0, 0

		outer, vertical = True, False
		cut_x, cut_y = 5, 10

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(occ.x - INF, occ.y - INF, 
						r2.x - occ.x + INF,
						r1.y - occ.y + INF)


	def test_inner_vertical(self):
		cloud = CLOUDS["slash"]
		r1, r2, r3 = cloud.get_rects()
		rectangle = R(0, 0, 20, 20)
		occ = cloud.get_occupied_rect()

		###################
		##  sector 1, 1  ##
		###################

		sector_x, sector_y = 1, 1
		outer, vertical = False, True
		cut_x, cut_y = 35, 40

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(occ.x - INF, r2.y + r2.h, 
						r3.x - occ.x + INF, 
						occ.y + occ.h - (r2.y + r2.h) + INF)

		####################
		##   sector 0, 0  ##
		####################

		sector_x, sector_y = 0, 0
		outer, vertical = False, True
		cut_x, cut_y = 15, 10

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(r1.x + r1.w, occ.y - INF, 
						occ.x + occ.w - (r1.x + r1.w) + INF,
						r2.y - occ.y  + INF)

		####################
		##   sector 1, 0  ##
		####################
		
		cloud = CLOUDS["back_slash"]
		r1, r2, r3 = cloud.get_rects()
		occ = cloud.get_occupied_rect()

		sector_x, sector_y = 1, 0
		outer, vertical = False, True
		cut_x, cut_y = 35, 10

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(occ.x - INF, occ.y - INF, 
						r3.x - occ.x + INF, 
						r2.y - occ.y + INF)


		####################
		##   sector 0, 1  ##
		####################

		sector_x, sector_y = 0, 1
		outer, vertical = False, True
		cut_x, cut_y = 15, 40

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(r1.x + r1.w, r2.y + r2.h, 
						occ.x + occ.w - (r1.x + r1.w) + INF,
						occ.y + occ.h - (r2.y + r2.h) + INF)


	def test_inner_horizontal(self):
		cloud = CLOUDS["slash"]
		r1, r2, r3 = cloud.get_rects()
		rectangle = R(0, 0, 20, 20)
		occ = cloud.get_occupied_rect()

		###################
		##  sector 1, 1  ##
		###################

		sector_x, sector_y = 1, 1
		outer, vertical = False, False
		cut_x, cut_y = 40, 35

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(r2.x + r2.w, occ.y - INF, 
						occ.x + occ.w - (r2.x + r2.w) + INF, 
						r3.y - occ.y + INF)

		####################
		##   sector 0, 0  ##
		####################

		sector_x, sector_y = 0, 0
		outer, vertical = False, False
		cut_x, cut_y = 5, 15

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(occ.x - INF, r1.y + r1.h, 
						r2.x - occ.x + INF, 
						occ.y + occ.h - (r1.y + r1.h) + INF)

		####################
		##   sector 1, 0  ##
		####################
		
		cloud = CLOUDS["back_slash"]
		r1, r2, r3 = cloud.get_rects()
		occ = cloud.get_occupied_rect()

		sector_x, sector_y = 1, 0
		outer, vertical = False, False
		cut_x, cut_y = 38, 15

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(r2.x + r2.w, r3.y + r3.h, 
						occ.x + occ.w - (r2.x + r2.w) + INF,
						occ.y + occ.h - (r3.y + r3.h) + INF)

		####################
		##   sector 0, 1  ##
		####################

		sector_x, sector_y = 0, 1
		outer, vertical = False, False
		cut_x, cut_y = 10, 35

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(occ.x - INF, occ.y - INF, 
						r2.x - occ.x + INF,
						r1.y - occ.y + INF)


class TestGetSpotStrip:
	"""Get spots that cover a strip across the occupied rect.
	They stretch over the occupied rect completely on one axis, 
	but on the other axis, their border is completely inside the 
	occupied rect.
	"""

	def test_inner_vertical(self):
		cloud = CLOUDS["explode"]
		
		r1, r2, r3, r4 = cloud.get_rects()
		rectangle = R(0, 0, 20, 20)
		occ = cloud.get_occupied_rect()
		
		expected_spot = R(r3.x + r3.w, occ.y - INF, 
							r4.x - (r3.x + r3.w), 
							occ.h + 2 * INF)

		###################
		##  sector 1, 1  ##
		###################

		sector_x, sector_y = 1, 1
		outer, vertical = False, True
		cut_x, cut_y = 35, 40

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 0, 0  ##
		####################

		sector_x, sector_y = 0, 0
		outer, vertical = False, True
		cut_x, cut_y = 15, 10

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 1, 0  ##
		####################

		sector_x, sector_y = 1, 0
		outer, vertical = False, True
		cut_x, cut_y = 35, 10

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 0, 1  ##
		####################

		sector_x, sector_y = 0, 1
		outer, vertical = False, True
		cut_x, cut_y = 15, 40

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

	def test_inner_horizontal(self):
		cloud = CLOUDS["explode"]
		r1, r2, r3, r4 = cloud.get_rects()
		rectangle = R(0, 0, 20, 20)
		occ = cloud.get_occupied_rect()
		
		expected_spot = R(occ.x - INF, r1.y + r1.h, 
							occ.w + 2 * INF, 
							r3.y - (r1.y + r1.h))

		###################
		##  sector 1, 1  ##
		###################

		sector_x, sector_y = 1, 1
		outer, vertical = False, False
		cut_x, cut_y = 40, 35

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		###################
		##  sector 1, 0  ##
		###################

		sector_x, sector_y = 1, 0
		outer, vertical = False, False
		cut_x, cut_y = 40, 15

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		###################
		##  sector 0, 1  ##
		###################

		sector_x, sector_y = 0, 1
		outer, vertical = False, False
		cut_x, cut_y = 10, 35

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		###################
		##  sector 0, 0  ##
		###################

		sector_x, sector_y = 0, 0
		outer, vertical = False, False
		cut_x, cut_y = 10, 15

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

	def test_outer_vertical(self):
		cloud = CLOUDS["ring"]
		r1, r2, r3, r4, r5, r6, r7, r8, = cloud.get_rects()
		rectangle = R(0, 0, 5, 5)
		occ = cloud.get_occupied_rect()

		###################
		##  sector 1, 1  ##
		###################

		sector_x, sector_y = 1, 1
		outer, vertical = True, True
		cut_x, cut_y = 30, 40

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(r7.x + r7.w, occ.y - INF,
							r8.x - (r7.x + r7.w),
							occ.h + 2 * INF)

		###################
		##  sector 1, 0  ##
		###################

		sector_x, sector_y = 1, 0
		outer, vertical = True, True
		cut_x, cut_y = 30, 10

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(r2.x + r2.w, occ.y - INF,
							r3.x - (r2.x + r2.w),
							occ.h + 2 * INF)

		###################
		##  sector 0, 1  ##
		###################

		sector_x, sector_y = 0, 1
		outer, vertical = True, True
		cut_x, cut_y = 20, 40

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(r6.x + r6.w, occ.y - INF,
							r7.x - (r6.x + r6.w),
							occ.h + 2 * INF)

		###################
		##  sector 0, 0  ##
		###################

		sector_x, sector_y = 0, 0
		outer, vertical = True, True
		cut_x, cut_y = 20, 10

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(r1.x + r1.w, occ.y - INF,
							r2.x - (r1.x + r1.w),
							occ.h + 2 * INF)

	def test_outer_horizontal(self):
		cloud = CLOUDS["ring"]
		r1, r2, r3, r4, r5, r6, r7, r8, = cloud.get_rects()
		rectangle = R(0, 0, 5, 5)
		occ = cloud.get_occupied_rect()

		###################
		##  sector 1, 1  ##
		###################

		sector_x, sector_y = 1, 1
		outer, vertical = True, False
		cut_x, cut_y = 40, 30

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(occ.x - INF, r5.y + r5.h,
							occ.w + 2 * INF,
							r8.y - (r5.y + r5.h))

		###################
		##  sector 1, 0  ##
		###################

		sector_x, sector_y = 1, 0
		outer, vertical = True, False
		cut_x, cut_y = 40, 20

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(occ.x - INF, r3.y + r3.h,
							occ.w + 2 * INF,
							r5.y - (r3.y + r3.h))

		###################
		##  sector 0, 1  ##
		###################

		sector_x, sector_y = 0, 1
		outer, vertical = True, False
		cut_x, cut_y = 10, 30

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(occ.x - INF, r4.y + r4.h,
							occ.w + 2 * INF,
							r6.y - (r4.y + r4.h))

		###################
		##  sector 0, 0  ##
		###################

		sector_x, sector_y = 0, 0
		outer, vertical = True, False
		cut_x, cut_y = 10, 20

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == R(occ.x - INF, r1.y + r1.h,
							occ.w + 2 * INF,
							r4.y - (r1.y + r1.h))


##! complete test_outer_XXX methods
class TestGetSpotMortarSituation:
	"""Get spots that are confined inside the occupied rect
	on all but one side.
	"""

	def test_inner_vertical(self):
		cloud = CLOUDS["c"]
		r1, r2, r3, r4, r5, r6, r7 = cloud.get_rects()

		rectangle = R(0, 0, 10, 10)
		occ = cloud.get_occupied_rect()

		expected_spot = R(r4.x + r4.w, r2.y + r2.h, 
							occ.x + occ.w - (r4.x + r4.w) + INF, 
							r6.y - (r2.y + r2.h))

		###################
		##  sector 0, 1  ##
		###################

		sector_x, sector_y = 0, 1
		outer, vertical = False, True
		cut_x, cut_y = 15, 26

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		###################
		##  sector 0, 0  ##
		###################

		sector_x, sector_y = 0, 0
		outer, vertical = False, True
		cut_x, cut_y = 15, 22

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		###################
		##  sector 1, 1  ##
		###################

		cloud = CLOUDS["mortar_left"]
		occ = cloud.get_occupied_rect()
		r1, r2, r3, r4, r5, r6, r7 = cloud.get_rects()
		
		expected_spot = R(occ.x - INF, r1.y + r1.h,
							r4.x - occ.x + INF,
							r6.y - (r2.y + r2.h))

		sector_x, sector_y = 1, 1
		outer, vertical = False, True
		cut_x, cut_y = 35, 26

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		###################
		##  sector 1, 0  ##
		###################

		sector_x, sector_y = 1, 0
		outer, vertical = False, True
		cut_x, cut_y = 35, 22

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

	def test_inner_horizontal(self):
		cloud = CLOUDS["c"]
		r1, r2, r3, r4, r5, r6, r7 = cloud.get_rects()

		rectangle = R(0, 0, 10, 10)
		occ = cloud.get_occupied_rect()

		expected_spot = R(r4.x + r4.w, r2.y + r2.h, 
							occ.x + occ.w - (r4.x + r4.w) + INF, 
							r6.y - (r2.y + r2.h))

		###################
		##  sector 0, 1  ##
		###################

		sector_x, sector_y = 0, 1
		outer, vertical = False, False
		cut_x, cut_y = 22, 35

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		###################
		##  sector 0, 0  ##
		###################

		sector_x, sector_y = 0, 0
		outer, vertical = False, False
		cut_x, cut_y = 22, 15

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		###################
		##  sector 1, 1  ##
		###################

		sector_x, sector_y = 1, 1
		outer, vertical = False, False
		cut_x, cut_y = 27, 35

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		###################
		##  sector 1, 0  ##
		###################

		sector_x, sector_y = 1, 0
		outer, vertical = False, False
		cut_x, cut_y = 27, 15

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

	def test_outer_vertical(self):
		return NotImplemented

	def test_outer_horizontal(self):
		return NotImplemented


class TestGetSpotCompletelyInside:
	"""Get spots that are completely confined inside 
	the occupied rect.
	"""

	def test_inner_vertical(self):
		cloud = CLOUDS["ring"]

		r1, r2, r3, r4, r5, r6, r7, r8 = cloud.get_rects()
		rectangle = R(0, 0, 20, 20)
		occ = cloud.get_occupied_rect()

		expected_spot = R(r4.x + r4.w, r2.y + r2.h, 
							r5.x - (r4.x + r4.w), 
							r7.y - (r2.y + r2.h))

		###################
		##  sector 1, 1  ##
		###################

		sector_x, sector_y = 1, 1
		outer, vertical = False, True
		cut_x, cut_y = 35, 26

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 0, 0  ##
		####################

		sector_x, sector_y = 0, 0
		outer, vertical = False, True
		cut_x, cut_y = 15, 24

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 1, 0  ##
		####################

		sector_x, sector_y = 1, 0
		outer, vertical = False, True
		cut_x, cut_y = 35, 24

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 0, 1  ##
		####################

		sector_x, sector_y = 0, 1
		outer, vertical = False, True
		cut_x, cut_y = 15, 26

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

	def test_inner_horizontal(self):
		cloud = CLOUDS["ring"]

		r1, r2, r3, r4, r5, r6, r7, r8 = cloud.get_rects()
		rectangle = R(0, 0, 20, 20)
		occ = cloud.get_occupied_rect()

		expected_spot = R(r4.x + r4.w, r2.y + r2.h, 
							r5.x - (r4.x + r4.w), 
							r7.y - (r2.y + r2.h))

		###################
		##  sector 1, 1  ##
		###################

		sector_x, sector_y = 1, 1
		outer, vertical = False, False
		cut_x, cut_y = 26, 35

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y, 
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 0, 0  ##
		####################

		sector_x, sector_y = 0, 0
		outer, vertical = False, False
		cut_x, cut_y = 24, 15

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 1, 0  ##
		####################

		sector_x, sector_y = 1, 0
		outer, vertical = False, False
		cut_x, cut_y = 26, 15

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 0, 1  ##
		####################

		sector_x, sector_y = 0, 1
		outer, vertical = False, False
		cut_x, cut_y = 24, 35

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot
	
	def test_outer_vertical(self):
		cloud = CLOUDS["wheel"]

		(r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, 
		r16, r17) = cloud.get_rects()

		rectangle = R(0, 0, 10, 10)
		occ = cloud.get_occupied_rect()

		expected_spot = R(r9.x + r9.w, r4.y + r4.h, 
							r10.x - (r9.x + r9.w), 
							r16.y - (r4.y + r4.h))

		###################
		##  sector 1, 1  ##
		###################

		sector_x, sector_y = 1, 1
		outer, vertical = True, True
		cut_x, cut_y = 45, 43

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 1, 0  ##
		####################

		sector_x, sector_y = 1, 0
		outer, vertical = True, True
		cut_x, cut_y = 45, 37

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 0, 0  ##
		####################

		expected_spot = R(r8.x + r8.w, r2.y + r2.h, 
							r9.x - (r8.x + r8.w), 
							r14.y - (r2.y + r2.h))

		sector_x, sector_y = 0, 0
		outer, vertical = True, True
		cut_x, cut_y = 35, 37

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 0, 1  ##
		####################

		sector_x, sector_y = 0, 1
		outer, vertical = True, True
		cut_x, cut_y = 35, 43

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

	def test_outer_horizontal(self):
		cloud = CLOUDS["wheel"]

		(r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, 
		r16, r17) = cloud.get_rects()

		rectangle = R(0, 0, 10, 10)
		occ = cloud.get_occupied_rect()

		expected_spot = R(r11.x + r11.w, r9.y + r9.h, 
							r12.x - (r11.x + r11.w), 
							r15.y - (r9.y + r9.h))

		###################
		##  sector 1, 1  ##
		###################

		sector_x, sector_y = 1, 1
		outer, vertical = True, False
		cut_x, cut_y = 44, 45

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 0, 1  ##
		####################

		sector_x, sector_y = 0, 1
		outer, vertical = True, False
		cut_x, cut_y = 36, 45

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 1, 0  ##
		####################

		expected_spot = R(r6.x + r6.w, r3.y + r3.h, 
							r7.x - (r6.x + r6.w), 
							r9.y - (r3.y + r3.h))

		sector_x, sector_y = 1, 0
		outer, vertical = True, False
		cut_x, cut_y = 43, 35

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

		####################
		##   sector 0, 0  ##
		####################

		sector_x, sector_y = 0, 0
		outer, vertical = True, False
		cut_x, cut_y = 39, 35

		sel = cloud._get_selector(occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical)
		spot = cloud._get_spot(rectangle, occ, cut_x, cut_y, sel, vertical)

		assert spot == expected_spot

