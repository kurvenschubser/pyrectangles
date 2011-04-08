from __future__ import print_function

import sys

from rectangles import Rectangle as R, RectangleCloud


RECTS = (R(10, 10, 10, 10), R(5, 10, 5, 10), R(25, 10, 10, 10),
			R(10, 25, 10, 10),
			R(10, 40, 10, 5))


def test__arrange():
	rects = r1, r2 = R(0, 0, 10, 30), R(10, 0, 20, 10)
	cloud = RectangleCloud(rects)
	cloud.arrange()
	
	assert r1.x == 20 and r2.x == 0 or r1.x == 0 and r2.x == 10
	assert r1.y == 0 and r2.y == 10
	assert r1.w == 10
	assert r1.h == 30

	assert r2.w == 20
	assert r2.h == 10		


def test__ratio():
	cloud = RectangleCloud()
	cloud.add_rect(RECTS[0].clone())
	


def test__add_rect():
	rects = r1, r2 = R(0, 0, 10, 30), R(10, 10, 20, 10)
	cloud = RectangleCloud(rects)
	
	# add a rect
	r = R(0, 0, 20, 10)
	cloud.add_rect(r)
	assert r == R(10, 20, 10, 0)


def test__add_rect_successive():

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


def test__get_sorted_left():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)

	assert cloud._rects == rects
	assert (
		cloud.get_sorted_left()
		== [rects[1], rects[0], rects[3], rects[4], rects[2]]
	)


def test__get_sorted_lower():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)
	assert (
		cloud.get_sorted_lower()
		== [rects[0], rects[1], rects[2], rects[3], rects[4]]
	)


def test__get_sorted_right():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)
	assert (
		cloud.get_sorted_right()
		== [rects[1], rects[0], rects[3], rects[4], rects[2]]
	)


def test__get_sorted_upper():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)
	assert (
		cloud.get_sorted_upper()
		== [rects[0], rects[1], rects[2], rects[3], rects[4]]
	)


def test__get_occupied_rect():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)
	assert (
		cloud.get_occupied_rect() 
		== R(5, 10, 30, 35)
	)


def test__get_sector_rect():
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


def test__get_selection_by_rect():
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


def test__get_spots_for_rectangle_outer_spots_simple():
	cloud = RectangleCloud()
	
	r1 = R(10, 10, 100, 100)
	cloud.add_rect(r1)
	
	r2 = R(0, 0, 20, 20)

	spots = cloud.get_spots_for_rectangle(r2, steps=4)

	expected_spots = [
		## facing left
		R(r1.x - sys.maxint, r1.y - sys.maxint, sys.maxint,  2 * sys.maxint + r1.h),
		## facing right
		R(r1.x + r1.w, r1.y - sys.maxint, sys.maxint, 2 * sys.maxint + r1.h),
		## facing up
		R(r1.x - sys.maxint, r1.y + r1.h, 2 * sys.maxint + r1.w, sys.maxint),
		## facing down
		R(r1.x - sys.maxint, r1.y - sys.maxint, 2 * sys.maxint + r1.w, sys.maxint)
	]

	assert sorted(spots, key=lambda r: tuple(r)) \
			== sorted(expected_spots, key=lambda r: tuple(r))

	## For *steps* > 4 there will be duplicate spots found, which are 
	## excluded from the the results.
	spots = cloud.get_spots_for_rectangle(r2, steps=8)
	assert sorted(spots, key=lambda r: tuple(r)) \
			== sorted(expected_spots, key=lambda r: tuple(r))


def test__get_spots_for_rectangle_outer_spots_complex():
	rects = [R(0, 0, 10, 30), R(10, 10, 20, 10)]
	cloud = RectangleCloud(rects)

	spots = cloud.get_spots_for_rectangle(R(0, 0, 20, 20), steps=24)

	expected_spots = [
		R(30, -sys.maxint, sys.maxint, 30 + 2 * sys.maxint),
		R(10, 20, 20 + sys.maxint, 10 + sys.maxint),
		R(-sys.maxint, 30, 30 + 2 * sys.maxint, sys.maxint),
		R(-sys.maxint, -sys.maxint, sys.maxint, 30 + 2 * sys.maxint),
		R(-sys.maxint, -sys.maxint, 30 + 2 * sys.maxint, sys.maxint),
		R(10, -sys.maxint, 20 + sys.maxint, 10 + sys.maxint)
	]

	assert sorted(spots, key=lambda r: tuple(r)) \
			== sorted(expected_spots, key=lambda r: tuple(r))


def test__make_candidates_data():
	rects = [R(0, 0, 10, 30)]
	cloud = RectangleCloud(rects)
	
	## Make a spot facing right to infinity.
	occ = cloud.get_occupied_rect()
	spot = R(occ.x, occ.y - sys.maxint, sys.maxint, 2 * sys.maxint - occ.h)
	rect = R(0, 0, 10, 10)
	
	data = cloud.make_candidates_data(spot, rect, occ)
	
	cand = R(10, 10, 10, 10)
	intsec = R()
	assert data == [(cand, intsec, spot)]
	
	## add *rect* and repeat with different *spot*
	cloud._rects.append(rect)
	cloud._invalidate()
	
	occ = cloud.get_occupied_rect()
	spot = R(10, 20, sys.maxint, sys.maxint)
	

def test__pick_best_spot():
	pass




## !!! Inner spots can't be reliably found. Ignored for now.
def test__get_spots_for_rectangle_inner_spots():
	rects = (
		R(0,0,10,20), R(10,15,10,5), R(10,0,10,12), R(20,0,10,20)
	)
	cloud = RectangleCloud(rects)

	assert (
		set(cloud.get_selection_by_rect(cloud.get_sector_rect(1,1)))
		== set([rects[1], rects[2], rects[3]])
	)

	accomodate_this = R(10.1,12.1,9.8,2.8)

	spots = cloud.get_spots_for_rectangle(accomodate_this)
	print(spots)

	expected_gap_rect = R(10,12,10,3)
	
	assert expected_gap_rect in spots