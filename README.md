# CGI / Common Gateway Interface

-------------------------------------------------------------

O que é o CGI(common gateway interface) e o que ele faz?
CGI(Common Gateway Interface) é uma tecnologia que permite gerar páginas dinâmicas com interação entre scripts de Servidores HTTP com Gateway Scripts e Programas através de parâmetros. Sendo assim Scripts CGI são os pequenos programas que interpretam esses parâmetros e geram uma página depois de os processar.

Porém o uso do CGI não é muito seguro, tendo em mente que é preciso tomar algumas precauções de seguranças. Logo abaixo será discutido sobre que precauções de segurança tomar baseado em algumas regras dos programas CGI após a explicação de como o CGI funciona.

Como funciona?
Exemplo:

O CLIENTE(Browser) solicita uma URL ao SERVIDOR
A URL solicitada é referente a um CGI, portanto o SERVIDOR executa o CGI
o CGI trabalha interagindo com outras aplicações do sistema, recupera dados destas aplicações e retorna o resultado ao SERVIDOR
O SERVIDOR envia os dados para o CLIENTE, que formata o resultado e apresenta ao usuário
inserir a descrição da imagem aqui

Para que usar CGI?
Com o CGI, seu servidor pode acessar informações que não estão de uma forma legível para o cliente (ex. SQL database), e age como gateway entre ambos para produzir alguma coisa que o cliente possa usar. Gateways podem ser usadas para uma variedade de propositos, os mais comuns são manipulação de ISINDEX e requisição de formulário para HTTP.

Exemplos do uso de CGI:
Converter páginas de manual de sistemas para HTML e enviar o resultado HTML para o cliente.
Fazer interface com WAIS e banco de dados archie, convertendo os resultados para HTML e enviando o resultado para o cliente.
Permitir ao usuário realimentar seu servidor atraves de um formulário HTML e um decodificador acompanhando o CGI.
Você pode estar escrevendo estes CGI's através de gateways que podem ser escritos em qualquer liguagem que permita ser executado no sistema, tais como:

C/C++
Fortran
Perl
TCL
Unix Shell
Visual Basic
Apple Script
Quais são as principais regras dos programas CGI?
Programas CGI, ou scripts, são programas executáveis que podem ser executados por si mesmo (o que não é uma maneira segura). Portanto existem algumas precauções de segurança que necessitam ser implementadas quando utilizando programas CGI.

As principais regras são:

O script CGI tem que estar em um lugar determinado pelo servidor para os scripts CGI ou tem que ter um sufixo especial, que o servidor está configurado para reconhecer como um script CGI legal.
A maioria dos sistemas armazena scripts CGI em um diretório raiz do servidor HTTP, chamado cgi-bin, que é configurado de tal forma que, somente determinados usuários de confiança, possam gravar nele. Isto evita problemas óbvios de segurança, que surgem ao se permitir que usuários anônimos remotos executem qualquer coisa no sistema.
Exemplo: /usr/local/apache/htdocs/cgi-bin

O script pode recolher seus parâmetros, da entrada padrão (via teclado), das variáveis de ambientes ou de ambas.

O script deve dar como saída, um dos três tipos de cabeçalho padrão, como uma string de texto normal. Sendo os três tipos:

CONTEXT_TYPE: O tipo de conteúdo se refere a qualquer tipo de dado MIME que seja aceito pelo servidor.
Os tipos comuns incluem texto/html, texto/simples e dados/gif.
Como o browser/servidor não pode deduzir este tipo de arquivo, a partir de uma localização ou sufixo de nome de arquivo, este título informará ao browser que tipo de dados esperar e como usá-lo.

Formato: tipo/tipo

LOCATION: Aponta para um documento em algum outro lugar do servidor.
Permite que você redirecione pedidos para documentos, baseando-se em algum critério enviado por um formulário ou variável de ambiente.

STATUS: Pode ser usado para executar um script, sem enviar uma nova página para o cliente. Também pode ser usado para enviar uma mensagem de erro ou outra informaçao para o cliente.

