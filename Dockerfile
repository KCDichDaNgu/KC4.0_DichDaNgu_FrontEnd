FROM nginx:1.10
ADD nginxconf.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
COPY ./build/ /var/www/
