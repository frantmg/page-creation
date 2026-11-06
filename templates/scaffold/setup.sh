# Run inside a new <page-slug> folder, after copying this scaffold into it.
echo '{"name":"<page-slug>","private":true,"type":"module","scripts":{"build":"vite build"}}' > package.json
npm i react react-dom @mui/material @emotion/react @emotion/styled @mui/icons-material
npm i -D vite @vitejs/plugin-react typescript @types/react @types/react-dom tailwindcss @tailwindcss/vite vite-plugin-singlefile
