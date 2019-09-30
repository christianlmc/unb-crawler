# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector

class UnbPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="J!@bt5A*(",
            database="secretaria_digital",
            use_unicode=True,
            charset='utf8'
        )

        self.curr = self.conn.cursor(buffered=True)

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS turmas, disciplinas, departamentos""")
        self.curr.execute("""
            CREATE TABLE departamentos(
                id INT NOT NULL AUTO_INCREMENT,
                nome VARCHAR(1000) NOT NULL UNIQUE,

                PRIMARY KEY ( id )
            );
        """)

        self.curr.execute("""
            CREATE TABLE disciplinas(
                id INT NOT NULL AUTO_INCREMENT,
                nome VARCHAR(1000) NOT NULL,
                departamento_id INT NOT NULL,

                FOREIGN KEY ( departamento_id ) REFERENCES departamentos(id),
                PRIMARY KEY ( id )
            );
        """)

        self.curr.execute("""
            CREATE TABLE turmas(
                id INT NOT NULL AUTO_INCREMENT,
                disciplina_id INT NOT NULL,
                letra TINYTEXT NOT NULL,
                vagas_total SMALLINT UNSIGNED NOT NULL,
                vagas_ocupadas SMALLINT UNSIGNED NOT NULL,
                vagas_disponiveis SMALLINT UNSIGNED NOT NULL,

                FOREIGN KEY ( disciplina_id ) REFERENCES disciplinas(id),
                PRIMARY KEY ( id )
            );
        """)

    def process_item(self, item, spider):
        depto_id = self.insert_departmento(item["departamento"])
        disciplina_id = self.insert_disciplina(depto_id, item["nome"])
        self.insert_turmas(disciplina_id, item["turmas"])

    def insert_departmento(self, departamento):
        select = """
            SELECT id FROM departamentos WHERE nome='"""+departamento+"""';
        """
        self.curr.execute(select)

        rows = self.curr.rowcount

        # print rows
        if rows == 0:
            self.curr.execute("""
                INSERT INTO departamentos (nome) VALUES (%s);
            """, (departamento,))
            self.conn.commit()
        
        self.curr.execute(select)
        
        return self.curr.fetchone()[0]

    def insert_disciplina(self, depto_id, nome):

        self.curr.execute("""
            INSERT INTO disciplinas (nome, departamento_id) VALUES (%s, %s);
        """, (nome, depto_id))
        self.conn.commit()

        select = """
            SELECT id FROM disciplinas WHERE nome='"""+nome+"""';
        """

        self.curr.execute(select)
        
        return self.curr.fetchone()[0]

    def insert_turmas(self, disciplina_id, turmas):
        turmas_query = []
        for turma in turmas:
            turmas_query.append((disciplina_id, turma["letra"], turma["vagas_total"], turma["vagas_ocupadas"], turma["vagas_disponiveis"]))

        self.curr.executemany("""
            INSERT INTO turmas (disciplina_id, letra, vagas_total, vagas_ocupadas, vagas_disponiveis) VALUES (%s, %s, %s, %s, %s);
        """, turmas_query)
        self.conn.commit()