import json, os, datetime

print("Bem vindo a AutieStore! Aqui você vai encontrar produtos para te ajudar com cada uma "
      "das suas necessidades.")

with open("cadastro.json", encoding = "utf-8") as usuariosAutie :
    usuarios = json.load(usuariosAutie)

with open("produtos.json", encoding = "utf-8") as produtosAutie :
    produtos = json.load(produtosAutie)

with open("compras.json", encoding = "utf-8") as comprasAutie:
    compras = json.load(comprasAutie)

dadosEmpresa = {
    "cnpj": "71.204.960/0001-11"
}

emailProv = input("Informe seu email para checarmos se você tem cadastro: ")
for usuario in usuarios :
    if emailProv == usuario["Email"] :
        print("Te encontramos! Vamos começar as compras")
        senha = input("Email encontrado. Informe a sua senha: ")
        if senha != usuario["Senha"] :
            for i in range (1,3) :
                senha = input(f"Senha incorreta. Tente Novamente (tentativa {i+1}/3): ")
        if senha != usuario["Senha"] :
            os.system("cls")
            print("Você esgotou as suas chances então não podemos continuar com o login. Até!")
            SystemExit
    else :
        print("Primeira vez aqui? Vamos te cadastrar!")

        maiorId = 0
        for id in usuario["UserId"] :
            if id > maiorId :
                maiorId = id

        nomeProv = input("Qual é o seu nome? ")
        senhaProv = input("Escolha a sua senha: ")
        usuarioNovo = {
            "UserId" : maiorId + 1,
            "Email" : emailProv,
            "Nome" : nomeProv,
            "Senha" : senhaProv
        }
        usuarios.append(usuarioNovo)
        with open("cadastro.json", "w") as usuariosAutie :
            json.dump(usuarios, usuariosAutie)
        break

usuarioAtual = {}
for usuario in usuarios :
    if emailProv == usuario["Email"] :
        usuarioAtual = usuario

os.system("cls")

carrinhoDeCompras = []

def AdicionarItem(categoria) :
    opcaoProduto = int(input("Escolha pelo índice: "))
    item = {}
    i = 1
    for produto in produtos[categoria] :
        if i == opcaoProduto :
            qtdDisponivel = produto['QuantiaDisponivel']
            qtdEscolhida = int(input("Quantos você quer? "))

            while qtdEscolhida > qtdDisponivel :
                qtdEscolhida = int(input("Escolha uma quantidade válida, por favor: "))

            produto['QuantiaDisponivel'] -= qtdEscolhida
            item.update({"NomeProduto":produto["NomeProduto"]}) 
            item.update({"Preco":produto["Preco"]})
            item.update({"QuantidadeProdutos":qtdEscolhida})

            with open ('produtos.json', 'w', encoding = 'utf-8') as produtosAutie:
                json.dump(produtos, produtosAutie)
    
        i += 1
    if item == {} :
        print("O índice inserido não está entre as opções. Vamos tentar de novo!")
        item = AdicionarItem(categoria)
    return(item)

def MostrarMenu() :
    print(f"Tudo certo, agora vamos às compras!\n Escolha uma das nossas opções:  \n"
          f" 1. Pelúcias\n 2. Abafadores\n 3. Brinquedos sensoriais\n 4. Cordões de identificação"
          f"\n 5. Finalizar compra")
    opcao = int(input("Pelo índice, escolha uma categoria: "))
    return(opcao)

def ListarProdutoPorCategoria (categoria) :
    print(f"Temos as seguintes opções de {categoria}: ")
    i = 1
    for produto in produtos[categoria]:
        print(f"{i}. {produto['NomeProduto']}\n  " 
              f"Preço: R${produto['Preco']}\n   "
              f"Quantidade disponível: {produto['QuantiaDisponivel']}\n")
        i += 1
    interesseCompra = input("Você deseja comprar? (s/n)  ")
    if interesseCompra == "s" :
        item = AdicionarItem(categoria)
        carrinhoDeCompras.append(item)
        
def FinalizarCompra() :
    valorTotal = 0
    dataHoraCompra = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for item in carrinhoDeCompras :
        valorTotal += item['QuantidadeProdutos'] * item['Preco']

    compra = {"ClienteId" : usuarioAtual["UserId"]}
    compra.update({"DataHoraCompra" : dataHoraCompra})
    compra.update({"Produtos" : carrinhoDeCompras})
    compras.append(compra)

    with open("compras.json", "w") as comprasAutie :
        json.dump(compras, comprasAutie)
    
    print(f"O valor total da compra deu: R${valorTotal:.2f}")
    return(compra)

def GerarNotaFiscal(compra) :
    nomeArquivo = compra['DataHoraCompra'].replace(':', '').replace(' ', '').replace('-', '') + str(compra['ClienteId'])
    with open(f'Notas\{nomeArquivo}.txt', 'w', encoding = 'utf-8') as notaArquivo :
        notaArquivo.write("-------------------- AutieStore --------------------\n")
        notaArquivo.write("\n")
        notaArquivo.write(f"CNPJ do emitente: {dadosEmpresa['cnpj']}\n")
        notaArquivo.write(f"Email do cliente: {usuarioAtual['Email']}\n")
        notaArquivo.write(f"Data e hora da compra: {compra['DataHoraCompra']}\n")
        notaArquivo.write("\n")
        notaArquivo.write("Produtos:\n")

        qtdProdutos = 0
        valorTotal = 0

        for item in compra["Produtos"] :
            notaArquivo.write(f"{item['NomeProduto']} - Qtd: {item['QuantidadeProdutos']} Preço un. R${item['Preco']}\n")
            qtdProdutos += item['QuantidadeProdutos']
            valorTotal += item['QuantidadeProdutos'] * item['Preco']
        notaArquivo.write("----------------------------------------------------\n")
        notaArquivo.write(f"Quantidade total: {qtdProdutos}\n")
        notaArquivo.write(f"Valor total: {valorTotal:.2f}\n")
opcaoProv = MostrarMenu()

while True :
    if opcaoProv == 1 :
        ListarProdutoPorCategoria("Pelucias")
    elif opcaoProv == 2 :
        ListarProdutoPorCategoria("Abafadores")
    elif opcaoProv == 3 :
        ListarProdutoPorCategoria("Brinquedos sensoriais")
    elif opcaoProv == 4 :
        ListarProdutoPorCategoria("Cordoes de identificacao")
    elif opcaoProv == 5 :
        os.system("cls")
        confirmaçãoCompra = input("Tem certeza que deseja finalizar? (s/n) ")
        while (confirmaçãoCompra.lower() != "n" and confirmaçãoCompra.lower() != "s") :
            confirmaCompra = input("Opção inválida... por favor, insira S ou N: ")
        if confirmaçãoCompra.lower() == "n" :
            print("Certo! Vamos dar mais uma olhadinha nas opções, então <3")
        elif confirmaçãoCompra.lower() == "s" :
            compra = FinalizarCompra()
            input("Certo! Pressione a tecla ENTER para receber sua nota fiscal. Obrigada pela preferência <3")
            GerarNotaFiscal(compra)
            break

    opcaoProv = MostrarMenu()
        
    