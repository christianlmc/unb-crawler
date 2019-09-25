import scrapy
from ..items import DepartamentoItem
from ..items import DisciplinasItem
from ..items import TurmaItem
from ..items import VagasItem

# -*- coding: utf-8 -*-

class UnbSpider(scrapy.Spider):
    name = "unb"

    start_urls = [
        'https://matriculaweb.unb.br/graduacao/oferta_dep.aspx'
    ]

    def parse(self, response):
        for depto in response.xpath("//div[@class='body table-responsive']//a"):
            departamento = DepartamentoItem()
            departamento["nome"] = depto.xpath("./text()").get().encode('utf-8')
            href = response.urljoin(depto.xpath("./@href").get())
            request = response.follow(href, self.parse_courses, cb_kwargs=dict(departamento=departamento))
            request.cb_kwargs['departamento'] = departamento

            yield request

    def parse_courses(self, response, departamento):
        # print "Parsing Courses..."
        requests = []
        disciplinas = []
        for course in response.xpath("//div[@class='body table-responsive']//a"):
            disciplina = course.xpath("./text()").get()
            if disciplina is not None:
                disciplinas.append(DisciplinasItem(nome=disciplina.strip().encode('utf-8')))

                href = response.urljoin(course.xpath("./@href").get())
                request = response.follow(href, self.parse_classes, cb_kwargs=dict(departamento=departamento))
                request.cb_kwargs['departamento'] = departamento
                requests.append(request)

        departamento["disciplinas"] = disciplinas

        for request in requests:
            yield request
            
    def parse_classes(self, response, departamento):
        # print "Parsing Classes..."
        turmas = []

        disciplina_oferta = response.xpath("//div[@class='header']//h2/text()").get().strip().encode('utf-8')

        for disciplina in departamento["disciplinas"]:
            if disciplina["nome"] == disciplina_oferta:
                for a_class in response.xpath("//table[@class='table table-striped table-bordered tabela-oferta']"):

                    letter = a_class.xpath(".//td[@class='turma']/text()").get().encode('utf-8')
                    vacancy = a_class.xpath('.//table[@class="table tabela-vagas"]//span/text()')
                    vacancy_total = vacancy.getall()[0].encode('utf-8')
                    vacancy_occupied = vacancy.getall()[1].encode('utf-8')
                    vacancy_free = vacancy.getall()[2].encode('utf-8')

                    vagas = VagasItem(total=vacancy_total, ocupadas=vacancy_occupied, disponiveis=vacancy_free)

                    turmas.append(TurmaItem(letra=letter, vagas=vagas))

                disciplina["turmas"] = turmas
        
        # departamento["disciplinas"]["turmas"] = turmas
        # print departamento
        # print turmas
        yield departamento
            

