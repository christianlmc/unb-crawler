import scrapy
from ..items import DisciplinaItem
from ..items import TurmaItem

# -*- coding: utf-8 -*-

class UnbSpider(scrapy.Spider):
    name = "unb"

    start_urls = [
        'https://matriculaweb.unb.br/graduacao/oferta_dep.aspx'
    ]

    def parse(self, response):
        for depto in response.xpath("//div[@class='body table-responsive']//a"):
            disciplina = DisciplinaItem()
            disciplina["departamento"] = depto.xpath("./text()").get().encode('utf-8')

            href = response.urljoin(depto.xpath("./@href").get())
            request = response.follow(href, self.parse_courses, cb_kwargs=dict(disciplina=disciplina))
            request.cb_kwargs['disciplina'] = disciplina

            yield request

    def parse_courses(self, response, disciplina):
        # print "Parsing Courses..."

        for course in response.xpath("//div[@class='body table-responsive']//a[not(@title)]"):

            href = response.urljoin(course.xpath("./@href").get())
            request = response.follow(href, self.parse_classes, cb_kwargs=dict(disciplina=disciplina))
            request.cb_kwargs['disciplina'] = disciplina

            yield request

    def parse_classes(self, response, disciplina):
        # print "Parsing Classes..."
        turmas = []
        disciplina["nome"] = response.xpath("//div[@class='header']/h2/text()").get().strip().encode('utf-8')

        for a_class in response.xpath("//table[@class='table table-striped table-bordered tabela-oferta']"):

            letter = a_class.xpath(".//td[@class='turma']/text()").get().encode('utf-8')
            vacancy = a_class.xpath('.//table[@class="table tabela-vagas"]//span/text()')
            vacancy_total = int(vacancy.getall()[0].encode('utf-8'))
            vacancy_occupied = int(vacancy.getall()[1].encode('utf-8'))
            vacancy_free = int(vacancy.getall()[2].encode('utf-8'))

            turma = TurmaItem(letra=letter, vagas_total=vacancy_total, vagas_ocupadas=vacancy_occupied, vagas_disponiveis=vacancy_free)

            turmas.append(turma)

        disciplina["turmas"] = turmas

        yield disciplina
        
        
            

