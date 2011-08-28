from __future__ import print_function


"""
Copyright (c) 2011 Malte Engelhardt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


import os
import sys
import math
import bisect
import operator

try:
	__version__ = tuple(map(int, os.path.split(os.path.dirname(
			os.path.abspath(__file__)))[-1].rsplit("-", 1)[-1].split(".")))
except ValueError:
	__version__ = (0, 0, 0)

__license__ = "MIT"
__author__ = "Malte Engelhardt"
__email__ = "@".join(("kurvenschubser", "gmail.com"))


__all__ = ["Rectangle", "RectangleCloud", "get_new_ratio", "get_distance",
			"rubberband", "center", "partition", "select_by_rect"]


## Must be something that can be used algebraically,
## so it can't be float('inf').
INFINITY = INF = sys.maxint

DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT = range(4)

SORTKEYS = {
	DIRECTION_LEFT: lambda r: r.x, 
	DIRECTION_DOWN: lambda r: r.y,
	DIRECTION_RIGHT: lambda r: r.x + r.w, 
	DIRECTION_UP: lambda r: r.y + r.h
}

HALVERS = {
	DIRECTION_RIGHT: lambda r: r.y + r.h / 2.0,
	DIRECTION_UP: lambda r: r.x + r.w / 2.0
}
HALVERS[DIRECTION_LEFT] = HALVERS[DIRECTION_RIGHT]
HALVERS[DIRECTION_DOWN] = HALVERS[DIRECTION_UP]

STAMPGETTERS = {
		DIRECTION_RIGHT : lambda r: (r.y, r.y + r.h),
		DIRECTION_UP: lambda r: (r.x, r.x + r.w),
}
STAMPGETTERS[DIRECTION_LEFT] = STAMPGETTERS[DIRECTION_RIGHT]
STAMPGETTERS[DIRECTION_DOWN] = STAMPGETTERS[DIRECTION_UP]


def get_new_ratio(baserect, tobeadded):
	"""If Rectangle *tobeadded* was added to Rectangle *baserect*,
	return the new aspect ratio.
	"""

	return baserect.get_union(tobeadded).get_aspect_ratio()


def get_distance((p1_x, p1_y), (p2_x, p2_y)):
	"""Return the distance from point (p1_x, p2_y) to point (p2_x, p2_y).
	"""

	return math.sqrt((p1_x - p2_x) ** 2 + (p1_y - p2_y) ** 2)


##? migrate to class Rectangle?
def rubberband((cx, cy), leeway, rect):
	"""A rubberband effect minimizes the distance from the
	center of *rect* to the point (cx, cy). Possible positions
	are restrained by the *leeway* Rectangle. *rect* will never
	be outside of *leeway*.
	Returns a Rectangle with the newly found coordinates
	and width and height of *rect*.
	"""

	## Minimize distance to x axis.
	if cx < leeway.x + rect.w / 2.0:
		x = leeway.x
	elif cx > leeway.x + leeway.w - rect.w / 2.0:
		x = leeway.x + leeway.w - rect.w
	else:
		x = cx - rect.w / 2.0

	## Minimize distance to y axis.
	if cy < leeway.y + rect.h / 2.0:
		y = leeway.y
	elif cy > leeway.y + leeway.h - rect.h / 2.0:
		y = leeway.y + leeway.h - rect.h
	else:
		y = cy - rect.h / 2.0

	return Rectangle(x, y, rect.w, rect.h)


##? migrate to class Rectangle?
def center(tobecentered, stable):
	"""Place center of Rectangle *tobecentered* exactly on
	center of Rectangle *stable*.
	"""

	tx, ty = tobecentered.get_center()
	sx, sy = stable.get_center()

	return Rectangle(sx - tx, sy - ty, tobecentered.w, tobecentered.h)


def partition(rect, seed, direction):
	"""Cut *rect* in half at *seed*. Return a Rectangle according to 
	direction *direction*.
	"""

	x, y = seed
	r = Rectangle()
	if direction == DIRECTION_RIGHT:
		r.x = x
		r.y = rect.y
		r.w = rect.x + rect.w - x
		r.h = rect.h
	elif direction == DIRECTION_LEFT:
		r.x = rect.x
		r.y = rect.y
		r.w = x - (rect.x)
		r.h = rect.h
	elif direction == DIRECTION_UP:
		r.x = rect.x
		r.y = y
		r.w = rect.w
		r.h = rect.y + rect.h - y
	else:
		r.x = rect.x
		r.y = rect.y
		r.w = rect.w
		r.h = y - rect.y
	return r


def _does_cut(r, pvt, horz):
	"""Rectangle *r* occupies space at point *pvt*.
	Take orientation *horz* into account.
	"""

	## it is r.y <= pvt (or r.x <= pvt) due to the way 
	## bisect.bisect works: pvt == r.y is treated the same as 
	## pvt > r.y and then the *leeway* rect (see below) will 
	## be placed at r.y + r.h which is wrong.
	return horz and (r.y <= pvt < r.y + r.h) \
		or not horz and (r.x <= pvt < r.x + r.w)


def select_by_rect(selectables, selector):
	return [r for r in selectables if r.intersects(selector)]



class Rectangle(object):
	def __init__(self, x=0, y=0, w=0, h=0):
		self.x, self.y, self.w, self.h = x, y, w, h

	def __repr__(self):
		return repr("<%s (%s, %s, %s, %s) at %i>" %(self.__class__.__name__,
									self.x, self.y, self.w, self.h, id(self)))

	def __nonzero__(self):
		return bool(self.get_area())

	def __iter__(self):
		return iter((self.x, self.y, self.w, self.h))

	def __contains__(self, (px, py)):
		return self.x < px < self.x + self.w and self.y < py < self.y + self.h

	def __eq__(self, other):
		return (
			self.x == other.x
			and self.y == other.y
			and self.w == other.w
			and self.h == other.h
		)

	def __ne__(self, other):
		return not self.__eq__(other)

	def __getw(self):
		return self._w

	def __setw(self, val):
		if val < 0:
			raise ValueError("Rectangle.w must be positive. Got %s" % val)
		self._w = val

	w = width = property(__getw, __setw)

	def __geth(self):
		return self._h

	def __seth(self, val):
		if val < 0:
			raise ValueError("Rectangle.h must be positive. Got %s" % val)
		self._h = val

	h = height = property(__geth, __seth)

	def clone(self):
		return self.__class__(*self)

	def intersects(self, other):
		"""Separating axis test."""

		return not (
			self.x >= other.x + other.w
			or other.x >= self.x + self.w
			or self.y >= other.y + other.h
			or other.y >= self.y + self.h
		)

	def get_intersection(self, other):
		if not self.intersects(other):
			return self.__class__()

		return self.__class__(
			max(self.x, other.x),
			max(self.y, other.y),
			min(self.x + self.w, other.x + other.w) - max(self.x, other.x),
			min(self.y + self.h, other.y + other.h) - max(self.y, other.y)
		)

	def get_union(self, other):
		return self.__class__(
			min((self.x, other.x)),
			min((self.y, other.y)),
			max((self.x + self.w - min((self.x, other.x)),
				other.x + other.w - min((self.x, other.x)))),
			max((self.y + self.h - min((self.y, other.y)),
				other.y + other.h - min((self.y, other.y))))
		)

	def get_center(self):
		return self.x + self.w / 2.0, self.y + self.h / 2.0

	def get_aspect_ratio(self):
		return self.w / float(self.h)

	def get_area(self):
		return self.w * self.h


class RectangleContainer(list): pass


class RectangleCloud(object):
	"""For arranging Rectangles into an ellipse-like shape."""
	
	_SORTED_DIRECTION_FMT = "_sdir_cache_%s"

	def __init__(self, rectangles=[], ratio=1.0):
		self._rects = list(rectangles)
		self.ratio = ratio

	def __contains__(self, obj):
		return obj in self._rects

	def clone(self):
		return self.__class__(iter(self._rects))

	def move_all(self, x=0, y=0):
		if x:
			for r in self._rects:
				r.x += x
		if y:
			for r in self._rects:
				r.y += y

	def get_sorted_left(self):
		return self._get_sorted_DIRECTION(DIRECTION_LEFT, 
										SORTKEYS[DIRECTION_LEFT])

	def get_sorted_lower(self):
		return self._get_sorted_DIRECTION(DIRECTION_DOWN, 
										SORTKEYS[DIRECTION_DOWN])

	def get_sorted_right(self):
		return self._get_sorted_DIRECTION(DIRECTION_RIGHT,
										SORTKEYS[DIRECTION_RIGHT])

	def get_sorted_upper(self):
		return self._get_sorted_DIRECTION(DIRECTION_UP, 
										SORTKEYS[DIRECTION_UP])

	def _get_sorted_DIRECTION(self, direction, sortkey):
		attrname = self._SORTED_DIRECTION_FMT % direction
		if not getattr(self, attrname, None) and self._rects:
			setattr(self, attrname, sorted(self._rects, key=sortkey))
		return getattr(self, attrname)

	def _invalidate(self):
		for direction in (DIRECTION_LEFT, DIRECTION_RIGHT,
							DIRECTION_UP, DIRECTION_DOWN):
			delattr(self, self._SORTED_DIRECTION_FMT % direction)
		del self._occupied_rect

	def get_rectangles(self):
		return self._rects
	get_rects = get_rectangles

	def get_occupied_rect(self):
		try:
			return self._occupied_rect
		except AttributeError:
			left = self.get_sorted_left()[0]
			lower = self.get_sorted_lower()[0]
			right = self.get_sorted_right()[-1]
			upper = self.get_sorted_upper()[-1]
			self._occupied_rect = Rectangle(
				left.x,
				lower.y,
				right.x + right.w - left.x,
				upper.y + upper.h - lower.y
			)
		return self._occupied_rect

	def get_selection_by_rect(self, selector):
		return select_by_rect(self._rects, selector)

	def add_rect(self, rect):
		"""Add Rectangle *rect* to the cloud and find a 
		non-overlapping spot for it amongst the other 
		rectangles.
		"""

		rect.x, rect.y = 0, 0		# placement of rect is totally automatic
		if not self._rects or not rect:
			self._rects.append(rect)
			return

		occ = self.get_occupied_rect()
		cx, cy = occ.get_center()

		candidates = set()

		for sp in self.get_spots_for_rectangle(rect):
			cands = self.make_candidates_data(sp, rect)
			candidates.update(cands)

		if not candidates:
			raise Exception("No candidates were found.")

		rated = self.rate_candidates(candidates)
		choice = self.choose_best_candidate(rated)
		rect.x = choice.x
		rect.y = choice.y

		self._rects.append(rect)

		## Compensate for negative coordinates
		self.move_all(rect.x < 0 and rect.x or 0, rect.y < 0 and rect.y or 0)
		self._invalidate()

	def arrange(self):
		rects = self._rects[:]
		self._rects = []
		for r in rects:
			self.add_rect(r)

	def make_candidates_data(self, spot, rect):
		occ = self.get_occupied_rect()
		intsec = spot.get_intersection(occ)
		if intsec:
			leeway = intsec
		else:
			## There is no intersection, so the spot points to infinity
			## on all sides but one.
			leeway = spot

		cand = rubberband(occ.get_center(), leeway, rect)
		return [(cand, intsec, spot)]

	def rate_candidates(self, candidates_data):
		occ = self.get_occupied_rect()
		ratios = []
		candidates = []
		for cand, intsec, spot in candidates_data:
			cand.debuginfo = dict(intsec=intsec, spot=spot)

			intsec_cand_intsec = cand.get_intersection(intsec)

			cand.debuginfo["intsec_cand_intsec"] = intsec_cand_intsec

			## Ratio of how much of *cand* is inside *occ*.
			inside = intsec_cand_intsec.get_area() / float(cand.get_area())

			cand.debuginfo["inside"] = inside

			ratio = 0.0
			if inside:
				## How well is the usage of space of *cand* in *intsec*?
				usage = intsec_cand_intsec.get_area() / float(intsec.get_area())

				cand.debuginfo["usage"] = usage
				ratio = inside * usage

			if (1.0 - inside):
				## By how much unused space will the global occupied area grow?
				excess = cand.get_union(occ).get_area() - cand.get_area() \
							- occ.get_area() \
							+ cand.get_intersection(occ).get_area()

				cand.debuginfo["excess"] = excess

				## The ratio of unused additional space to the now occupied 
				## space.
				excess_ratio = excess / float(occ.get_area())
				cand.debuginfo["excess_ratio"] = excess_ratio

				## How much (in percent) does the new aspect ratio
				## deviate from the desired ratio?
				ratio_dist = (abs(
					occ.get_aspect_ratio()
					/ get_new_ratio(occ, cand)
					- self.ratio + 1
				))
				cand.debuginfo.update(ratio_dist=ratio_dist)
				cand.debuginfo.update(get_new_ratio=get_new_ratio(occ,cand))
				cand.debuginfo.update(self_ratio=self.ratio)

				ratio += ((1 - inside) / excess_ratio) / (10 ** ratio_dist)

			cand.debuginfo["ratio"] = ratio
			ratios.append(ratio)
			candidates.append(cand)

		return zip(ratios, candidates)

	def choose_best_candidate(self, rated_candidates):
		return sorted(rated_candidates, key=lambda t:t[0])[-1][1]

	def get_spots_for_rectangle(self, rectangle):
		"""Return regions of empty space amongst the 
		rectangles in the cloud where *rectangle* fits in.
		"""

		spots = []
		for direction in (DIRECTION_RIGHT, DIRECTION_LEFT, DIRECTION_UP,
														DIRECTION_DOWN):
			seeds = self._get_seed_points(direction)
			for seed in seeds:
				sp = self._get_spot(rectangle, seed, direction)
				if sp and sp not in spots:
					spots.append(sp)
		return spots

	def _get_seed_points(self, direction):
		"""Return points on the rectangles in the cloud,
		where a search (as done in self._get_spot) can
		start from.
		"""

		sortkey = SORTKEYS[direction]
		halver = HALVERS[direction]
		stampgetter = STAMPGETTERS[direction]

		if direction in (DIRECTION_RIGHT, DIRECTION_LEFT):
			seedgetter = lambda r: (sortkey(r), halver(r))
			swapper = lambda current, half: (sortkey(current), half)
		else:
			seedgetter = lambda r: (halver(r), sortkey(r))
			swapper = lambda current, half: (half, sortkey(current))
		
		seeds = []

		s = self._get_sorted_DIRECTION(direction, sortkey)
		if direction in (DIRECTION_RIGHT, DIRECTION_UP):
			s.reverse()
		
		print(s)

		cur = s[0]
		seeds.append(seedgetter(cur))
		stamps = [stampgetter(cur)]
		
		print(seeds)
		print(stamps)

		i = 1
		while i < len(s):
			cur = s[i]

			curlo, curhi = stampgetter(cur)
			
			print(i)

			j = 0
			while j < len(stamps):
				stamplo, stamphi = stamps[j]
				
				print("cur:", curlo, curhi)
				print("", j, stamplo, stamphi)
				

				if curlo < stamplo <= curhi:
					seeds.append(swapper(cur,
									curlo + (stamplo - curlo) / 2.0))
					stamps[j] = (curlo, stamphi)

					print(" cond below")
					print(" new stamp borders:", curlo, stamphi)
					print(" break on curhi <= stamphi", curhi <= stamphi)
					
					if curhi <= stamphi:
						break

				if curlo <= stamphi < curhi:
					## It's the last stamp or not the last stamp and
					## the following stamps lower point is above
					## the rects upper border.
					if j == len(stamps) - 1 \
						or j < len(stamps) - 1 and curhi <= stamps[j+1][0]:
						seeds.append(swapper(cur, 
										stamphi + (curhi - stamphi) / 2.0))
						stamps[j] = (stamplo, curhi)
						
						print(" cond above")
						print(" new stamp borders:", stamplo, curhi)
						print(" break")
						break
						
				if curhi < stamplo:
					seeds.append(swapper(cur,
									curlo + (curhi - curlo) / 2.0))
					stamps.append(stampgetter(cur))
					
					print(" cond curhi < stamplo")
					print(" stamp appended:", stamps[-1])

					break

				curlo = stamphi
				j += 1

			stamps.sort()
			i += 1
		return seeds

	def	_get_spot(self, rectangle, seed, direction):
		"""Return a region of empty space between the
		rectangles of the cloud where *rectangle* fits in,
		or *None* if the search fails.

		A spot's borders are defined by rectangles 
		encountered in a search. The search begins at
		the point *seed* and first tries to accomodate
		*rectangle* on the axis perpendicular to
		*direction*, so it is not blocked by other
		rectangles along that axis. E.g.: 
			
			*direction* == DIRECTION_RIGHT =>
				Accomodate along vertical axis.
			*direction* == DIRECTION_DOWN =>
				Accomodate along horizontal axis.

		From the accomodation point, the search continues
		along *direction* until it hits a rectangle. The 
		border of that rectangle that is nearest to *seed*
		determines the 'upper' limit of the spot (the 
		'lower' one being determined by *seed*). If there 
		are no rectangles encountered, the spot points
		to *INFINITY* in that direction.

		From there, the selection is extended on its sides. 
		The nearest Rectangles found determine the sides of 
		the spot.

		Parameters:
			*rectangle*: type Rectangle.
			*seed*: type tuple, length 2.
			*direction*: type int, one of (
							DIRECTION_RIGHT, 
							DIRECTION_LEFT, 
							DIRECTION_UP,
							DIRECTION_DOWN
						)
		"""
		
		sx, sy = seed

		facing_right = direction == DIRECTION_RIGHT
		facing_up = direction == DIRECTION_UP
		facing_left = direction == DIRECTION_LEFT
		facing_down = direction == DIRECTION_DOWN
		horizontal = facing_left or facing_right

		occ = self.get_occupied_rect()

		sel = partition(occ, seed, direction)
		sidesel = sel.clone()
		ortsel = Rectangle(
			0,
			0, 
			sel.w if horizontal else rectangle.w,
			sel.h if not horizontal else rectangle.h
		)

		if horizontal:
			sortkey_sides = lambda r: r.y
			pivot = sy
		else:
			sortkey_sides = lambda r: r.x
			pivot = sx

		selection = self.get_selection_by_rect(sel)

		########################################################
		##  Make sure *rectangle* fits on the sideways axis.  ##
		## Move *ortsel* so its middle is closest to *pivot*. ##
		########################################################

		restrictor = Rectangle(
			sel.x + (sel.w - rectangle.w) * facing_left,
			sel.y + (sel.h - rectangle.h) * facing_down,
			rectangle.w if horizontal else sel.w,
			rectangle.h if not horizontal else sel.h
		)
		
		leeway = sel.clone()

		sideways = select_by_rect(selection, restrictor)
		if sideways:
			sideways.sort(key=sortkey_sides)
			extract = [sortkey_sides(r) for r in sideways]
			i = bisect.bisect(extract, pivot)

			## Fringe case 1: sy is below lowest rect's y.
			if not i:
				ir = sideways[0]
				if horizontal:
					leeway.y = min((leeway.y, ir.y - rectangle.h))
					leeway.h = ir.y - leeway.y
				else:
					leeway.x = min((leeway.x, ir.x - rectangle.w))
					leeway.w = ir.x - leeway.x

			## Fringe case 2: sy is above highest rect's y.
			elif i == len(sideways):
				ir = sideways[-1]

				if _does_cut(ir, pivot, horizontal):
					return None

				if horizontal:
					leeway.y = ir.y + ir.h
					leeway.h = max((leeway.y + rectangle.h, sel.y + sel.h)) \
								- leeway.y
				else:
					leeway.x = ir.x + ir.w
					leeway.w = max((leeway.x + rectangle.w, sel.x + sel.w)) \
								- leeway.x

			## Norm case: sy is inside the rects' y values.
			else:
				ir0 = sideways[i-1]
				if _does_cut(ir0, pivot, horizontal):
					return None

				ir1 = sideways[i]
				## space between ir0 and ir1 is too small for rectangle.
				if horizontal and (ir1.y - (ir0.y + ir0.h) < rectangle.h) \
					or not horizontal and (ir1.x - (ir0.x + ir0.w) < rectangle.w):
					return None

				if horizontal:
					leeway.y = ir0.y + ir0.h
					leeway.h = ir1.y - leeway.y
				else:
					leeway.x = ir0.x + ir0.w
					leeway.w = ir1.x - leeway.x

		ortsel = rubberband(seed, leeway, ortsel)

		############################################
		## Determine orthogonal top of *sidesel*. ##
		############################################

		orthogonals = select_by_rect(selection, ortsel)
		if orthogonals:
			if facing_left:
				sortkey_orth = lambda r: r.x + r.w
			elif facing_right:
				sortkey_orth = lambda r: r.x
			elif facing_up:
				sortkey_orth = lambda r: r.y
			elif facing_down:
				sortkey_orth = lambda r: r.y + r.h

			orthogonals.sort(key=sortkey_orth, 
								reverse=(facing_right or facing_up))

			sr = orthogonals[-1]
			if facing_left:
				sidesel.x = sr.x + sr.w
				sidesel.w = sel.x + sel.w - sidesel.x
			elif facing_right:
				sidesel.w = sr.x - sel.x
			elif facing_down:
				sidesel.y = sr.y + sr.h
				sidesel.h = sel.y + sel.h - sidesel.y
			elif facing_up:
				sidesel.h = sr.y - sel.y
		else:
			if facing_left:
				sidesel.x = sel.x - INF
				sidesel.w = INF + sel.w
			elif facing_right:
				sidesel.w = INF + sel.w
			elif facing_up:
				sidesel.h = INF + sel.h
			elif facing_down:
				sidesel.y = sel.y - INF
				sidesel.h = INF + sel.h

		####################################
		## Select values for side bounds. ##
		####################################

		sideways = select_by_rect(selection, sidesel)
		if sideways:
			sideways.sort(key=sortkey_sides)
			extract = [sortkey_sides(r) for r in sideways]
			i = bisect.bisect(extract, pivot)

			## Fringe case 1: *pivot* is below lowest rect's pivot value.
			if not i:
				if horizontal:
					sidesel.y = sel.y - INF
					sidesel.h = sideways[0].y - sel.y + INF
				else:
					sidesel.x = sel.x - INF
					sidesel.w = sideways[0].x - sel.x + INF

			## Fringe case 2: *pivot* is above highest rect's pivot value.
			elif i == len(sideways):
				ir = sideways[-1]

				if _does_cut(ir, pivot, horizontal):
					return None

				if horizontal:
					sidesel.y = ir.y + ir.h
					sidesel.h = sel.y + sel.h - sidesel.y + INF
				else:
					sidesel.x = ir.x + ir.w
					sidesel.w = sel.x + sel.w - sidesel.x + INF

			## Norm case: *pivot* is inside the rects' 
			## corresponding axis' values.
			else:
				ir0 = sideways[i-1]

				if _does_cut(ir0, pivot, horizontal):
					return None

				ir1 = sideways[i]
				## space between ir0 and ir1 is too small for rectangle.
				if horizontal and (ir1.y - (ir0.y + ir0.h) < rectangle.h) \
					or not horizontal and (ir1.x - (ir0.x + ir0.w) < rectangle.w):
					return None

				if horizontal:
					sidesel.y = ir0.y + ir0.h
					sidesel.h = ir1.y - sidesel.y
				else:
					sidesel.x = ir0.x + ir0.w
					sidesel.w = ir1.x - sidesel.x
		else:
			if horizontal:
				sidesel.y = sel.y - INF
				sidesel.h = sel.h + 2 * INF
			else:
				sidesel.x = sel.x - INF
				sidesel.w = sel.w + 2 * INF

		return sidesel
