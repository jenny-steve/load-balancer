# Dockerfile for NGINX
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
