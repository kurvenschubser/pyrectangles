def _get_spot_inner_vertical(self, rectangle, occ, sector_x, sector_y,
										cut_x, cut_y, inner, vertical):

	left_bound = cut_x - rectangle.w * sector_x
	right_bound = left_bound + rectangle.w
	lower_bound = cut_y - rectangle.h * (not sector_y)
	upper_bound = lower_bound + rectangle.h

	hsel = Rectangle(
		left_bound if not sector_x else occ.x - INF,
		lower_bound,
		occ.x + occ.w - left_bound + INF if not sector_x \
			else right_bound - occ.x + INF,
		rectangle.h
	)

	horizontals = self.get_selection_by_rect(hsel)
	if horizontals:
		if not sector_x:
			horizontals.sort(key=lambda r: r.x)
			nearest = horizontals[0]
			right_bound = nearest.x
		else:
			horizontals.sort(key=lambda r: r.x + r.w)
			nearest = horizontals[-1]
			left_bound = nearest.x + nearest.w
	else:
		left_bound = hsel.x
		right_bound = left_bound + hsel.w

	if right_bound - left_bound < rectangle.w:
		return []

	vsel = Rectangle(
		left_bound,
		occ.y - INF,
		right_bound - left_bound,
		occ.h + 2 * INF
	)

	verticals = self.get_selection_by_rect(vsel)
	if verticals:
		verticals.sort(key=lambda r: r.y)
		i = bisect.bisect([r.y for r in verticals], cut_y)

		## Fringe case 1: cut_y is below lowest rect's y.
		if i == 0:
			upper_bound = verticals[0].y
			lower_bound = vsel.y

		## Fringe case 2: cut_y is above highest rect's y.
		elif i == len(verticals):
			## There is a rect occupying the space, continue.
			if (verticals[-1].y < cut_y 
					< verticals[-1].y + verticals[-1].h):
					## !!! This test is probably unnecessary
					## since an overlapping on the 
					## point is eliminated by the *hsel*
					## selector rectangle.
				return []
			else:
				lower_bound = verticals[-1].y + verticals[-1].h
				upper_bound = occ.y + occ.h + INF

		## Norm case: cut_y is inside the rects' y values.
		else:
			upper_bound = verticals[i].y
			lower_bound = verticals[i-1].y + verticals[i-1].h
	else:
		lower_bound = vsel.y
		upper_bound = vsel.y + vsel.h

	if upper_bound - lower_bound < rectangle.h:
		if __debug__:
			print("	vertical cut: aborted on h too small.")
			
		return []

	## Candidate spot was found
	newr = Rectangle(
		left_bound,
		lower_bound,
		right_bound - left_bound,
		upper_bound - lower_bound
	)

	return [newr]

