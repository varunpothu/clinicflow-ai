FROM node:24-alpine AS build
WORKDIR /app
COPY package.json ./package.json
COPY tsconfig.json ./tsconfig.json
COPY tsconfig.app.json ./tsconfig.app.json
COPY tsconfig.node.json ./tsconfig.node.json
COPY vite.config.ts ./vite.config.ts
COPY index.html ./index.html
COPY src ./src
RUN npm install && npm run build

FROM nginx:alpine AS runtime
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
