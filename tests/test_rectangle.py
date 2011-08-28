from __future__ import with_statement

import pytest

from rectangles import Rectangle as R


def test_intersects():
	r1 = R(10, 10, 10, 10)
	assert not r1.intersects(R(0, 10, 9.999, 10))
	assert not r1.intersects(R(0, 10, 10, 10))
	assert r1.intersects(R(0, 10, 10.0000001, 10))
	assert not r1.intersects(R(10, 0, 0, 9.999))
	assert not r1.intersects(R(10, 0, 0, 10))
	assert not r1.intersects(R(10, 0, 0, 10.00001))
	
	assert not r1.intersects(R(20.001, 11, 10, 10))
	assert not r1.intersects(R(19.999, 9.999, 10, 0.0001))
	assert r1.intersects(R(19.999, 9.999, 10, 0.01))

	
def test_get_intersection():
	r1 = R(0, 0, 10, 10)
	r2 = R(0, 0, 20, 20)

	assert r1.get_intersection(r2) == R(0, 0, 10, 10)

	r3 = R(5, 5, 15, 15)
	assert r1.get_intersection(r3) == R(5, 5, 5, 5)
	
	leeway = R(10, 5, 30, 15)
	rect = R(0, 0, 10, 10)
	intsec = leeway.get_intersection(R(leeway.x, leeway.y, rect.w, rect.h))
	assert intsec == R(10, 5, 10, 10)
	
	## test no intersection
	intsec = r1.get_intersection(R(10, 10, 10, 10))
	assert intsec == R()


def test_get_union():
	r1 = R(10, 20, 30, 40)
	r2 = R(5, 10, 15, 20)
	union = r1.get_union(r2)
	
	assert union == R(min((r1.x, r2.x)), min((r1.y, r2.y)), 
						max((r1.x + r1.w - min((r1.x, r2.x)), 
								r2.x + r2.w - min((r1.x, r2.x)))),
						max((r1.y + r1.h - min((r1.y, r2.y)), 
								r2.y + r2.h - min((r1.y, r2.y))))
					)


def test_get_set_delete():
	r1 = R(0, 0, 0, 0)
	
	## negative values for width and height are disallowed
	with pytest.raises(ValueError):
		r1.w = -1
	with pytest.raises(ValueError):
		r1.h = -1

	## Rectangle.w and Rectangle.h don't have a delete method.
	## If you want to reset them to a certain value, just set
	## them explicitly.
	with pytest.raises(AttributeError):
		del r1.w
	with pytest.raises(AttributeError):
		del r1.h