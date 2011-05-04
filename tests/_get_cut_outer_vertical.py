## outer vertical
rel_x = abs(cx - (rect.x + rect.w * sector_x))
rel_y = rel_x * tan
cut_x = rect.x + rect.w * sector_x
cut_y = cy + rel_y * (sector_y or -1)

## outer vertical cut
if (rect.y <= cut_y <= rect.y + rect.h):
	res.extend(((cut_x, cut_y), ()))