from __future__ import print_function


"""
Copyright (c) 2011 kurvenschubser

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

"""
rectangles.py
"""


import os
import sys
import math
import bisect


__version__ = tuple(
	os.path.dirname(os.path.abspath(__file__)).rsplit("/", 1)[-1].split(".")
)
__license__ = "MIT"
__author__ = "kurvenschubser"
__email__ = u"@".join((__author__, "googlemail.com"))


__all__ = ["Rectangle", "RectangleCloud", "get_new_ratio", "get_distance",
			"apply_rubberband", "apply_centering"]


def get_new_ratio(baserect, tobeadded):
	"""If Rectangle *tobeadded* was added to Rectangle *baserect*,
	return the new aspect ratio.
	"""

	return (
		abs(max(tobeadded.x + tobeadded.w, baserect.x + baserect.w)
			- min(tobeadded.x, baserect.x))
		/ float(abs(max(tobeadded.y + tobeadded.h, baserect.y + baserect.h)
			- min(tobeadded.y, baserect.y)))
	)


def get_distance((p1_x, p1_y), (p2_x, p2_y)):
	"""Return the distance from point (p1_x, p2_y) to point (p2_x, p2_y).
	"""

	return math.sqrt((p1_x - p2_x) ** 2 + (p1_y - p2_y) ** 2)


def apply_rubberband((cx, cy), leeway, rect):
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


def apply_centering(tobecentered, stable):
	"""Place center of Rectangle *tobecentered* exactly on 
	center of Rectangle *stable*.
	"""

	tx, ty = tobecentered.get_center()
	sx, sy = stable.get_center()

	return Rectangle(sx - tx, sy - ty, tobecentered.w, tobecentered.h)


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
			raise ValueError("Rectangle.w must be positive.")
		self._w = val

	w = property(__getw, __setw)
	
	def __geth(self):
		return self._h

	def __seth(self, val):
		if val < 0:
			raise ValueError("Rectangle.h must be positive.")
		self._h = val

	h = property(__geth, __seth)

	def clone(self):
		return self.__class__(*self)

	def get_intersection(self, other):
		return Rectangle(
			max(self.x, other.x),
			max(self.y, other.y),
			min(self.x + self.w, other.x + other.w) - max(self.x, other.x),
			min(self.y + self.h, other.y + other.h) - max(self.y, other.y)
		)

	def get_center(self):
		return self.x + self.w / 2.0, self.y + self.h / 2.0

	def get_aspect_ratio(self):
		return self.w / float(self.h)

	def get_area(self):
		return self.w * self.h

	def intersects(self, other):
		"""Separating axis test."""

		return not (
			self.x >= other.x + other.w
			or other.x >= self.x + self.w
			or self.y >= other.y + other.h
			or other.y >= self.y + self.h
		)


class RectangleCloud(object):
	"""For arranging Rectangles into an ellipse-like shape."""

	def __init__(self, rectangles=[], max_steps=12, ratio=1.0):
		self._rects = list(rectangles)
		self._invalidate()
		
		## maximum of cirular scanning steps for each rect that is fitted in.
		self._max_steps = max_steps

		## The aspect ratio the rectangles should fit in.
		self._ratio = ratio

	def __contains__(self, obj):
		return obj in self._rects

	def arrange(self):
		rects = self._rects[:]
		self._rects = []
		for r in rects:
			self.add_rect(r)

	def set_ratio(self, ratio):
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
			choice = self.pick_best_spot(list(candidates), occ)
			rect.x = choice.x
			rect.y = choice.y
		
		else:
			print("rect.tag.name: %s. rect: %s." %(rect.tag.name, rect))
			print("spots: %s" %self.get_spots_for_rectangle(rect))
			print("rect.tag.layout: %s." %rect.tag.layout)
			raise Exception("Should never happen. Please report bug to author.")

		self._rects.append(rect)

		## Compensate for negative coordinates
		move_x, move_y = 0, 0
		if rect.x < 0:
			move_x = abs(rect.x)
		if rect.y < 0:
			move_y = abs(rect.y)
		self.move_all(move_x, move_y)

		print("self._rects", self._rects)

		self._invalidate()

	def make_candidates_data(self, spot, rect, occupation_rect):
		intsec = spot.get_intersection(occupation_rect)
		if intsec:
			leeway = intsec
		else:
			## There is no intersection, so the spot points to infinity
			## on all sides but one.
			leeway = spot

		cand = apply_rubberband(occupation_rect.get_center(), leeway, rect)

		return [(cand, intsec, spot)]
 
	def pick_best_spot(self, candidates_data, occupation_rect):
		cx, cy = occupation_rect.get_center()
		ratios = []
		for cand, intsec, spot in candidates_data:
			cmpratio = get_new_ratio(occupation_rect, cand) / self._ratio
			if intsec:
				intsec_cand_intsec = cand.get_intersection(intsec)

				## Ratio of how much of *cand* is inside *occupation_rect*.
				inside = intsec_cand_intsec.get_area() / cand.get_area()

				## How well is the usage of space of *cand* in *intsec*?
				usage = intsec_cand_intsec.get_area() / intsec.get_area()

				ratio = (inside * usage + (1 - inside) * cmpratio)
			else:
				ratio = cmpratio
			ratios.append(ratio)		

		ratios.sort()
		i = bisect.bisect(ratios, 1.0)
		if i == len(ratios):
			best = candidates_data[-1][0]
		else:
			best = candidates_data[i][0]

		return best

	def get_sorted_left(self):
		if not self._sorted_left and self._rects:
			self._rects.sort(key=lambda r: r.x)
			self._sorted_left = self._rects[:]
		return self._sorted_left

	def get_sorted_lower(self):
		if not self._sorted_lower and self._rects:
			self._rects.sort(key=lambda r: r.y)
			self._sorted_lower = self._rects[:]
		return self._sorted_lower

	def get_sorted_right(self):
		if not self._sorted_right and self._rects:
			self._rects.sort(key=lambda r: r.x + r.w)
			self._sorted_right = self._rects[:]
		return self._sorted_right

	def get_sorted_upper(self):
		if not self._sorted_upper and self._rects:
			self._rects.sort(key=lambda r: r.y + r.h)
			self._sorted_upper = self._rects[:]
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

	def get_selection_by_rect(self, selectionrect):
		return [r for r in self._rects if r.intersects(selectionrect)]

	def get_spots_for_rectangle(self, rectangle, steps=None):
		if steps is None:
			steps = self._max_steps

		stepped_pi = math.pi / steps
		avoid_zero_div = 0.000001

		occ = self.get_occupied_rect()

		results = []

		print(locals())

		for i in xrange(steps):
			cos = math.cos(2 * stepped_pi * i + avoid_zero_div)
			sin = math.sin(2 * stepped_pi * i + avoid_zero_div)
			tan = abs(sin / cos)

			sector_x = int(cos > 0)
			sector_y = int(sin > 0)

			sector_rects = self.get_selection_by_rect(
				self.get_sector_rect(sector_x, sector_y)
			)

			for rect in sector_rects:
				# print("rect in sector_rects", rect, rect.tag.name)
				if rect is rectangle:
					continue

				# Get distance from sector origin to outer vertical boundary 
				# of rect, seen from sector origin (normalized to centered coordinates).
				curr_x = abs(occ.x + occ.w / 2.0 - (rect.x + rect.w * sector_x))
				curr_y = curr_x * tan

				# curr_x and curr_y denormalized
				x_section = rect.x + rect.w * sector_x
				y_section = occ.y + occ.h / 2.0 + curr_y * (sector_y or -1)
				
				print("RectangleCloud.get_spots_for_rectangle")
				print(sector_x, sector_y)
				print(rect)
				if (rect.y <= y_section <= rect.y + rect.h):
					print("vertical cut")
					print(curr_x, curr_y, x_section, y_section)
				print("")

				if (rect.y <= y_section <= rect.y + rect.h):
					left_bound = x_section - rectangle.w * (not sector_x)
					right_bound = left_bound + rectangle.w
					lower_bound = y_section - rectangle.h * (not sector_y)
					upper_bound = lower_bound + rectangle.h

					horizontal_selector = Rectangle(
						left_bound if sector_x else - sys.maxint,
						lower_bound,
						occ.x + occ.w - left_bound + sys.maxint if sector_x \
							else sys.maxint + right_bound,
						rectangle.h
					)

					horizontals = self.get_selection_by_rect(horizontal_selector)

					if horizontals:
						if sector_x:
							horizontals.sort(key=lambda r: r.x)
							nearest = horizontals[0]
							right_bound = nearest.x
						else:
							horizontals.sort(key=lambda r: r.x + r.w, reverse=True)
							nearest = horizontals[0]
							left_bound = nearest.x + nearest.w
					else:
						left_bound = horizontal_selector.x
						right_bound = left_bound + horizontal_selector.w

					print("	vertical cut:", left_bound, lower_bound, 
												right_bound, upper_bound)
					
					if right_bound - left_bound < rectangle.w:
						print("	vertical cut: aborted on w too small?", right_bound-left_bound<rectangle.w)
						continue

					vertical_selector = Rectangle(
						left_bound,
						- sys.maxint,
						right_bound - left_bound,
						occ.y + occ.h + sys.maxint * 2
					)

					verticals = self.get_selection_by_rect(vertical_selector)

					if verticals:
						verticals.sort(key=lambda r: r.y)
						i = bisect.bisect([r.y for r in verticals], y_section)
						# Fringe case 1: y_section is below lowest rect's y.
						if i == 0:
							upper_bound = verticals[0].y
							lower_bound = vertical_selector.y
						# Fringe case 2: y_section is above highest rect's y.
						elif i == len(verticals):
							# There is a rect occuying the space, continue.
							if (verticals[-1].y < y_section 
									< verticals[-1].y + verticals[-1].h):
								continue
							else:
								lower_bound = verticals[-1].y + verticals[-1].h
								upper_bound = vertical_selector.y + vertical_selector.h
						# Norm case: y_section is inside the rects' y values.
						else:
							upper_bound = verticals[i].y
							lower_bound = verticals[i-1].y + verticals[i-1].h
					else:
						lower_bound = vertical_selector.y
						upper_bound = vertical_selector.y + vertical_selector.h

					print("	vertical cut:", left_bound, lower_bound, 
												right_bound, upper_bound)
												
					if upper_bound - lower_bound < rectangle.h:
						print("	vertical cut: aborted on h too small?", upper_bound-lower_bound<rectangle.h)
						continue

					# Candidate spot was found
					newr = Rectangle(
						left_bound,
						lower_bound,
						right_bound - left_bound,
						upper_bound - lower_bound
					)

					if not newr in results:
						results.append(newr)

					continue
						

				# Get distance from sector origin to outer horizontal boundary 
				# of rect, seen from sector origin.
				curr_y = abs(occ.y + occ.h / 2.0 - (rect.y + rect.h * sector_y))
				curr_x = curr_y / tan
				
				# curr_x and curr_y denormalized
				y_section = rect.y + rect.h * sector_y
				x_section = occ.x + occ.w / 2.0 + curr_x * (sector_x or -1)
				
				print("RectangleCloud.get_spots_for_rectangle")
				print(sector_x, sector_y)
				print(rect)
				if (rect.x <= x_section <= rect.x + rect.w):
					print("horizontal cut")
					print(curr_x, curr_y, x_section, y_section)
				print("")

				if (rect.x <= x_section <= rect.x + rect.w):
					left_bound = x_section - rectangle.w * (not sector_x)
					right_bound = left_bound + rectangle.w
					lower_bound = y_section - rectangle.h * (not sector_y)
					upper_bound = lower_bound + rectangle.h

					vertical_selector = Rectangle(
						left_bound,
						lower_bound if sector_y else - sys.maxint,
						rectangle.w,
						occ.y + occ.h - lower_bound + sys.maxint if sector_y else sys.maxint + upper_bound
					)

					verticals = self.get_selection_by_rect(vertical_selector)

					if verticals:
						if sector_y:
							verticals.sort(key=lambda r: r.y)
							nearest = verticals[0]
							upper_bound = nearest.y
						else:
							verticals.sort(key=lambda r: r.y + r.h, reverse=True)
							nearest = verticals[0]
							lower_bound = nearest.y + nearest.h
					else:
						lower_bound = vertical_selector.y
						upper_bound = lower_bound + vertical_selector.h
					
					print("	horizontal cut:" ,left_bound, lower_bound, 
												right_bound, upper_bound)

					if upper_bound - lower_bound < rectangle.h:
						print("	horizontal cut: aborted on h too small?", upper_bound-lower_bound<rectangle.h)
						continue

					horizontal_selector = Rectangle(
						-sys.maxint,
						lower_bound,
						occ.x + occ.w + sys.maxint * 2,
						upper_bound - lower_bound
					)

					horizontals = self.get_selection_by_rect(horizontal_selector)

					if horizontals:
						horizontals.sort(key=lambda r: r.x)
						i = bisect.bisect([r.x for r in horizontals], x_section)
						# Fringe case 1: x_section is below lowest rect's x.
						if i == 0:
							right_bound = horizontals[0].x
							left_bound = right_bound - horizontal_selector.w
						# Fringe case 2: x_section is above highest rect's x.
						elif i == len(horizontals):
							# There is a rect occuying the space, continue.
							if (horizontals[-1].x < x_section 
									< horizontals[-1].x + horizontals[-1].w):
								continue
							else:
								left_bound = horizontals[-1].x + horizontals[-1].w
								right_bound = horizontal_selector.x + horizontal_selector.w
						# Norm case: x_section is inside the rects' x values.
						else:
							right_bound = horizontals[i].x
							left_bound = horizontals[i-1].x + horizontals[i-1].w
					else:
						left_bound = horizontal_selector.x
						right_bound = left_bound + horizontal_selector.w

						
					print("	horizontal cut:" ,left_bound, lower_bound, 
												right_bound, upper_bound)
						
					if right_bound - left_bound < rectangle.w:
						print("	horizontal cut: aborted on w too small?", right_bound-left_bound<rectangle.w)
						continue

					# Candidate spot was found
					newr = Rectangle(
						left_bound,
						lower_bound,
						right_bound - left_bound,
						upper_bound - lower_bound
					)
					
					
					for rr in self._rects:
						if newr.intersects(rr):
							print(
								newr, rr, self._rects.index(rr), self._rects,
								newr.get_intersection(rr), i, x_section, y_section,
								vertical_selector, verticals, 
								horizontal_selector, horizontals
							)
							raise Exception("Candidate spot overlaps.")

					if not newr in results:
						results.append(newr)

			
		return results
			
			
			
			
			