from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import logging
import sys
import os
import pandas as pd

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(FILE_DIR, "../../logic/Textures"))

from .models import ProposedItem, TextureItem, ItemPair
import wallpapers
import constants

from wallpapers import WallpaperMaster
from constants import COLORS, N_CLUSTERS, POWER, NB_RANKED_PICTURES


def parameters(request):
        template = loader.get_template('parameters.html')
        context = {}
        response = HttpResponse(template.render(context, request))
        return response


def text2id_color(text):
        converter = {
            "bezh" :  0,
            "blue" :  1,
            "gray" :  2,
            "rose" :  3,
            "green" :  4,
            "brown" : 5,
            "red" : 6,
            "white" : 7,
            "black" : 8,
            "violet" : 9,
            "yellow" : 10,
        }
        if text in converter:
            return converter[text]
        else:
            raise ValueError("Strange text!")


def transform_path(path):
        host = os.path.dirname(os.path.dirname(path))
        return os.path.relpath(path, host)


def textures(request):
        material_names = request.POST.getlist('materials')
        color_names = request.POST.getlist('colors')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        
        color_ids = [text2id_color(name) for name in color_names]
        assert len(color_ids) > 0
        master = WallpaperMaster()
        names, paths = master.get_pictures_by_color_id(color_ids[0])

        texture_list = []
        idx = 0
        while idx < len(names):
                link = paths[idx]
                lhs = TextureItem(transform_path(paths[idx]), names[idx])
                rhs = TextureItem(transform_path(paths[idx+1]), names[idx+1])
                pair = ItemPair(lhs, rhs)
                texture_list.append(pair)
                idx += 2

        session = request.session
        session['materials'] = material_names
        session['colors'] = color_names
        session['min_price'] = min_price
        session['max_price'] = max_price

        template = loader.get_template('textures.html')
        context = {
            "texture_list" : texture_list    
        }
        response = HttpResponse(template.render(context, request))
        return response


def selection(request):        
        texture_ids = request.POST.getlist('textures')
        material_names = request.session['materials']
        color_names = request.session['colors']
        color_ids = [text2id_color(name) for name in color_names]
        master = WallpaperMaster()
        names, links = master.get_ranked_pictures(color_ids[0], texture_ids[0])
        data_texture = pd.read_excel("data/data_part_1.xls")
        data_texture_cols = data_texture.columns
        data_texture_filter = data_texture[[data_texture_cols[0], data_texture_cols[1], data_texture_cols[17]]]
        data_texture_filter.columns = ["name", "id", "color"]
        product_list = []
        for index, path in zip(names, links):
                goal = int(index)
                name = "Unknown"
                color = "Unknown"
                for idx, item in enumerate(data_texture_filter["id"].values):
                        if goal == item:
                                name = data_texture_filter["name"][idx]
                                color = data_texture_filter["color"][idx]
                product_list.append(ProposedItem(color, transform_path(path), goal, name))
        template = loader.get_template('selection.html')
        context = {
            "product_list" : product_list
        }
        response = HttpResponse(template.render(context, request))
        return response

