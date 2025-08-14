# Stage 1: Build the React app
FROM node:18-alpine AS build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . ./

RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:stable-alpine AS production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY /nginx-custom.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]