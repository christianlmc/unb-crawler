# -*- coding: utf-8 -*-
import scrapy
from ..items import CursoItem

class CursoSpider(scrapy.Spider):
    name = 'curso'
    allowed_domains = ['matriculaweb.unb.br']
    start_urls = ['https://matriculaweb.unb.br/graduacao/curso_rel.aspx?cod=1/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'unb.pipelines.CursoPipeline': 400
        }
    }
    def parse(self, response):
        for link_curso in response.xpath("//div[@class='body table-responsive']//tr"):
            curso = CursoItem()
            curso['nome'] = link_curso.xpath(".//a/text()").get()
            curso['turno'] = link_curso.xpath(".//td[4]/text()").get()
            yield curso
