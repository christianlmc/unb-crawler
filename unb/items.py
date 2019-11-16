# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CursoItem(scrapy.Item):
    nome = scrapy.Field()
    turno = scrapy.Field()
    
class UnbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DisciplinaItem(scrapy.Item):
    # define the fields for your item here like:
    nome = scrapy.Field()
    turmas = scrapy.Field()
    departamento = scrapy.Field()

class TurmaItem(scrapy.Item):
    # define the fields for your item here like:
    letra = scrapy.Field()

    vagas_total = scrapy.Field()
    vagas_ocupadas = scrapy.Field()
    vagas_disponiveis = scrapy.Field()
