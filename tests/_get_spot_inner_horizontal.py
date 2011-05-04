def _get_spot_inner_horizontal(self, rectangle, occ, sector_x, sector_y,
										cut_x, cut_y, inner, vertical):

	left_bound = cut_x - rectangle.w * (not sector_x)
	right_bound = left_bound + rectangle.w
	lower_bound = cut_y - rectangle.h * sector_y
	upper_bound = lower_bound + rectangle.h

	vsel = Rectangle(
		left_bound,
		lower_bound if not sector_y else occ.y - INF,
		rectangle.w,
		occ.y + occ.h - lower_bound + INF if not sector_y \
						else upper_bound - occ.y + INF
	)

	verticals = self.get_selection_by_rect(vsel)
	if verticals:
		if not sector_y:
			verticals.sort(key=lambda r: r.y)
			nearest = verticals[0]
			upper_bound = nearest.y
		else:
			verticals.sort(key=lambda r: r.y + r.h)
			nearest = verticals[-1]
			lower_bound = nearest.y + nearest.h
	else:
		lower_bound = vsel.y
		upper_bound = lower_bound + vsel.h

	if upper_bound - lower_bound < rectangle.h:
		return []

	hsel = Rectangle(
		occ.x - INF,
		lower_bound,
		occ.w + 2 * INF,
		upper_bound - lower_bound
	)

	horizontals = self.get_selection_by_rect(hsel)
	if horizontals:
		horizontals.sort(key=lambda r: r.x)
		i = bisect.bisect([r.x for r in horizontals], cut_x)

		## Fringe case 1: all found rect's are farther right than
		## *cut_x*.
		if i == 0:
			right_bound = horizontals[0].x
			left_bound = hsel.x

		## Fringe case 2: all found rect's are farther left than
		## *cut_x*.
		elif i == len(horizontals):
			## There is a rect occuying the space, continue.
			if (horizontals[-1].x < cut_x 
					< horizontals[-1].x + horizontals[-1].w):
				return []
			else:
				left_bound = horizontals[-1].x + horizontals[-1].w
				right_bound = occ.x + occ.w + INF

		## Case 3: cut_x is somewhere among the rects.
		else:
			right_bound = horizontals[i].x
			left_bound = horizontals[i-1].x + horizontals[i-1].w
	else:
		left_bound = hsel.x
		right_bound = left_bound + hsel.w

	if right_bound - left_bound < rectangle.w:
		if __debug__:
			print("	horizontal cut: aborted on w too small.")
			
		return []

	## Candidate spot was found
	newr = Rectangle(
		left_bound,
		lower_bound,
		right_bound - left_bound,
		upper_bound - lower_bound
	)

	return [newr]