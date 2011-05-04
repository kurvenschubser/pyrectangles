## outer horizontal
rel_y = abs(cy - (rect.y + rect.h * sector_y))
rel_x = rel_y / tan
cut_y = rect.y + rect.h * sector_y
cut_x = cx + rel_x * (sector_x or -1)

## outer horizontal cut
if (rect.x <= cut_x <= rect.x + rect.w):
	res.extend(((), (cut_x, cut_y)))