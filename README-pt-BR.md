# Django Recipes

➡️ Deploy: https://recipes-django.onrender.com

➡️ Um site de receitas criado com Django e Django REST frameworks.

❕Página Inicial
- A página inicial exibe as receitas publicadas mais recentes.
- A barra de busca pode ser usada para encontrar categorias, nomes de receitas ou tags específicas.
- Clique em `Veja mais...` para ver detalhes sobre uma receita específica.

❕Dashboard
- Quando você está logado, você pode criar novas receitas e enviar uma solicitação para um administrador publicá-la.
- Enquanto a receita não for publicada, você pode editar seus detalhes no dashboard de usuário.

❕REST API v1
- Esta API permite obter dados de todas as receitas da página inicial usando a URL `/recipes/api/v1`.
- Detalhes sobre uma receita podem ser acessados usando seu id com a URL `/recipes/api/v1/<int:id>`.
  
❕REST API v2
- Esta API permite obter dados de uma tag de receita específica usando a URL `/recipes/api/v2/tag/<int:id>`.
- Você pode usar Autenticação JWT para se conectar à API v2, criando e verificando um token na URL `/recipes/api/token`.
- Ao se autenticar, você pode usar a URL `/recipes/api/v2` para criar, ler, atualizar e deletar receitas usando o método HTTP apropriado.

➡️ Testes funcionais usando `Selenium` estão localizados no diretório `/tests`, e testes unitários Django estão armazenados dentro dos diretórios `/tests` na pasta de cada app.
