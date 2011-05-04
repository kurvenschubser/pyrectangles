## inner vertical
rel_x = abs(cx - (rect.x + rect.w * (not sector_x)))
rel_y = rel_x * tan
cut_x = rect.x + rect.w * (not sector_x)
cut_y = cy + rel_y * (sector_y or -1)

## inner vertical cut
if (rect.y <= cut_y <= rect.y + rect.h):
	res.extend(((cut_x, cut_y), ()))