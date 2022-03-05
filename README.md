# CGI / Common Gateway Interface

CGI (sigla em inglês para Common Gateway Interface), em português , Interface Comum de Porta de entrada.

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
O servidor ao receber um URL com uma query-string, chama o programa cgi identificado na 1ª parte do URL (antes do '?') e guarda a parte depois do '?' na variável de ambiente QUERY_STRING (a string de consultas contida na URL após o '?') . Supondo que o utilizador digitou "guest" no campo login, quando o botão submit é clicado, o browser envia, ao servidor, um pedido do tipo:

GET /cgi-bin/registra.pl?login='guest' HTTP/1.0 
Accept: www/source
Accept: text/html
Accept: image.gif
User-Agent: Lynx/2.4 libwww/2.14
From: shisshir@bu.edu 
O pedido GET identifica o documento a enviar (cgi-bin/registra.pl). Desde que o servidor esteja configurado para reconhecer todos os ficheiros no diretório cgi-bin como sendo um programa cgi, executa o programa em vez de enviar o documento diretamente ao browser, além disso coloca a string login='guest' na variável de ambiente QUERY_STRING.

