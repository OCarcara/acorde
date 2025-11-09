# ACORDE – Gestão do Memorial Olhos D’Água

Este projeto é uma aplicação Django que centraliza o gerenciamento do acervo do Memorial Olhos D’Água (ACORDE). Ele foi desenvolvido com recursos do projeto **ACORDE para a preservação dos saberes** do edital de MANUTENÇÃO DE ESPAÇOS CULTURAIS da Política Nacional Aldir Blanc, Edital de 2024.

A solução oferece duas frentes:

- **Interface administrativa** (restrita): cadastro de peças, pessoas, exposições, configurações de sistema e geração de materiais auxiliares como audiodescrições e QR Codes.  
- **Interface pública** (aberta): navegação pelo acervo publicado, com filtros por tipo, exposição e busca textual.

## Funcionalidades principais

- Autenticação via `/entrar/`, com proteção por grupo (`editores` não acessam configurações).  
- Cadastro e manutenção de peças, histórico, mídias e audiodescrições com integração à API da OpenAI.  
- Geração de QR Codes que apontam para os áudios gerados e disponibilização na interface pública.  
- Site público responsivo, destacando imagens, autores e resumo das peças.

## Tecnologias

- Python 3.12  
- Django 5.2.6  
- SQLite (desenvolvimento) / PostgreSQL (produção)  
- Bootstrap 5 + CSS customizado

## Configuração local rápida

1. Crie o ambiente virtual e instale as dependências:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
2. Aplique as migrações:  
   ```bash
   python manage.py migrate
   ```
3. Crie um superusuário:  
   ```bash
   python manage.py createsuperuser
   ```
4. Execute o servidor:  
   ```bash
   python manage.py runserver
   ```
5. Acesse:
   - Administração: `http://127.0.0.1:8000/entrar/`  
   - Site público: `http://127.0.0.1:8000/memorial/`

## Configurações importantes

- Defina `SITE_BASE_URL` no `.env` (produção) para geração correta de URLs absolutas.  
- Em produção, garanta que `LOGIN_URL`, `LOGIN_REDIRECT_URL` e `LOGOUT_REDIRECT_URL` estejam configurados para manter o fluxo pós-login.

## Estrutura relevante

- `acervo/` – app principal com models, views, templates e integrações.  
- `templates/` – HTMLs da interface pública e administrativa.  
- `static/` e `media/` – arquivos estáticos e armazenamentos de uploads.

## Licença

Projeto interno ACORDE – uso restrito. Consulte os mantenedores antes de distribuir.

---

**Desenvolvedor:** O Carcará – LTDA  
**Data:** 2025
