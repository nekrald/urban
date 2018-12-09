from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import logging

from .models import Item


def parameters(request):
        template = loader.get_template('parameters.html')
        context = {}
        response = HttpResponse(template.render(context, request))
        return response


def textures(request):
        material_ids = request.POST.getlist('materials')
        color_ids = request.POST.getlist('colors')
        logging.error("textures: material_ids = {}".format(material_ids))
        logging.error("textures: color_ids = {}".format(color_ids))
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')

        session = request.session
        session['materials'] = material_ids
        session['colors'] = color_ids
        session['min_price'] = min_price
        session['max_price'] = max_price

        template = loader.get_template('textures.html')
        context = {}
        response = HttpResponse(template.render(context, request))
        return response


def selection(request):        
        texture_ids = request.POST.getlist('textures')
        material_ids = request.session['materials']
        color_ids = request.session['colors']

        logging.error("selection: material_ids = {}".format(material_ids))
        logging.error("selection: color_ids = {}".format(color_ids))
        logging.error("selection: texture_ids = {}".format(texture_ids))

        template = loader.get_template('selection.html')
        context = {
            "product_list" : [
                Item(1, 'green', 'src/img.jpg', 'paper'),
                Item(2, 'blue', 'src/for.jpg', 'vynil'),
            ]
        }
        response = HttpResponse(template.render(context, request))
        return response