O script deve ser executável pelo usuário que o servidor tem configurado. (Existe um usuário especial chamado "NOBODY" que é o usuário padrão para a maioria dos servidores Web. Você deve se certificar de que o usuário "NOBODY" ou o usuário para o qual o seu servidor está configurado para trabalhar, tem permissão para executar os seus scripts e ler/escrever em quaisquer arquivos que o script possa usar).

Mais detalhes de Segurança em Scripts CGI

Como obter informações do servidor?
Cada vez que um usuário solicita a URL correspondente ao seu programa CGI, o servidor irá executá-lo em tempo real. Um conceito errado sobre CGI é que você pode enviar linhas de comandos opcionais e argumentos para seu programa, tal como:

command% myprog -qa blorf

CGI utiliza a linha de comando para outros propositos. Gateway usa variaveis de ambiente para enviar ao programa seus parametros.

Como enviar documentos para o usuário?
Programas CGI podem retornar um grande número de tipos de documentos. Podem retornar uma imagem ao usuário, um documento HTML, ou talvez um clip de áudio. Podem também referenciar outros documentos.

O cliente necessita saber que tipo de documento receberá, para que possa apresentá-lo de maneira adequada. Logo o programa CGI deve informar ao servidor que tipo de documento está sendo enviado.

De forma a comunicar ao servidor o tipo de documento que está retornando, se é um documento completo ou uma referência para outro, CGI requer um pequeno cabeçalho na saída. Este cabeçalho é um texto ASCII, consistindo de linhas separadas ou por linefeeds ou por carriage returns (ou por ambos) seguidos de uma linha em branco.

Exemplo:

Um documento completo com o tipo MIME correspondente.
Enviando um documento HTML para o cliente.

Content-type: text/html

<html>
<head>
    <title>saída HTML de um script CGI</title>
</head>
<body>
    <h1>Saída de exemplo</h1>
    O que você acha <strong>disso?</strong>
</body>
</html>
Uma referência a outro documento.

Content-type: text/html
Location: gopher://httprules.foobar.org/0

<html>
<head>
    <title>Desculpe...moveu-se</title>
</head>
<body>
    <h1>Ir para vez do Gopher</h1>
    Agora disponível em
    <a href="gopher://httprules.foobar.org/0">uma nova localização</a> no nosso servidor do Gopher.
</body>
</html>
Como construir um formulário?
Um formulário pode ser criado dentro de uma página html usando a tag FORM. Uma página pode conter vários formulários, mas os formulários não podem estar contidos uns nos outros.

<form method="Método GET ou POST" action="A URL">...</form>
Onde o ACTION é a URL do servidor que receberá os dados do formulário (isto é, é o endereço do programa CGI responsável pelo tratamento dos dados) e METHOD é a forma como os dados serão passados para o programa CGI.

Um formulário pode conter vários componentes, como inputs, check boxes e radio.

Como obter os dados do formulário?
Existem dois métodos que podem ser usados para acessar os formulários, GET e POST. Dependendo do método utilizado, você receberá os dados de maneira diferente.

O método GET: Se o seu formulário usa method="GET", seu programa CGI receberá os dados codificados na variável de ambiente QUERY_STRING.
Exemplo:

<form method="GET" action="get-query.cgi">
    Login: <input type="text" name="login" />
    Senha: <input type="text" name="senha" />
    <input type="submit" value="Enviar" />
</form>

O método POST: Se o seu formulário usa method="POST", seu programa CGI receberá os dados da entrada padrão stdin. O servidor NÃO enviará um EOF ao término dos dados. Ao invés disso você terá que usar a variável de ambiente CONTENT_LENGTH para determinar a quantidade de dados a serem lidos de stdin.

Exemplo:

<form method="POST" action="post-query.cgi">
    Login: <input type="text" name="login" />
    Senha: <input type="text" name="senha" />
    <input type="submit" value="Enviar" />
</form>

Como fazer para ler uma variável de ambiente dependerá do Sistema Operacional em que o programa CGI será executado e da linguagem de programação em que foi escrito. Um programa C rodando em UNIX pode usar a função char *getenv(const char *name); que recebe o nome da variável como argumento e retorna o seu valor em um string.

