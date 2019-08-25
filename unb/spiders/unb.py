import scrapy
from ..items import DepartamentoItem
from ..items import DisciplinaItem
from ..items import TurmaItem
from ..items import VagasItem

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
        for course in response.xpath("//div[@class='body table-responsive']//a"):
            if course.xpath("./text()").get() is not None:
                href = response.urljoin(course.xpath("./@href").get())
                request = response.follow(href, self.parse_classes, cb_kwargs=dict(departamento=departamento))
                request.cb_kwargs['departamento'] = departamento
                yield request
        
            
    def parse_classes(self, response, departamento):
        # print "Parsing Classes..."
        disciplina = response.xpath("//div[@class='header']//h2/text()").get().strip().encode('utf-8')
        departamento["disciplina"] = DisciplinaItem(nome=disciplina)
        turmas = []
        for a_class in response.xpath("//table[@class='table table-striped table-bordered tabela-oferta']"):
            letter = a_class.xpath(".//td[@class='turma']/text()").get().encode('utf-8')
            vacancy = a_class.xpath('.//table[@class="table tabela-vagas"]//span/text()')
            vacancy_total = vacancy.getall()[0].encode('utf-8')
            vacancy_occupied = vacancy.getall()[1].encode('utf-8')
            vacancy_free = vacancy.getall()[2].encode('utf-8')

            vagas = VagasItem(total=vacancy_total, ocupadas=vacancy_occupied, disponiveis=vacancy_free)

            turmas.append(TurmaItem(letra=letter, vagas=vagas))
        
        departamento["disciplina"]["turmas"] = turmas
        yield departamento
            

