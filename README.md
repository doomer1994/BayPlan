# BayPlan - Sistema de Planejamento de Estufagem Naval

Sistema web para planejamento de estufagem (stowage planning) de navios cargueiros, desenvolvido em Python com interface interativa.

## 📋 Sobre o Projeto

O BayPlan é uma ferramenta especializada para planejamento naval que permite:
- **Cadastro de navios** com suas dimensões e capacidades
- **Visualização 2D das bays** (seções do navio)
- **Edição interativa** de posições para contêineres e tanques
- **Gerenciamento completo** do layout de estufagem

### Conceitos Navais

- **Bay**: Seção vertical longitudinal do navio (fatias de frente para trás)
- **Row**: Posição lateral (bombordo/estibordo)
- **Tier**: Altura (porão/deck)
- **Coordenadas**: Sistema 3D (Bay, Row, Tier) para localização precisa

## 🚀 Tecnologias

- **Python 3.8+** - Linguagem principal
- **Dash (Plotly)** - Interface web interativa
- **Plotly** - Gráficos e visualizações
- **SQLite** - Banco de dados local
- **Pandas** - Manipulação de dados

## 📁 Estrutura do Projeto

```
BayPlan/
├── pages/                    # Páginas da aplicação Dash
│   ├── cadastro.py          # Cadastro de navios
│   ├── layout.py            # Edição de layout das bays
│   └── visualizar.py        # Visualização de dados
├── callbacks/               # Lógica de interação
│   ├── cadastro_callbacks.py
│   ├── layout_callbacks.py
│   └── visualizar_callbacks.py
├── utils/                   # Utilitários
│   ├── grid_generator.py    # Geração de grids
│   ├── database.py          # Operações de banco
│   └── plotly_utils.py      # Utilitários Plotly
├── assets/                  # Arquivos estáticos
├── Stow_Planing.db         # Banco de dados SQLite
├── main.py                 # Arquivo principal
└── requirements.txt        # Dependências
```

## ⚙️ Instalação

### 1. Clonar o Repositório
```bash
git clone https://github.com/seuusername/BayPlan.git
cd BayPlan
```

### 2. Criar Ambiente Virtual (Recomendado)
```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação
```bash
python main.py
```

### 5. Acessar no Navegador
```
http://localhost:8050
```

## 📊 Banco de Dados

### Tabelas Principais

#### Vessel (Navios)
- Armazena dados básicos dos navios
- Dimensões: número de bays, rows, tiers
- Capacidades de combustível e lastro

#### Vessel_Stow (Layout)
- Posições específicas de cada bay
- Coordenadas (Bay, Row, Tier)
- Tipos: Contêiner (C), Água (W), Combustível (F)

#### W_F (Tanques)
- Dados de tanques de água e combustível
- Volume e densidade

### Exemplo de Uso
```sql
-- Buscar posições de uma bay específica
SELECT Bay, Row, Tier, Type, Position 
FROM Vessel_Stow 
WHERE FK_Vessel_Id = 'MV-2' AND Bay = 2;
```

## 🎯 Funcionalidades

### ✅ Implementadas
- [x] Cadastro de navios com validação
- [x] Visualização de bays com dados reais
- [x] Estrutura modular e organizanda
- [x] Banco de dados relacional

### 🔧 Em Desenvolvimento
- [ ] Edição interativa por cliques
- [ ] Controle de bay frente/trás
- [ ] Validação de posições
- [ ] Export de layouts

### 🚀 Roadmap
- [ ] Sistema de autenticação
- [ ] Deploy em nuvem
- [ ] API REST
- [ ] Controle de versões
- [ ] Relatórios automatizados

## 📖 Como Usar

### 1. Cadastrar Navio
1. Acesse a página "Cadastro"
2. Preencha nome e dimensões do navio
3. Defina capacidades de combustível/lastro
4. Salve o cadastro

### 2. Definir Layout
1. Vá para "Layout"
2. Selecione o navio cadastrado
3. Escolha a bay e bay_side
4. Clique nas posições para definir tipo:
   - **C**: Contêiner
   - **W**: Água de lastro
   - **F**: Combustível
5. Salve o layout

### 3. Visualizar
1. Acesse "Visualizar"
2. Selecione navio e bay
3. Veja o layout configurado

## 🔧 Configuração

### Variáveis de Ambiente
Crie um arquivo `.env` (opcional):
```env
DEBUG=True
DATABASE_PATH=./Stow_Planing.db
PORT=8050
```

### Personalização
- Modifique `assets/style.css` para alterar aparência
- Ajuste configurações em `utils/database.py`
- Adicione novas páginas em `pages/`

## 📝 Convenções do Sistema

### Numeração de Bays
- **Ímpares** (01, 03, 05...): Contêineres de 20 pés
- **Pares** (02, 04, 06...): Contêineres de 40 pés

### Numeração de Rows
- **Ímpares** (01, 03, 05...): Lado bombordo (esquerda)
- **Pares** (02, 04, 06...): Lado estibordo (direita)

### Numeração de Tiers
- **< 80**: Porão (Hold) - 02, 04, 06, 08, 10...
- **≥ 80**: Convés (Deck) - 80, 82, 84, 86, 88...

## 🐛 Problemas Conhecidos

- Edição por clique ainda em desenvolvimento
- Callback de checkbox "apenas frente" precisa ajuste
- Sincronização banco → interface em correção

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@doomer1994](https://github.com/doomer1994)
- Email: everaldo8luiz@gmail.com

## 🙏 Agradecimentos

- Comunidade Plotly/Dash
- Documentação da indústria naval
- Especialistas em logística marítima

---

## 📚 Recursos Úteis

- [Documentação Dash](https://dash.plotly.com/)
- [Plotly Python](https://plotly.com/python/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Conceitos de Stowage Planning](https://example.com)

---

**Status do Projeto:** Em desenvolvimento ativo
**Última atualização:** Junho 2025
