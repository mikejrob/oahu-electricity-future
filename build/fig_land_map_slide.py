#!/usr/bin/env python3
"""Slide copy of the Figure 2.3 land map: the embedded title and caption
(top 138 px) cropped off. The talk frame supplies its own title and an
abbreviated caption beside the map (slides/talk_weer.tex)."""
from PIL import Image

im = Image.open("report/figures/fig_2_3_available_land_map.png")
im.crop((0, 138, im.size[0], im.size[1])).save(
    "report/figures/fig_2_3_available_land_map_slide.png")
print("wrote report/figures/fig_2_3_available_land_map_slide.png")
