# Exportar e importar un índice de Elasticsearch con Elasticdump

Este repositorio contiene los archivos necesarios para exportar e importar un índice llamado `faq-repsol-embeddings` de Elasticsearch, incluyendo sus **documentos** y su **template de índice**.

## 🛠 Requisitos

- Tener instalado [`elasticdump`](https://www.npmjs.com/package/elasticdump):
### MACOS & Homebrew

  ```bash
  npm install -g elasticdump
  ```
### WINDOWS
  ```bash
  Toca investigar
  ```
- Tener un clúster de Elasticsearch accesible (en este ejemplo: `https://localhost:9200`).
- Usuario con permisos (`elastic`) y su contraseña (`changeme`).
- Node.js instalado (usado internamente por `elasticdump`).

---

## 📄 Exportar desde Elasticsearch

### Exportar los documentos

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 elasticdump \
  --input=https://elastic:changeme@localhost:9200/faq-repsol-embeddings \
  --output=faq-repsol-embeddings-docs.json \
  --type=data
```

### Exportar el template/mapping

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 elasticdump \
  --input=https://elastic:changeme@localhost:9200/faq-repsol-embeddings \
  --output=faq-repsol-embeddings-template.json \
  --type=mapping
```

---

## 📅 Importar a otro Elasticsearch

### Importar el template/mapping

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 elasticdump \
  --input=faq-repsol-embeddings-template.json \
  --output=https://elastic:changeme@localhost:9200/faq-repsol-embeddings \
  --type=mapping
```

### Importar los documentos

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 elasticdump \
  --input=faq-repsol-embeddings-docs.json \
  --output=https://elastic:changeme@localhost:9200/faq-repsol-embeddings \
  --type=data
```

---

## ⚠️ Notas

- La variable `NODE_TLS_REJECT_UNAUTHORIZED=0` desactiva la verificación del certificado SSL. Úsala **solo en entornos locales o de desarrollo**.
- Asegúrate de que el índice de destino esté vacío antes de importar datos, si no deseas duplicados.
- Puedes modificar el nombre del índice (`faq-repsol-embeddings`) si quieres restaurarlo con otro nombre.

---

## 📂 Archivos incluidos

- `faq-repsol-embeddings-docs.json`: documentos del índice.
- `faq-repsol-embeddings-template.json`: mapping del índice.

---

## 📚 Referencias

- [Documentación de elasticdump](https://github.com/elasticsearch-dump/elasticsearch-dump)
- [Elasticsearch Index Templates](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-templates.html)