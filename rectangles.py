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


__version__ = tuple(
	os.path.dirname(os.path.abspath(__file__)).rsplit("/", 1)[-1].split(".")
)
__license__ = "MIT"
__author__ = "kurvenschubser"
__email__ = "@".join((__author__, "gmail.com"))


__all__ = ["Rectangle", "RectangleCloud", "get_new_ratio", "get_distance",
			"rubberband", "center"]



## Must be something that can be used algebraically,
## so it can't be float('inf').
INFINITY = INF = sys.maxint


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

	def __init__(self, rectangles=[], steps=24, ratio=1.0):
		self._rects = list(rectangles)
		self._invalidate()

		self.set_steps(steps)
		self.set_ratio(ratio)

	def __contains__(self, obj):
		return obj in self._rects

	def arrange(self):
		rects = self._rects[:]
		self._rects = []
		for r in rects:
			self.add_rect(r)

	def set_steps(self, steps):
		"""*steps*: the number of scanning steps to find a space
		for a Rectangle that is added to the RectangleCloud.
		Must be of type int or long and be a multiple of 4.
		"""

		if int(steps+1) % steps != 1:
			raise Exception("Need type int or long, got %s" % type(steps))
		if steps % 4:
			raise Exception("%s must be multiple of 4" % steps)
		self._steps = steps

	def set_ratio(self, ratio):
		"""This is used (amongst other variables) to determine
		the best fitting space for a Rectangle when it's added to
		RectangleCloud.
		"""

		self._ratio = ratio

	def move_all(self, x=0, y=0):
		if x:
			for r in self._rects:
				r.x += x
		if y:
			for r in self._rects:
				r.y += y

	def add_rect(self, rect):
		"""Add Rectangle *rect* and find a non-overlapping
		spot for it amongst the other rectangles.
		"""

		rect.x, rect.y = 0, 0		# placement of rect is totally automatic
		if not self._rects or not rect:
			self._rects.append(rect)
			self._invalidate()
			return

		occ = self.get_occupied_rect()
		cx, cy = occ.get_center()

		candidates = set()

		for sp in self.get_spots_for_rectangle(rect):
			cands = self.make_candidates_data(sp, rect, occ)
			candidates.update(cands)

		if candidates:
			rated = self.rate_candidates(list(candidates), occ)
			choice = self.choose_best_candidate(rated)
			rect.x = choice.x
			rect.y = choice.y
		else:
			raise Exception("Should never happen. Please report bug.")

		self._rects.append(rect)

		## Compensate for negative coordinates
		self.move_all(rect.x < 0 and rect.x or 0, rect.y < 0 and rect.y or 0)
		self._invalidate()

	def make_candidates_data(self, spot, rect, occupation_rect):
		intsec = spot.get_intersection(occupation_rect)
		if intsec:
			leeway = intsec
		else:
			## There is no intersection, so the spot points to infinity
			## on all sides but one.
			leeway = spot

		cand = rubberband(occupation_rect.get_center(), leeway, rect)

		return [(cand, intsec, spot)]

	def rate_candidates(self, candidates_data, occupation_rect):
		occ = occupation_rect
		ratios = []
		candidates = []
		for cand, intsec, spot in candidates_data:
			candidates.append(cand)
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

				## The bigger this rate, the worse.
				excess_ratio = excess / float(occ.get_area())
				cand.debuginfo["excess_ratio"] = excess_ratio

				## How much (in percentage _points_) does the new aspect ratio
				## deviate from the desired ratio?
				ratio_dist = abs(get_new_ratio(occ, cand) - self._ratio)

				cand.debuginfo.update(dict(ratio_dist=ratio_dist))

				ratio += ((1 - inside) / excess_ratio) / (10 ** ratio_dist)

			cand.debuginfo["ratio"] = ratio
			ratios.append(ratio)

		return zip(ratios, candidates)

	def choose_best_candidate(self, rated_candidates):
		return sorted(rated_candidates, key=lambda t:t[0])[-1][1]

	def get_sorted_left(self):
		if not self._sorted_left and self._rects:
			self._sorted_left = sorted(self._rects, key=lambda r: r.x)
		return self._sorted_left

	def get_sorted_lower(self):
		if not self._sorted_lower and self._rects:
			self._sorted_lower = sorted(self._rects, key=lambda r: r.y)
		return self._sorted_lower

	def get_sorted_right(self):
		if not self._sorted_right and self._rects:
			self._sorted_right = sorted(self._rects, key=lambda r: r.x + r.w)
		return self._sorted_right

	def get_sorted_upper(self):
		if not self._sorted_upper and self._rects:
			self._sorted_upper = sorted(self._rects, key=lambda r: r.y + r.h)
		return self._sorted_upper

	def _invalidate(self):
		self._sorted_left = []
		self._sorted_lower = []
		self._sorted_right = []
		self._sorted_upper = []

	def get_rectangles(self):
		return self._rects
	get_rects = get_rectangles

	def get_occupied_rect(self):
		left = self.get_sorted_left()[0]
		lower = self.get_sorted_lower()[0]
		right = self.get_sorted_right()[-1]
		upper = self.get_sorted_upper()[-1]
		return Rectangle(
			left.x,
			lower.y,
			right.x + right.w - left.x,
			upper.y + upper.h - lower.y
		)

	def get_sector_rect(self, sector_x, sector_y):
		occ = self.get_occupied_rect()
		return Rectangle(
			occ.x + sector_x * occ.w / 2.0,
			occ.y + sector_y * occ.h / 2.0,
			occ.w / 2.0,
			occ.h / 2.0
		)

	def get_selection_by_rect(self, selector):
		return select_by_rect(self._rects, selector)

	def get_spots_for_rectangle(self, rectangle):
		"""Determine possible leeway Rectangles for the placement
		of *rectangle*. A leeway Rectangle covers a spot between
		Rectangles already placed in the cloud.

		To achieve this goal, all existing Rectangles in
		RectangleCloud.get_rects() are scanned by a beam emanating
		from their common center,
		RectangleCloud.get_occupation_rect().get_center().
		The beam rotates anti-clockwise in *steps* steps. If it
		cuts any of RectangleCloud.get_rects(), Rectangles
		representing the unoccupied space until another Retangle
		is found, are computed. If there are no Rectangles found
		for any one direction, the computed Rectangle will point
		to *INFINITY* for that direction.

		A found leeway is guaranteed to fully accomodate *rectangle*.

		Returns found leeway spots.
		"""

		steps = self._steps

		stepped_pi = math.pi / steps
		avoid_zero_div = 0.000001

		occ = self.get_occupied_rect()
		cx, cy = occ.get_center()

		results = []
		
		## Bind locally, to speed up lookup
		get_cut_point = self._get_cut_point

		s_steps = steps // 4		# steps per sector
		i = 0
		while i < steps:
			quadrant, rest = divmod(i, s_steps)

			## At sector boundary
			if not rest:
				sector_x = int(quadrant in (0, 3))
				sector_y = int(quadrant in (0, 1))

				# sector_x = int(not(steps-s_steps < steps - i < s_steps))
				# sector_y = int(i < steps / 2)

				rects_in_sector = self.get_selection_by_rect(
					self.get_sector_rect(sector_x, sector_y)
				)

				## nothing to scan, advance loop to next sector
				if not rects_in_sector:
					i += s_steps
					continue

			tan = math.tan(2 * stepped_pi * i + avoid_zero_div)
			
			i += 1

			res = []
			for rect in rects_in_sector:
				if rect is rectangle:
					continue

				## inner vertical cut
				p = get_cut_point(rect, cx, cy, tan, sector_x, sector_y,
															False, True)
				if p:
					sel = self._get_selector(occ, sector_x, sector_y, 
										cut_x, cut_y, outer, vertical)
					sp = self._get_spot(rectangle, occ, p[0], p[1], sel,
																vertical)
					res.append(sp)

				## inner horizontal cut
				else:
					p = get_cut_point(rect, cx, cy, tan, sector_x,
												sector_y, False, False)
					if p:
						sel = self._get_selector(occ, sector_x, sector_y, 
										cut_x, cut_y, outer, vertical)
						sp = self._get_spot(rectangle, occ, p[0], p[1], sel,
																vertical)
						res.append(sp)

				## outer vertical cut
				p = get_cut_point(rect, cx, cy, tan, sector_x, sector_y,
															True, True)
				if p:
					sel = self._get_selector(occ, sector_x, sector_y, 
										cut_x, cut_y, outer, vertical)
					sp = self._get_spot(rectangle, occ, p[0], p[1], sel, 
																vertical)
					res.append(sp)

				## outer horizontal cut
				else:
					p = get_cut_point(rect, cx, cy, tan, sector_x,
												sector_y, True, False)
					if p:
						sel = self._get_selector(occ, sector_x, sector_y, 
										cut_x, cut_y, outer, vertical)
						sp = self._get_spot(rectangle, occ, p[0], p[1], sel,
																vertical)
						res.append(sp)

			for sp in filter(None, res):
				if sp not in results:
					results.extend(sp)

		return results

	def _get_cut_point(self, rect, cx, cy, tan, sector_x, sector_y,
												outer, vertical):

		if vertical:
			considerw = int((not outer and not sector_x) \
								or (outer and sector_x))
			rel_x = abs(cx - (rect.x + rect.w * considerw))
			rel_y = rel_x * tan
			cut_x = rect.x + rect.w * considerw
			cut_y = cy + rel_y * (sector_y or -1)

			print("_get_cut_point", rel_y, rel_x, cut_y, cut_x)

			if rect.y <= cut_y <= rect.y + rect.h:
				return (cut_x, cut_y)
		else:
			considerh = int((not outer and not sector_y) \
								or (outer and sector_y))
			rel_y = abs(cy - (rect.y + rect.h * considerh))
			rel_x = rel_y / tan
			cut_y = rect.y + rect.h * considerh
			cut_x = cx + rel_x * (sector_x or -1)

			print("_get_cut_point", rel_y, rel_x, cut_y, cut_x)

			if (rect.x <= cut_x <= rect.x + rect.w):
				return (cut_x, cut_y)

		return ()


	def	_get_spot(self, rectangle, occ, cut_x, cut_y, sel, vertical):
		## spot is outside occupied rect: return a spot facing
		## away from *occ* in the direction that *sel*
		## points to. The spot's innermost boundary is 
		## *sel*'s outermost boundary (from the direction it
		## is facing) and the other boundaries are pointing 
		## to INFINITY.		
		if not sel:
			if sel.h:
				## facing left
				if sel.x == occ.x:
					return Rectangle(
						occ.x - INF,
						occ.y - INF,
						INF,
						occ.h + 2 * INF
					)

				## facing right
				else:
					return Rectangle(
						occ.x + occ.w,
						occ.y - INF,
						INF,
						occ.h + 2 * INF
					)
			
			elif sel.w:
				## facing down
				if sel.y == occ.y:
					return Rectangle(
						occ.x - INF,
						occ.y - INF,
						occ.w + 2 * INF,
						INF
					)

				## facing up
				else:
					return Rectangle(
						occ.x - INF,
						occ.y + occ.h,
						occ.w + 2 * INF,
						INF
					)
			else:
				raise Exception("*sel* has no dimension.")


		print("\nnew run")		
		
		ortsel = Rectangle(
			0,
			0, 
			sel.w if vertical else rectangle.w,
			sel.h if not vertical else rectangle.h
		)

		sidesel = sel.clone()

		facing_right = occ.x < sel.x
		facing_up = occ.y < sel.y
		facing_left = occ.x + occ.w > sel.x + sel.w
		facing_down = occ.y + occ.h > sel.y + sel.h

		##debug
		if not len(filter(None, (facing_right, facing_left, facing_up, 
												facing_down))) == 1:
			raise Exception("*sel*'s orientation is nonsense.")

		## rect occupies space where pivot is.
		does_cut = (lambda r, pvt: r.y < pvt < r.y + r.h) if vertical \
					else (lambda r, pvt: r.x < pvt < r.x + r.w)

		sortkey_sides = (lambda r: r.y) if vertical else (lambda r: r.x)

		selection = self.get_selection_by_rect(sel)

		######################################################
		## Make sure *rectangle* fits on the sideways axis. ##
		######################################################

		restrictor = Rectangle(
			sel.x + (sel.w - rectangle.w) * facing_left,
			sel.y + (sel.h - rectangle.h) * facing_down,
			rectangle.w if vertical else sel.w,
			rectangle.h if not vertical else sel.h
		)
		sideways = select_by_rect(selection, restrictor)

		if sideways:
			sideways.sort(key=sortkey_sides)
			extract = [r.y for r in sideways] if vertical \
								else [r.x for r in sideways]
			pivot = cut_y if vertical else cut_x
			i = bisect.bisect(extract, pivot)
			
			print("i",i, "pivot",pivot)
			print("ortsel 1", ortsel)
			print("sideways 1", sideways)
			print("restrictor", restrictor)

			## Fringe case 1: cut_y is below lowest rect's y.
			if not i:
				if vertical:
					ortsel.y = cut_y \
							+ min((rectangle.h / 2.0, sideways[0].y - cut_y)) \
							- rectangle.h

				else:
					ortsel.x = cut_x \
							+ min((rectangle.w / 2.0, sideways[0].x - cut_x)) \
							- rectangle.w

			## Fringe case 2: cut_y is above highest rect's y.
			elif i == len(sideways):
				ir = sideways[-1]

				if does_cut(ir, pivot):
					return None

				if vertical:
					ortsel.y = cut_y - min((rectangle.h / 2.0, 
											cut_y - (ir.y + ir.h)))
				else:
					ortsel.x = cut_x - min((rectangle.w / 2.0, 
											cut_x - (ir.x + ir.w)))

			## Norm case: cut_y is inside the rects' y values.
			else:
				ir0 = sideways[i-1]
				if does_cut(ir0, pivot):
					return None

				ir1 = sideways[i]
				## space between ir0 and ir1 is too small for rectangle.
				if vertical and (ir1.y - (ir0.y + ir0.h) < rectangle.h) \
					or not vertical and (ir1.x - (ir0.x + ir0.w) < rectangle.w):
					return None

				## move ortsel so its middle is closest to pivot
				if vertical:
					ortsel.h = rectangle.h
					leeway = Rectangle(
						sel.x,
						ir0.y + ir0.h,
						sel.w,
						ir1.y - (ir0.y + ir0.h)
					)
				else:
					ortsel.w = rectangle.w
					leeway = Rectangle(
						ir0.x + ir0.w,
						sel.y,
						ir1.x - (ir0.x + ir0.w),
						sel.h
					)
				ortsel = rubberband((cut_x, cut_y), leeway, ortsel)
				
				print("leeway", leeway)

		else:
			## since there are no colliding rects on the sideways axis,
			## shrink *ordsel* to width/height (according to orientation) 
			## of *rectangle* and center on (cut_x, cut_y).
			tmpsel = rubberband((cut_x, cut_y), ortsel, rectangle)
			if vertical:
				ortsel.y = tmpsel.y
				ortsel.h = tmpsel.h
			else:
				ortsel.x = tmpsel.x
				ortsel.w = tmpsel.w

		if vertical:
			ortsel.h = rectangle.h
		else:
			ortsel.w = rectangle.w

		print ("ortsel 2", ortsel)

		##########################################
		## Determine orthogonal top of sidesel. ##
		##########################################

		orthogonals = select_by_rect(selection, ortsel)

		print("orthogonals", orthogonals, selection, ortsel)

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
		
		print ("sideways 2", sideways, selection, sidesel)
		

		if sideways:
			sideways.sort(key=sortkey_sides)

			extract = [r.y for r in sideways] if vertical \
								else [r.x for r in sideways]
			i = bisect.bisect(extract, pivot)
			
			print("i", i, "pivot", pivot)

			## Fringe case 1: *pivot* is below lowest rect's pivot value.
			if not i:
				if vertical:
					sidesel.y = sel.y - INF
					sidesel.h = sideways[0].y - sel.y + INF
				else:
					sidesel.x = sel.x - INF
					sidesel.w = sideways[0].x - sel.x + INF
				
					print("hier!!!, sidesel", sidesel, sideways[0].x, sidesel.x, sidesel.w, INF)

			## Fringe case 2: *pivot* is above highest rect's pivot value.
			elif i == len(sideways):
				ir = sideways[-1]
				## ir occupies space where pivot is.
				if does_cut(ir, pivot):
					return None

				if vertical:
					sidesel.y = ir.y + ir.h
					sidesel.h = sel.y + sel.h - sidesel.y + INF
				else:
					sidesel.x = ir.x + ir.w
					sidesel.w = sel.x + sel.w - sidesel.x + INF

			## Norm case: *pivot* is inside the rects' 
			## corresponding axis' values.
			else:
				ir0 = sideways[i-1]
				## ir0 occupies space where *pivot* is.
				if does_cut(ir0, pivot):
					return None

				ir1 = sideways[i]
				## space between ir0 and ir1 is too small for rectangle.
				if vertical and (ir1.y - (ir0.y + ir0.h) < rectangle.h) \
					or not vertical and (ir1.x - (ir0.x + ir0.w) < rectangle.w):
					return None

				if vertical:
					sidesel.y = ir0.y + ir0.h
					sidesel.h = ir1.y - sidesel.y
				else:
					sidesel.x = ir0.x + ir0.y
					sidesel.w = irl.x - sidesel.x
		else:
			if vertical:
				sidesel.y = sel.y - INF
				sidesel.h = sel.h + 2 * INF
			else:
				sidesel.x = sel.x - INF
				sidesel.w = sel.w + 2 * INF

		return sidesel

	def _get_selector(self, occ, sector_x, sector_y, cut_x, cut_y,
													outer, vertical):
		return Rectangle(
			cut_x if vertical and ((sector_x and outer) \
				or (not sector_x and not outer)) else occ.x,
			cut_y if not vertical and ((sector_y and outer) \
				or (not sector_y and not outer)) else occ.y,
			occ.w * ((sector_x and outer) or (not sector_x and not outer)) \
				+ (cut_x - occ.x) * ((not sector_x and outer) or \
					(sector_x and not outer) or -1) \
				if vertical else occ.w,
			occ.h * ((sector_y and outer) or (not sector_y and not outer)) \
				+ (cut_y - occ.y) * ((not sector_y and outer) or \
					(sector_y and not outer) or -1) \
				if not vertical else occ.h
			)
