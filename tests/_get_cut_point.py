def _get_cut_point(self, rect, occ, tan, sector_x, sector_y, 
											outer, vertical):
	cx, cy = occ.get_center()
	outer = int(outer)

	if vertical:
		rel_x = abs(cx - (rect.x + rect.w * (outer * sector_x)))
		rel_y = rel_x * tan
		cut_x = rect.x + rect.w * (int(outer) * sector_x)
		cut_y = cy + rel_y * (sector_y or -1)
		if rect.y <= crt_y <= rect.y + rect.h:
			return (cut_x, cut_y)
	else:
		rel_y = abs(cy - (rect.y + rect.h * (outer * sector_y)))
		rel_x = rel_y / tan
		cut_y = rect.y + rect.h * (outer * sector_y)
		cut_x = cx + rel_x * (sector_x or -1)
		if (rect.x <= cut_x <= rect.x + rect.w):
			return (cut_x, cut_y)

	return ()