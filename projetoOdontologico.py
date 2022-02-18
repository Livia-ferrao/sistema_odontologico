from tkinter import *
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser


root = Tk()

class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    def geraRelatCliente(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.foneRel = self.fone_entry.get()
        self.precoRel = self.preco_entry.get()
        self.cpfRel = self.cpf_entry.get()
        self.horaRel = self.hora_entry.get()
        self.dataRel = self.data_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Codigo: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 630, 'Telefone: ')
        self.c.drawString(50, 600, 'Preço: ')
        self.c.drawString(50, 570, 'CPF:: ')
        self.c.drawString(50, 540, 'Horário: ')
        self.c.drawString(50, 510, 'Data: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670, self.nomeRel)
        self.c.drawString(150, 630, self.foneRel)
        self.c.drawString(150, 600, self.precoRel)
        self.c.drawString(150, 570, self.cpfRel)
        self.c.drawString(150, 540, self.horaRel)
        self.c.drawString(150, 510, self.dataRel)

        self.c.showPage()
        self.c.save()
        self.printCliente()

class Funcs():
    def limpa_cliente(self):
        self.codigo_entry.delete(0, END)
        self.preco_entry.delete(0, END)
        self.fone_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.cpf_entry.delete(0, END)
        self.hora_entry.delete(0, END)
        self.data_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando ao banco de dados")
    def montaTabelas(self):
        self.conecta_bd()
        ### Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                preco CHAR(40),
                cpf INTEGER(20),
                hora INTEGER(20),
                data INTEGER(20)               
            );
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.fone = self.fone_entry.get()
        self.preco = self.preco_entry.get()
        self.cpf = self.cpf_entry.get()
        self.hora = self.hora_entry.get()
        self.data = self.data_entry.get()
    def OnDoubleClick(self, event):
        self.limpa_cliente()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6, col7 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.fone_entry.insert(END, col3)
            self.preco_entry.insert(END, col4)
            self.cpf_entry.insert(END, col5)
            self.hora_entry.insert(END, col6)
            self.data_entry.insert(END, col7)

    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, preco, cpf, data, hora)
            VALUES (?, ?, ?, ?, ?, ?)""", (self.nome, self.fone, self.preco, self.cpf, self.hora, self.data))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""UPDATE clientes SET nome_cliente = ?, telefone = ?, preco = ?, cpf = ?, hora = ?, 
        data = ? WHERE cod = ? """,
                            (self.nome, self.fone, self.preco, self.cpf, self.hora, self.data,  self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_cliente()
        self.select_lista()

    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, preco, cpf, hora, data FROM clientes
            ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone, preco, cpf, hora, data FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_cliente()
        self.desconecta_bd()

class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()
    def tela(self):
        self.root.title("Agendamento odontológico")
        self.root.configure(background= '#292325')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width= 900, height= 700)
        self.root.minsize(width=500, height= 400)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd = 4, bg= '#dfe3ee',
                             highlightbackground= '#FFC0CB', highlightthickness=3 )
        self.frame_1.place(relx= 0.02, rely=0.02, relwidth= 0.96, relheight= 0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#FFC0CB', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    def widgets_frame1(self):
        ### Criação do botao limpar
        self.bt_limpar = Button(self.frame_1, text= "Limpar", bd=2, bg = '#ea899a',fg = 'white',
                                activebackground='#FFC0CB', activeforeground="white"
                                , font = ('verdana', 8, 'bold'), command= self.limpa_cliente)
        self.bt_limpar.place(relx= 0.2, rely=0.1, relwidth=0.1, relheight= 0.15)
        ### Criação do botao buscar
        self.bt_limpar = Button(self.frame_1, text="Buscar", bd=2, bg = '#ea899a',fg = 'white',
                                activebackground='#FFC0CB', activeforeground="white"
                                , font = ('verdana', 8, 'bold'), command = self.busca_cliente)
        self.bt_limpar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        ### Criação do botao novo
        self.bt_limpar = Button(self.frame_1, text="Novo", bd=2, bg='#ea899a', fg='white'
                                , font=('verdana', 8, 'bold'), command=self.add_cliente)
        self.bt_limpar.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        ### Criação do botao alterar
        self.bt_limpar = Button(self.frame_1, text="Alterar", bd=2, bg='#ea899a', fg='white'
                                , font=('verdana', 8, 'bold'), command=self.altera_cliente)
        self.bt_limpar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        ### Criação do botao apagar
        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=2, bg = '#ea899a',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        ## Criação da label e entrada do codigo
        self.lb_codigo = Label(self.frame_1, text = "Código", bg= '#dfe3ee', fg = '#8C5B65')
        self.lb_codigo.place(relx= 0.05, rely= 0.05)

        self.codigo_entry = Entry(self.frame_1 )
        self.codigo_entry.place(relx= 0.05, rely= 0.15, relwidth= 0.08)

        ## Criação da label e entrada do nome
        self.lb_nome = Label(self.frame_1, text="Nome do paciente", bg= '#dfe3ee', fg = '#8C5B65')
        self.lb_nome.place(relx=0.05, rely=0.35)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.4)

        ## Criação da label e entrada do telefone
        self.lb_nome = Label(self.frame_1, text="Telefone", bg= '#dfe3ee', fg = '#8C5B65')
        self.lb_nome.place(relx=0.05, rely=0.56)

        self.fone_entry = Entry(self.frame_1)
        self.fone_entry.place(relx=0.05, rely=0.66, relwidth=0.4)

        ## Criação da label e entrada do preço
        self.lb_nome = Label(self.frame_1, text="Preço da consulta (R$)", bg= '#dfe3ee', fg = '#8C5B65')
        self.lb_nome.place(relx=0.5, rely=0.56)

        self.preco_entry = Entry(self.frame_1)
        self.preco_entry.place(relx=0.5, rely=0.66, relwidth=0.4)

        ## Criação da label e entrada do cpf
        self.lb_cpf = Label(self.frame_1, text="CPF", bg='#dfe3ee', fg='#8C5B65')
        self.lb_cpf.place(relx=0.5, rely=0.35)

        self.cpf_entry = Entry(self.frame_1)
        self.cpf_entry.place(relx=0.5, rely=0.45, relwidth=0.4)

        ## Criação da label e entrada do horário
        self.hora = Label(self.frame_1, text="Horário", bg='#dfe3ee', fg='#8C5B65')
        self.hora.place(relx=0.05, rely=0.78)

        self.hora_entry = Entry(self.frame_1)
        self.hora_entry.place(relx=0.05, rely=0.88, relwidth=0.4)

        ## Criação da label e entrada da data
        self.data = Label(self.frame_1, text="Data", bg='#dfe3ee', fg='#8C5B65')
        self.data.place(relx=0.5, rely=0.78)

        self.data_entry = Entry(self.frame_1)
        self.data_entry.place(relx=0.5, rely=0.88, relwidth=0.4)


    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3,
                                     column=("col1", "col2", "col3", "col4", "col5", "col6", "col7"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Codigo")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Preço")
        self.listaCli.heading("#5", text="CPF")
        self.listaCli.heading("#6", text="Data")
        self.listaCli.heading("#7", text="Horário")
        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=25)
        self.listaCli.column("#2", width=90)
        self.listaCli.column("#3", width=70)
        self.listaCli.column("#4", width=50)
        self.listaCli.column("#5", width=70)
        self.listaCli.column("#6", width=70)
        self.listaCli.column("#7", width=70)
        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label= "Opções", menu=filemenu)
        menubar.add_cascade(label="Relatorios", menu=filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu.add_command(label="Limpa cliente", command= self.limpa_cliente)

        filemenu2.add_command(label="Ficha do cliente", command=self.geraRelatCliente)

Application()