# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UnbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DepartamentoItem(scrapy.Item):
    # define the fields for your item here like:
    nome = scrapy.Field()
    disciplinas = scrapy.Field()

class DisciplinasItem(scrapy.Item):
    # define the fields for your item here like:
    nome = scrapy.Field()
    turmas = scrapy.Field()

class TurmaItem(scrapy.Item):
    # define the fields for your item here like:
    letra = scrapy.Field()
    vagas = scrapy.Field()

class VagasItem(scrapy.Item):
    # define the fields for your item here like:
    total = scrapy.Field()
    ocupadas = scrapy.Field()
    disponiveis = scrapy.Field()