É uma tecnologia antiga?
O CGI foi concebido como o culminar de discussões por especialistas durante os primórdios da Internet, em 1993 pela NSCA(National Center for Supercomputing Applications) nomeadamente entre Rob McCool, John Franks, Ari Luotonen, George Phillips e Tony Sanders. O que pode fazer dela ser considerada uma tecnologia antiga.

Especificação do CGI 1.1: RFC3875

Embora a linguagem tipicamente associada aos CGI seja o Perl, o CGI foi concebido de forma a ser independente da linguagem utilizada. Atualmente tecnologias como ASP.NET, PHP, Python e Ruby continuam a utilizar a especificação.

Existem outras alternativas a ele(quais)?
FastCGI: É um protocolo binário para interação de interfaces de programas com um Servidor Web.

PSGI: É uma interface entre servidores web e Aplicações web PERL e Frameworks que permite escrever aplicações que podem ser executados como servidores autônomos ou usando o CGI.
Rack: Fornece uma interface modular e adaptável para o desenvolvimento de aplicações web em Ruby.

WRB: Tecnologia de servidor HTTP similar ao CGI distribuído pela Oracle.

Fontes:

http://penta.ufrgs.br/edu/forms/cgi.html

https://www.w3.org/CGI/

https://en.wikipedia.org/wiki/Common_Gateway_Interface

https://pt.wikipedia.org/wiki/CGI

http://homepages.dcc.ufmg.br/~mlbc/cursos/internet/cgi/intro.htm


-------------------------------------------------------------

# CGI (sigla em inglês para Common Gateway Interface), em português , Interface Comum de Porta de entrada.

Interface: elemento que proporciona uma ligação física ou lógica entre dois sistemas ou partes de um sistema que não poderiam ser conectados diretamente.

Visão Geral
inserir a descrição da imagem aqui

Geralmente, o servidor HTTP tem um diretório (pasta), que é designado como uma coleção de documentos(arquivos), que podem ser enviados para navegadores da Web ligados a este servidor. Por exemplo, se o servidor Web tem o nome de domínio exemplo.com , e sua coleção de documentos é armazenado em /usr/local/apache/htdocs no sistema de arquivos local, em seguida, o servidor web irá responder a um pedido de http://exemplo.com/index.html enviando para o navegador o arquivo /usr/local/apache/htdocs/index.html.

