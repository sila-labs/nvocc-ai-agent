# Build Stage
FROM node:20-alpine as build

WORKDIR /app

COPY . .

RUN npm install
RUN npm run build

# Production Stage
FROM nginx:stable-alpine as production

COPY --from=build /app/dist /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
