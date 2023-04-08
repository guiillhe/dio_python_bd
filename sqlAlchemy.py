"""
    Primeiro programa de integração com banco de dados
    utilizando SQLAlchemy e modelo ORM

"""
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()


class Cliente(Base):
    __tablename__ = "clientes"
    # atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String)
    endereco = Column(String)
    contas = relationship('Conta', back_populates='cliente')

    def __repr__(self):
        return f"Cliente(id={self.id}, name={self.name}, cpf={self.cpf}, endereco={self.endereco})"



class Conta(Base):
    __tablename__ = "contas"
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    numero = Column(Integer)
    saldo = Column(Float)
    id_cliente = Column(Integer, ForeignKey('clientes.id'))
    cliente = relationship('Cliente', back_populates='contas')

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo})"


print(Cliente.__tablename__)
print(Conta.__tablename__)

# conexão com o banco de dados
engine = create_engine("sqlite:///meubd.bd")

# criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# investiga o esquema de banco de dados
inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("clientes"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    guilherme = Cliente(
        name="Guilherme ",
        cpf="123456789-11",
        endereco="Rua de casa",
        contas=[Conta(
            tipo='corrente',
            agencia='001',
            numero=1,
            saldo=500.10

        )]
    )
    joao = Cliente(
        name="João  ",
        cpf="123654987-66",
        endereco="Rua B",
        contas=[Conta(
            tipo='corrente',
            agencia='001',
            numero=2,
            saldo=600.10

        )]
    )
    regina = Cliente(
        name="Regina",
        cpf="7895423211-11",
        endereco="Rua B",
        contas=[Conta(
            tipo='corrente',
            agencia='003',
            numero=3,
            saldo=1500.10

        )]
    )

    # enviando para o BD (persitência de dados)
    #session.add_all([guilherme, joao, regina])

    session.commit()

stmt = select(Cliente).where(Cliente.name.in_(["Guilherme", 'Regina']))
print('Recuperando usuários a partir de condição de filtragem')
for cliente in session.execute(stmt):
    print(cliente)

stmt_address = select(Conta).where(Conta.id_cliente.in_([2]))
print('\nRecuperando os endereços de email de Sandy')
for address in session.scalars(stmt_address):
    print(address)

stmt_join = select(Cliente.name, Conta.saldo).join_from(Cliente, Conta)
print("\n")
for result in session.scalars(stmt_join):
    print(result)

# print(select(User.fullname, Address.email_address).join_from(Address, User))

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(Cliente)
print('\nTotal de instâncias em User')
for result in session.scalars(stmt_count):
    print(result)

# encerrando de fato a session
session.close()
