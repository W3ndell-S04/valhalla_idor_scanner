# 🔥 Valhalla IDOR Scanner

Ferramenta de **pentest automatizado** para detecção de vulnerabilidades do tipo **IDOR (Insecure Direct Object Reference)** em aplicações web e APIs.

---

## 🚀 Sobre o projeto

O **Valhalla IDOR Scanner** foi desenvolvido com foco em segurança ofensiva, permitindo a identificação de falhas de autorização através da enumeração de identificadores expostos em endpoints.

Esse tipo de vulnerabilidade é comum em APIs mal protegidas e pode levar ao vazamento de dados sensíveis.

---

## 🛠️ Funcionalidades

* 🔍 Enumeração automática de IDs
* ⚡ Multithread (alta performance)
* 🔐 Suporte a autenticação (headers e cookies)
* 🧠 Detecção por hash (comparação inteligente)
* 🎯 Filtro por palavras-chave (email, cpf, etc.)
* 🌐 Suporte a GET e POST
* 🔌 Integração com proxy (Burp Suite)
* 💾 Exportação de resultados

---

## 📦 Instalação

```bash
git clone https://github.com/SEU-USUARIO/valhalla-idor-scanner.git
cd valhalla-idor-scanner

pip install -r requirements.txt
```

---

## ⚙️ Uso

### 🔹 Scan básico

```bash
python valhalla_idor.py -u "https://site.com/api/user?id={}" -s 1 -e 100
```

---

### 🔐 Com autenticação

```bash
python valhalla_idor.py \
-u "https://site.com/api/user?id={}" \
-H "Authorization: Bearer TOKEN" \
-H "Cookie: session=abc123"
```

---

### 🔍 Filtrar resultados

```bash
python valhalla_idor.py -u "https://site.com/api/user?id={}" -k email
```

---

### 🔌 Usando proxy (Burp Suite)

```bash
python valhalla_idor.py \
-u "https://site.com/api/user?id={}" \
-p http://127.0.0.1:8080
```

---

### 📦 Requisições POST

```bash
python valhalla_idor.py \
-u "https://site.com/api/user" \
-m POST \
-d "id={}"
```

---

## 🧠 Conceito: IDOR

IDOR (Insecure Direct Object Reference) ocorre quando um sistema permite acesso direto a objetos internos (como registros de banco de dados) sem validação adequada de autorização.

Exemplo:

```
/api/user?id=1
/api/user?id=2
```

Se um usuário consegue acessar dados de outro apenas alterando o ID, a aplicação é vulnerável.

---

## ⚠️ Aviso Legal

Esta ferramenta deve ser utilizada **apenas em ambientes autorizados**, como:

* Laboratórios de estudo
* Aplicações próprias
* Programas de Bug Bounty

O uso indevido pode ser ilegal.

---

## 👨‍💻 Autor

Desenvolvido por Wendell Soares

Estudante de Segurança da Informação | Pentest | Python