CGI estende esse sistema, permitindo ao proprietário do servidor Web designar um diretório dentro da coleção de documento contendo scripts executáveis ​​(ou arquivos binários) em vez de páginas pré-escritas, isto é conhecido como um diretório CGI. Por exemplo, /usr/local/apache/htdocs/cgi-bin poderia ser designado como um diretório CGI no servidor Web. Se um navegador da Web solicita a URL que aponta para um arquivo dentro do diretório CGI (por exemplo, http://exemplo.com/cgi-bin/printenv.pl), em vez de simplesmente enviar o arquivo ( /usr/local/apache/htdocs/cgi-bin/printenv.pl) para o navegador web, o servidor HTTP executa o script especificado e passa a saída do script para o navegador da web. Ou seja, qualquer coisa que o script envia a saída padrão é passado para o cliente Web em vez de ser mostrado na tela em uma janela de terminal.

Estrutura geral de scripts CGI:
Leitura e descodificação de dados (e/ou campos de informação de um pacote HTTP);

Processamento dos dados (gravar informação em bases de dados,
realizar cálculos, recuperar dados);

Criação de uma página Web com os resultados produzidos.

Exemplos de aplicação de CGI's
Processamento de dados submetidos através de formulários;

Servir de interface com a bases de dados, fazendo a conversão da
transação de HTML para SQL e formatar em HTML as respostas obtidas,
enviando em seguida os resultados para o cliente;

Converter dados do sistema para HTML e retornar o resultado para o
cliente;

Criação de documentos personalizados;

Gerir contadores de acesso;

Processamento de mapas.

Métodos de transmissão
O protocolo HTTP, utiliza vários métodos de manipulação e organização dos dados. Os dois métodos mais utilizados para submeter dados de formulários são o GET e o POST. Ambos os métodos transferem dados do browser para o servidor, a maior diferença entre eles é a maneira como a informação é passada para o programa CGI:

GET

CGI chamada através do método GET

O browser acrescenta um "?" ao URL especificado no atributo ACTION, e os valores codificados;

http://exemplo.com/cgi-bin/registra.pl?login=guest 

O servidor ao receber um URL com uma query-string, chama o programa cgi identificado na 1ª parte do URL (antes do '?') e guarda a parte depois do '?' na variável de ambiente QUERY_STRING (a string de consultas contida na URL após o '?') . Supondo que o utilizador digitou "guest" no campo login, quando o botão submit é clicado, o browser envia, ao servidor.

O pedido GET identifica o documento a enviar (cgi-bin/registra.pl). Desde que o servidor esteja configurado para reconhecer todos os ficheiros no diretório cgi-bin como sendo um programa cgi, executa o programa em vez de enviar o documento diretamente ao browser, além disso coloca a string login='guest' na variável de ambiente QUERY_STRING.

O programador de CGI's não consegue controlar por qual método o programa vai ser chamado. Assim os scripts são geralmente escritos para suportar ambos os métodos.


Os dados introduzidos em um formulário fazem parte do corpo da mensagem enviada para o servidor.

Enquanto o método GET passa a informação através de variáveis de ambiente , o POST envia os dados para o programa CGI através do standard input (entrada padrão,stdio.h), como uma string de comprimento especificado na variável de ambiente CONTENT_LENGTH;

Faz 2 ligações ao servidor, uma para contactar o servidor e outra para enviar os parâmetros. Em outras palavras, se o servidor receber um pedido de um formulário usando o POST, ele sabe que tem que continuar "à espera" do resto da informação.

Vantagens/Desvantagens

A vantagem do GET é que permite aceder ao programa CGI com uma query sem utilizar um formulário, basicamente estamos a passar parâmetros para um programa. Exemplo: <A HREF="/cgi-bin/program.pl?user=Larry%20Bird&age=35&pass=testing"> Programa CGI </A>

A maior desvantagem do GET é a falta de segurança e o facto de ter de haver algum cuidado para que o browser ou o servidor não trunquem a informação que exceda o número de caracteres permitido.

A maior vantagem do método POST é o tamanho da query poder ser ilimitada. Para obter informação através do método POST, o programa CGI lê do standard input, por essa razão não é possivel aceder à CGI sem utilizar um formulário.

História
Levando em conta a velocidade com a qual as inovações acontecem, CGI pode ser considerado antigo, levando em consideração a criação do computador pode se dizer que está na meia-idade.

Em 1993, a equipe o National Center for Supercomputing Applications (NCSA),escreveu uma especificação para chamar executáveis ​​de linha de comando na www-talk lista de emails. No entanto, NCSA não hospeda a especificação.

Outros desenvolvedores adotaram a especificação, e tem sido um padrão para servidores web desde então. Um grupo presidido por Ken Coar começou em novembro de 1997 um trabalho para obter a definição NCSA de CGI mais formalmente definida. Este trabalho resultou em RFC3875 , que especifica a versão CGI 1.1. Expressamente mencionados na RFC são os contribuintes que se segue:

Rob McCool (autor do NCSA HTTPd Web Server ) John Franks (autor do Web Server GN) Ari Luotonen (o desenvolvedor do CERN httpd servidor Web) Tony Sanders (autor do servidor Plexus Web) George Phillips (mantenedor do servidor Web na University of British Columbia ).

Como alternativa pode considerar:

FastCGI

PSGI(Perl Web Server Gateway Interface)

Rack (web server interface)

WSGI(Web Server Gateway Interface)

Exemplo simples de um script CGI

<!DOCTYPE html>
<html>
 <body>
  <form action="add.cgi" method="POST">
   Coloque os dois números:<br />
   Primeiro número: <input type="text" name="num1" /><br />
   Segundo número: <input type="text" name="num2" /><br />
   <input type="submit" value="Enviar" />
  </form>
 </body>
</html>

