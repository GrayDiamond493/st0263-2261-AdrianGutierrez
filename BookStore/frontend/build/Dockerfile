FROM nginx:alpine
COPY diamondbookstore.tk.conf /etc/nginx/sites-enabled/
COPY nginx.conf /etc/nginx/nginx.conf
COPY . /usr/share/nginx/html/
WORKDIR /usr/share/nginx/html/